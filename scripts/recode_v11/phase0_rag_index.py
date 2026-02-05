#!/usr/bin/env python3
"""
Phase 0: Build RAG Index for all studies.
Reuses extract_v10 document_processor and rag_builder patterns.
"""

import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import yaml
import json

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_v10.document_processor import process_document, DocumentResult
from extract_v10.rag_builder import (
    RAGConfig, build_study_collection, build_rag_for_studies,
    list_study_collections, get_embedding_model
)
from recode_v11.utils.data_loader import load_v81_csv, get_unique_studies, build_study_pdf_mapping
from recode_v11.utils.audit import AuditLogger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Phase0RAGBuilder:
    """Build RAG index for all studies in the dataset."""

    def __init__(self, config: Dict):
        self.config = config
        rag_cfg = config.get('rag', {})
        self.rag_config = RAGConfig(
            chunk_size=rag_cfg.get('chunk_size', 1000),
            chunk_overlap=rag_cfg.get('chunk_overlap', 200),
            embedding_model=rag_cfg.get('embedding_model', 'all-MiniLM-L6-v2'),
            persist_directory=rag_cfg.get('persist_directory', 'data/recode_v11/01_rag_index'),
            n_results=rag_cfg.get('n_results', 8),
        )
        self.audit = AuditLogger(config.get('audit', {}).get('log_file', 'data/recode_v11/audit/pipeline_audit.jsonl'))

    def build_all(self, pdf_mapping: Dict[str, Optional[str]], limit: Optional[int] = None) -> Dict:
        """Build RAG collections for all studies with PDFs."""
        # Pre-load embedding model
        logger.info("Loading embedding model...")
        get_embedding_model(self.rag_config.embedding_model)

        results = {'success': [], 'failed': [], 'skipped': []}
        items = list(pdf_mapping.items())
        if limit:
            items = items[:limit]

        for i, (study_id, pdf_path) in enumerate(items):
            if not pdf_path or not Path(pdf_path).exists():
                logger.warning(f"[{i+1}/{len(items)}] No PDF for study {study_id}, skipping")
                results['skipped'].append(study_id)
                continue

            try:
                logger.info(f"[{i+1}/{len(items)}] Processing study {study_id}...")

                # Process document to extract sections
                doc_result = process_document(Path(pdf_path), study_id)

                if not doc_result.sections or not doc_result.sections.get('full_text', '').strip():
                    logger.warning(f"  No text extracted for {study_id}")
                    results['failed'].append(study_id)
                    continue

                # Build RAG collection
                collection_name = build_study_collection(
                    study_id, doc_result.sections, self.rag_config
                )

                results['success'].append(study_id)

                self.audit.log(
                    phase='phase0', action='rag_build',
                    paper_id=study_id,
                    reason=f"RAG collection built: {collection_name}",
                    actor='system',
                    metadata={
                        'quality_score': doc_result.text_quality_score,
                        'page_count': doc_result.page_count,
                        'total_chars': doc_result.total_chars,
                        'sections_found': [s for s in ['abstract', 'methods', 'results', 'discussion']
                                          if doc_result.sections.get(s, '').strip()]
                    }
                )

            except Exception as e:
                logger.error(f"  Failed for {study_id}: {e}")
                results['failed'].append(study_id)

        logger.info(f"\nPhase 0 Complete: {len(results['success'])} success, "
                    f"{len(results['failed'])} failed, {len(results['skipped'])} skipped")
        return results


def main():
    parser = argparse.ArgumentParser(description="Phase 0: Build RAG Index")
    parser.add_argument("--config", default="configs/recode_v11/pipeline_config.yaml")
    parser.add_argument("--limit", type=int, default=None, help="Limit studies (for testing)")
    args = parser.parse_args()

    # Load config
    base_dir = Path(__file__).parent.parent.parent
    config_path = base_dir / args.config
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Load data and build PDF mapping
    csv_path = base_dir / config['input']['csv_path']
    pdf_dir = base_dir / config['input']['pdf_directory']

    rows = load_v81_csv(str(csv_path))
    pdf_mapping = build_study_pdf_mapping(str(pdf_dir), rows)

    # Build RAG index
    builder = Phase0RAGBuilder(config)
    results = builder.build_all(pdf_mapping, limit=args.limit)

    # Save summary
    summary_path = base_dir / config['paths']['rag_index'] / "phase0_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print("PHASE 0: RAG INDEX BUILD COMPLETE")
    print(f"{'='*60}")
    print(f"Success: {len(results['success'])}")
    print(f"Failed:  {len(results['failed'])}")
    print(f"Skipped: {len(results['skipped'])}")
    print(f"Collections: {len(list_study_collections(builder.rag_config))}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
