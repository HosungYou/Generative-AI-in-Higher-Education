#!/usr/bin/env python3
"""
Phase 2: Multi-Model Consensus
3 models independently verify Phase 1 results.
Field-type-specific consensus rules.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_v10.rag_builder import RAGConfig, query_study_collection
from recode_v11.schema import (
    RECODE_FIELDS, FieldType, FieldCategory, ConsensusMethod,
    get_ordinal_distance, get_critical_fields
)
from recode_v11.utils.llm_clients import UnifiedLLMClient
from recode_v11.utils.cost_tracker import CostTracker
from recode_v11.utils.audit import AuditLogger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConsensusStatus(str, Enum):
    UNANIMOUS = "unanimous"
    MAJORITY = "majority"
    NEAR_CONCORDANT = "near_concordant"
    CONCORDANT = "concordant"
    DISCORDANT = "discordant"


class Phase2Consensus:
    """Multi-model consensus verification."""

    MODEL_CONFIGS = [
        {"provider": "anthropic", "model": "claude-sonnet-4-5-20250929", "name": "claude"},
        {"provider": "openai", "model": "gpt-4o", "name": "gpt4o"},
        {"provider": "groq", "model": "llama-3.3-70b-versatile", "name": "groq"},
    ]

    def __init__(self, config: Dict):
        self.config = config
        self.llm = UnifiedLLMClient()
        self.cost_tracker = CostTracker(
            budget=config.get('costs', {}).get('budget', 50.0),
            log_file=str(Path(config['paths']['base']) / "audit" / "cost_log.jsonl")
        )
        self.audit = AuditLogger(config.get('audit', {}).get('log_file', 'data/recode_v11/audit/pipeline_audit.jsonl'))
        self.rag_config = RAGConfig(
            persist_directory=config.get('rag', {}).get('persist_directory', 'data/recode_v11/01_rag_index'),
        )
        self.critical_fields = set(get_critical_fields().keys())

    def _build_verification_prompt(self, field_name: str, phase1_value: str,
                                    rag_context: str, study_meta: Dict) -> str:
        """Build verification prompt for a model."""
        field_def = RECODE_FIELDS[field_name]
        allowed = ", ".join(field_def.allowed_values) if field_def.allowed_values else "any"

        return f"""Verify this classification of an academic paper.

PAPER: {study_meta.get('title', 'Unknown')} ({study_meta.get('year', '')})

FIELD: {field_name} - {field_def.description}
INITIAL VALUE (from another AI): {phase1_value}
ALLOWED VALUES: {allowed}

PAPER EXCERPTS:
{rag_context}

Independently assess this field. Do NOT simply agree with the initial value.
Provide your own assessment based on the paper content.

