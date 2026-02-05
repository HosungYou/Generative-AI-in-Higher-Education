#!/usr/bin/env python3
"""
Phase 1: RAG-based Claude Extraction
Extracts 11 fields using field-specific prompts + RAG context.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_v10.rag_builder import (
    RAGConfig, query_study_collection, extract_moderator_with_rag
)
from recode_v11.schema import (
    RECODE_FIELDS, FieldCategory, get_study_level_fields,
    get_outcome_level_fields, validate_extraction
)
from recode_v11.utils.llm_clients import UnifiedLLMClient
from recode_v11.utils.data_loader import load_v81_csv, get_unique_studies, build_study_pdf_mapping
from recode_v11.utils.cost_tracker import CostTracker
from recode_v11.utils.audit import AuditLogger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Field-specific RAG queries
FIELD_RAG_QUERIES = {
    "blooms_level": "What learning outcomes are measured? What cognitive level (remembering, understanding, applying, analyzing, evaluating, creating) does the assessment target?",
    "outcome_dimension": "What dimension of learning is the outcome measuring? Is it cognitive (knowledge/skills), affective (attitudes/motivation), behavioral (actions/practices), or metacognitive (self-regulation/awareness)?",
    "study_design": "What is the research design? Is it a randomized controlled trial (RCT), quasi-experimental, pre-post, or crossover design? How were participants assigned to groups?",
    "control_condition": "What did the control group receive? Was it no treatment, traditional instruction, human tutoring, alternative technology, or a waitlist?",
    "genai_tool": "What generative AI tool was used in the intervention? Was it ChatGPT, Claude, Gemini, Copilot, or a custom tool?",
    "genai_tool_version": "What specific version of the AI tool was used? Was it GPT-3.5, GPT-4, GPT-4o, Claude 3, Gemini Pro?",
    "intervention_duration": "How long did the intervention last? Was it a single session, less than a week, 1-4 weeks, 1-3 months, or more than 3 months?",
    "education_level": "What education level were the participants? Were they K-12 students, undergraduates, graduates, or professional learners?",
    "discipline": "What academic discipline or subject area was the study conducted in? Was it STEM, humanities, social sciences, medicine, business, education, language, CS, or engineering?",
}


class Phase1Extractor:
    """RAG-based extraction using Claude for all 11 fields."""

    CONFIDENCE_THRESHOLD = 0.75

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

        # Load prompts
        self.prompts = {}
        prompts_dir = Path(__file__).parent / "prompts"
        for field_name in RECODE_FIELDS:
            prompt_file = prompts_dir / f"{field_name}.txt"
            if prompt_file.exists():
                self.prompts[field_name] = prompt_file.read_text().strip()

        model_cfg = config.get('models', {}).get('primary', {})
        self.model = model_cfg.get('model', 'claude-sonnet-4-5-20250929')
        self.provider = model_cfg.get('provider', 'anthropic')

    def _build_field_prompt(self, field_name: str, rag_context: str,
                            outcome_name: str = "", study_meta: Dict = None) -> str:
        """Build extraction prompt for a specific field."""
        field_def = RECODE_FIELDS[field_name]

        # Use custom prompt if available, else generate
        if field_name in self.prompts:
            base_prompt = self.prompts[field_name]
        else:
            base_prompt = f"Extract the {field_name} from this academic paper."

        allowed = field_def.allowed_values
        allowed_str = ", ".join(allowed) if allowed else "any value"

        meta_str = ""
        if study_meta:
            meta_str = f"\nPAPER: {study_meta.get('title', 'Unknown')} ({study_meta.get('year', '')})\nAuthors: {study_meta.get('authors', '')}\n"

        outcome_str = ""
        if outcome_name:
            outcome_str = f'\nOUTCOME BEING CLASSIFIED: "{outcome_name}"\n'

        return f"""{base_prompt}

{meta_str}{outcome_str}
RELEVANT PAPER EXCERPTS:
{rag_context}

ALLOWED VALUES: {allowed_str}

