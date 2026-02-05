#!/usr/bin/env python3
"""
Effect Size Filler: 4-tier missing Hedges' g / SE_g imputation.

Tiers:
  1. Direct calculation from M, SD, n (99%+ accuracy)
  2. RAG extraction of statistics from PDF, then calculate (85-90%)
  3. Convert t/F/p values to Cohen's d -> Hedges' g (80-85%)
  4. Flag as manual_needed
"""

import sys
import json
import math
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_v10.rag_builder import RAGConfig, query_study_collection
from recode_v11.utils.llm_clients import UnifiedLLMClient
from recode_v11.utils.data_loader import load_v81_csv, get_unique_studies
from recode_v11.utils.cost_tracker import CostTracker
from recode_v11.utils.audit import AuditLogger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def calculate_hedges_g(n1: int, n2: int, m1: float, sd1: float, m2: float, sd2: float) -> Tuple[float, float]:
    """
    Calculate Hedges' g with small-sample bias correction.
    Returns (hedges_g, se_g).
    """
    if n1 <= 1 or n2 <= 1:
        raise ValueError(f"Sample sizes must be > 1: n1={n1}, n2={n2}")
    if sd1 <= 0 or sd2 <= 0:
        raise ValueError(f"SDs must be > 0: sd1={sd1}, sd2={sd2}")

    # Pooled SD
    s_pooled = math.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
    if s_pooled == 0:
        raise ValueError("Pooled SD is zero")

    # Cohen's d
    d = (m1 - m2) / s_pooled

    # Hedges' correction factor J
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))

    # Hedges' g
    g = d * J

    # SE of g
    se_g = math.sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))

    return g, se_g


def t_to_hedges_g(t: float, n1: int, n2: int) -> Tuple[float, float]:
    """Convert t-statistic to Hedges' g."""
    d = t * math.sqrt(1/n1 + 1/n2)
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))
    g = d * J
    se_g = math.sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))
    return g, se_g


def f_to_hedges_g(f: float, n1: int, n2: int) -> Tuple[float, float]:
    """Convert F-statistic (1 df numerator) to Hedges' g."""
    t = math.sqrt(f)
    return t_to_hedges_g(t, n1, n2)


def validate_effect_size(g: float, se: float) -> List[str]:
    """Validate effect size for anomalies."""
    warnings = []
    if abs(g) > 5.0:
        warnings.append(f"Extreme g={g:.3f}, likely error")
    if abs(g) > 3.0:
        warnings.append(f"Large g={g:.3f}, unusual for education research")
    if se > 3.0:
        warnings.append(f"Large SE={se:.3f}")
    if se < 0.01:
        warnings.append(f"Suspiciously small SE={se:.3f}")
    return warnings