Respond in JSON:
{{"value": "<your assessment>", "confidence": <0.0-1.0>, "reasoning": "<brief explanation>"}}"""

    def _calculate_consensus(self, field_name: str, model_values: Dict[str, Dict]) -> Dict:
        """Calculate consensus for a field based on its type."""
        field_def = RECODE_FIELDS[field_name]
        values = {k: v.get('value') for k, v in model_values.items() if v.get('value') is not None}

        if len(values) < 2:
            return {
                'consensus_value': list(values.values())[0] if values else None,
                'status': ConsensusStatus.DISCORDANT.value,
                'agreement': 0.0,
                'model_values': model_values,
            }

        val_list = list(values.values())
        val_keys = list(values.keys())

        # Categorical: exact match
        if field_def.field_type == FieldType.CATEGORICAL:
            # Count exact matches (case-insensitive)
            normalized = [str(v).lower().strip() for v in val_list]
            from collections import Counter
            counts = Counter(normalized)
            most_common_val, most_common_count = counts.most_common(1)[0]

            # Map back to original case
            consensus_val = None
            for v in val_list:
                if str(v).lower().strip() == most_common_val:
                    consensus_val = v
                    break

            if most_common_count == len(val_list):
                status = ConsensusStatus.UNANIMOUS
            elif most_common_count >= 2:
                status = ConsensusStatus.MAJORITY
            else:
                status = ConsensusStatus.DISCORDANT

            # Critical fields need 3/3
            if field_name in self.critical_fields and status != ConsensusStatus.UNANIMOUS:
                if field_def.consensus_method == ConsensusMethod.UNANIMOUS:
                    status = ConsensusStatus.DISCORDANT

            return {
                'consensus_value': consensus_val,
                'status': status.value,
                'agreement': most_common_count / len(val_list),
                'model_values': model_values,
            }

        # Ordinal: with tolerance
        elif field_def.field_type == FieldType.ORDINAL:
            normalized = [str(v).lower().strip() for v in val_list]
            from collections import Counter
            counts = Counter(normalized)
            most_common_val, most_common_count = counts.most_common(1)[0]

            consensus_val = None
            for v in val_list:
                if str(v).lower().strip() == most_common_val:
                    consensus_val = v
                    break

            if most_common_count == len(val_list):
                status = ConsensusStatus.UNANIMOUS
            elif most_common_count >= 2:
                status = ConsensusStatus.MAJORITY
            else:
                # Check tolerance (1-level)
                tolerance = field_def.tolerance or 1
                pairs_within_tolerance = 0
                total_pairs = 0
                for i in range(len(val_list)):
                    for j in range(i+1, len(val_list)):
                        dist = get_ordinal_distance(field_name, val_list[i], val_list[j])
                        total_pairs += 1
                        if dist >= 0 and dist <= tolerance:
                            pairs_within_tolerance += 1

                if pairs_within_tolerance >= 2:  # At least 2 pairs within tolerance
                    status = ConsensusStatus.NEAR_CONCORDANT
                    # Use median ordinal value
                    if field_def.ordinal_order:
                        order = [v.lower() for v in field_def.ordinal_order]
                        indices = []
                        for v in val_list:
                            v_lower = str(v).lower().strip()
                            if v_lower in order:
                                indices.append(order.index(v_lower))
                        if indices:
                            median_idx = sorted(indices)[len(indices) // 2]
                            consensus_val = field_def.ordinal_order[median_idx]
                else:
                    status = ConsensusStatus.DISCORDANT

            return {
                'consensus_value': consensus_val,
                'status': status.value,
                'agreement': most_common_count / len(val_list),
                'model_values': model_values,
            }

        # Numerical: relative tolerance
        elif field_def.field_type == FieldType.FLOAT:
            try:
                float_vals = [float(v) for v in val_list]
                avg = sum(float_vals) / len(float_vals)
                tolerance = field_def.tolerance or 0.05

                # Check pairwise relative differences
                all_within = True
                for i in range(len(float_vals)):
                    for j in range(i+1, len(float_vals)):
                        ref = (abs(float_vals[i]) + abs(float_vals[j])) / 2
                        if ref > 0:
                            rel_diff = abs(float_vals[i] - float_vals[j]) / ref
                            if rel_diff > tolerance:
                                all_within = False

                if all_within:
                    status = ConsensusStatus.CONCORDANT
                    consensus_val = round(avg, 4)
                else:
                    status = ConsensusStatus.DISCORDANT
                    # Use value from highest-confidence model
                    best_model = max(model_values.items(),
                                    key=lambda x: x[1].get('confidence', 0))
                    consensus_val = float(best_model[1].get('value', avg))

                return {
                    'consensus_value': consensus_val,
                    'status': status.value,
                    'agreement': 1.0 if all_within else 0.5,
                    'model_values': model_values,
                }
            except (ValueError, TypeError):
                return {
                    'consensus_value': None,
                    'status': ConsensusStatus.DISCORDANT.value,
                    'agreement': 0.0,
                    'model_values': model_values,
                }

    def verify_study(self, phase1_result: Dict) -> Dict:
        """Run 3-model consensus on a Phase 1 result."""
        study_id = phase1_result['study_id']
        result = {
            'study_id': study_id,
            'consensus_date': datetime.now().isoformat(),
            'study_level': {},
            'outcome_level': {},
            'phase5_queue': [],
            'overall_agreement': 0.0,
        }

        # Verify study-level fields
        for field_name, phase1_data in phase1_result.get('study_level', {}).items():
            if field_name not in RECODE_FIELDS:
                continue

            phase1_value = phase1_data.get('value', '')

            # Get RAG context for this field
            from recode_v11.phase1_extract import FIELD_RAG_QUERIES
            query = FIELD_RAG_QUERIES.get(field_name, f"What is the {field_name}?")
            rag_result = query_study_collection(
                study_id, query, n_results=6, config=self.rag_config
            )

            study_meta = {'title': phase1_result.get('title', ''),
                         'year': phase1_result.get('year', '')}

            # Get independent extractions from all models
            model_values = {}
            for model_cfg in self.MODEL_CONFIGS:
                if not self.llm.is_available(model_cfg['provider']):
                    continue

                prompt = self._build_verification_prompt(
                    field_name, phase1_value,
                    rag_result.context_combined, study_meta
                )

                response = self.llm.call(
                    provider=model_cfg['provider'],
                    model=model_cfg['model'],
                    prompt=prompt, temperature=0.1, max_tokens=300
                )

                if response:
                    self.cost_tracker.add(
                        provider=model_cfg['provider'], model=model_cfg['model'],
                        phase='phase2', input_tokens=response.input_tokens,
                        output_tokens=response.output_tokens, cost=response.cost,
                        study_id=study_id
                    )
                    try:
                        model_values[model_cfg['name']] = response.parse_json()
                    except json.JSONDecodeError:
                        model_values[model_cfg['name']] = {
                            'value': phase1_value, 'confidence': 0.3,
                            'reasoning': 'Failed to parse response'
                        }

            # Calculate consensus
            consensus = self._calculate_consensus(field_name, model_values)
            result['study_level'][field_name] = consensus

            if consensus['status'] == ConsensusStatus.DISCORDANT.value:
                result['phase5_queue'].append({
                    'field_name': field_name,
                    'level': 'study',
                    'model_values': model_values,
                })

            self.audit.log_consensus(
                paper_id=study_id, field_name=field_name,
                model_values={k: v.get('value') for k, v in model_values.items()},
                consensus_value=consensus['consensus_value'],
                status=consensus['status']
            )

        # Verify outcome-level fields
        for es_id, outcome_data in phase1_result.get('outcome_level', {}).items():
            result['outcome_level'].setdefault(es_id, {})

            for field_name, phase1_data in outcome_data.items():
                if field_name not in RECODE_FIELDS:
                    continue

                phase1_value = phase1_data.get('value', '')

                # Simplified: use Phase 1 value with cross-model verification
                model_values = {}
                for model_cfg in self.MODEL_CONFIGS:
                    if not self.llm.is_available(model_cfg['provider']):
                        continue

                    query = f"What is the {field_name} for the outcome measurement in this study?"
                    rag_result = query_study_collection(
                        study_id, query, n_results=4, config=self.rag_config
                    )

                    prompt = self._build_verification_prompt(
                        field_name, phase1_value,
                        rag_result.context_combined,
                        {'title': phase1_result.get('title', ''), 'year': ''}
                    )

                    response = self.llm.call(
                        provider=model_cfg['provider'],
                        model=model_cfg['model'],
                        prompt=prompt, temperature=0.1, max_tokens=300
                    )

                    if response:
                        self.cost_tracker.add(
                            provider=model_cfg['provider'], model=model_cfg['model'],
                            phase='phase2', input_tokens=response.input_tokens,
                            output_tokens=response.output_tokens, cost=response.cost,
                            study_id=study_id
                        )
                        try:
                            model_values[model_cfg['name']] = response.parse_json()
                        except json.JSONDecodeError:
                            model_values[model_cfg['name']] = {
                                'value': phase1_value, 'confidence': 0.3
                            }

                consensus = self._calculate_consensus(field_name, model_values)
                result['outcome_level'][es_id][field_name] = consensus

                if consensus['status'] == ConsensusStatus.DISCORDANT.value:
                    result['phase5_queue'].append({
                        'field_name': field_name,
                        'level': 'outcome',
                        'es_id': es_id,
                        'model_values': model_values,
                    })

        # Calculate overall agreement
        all_consensuses = list(result['study_level'].values())
        for es_data in result['outcome_level'].values():
            all_consensuses.extend(es_data.values())

        if all_consensuses:
            result['overall_agreement'] = sum(
                c.get('agreement', 0) for c in all_consensuses
            ) / len(all_consensuses)

        return result

    def verify_all(self, phase1_results: List[Dict], limit: Optional[int] = None) -> List[Dict]:
        """Run consensus on all Phase 1 results."""
        results = []
        items = phase1_results[:limit] if limit else phase1_results

        for i, p1 in enumerate(items):
            study_id = p1.get('study_id', 'unknown')
            logger.info(f"\n[{i+1}/{len(items)}] Consensus for study {study_id}")

            if not self.cost_tracker.check_budget(2.0):
                logger.error("Budget limit approaching, stopping")
                break

            result = self.verify_study(p1)
            results.append(result)

            # Save per-study
            output_dir = Path(self.config['paths']['phase2_consensus'])
            output_dir.mkdir(parents=True, exist_ok=True)
            with open(output_dir / f"{study_id}_consensus.json", 'w') as f:
                json.dump(result, f, indent=2)

        return results


def main():
    parser = argparse.ArgumentParser(description="Phase 2: Multi-Model Consensus")
    parser.add_argument("--config", default="configs/recode_v11/pipeline_config.yaml")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent.parent
    with open(base_dir / args.config) as f:
        config = yaml.safe_load(f)

    # Load Phase 1 results
    phase1_dir = Path(config['paths']['phase1_raw'])
    phase1_file = phase1_dir / "all_phase1_results.json"
    with open(phase1_file) as f:
        phase1_results = json.load(f)

    consensus = Phase2Consensus(config)
    results = consensus.verify_all(phase1_results, limit=args.limit)

    # Save combined + phase5 queue
    output_dir = Path(config['paths']['phase2_consensus'])
    with open(output_dir / "all_phase2_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    phase5_queue = []
    for r in results:
        phase5_queue.extend(r.get('phase5_queue', []))
    with open(output_dir / "phase5_queue.json", 'w') as f:
        json.dump(phase5_queue, f, indent=2)

    avg_agreement = sum(r.get('overall_agreement', 0) for r in results) / len(results) if results else 0

    print(f"\n{'='*60}")
    print("PHASE 2: MULTI-MODEL CONSENSUS COMPLETE")
    print(f"{'='*60}")
    print(f"Studies: {len(results)}")
    print(f"Avg agreement: {avg_agreement:.1%}")
    print(f"Phase 5 queue: {len(phase5_queue)} items")
    print(f"Cost: ${consensus.cost_tracker.total_cost:.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