Respond ONLY in this exact JSON format:
{{
    "value": "<your classification>",
    "confidence": <0.0-1.0>,
    "evidence_quote": "<exact quote from paper supporting your choice>",
    "reasoning": "<brief explanation>"
}}"""

    def extract_study(self, study_id: str, rows: List[Dict], study_meta: Dict) -> Dict:
        """Extract all fields for a study."""
        result = {
            'study_id': study_id,
            'extraction_date': datetime.now().isoformat(),
            'model': self.model,
            'study_level': {},
            'outcome_level': {},
            'low_confidence_fields': [],
        }

        # --- Extract study-level fields (once per study) ---
        for field_name, field_def in get_study_level_fields().items():
            if field_def.category == FieldCategory.NUMERICAL:
                continue  # Numerical handled by effect_size_filler

            try:
                # Get RAG context
                query = FIELD_RAG_QUERIES.get(field_name, f"What is the {field_name}?")
                rag_result = query_study_collection(
                    study_id, query, n_results=self.rag_config.n_results, config=self.rag_config
                )

                if not rag_result.context_combined:
                    logger.warning(f"  No RAG context for {study_id}.{field_name}")
                    result['study_level'][field_name] = {
                        'value': None, 'confidence': 0.0,
                        'evidence_quote': '', 'reasoning': 'No RAG context available'
                    }
                    continue

                # Build prompt and call LLM
                prompt = self._build_field_prompt(
                    field_name, rag_result.context_combined, study_meta=study_meta
                )

                response = self.llm.call(
                    provider=self.provider, model=self.model,
                    prompt=prompt, temperature=0.1, max_tokens=500
                )

                if response:
                    self.cost_tracker.add(
                        provider=self.provider, model=self.model, phase='phase1',
                        input_tokens=response.input_tokens, output_tokens=response.output_tokens,
                        cost=response.cost, study_id=study_id
                    )

                    extraction = response.parse_json()
                    result['study_level'][field_name] = extraction

                    # Track low confidence
                    if extraction.get('confidence', 0) < self.CONFIDENCE_THRESHOLD:
                        result['low_confidence_fields'].append(field_name)

                    logger.info(f"  {field_name}: {extraction.get('value')} "
                              f"(conf: {extraction.get('confidence', 0):.2f})")
                else:
                    result['study_level'][field_name] = {
                        'value': None, 'confidence': 0.0,
                        'evidence_quote': '', 'reasoning': 'LLM call failed'
                    }

            except Exception as e:
                logger.error(f"  Error extracting {field_name} for {study_id}: {e}")
                result['study_level'][field_name] = {
                    'value': None, 'confidence': 0.0,
                    'evidence_quote': '', 'reasoning': str(e)
                }

        # --- Extract outcome-level fields (per ES_ID) ---
        for row in rows:
            es_id = row.get('ES_ID', '')
            outcome_name = row.get('Outcome_Name', '')

            result['outcome_level'].setdefault(es_id, {})

            for field_name, field_def in get_outcome_level_fields().items():
                if field_def.category == FieldCategory.NUMERICAL:
                    continue

                try:
                    query = FIELD_RAG_QUERIES.get(field_name, f"What is the {field_name}?")
                    rag_result = query_study_collection(
                        study_id, query, n_results=self.rag_config.n_results, config=self.rag_config
                    )

                    prompt = self._build_field_prompt(
                        field_name, rag_result.context_combined,
                        outcome_name=outcome_name, study_meta=study_meta
                    )

                    response = self.llm.call(
                        provider=self.provider, model=self.model,
                        prompt=prompt, temperature=0.1, max_tokens=500
                    )

                    if response:
                        self.cost_tracker.add(
                            provider=self.provider, model=self.model, phase='phase1',
                            input_tokens=response.input_tokens, output_tokens=response.output_tokens,
                            cost=response.cost, study_id=study_id
                        )
                        extraction = response.parse_json()
                        result['outcome_level'][es_id][field_name] = extraction

                        if extraction.get('confidence', 0) < self.CONFIDENCE_THRESHOLD:
                            result['low_confidence_fields'].append(f"{es_id}.{field_name}")
                    else:
                        result['outcome_level'][es_id][field_name] = {
                            'value': None, 'confidence': 0.0,
                            'evidence_quote': '', 'reasoning': 'LLM call failed'
                        }

                except Exception as e:
                    logger.error(f"  Error extracting {field_name} for {es_id}: {e}")
                    result['outcome_level'][es_id][field_name] = {
                        'value': None, 'confidence': 0.0,
                        'evidence_quote': '', 'reasoning': str(e)
                    }

        # Log audit
        self.audit.log(
            phase='phase1', action='extract', paper_id=study_id,
            reason=f"Extracted {len(result['study_level'])} study-level + "
                   f"{sum(len(v) for v in result['outcome_level'].values())} outcome-level fields",
            actor=f'ai:{self.model}',
            metadata={'low_confidence': result['low_confidence_fields']}
        )

        return result

    def extract_all(self, rows: List[Dict], pdf_mapping: Dict, limit: Optional[int] = None) -> List[Dict]:
        """Extract all studies."""
        studies = get_unique_studies(rows)
        results = []
        items = list(studies.items())
        if limit:
            items = items[:limit]

        for i, (study_id, study_rows) in enumerate(items):
            logger.info(f"\n[{i+1}/{len(items)}] Study {study_id} ({len(study_rows)} outcomes)")

            if not self.cost_tracker.check_budget(1.0):
                logger.error("Budget limit approaching, stopping extraction")
                break

            study_meta = {
                'study_id': study_id,
                'title': study_rows[0].get('Title', ''),
                'year': study_rows[0].get('Year', ''),
                'authors': study_rows[0].get('Authors', ''),
            }

            result = self.extract_study(study_id, study_rows, study_meta)
            results.append(result)

            # Save per-study JSON
            output_dir = Path(self.config['paths']['phase1_raw'])
            output_dir.mkdir(parents=True, exist_ok=True)
            with open(output_dir / f"{study_id}_phase1.json", 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        return results


def main():
    parser = argparse.ArgumentParser(description="Phase 1: RAG-based Claude Extraction")
    parser.add_argument("--config", default="configs/recode_v11/pipeline_config.yaml")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent.parent
    with open(base_dir / args.config) as f:
        config = yaml.safe_load(f)

    rows = load_v81_csv(str(base_dir / config['input']['csv_path']))
    pdf_mapping = build_study_pdf_mapping(str(base_dir / config['input']['pdf_directory']), rows)

    extractor = Phase1Extractor(config)
    results = extractor.extract_all(rows, pdf_mapping, limit=args.limit)

    # Save summary
    output_dir = Path(config['paths']['phase1_raw'])
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        'phase': 1,
        'date': datetime.now().isoformat(),
        'total_studies': len(results),
        'avg_study_fields': sum(len(r['study_level']) for r in results) / len(results) if results else 0,
        'total_low_confidence': sum(len(r['low_confidence_fields']) for r in results),
        'cost': extractor.cost_tracker.get_summary(),
    }
    with open(output_dir / "phase1_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    # Save all results combined
    with open(output_dir / "all_phase1_results.json", 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("PHASE 1: RAG-BASED EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Studies processed: {len(results)}")
    print(f"Total cost: ${extractor.cost_tracker.total_cost:.2f}")
    print(f"Low confidence fields: {summary['total_low_confidence']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