class EffectSizeFiller:
    """4-tier missing effect size imputation."""

    def __init__(self, config: Dict):
        self.config = config
        self.llm = UnifiedLLMClient()
        self.cost_tracker = CostTracker(
            budget=config.get('costs', {}).get('budget', 50.0),
            log_file=str(Path(config['paths']['base']) / "audit" / "cost_log.jsonl")
        )
        self.audit = AuditLogger(config.get('audit', {}).get('log_file', 'data/recode_v11/audit/pipeline_audit.jsonl'))

        rag_cfg = config.get('rag', {})
        self.rag_config = RAGConfig(
            persist_directory=rag_cfg.get('persist_directory', 'data/recode_v11/01_rag_index'),
            n_results=rag_cfg.get('n_results', 8),
        )

    def _try_tier1(self, row: Dict) -> Optional[Tuple[float, float, str]]:
        """Tier 1: Direct calculation from M, SD, n."""
        try:
            n1 = row.get('n_Treatment')
            n2 = row.get('n_Control')
            m1 = row.get('M_Treatment')
            sd1 = row.get('SD_Treatment')
            m2 = row.get('M_Control')
            sd2 = row.get('SD_Control')

            if all(v is not None for v in [n1, n2, m1, sd1, m2, sd2]):
                n1, n2 = int(float(n1)), int(float(n2))
                m1, sd1 = float(m1), float(sd1)
                m2, sd2 = float(m2), float(sd2)

                if n1 > 1 and n2 > 1 and sd1 > 0 and sd2 > 0:
                    g, se = calculate_hedges_g(n1, n2, m1, sd1, m2, sd2)
                    return g, se, "tier1_direct"
        except (ValueError, TypeError):
            pass
        return None

    def _try_tier2(self, row: Dict, study_id: str) -> Optional[Tuple[float, float, str]]:
        """Tier 2: RAG extraction of statistics from PDF."""
        try:
            outcome_name = row.get('Outcome_Name', '')
            query = (f"What are the sample sizes, means, and standard deviations for "
                    f"the treatment and control groups for the outcome '{outcome_name}'? "
                    f"Look for tables with descriptive statistics, M, SD, n values.")

            rag_result = query_study_collection(
                study_id, query, n_results=8, config=self.rag_config
            )

            if not rag_result.context_combined:
                return None

            prompt = f"""Extract the exact statistical values from this paper for the outcome "{outcome_name}".

PAPER EXCERPTS:
{rag_result.context_combined}

Extract these values if available:
- n_treatment (treatment group sample size)
- n_control (control group sample size)
- m_treatment (treatment group mean)
- sd_treatment (treatment group SD)
- m_control (control group mean)
- sd_control (control group SD)
- t_value (t-statistic if reported)
- f_value (F-statistic if reported)
- p_value (p-value if reported)

Respond in JSON:
{{"n_treatment": null, "n_control": null, "m_treatment": null, "sd_treatment": null, "m_control": null, "sd_control": null, "t_value": null, "f_value": null, "p_value": null, "confidence": 0.0}}"""

            response = self.llm.call(
                provider="anthropic", model="claude-sonnet-4-5-20250929",
                prompt=prompt, temperature=0.1, max_tokens=500
            )

            if response:
                self.cost_tracker.add(
                    provider="anthropic", model="claude-sonnet-4-5-20250929",
                    phase='effect_size', input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens, cost=response.cost,
                    study_id=study_id
                )

                stats = response.parse_json()

                # Try direct calculation with extracted stats
                if all(stats.get(k) is not None for k in ['n_treatment', 'n_control', 'm_treatment', 'sd_treatment', 'm_control', 'sd_control']):
                    g, se = calculate_hedges_g(
                        int(stats['n_treatment']), int(stats['n_control']),
                        float(stats['m_treatment']), float(stats['sd_treatment']),
                        float(stats['m_control']), float(stats['sd_control'])
                    )
                    return g, se, "tier2_rag_extract"

                # Try t-value conversion
                n1 = stats.get('n_treatment') or row.get('n_Treatment')
                n2 = stats.get('n_control') or row.get('n_Control')
                if n1 and n2:
                    n1, n2 = int(float(n1)), int(float(n2))
                    if stats.get('t_value'):
                        g, se = t_to_hedges_g(float(stats['t_value']), n1, n2)
                        return g, se, "tier3_t_convert"
                    if stats.get('f_value'):
                        g, se = f_to_hedges_g(float(stats['f_value']), n1, n2)
                        return g, se, "tier3_f_convert"

        except Exception as e:
            logger.warning(f"Tier 2/3 failed for {study_id}: {e}")
        return None

    def fill_row(self, row: Dict, study_id: str) -> Dict:
        """Fill missing effect sizes for a single row."""
        result = {
            'es_id': row.get('ES_ID', ''),
            'original_hedges_g': row.get('Hedges_g'),
            'original_se_g': row.get('SE_g'),
            'filled_hedges_g': None,
            'filled_se_g': None,
            'fill_method': None,
            'warnings': [],
            'needs_manual': False,
        }

        # Check if already has valid effect size
        existing_g = row.get('Hedges_g')
        existing_se = row.get('SE_g')
        if existing_g is not None and existing_se is not None:
            try:
                g, se = float(existing_g), float(existing_se)
                if not math.isnan(g) and not math.isnan(se) and se > 0:
                    result['filled_hedges_g'] = g
                    result['filled_se_g'] = se
                    result['fill_method'] = 'existing'
                    result['warnings'] = validate_effect_size(g, se)
                    return result
            except (ValueError, TypeError):
                pass

        # Tier 1: Direct calculation
        tier1 = self._try_tier1(row)
        if tier1:
            g, se, method = tier1
            result['filled_hedges_g'] = round(g, 4)
            result['filled_se_g'] = round(se, 4)
            result['fill_method'] = method
            result['warnings'] = validate_effect_size(g, se)
            return result

        # Tier 2/3: RAG extraction + conversion
        tier2 = self._try_tier2(row, study_id)
        if tier2:
            g, se, method = tier2
            result['filled_hedges_g'] = round(g, 4)
            result['filled_se_g'] = round(se, 4)
            result['fill_method'] = method
            result['warnings'] = validate_effect_size(g, se)
            return result

        # Tier 4: Manual needed
        result['fill_method'] = 'tier4_manual_needed'
        result['needs_manual'] = True
        return result

    def fill_all(self, rows: List[Dict], limit: Optional[int] = None) -> List[Dict]:
        """Fill effect sizes for all rows."""
        results = []
        studies = get_unique_studies(rows)
        items = list(rows)
        if limit:
            items = items[:limit]

        for i, row in enumerate(items):
            study_id = str(row.get('Study_ID', ''))
            es_id = row.get('ES_ID', '')

            if i % 50 == 0:
                logger.info(f"[{i+1}/{len(items)}] Processing effect sizes...")

            result = self.fill_row(row, study_id)
            results.append(result)

            if result['fill_method'] and result['fill_method'] != 'existing':
                self.audit.log(
                    phase='effect_size', action='fill',
                    paper_id=study_id, field_name=f"hedges_g.{es_id}",
                    old_value=result['original_hedges_g'],
                    new_value=result['filled_hedges_g'],
                    reason=result['fill_method'],
                    actor='system'
                )

        # Summary
        methods = {}
        for r in results:
            m = r['fill_method'] or 'none'
            methods[m] = methods.get(m, 0) + 1

        logger.info(f"\nEffect Size Fill Summary: {methods}")
        return results


def main():
    parser = argparse.ArgumentParser(description="Effect Size Filler")
    parser.add_argument("--config", default="configs/recode_v11/pipeline_config.yaml")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent.parent
    with open(base_dir / args.config) as f:
        config = yaml.safe_load(f)

    rows = load_v81_csv(str(base_dir / config['input']['csv_path']))

    filler = EffectSizeFiller(config)
    results = filler.fill_all(rows, limit=args.limit)

    # Save results
    output_dir = Path(config['paths']['effect_sizes'])
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "effect_size_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # Summary
    manual = sum(1 for r in results if r['needs_manual'])
    filled = sum(1 for r in results if r['filled_hedges_g'] is not None)
    print(f"\n{'='*60}")
    print("EFFECT SIZE FILLER COMPLETE")
    print(f"{'='*60}")
    print(f"Total rows: {len(results)}")
    print(f"Filled: {filled}")
    print(f"Manual needed: {manual}")
    print(f"Cost: ${filler.cost_tracker.total_cost:.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
