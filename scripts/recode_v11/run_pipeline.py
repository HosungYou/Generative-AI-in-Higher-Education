#!/usr/bin/env python3
"""
GenAI-HE Meta-Analysis v11: Master Pipeline Orchestrator

Coordinates all 7 phases (Phase 0-6) of the validated re-coding pipeline.

Usage:
    python scripts/recode_v11/run_pipeline.py --phase 0      # Only Phase 0
    python scripts/recode_v11/run_pipeline.py --phase 1      # Only Phase 1
    python scripts/recode_v11/run_pipeline.py --phase 0-2    # Phases 0 through 2
    python scripts/recode_v11/run_pipeline.py --phase 0-6    # Full pipeline
    python scripts/recode_v11/run_pipeline.py --full         # Same as 0-6
    python scripts/recode_v11/run_pipeline.py --smoke-test   # 5 studies, Phase 0-2 only
"""

import sys
import json
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from recode_v11.utils.cost_tracker import CostTracker
from recode_v11.utils.data_loader import load_v81_csv, get_unique_studies, build_study_pdf_mapping

# Phase imports (will be imported dynamically to avoid circular dependencies)
# from recode_v11.phase0_rag_index import Phase0RAGBuilder
# from recode_v11.phase1_extract import Phase1Extractor
# from recode_v11.effect_size_filler import EffectSizeFiller
# from recode_v11.phase2_consensus import Phase2Consensus
# from recode_v11.phase3_sampling import StratifiedSampler
# from recode_v11.phase4_reliability import Phase4Reliability
# from recode_v11.phase5_resolution import DiscrepancyResolver
# from recode_v11.phase6_qa import Phase6QA

logger = logging.getLogger(__name__)


class PipelineState:
    """Track pipeline execution state."""

    def __init__(self, state_file: str):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load existing state or create new."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "last_completed_phase": -1,
            "timestamp": datetime.now().isoformat(),
            "studies_processed": 0,
            "cost_so_far": 0.0,
            "phases": {
                str(i): {"status": "pending", "duration_sec": 0}
                for i in range(7)
            }
        }

    def save(self):
        """Save state to disk."""
        self.state['timestamp'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def mark_phase_start(self, phase: int):
        """Mark a phase as started."""
        self.state['phases'][str(phase)]['status'] = 'running'
        self.state['phases'][str(phase)]['start_time'] = time.time()
        self.save()

    def mark_phase_complete(self, phase: int):
        """Mark a phase as completed."""
        start_time = self.state['phases'][str(phase)].get('start_time', time.time())
        duration = time.time() - start_time
        self.state['phases'][str(phase)]['status'] = 'complete'
        self.state['phases'][str(phase)]['duration_sec'] = int(duration)
        self.state['last_completed_phase'] = max(self.state['last_completed_phase'], phase)
        self.save()

    def mark_phase_failed(self, phase: int, error: str):
        """Mark a phase as failed."""
        self.state['phases'][str(phase)]['status'] = 'failed'
        self.state['phases'][str(phase)]['error'] = error
        self.save()

    def update_cost(self, cost: float):
        """Update total cost."""
        self.state['cost_so_far'] = cost
        self.save()

    def update_studies(self, count: int):
        """Update studies processed count."""
        self.state['studies_processed'] = count
        self.save()


class PipelineOrchestrator:
    """Orchestrates the 7-phase re-coding pipeline."""

    def __init__(
        self,
        config_path: str,
        limit: Optional[int] = None,
        dry_run: bool = False
    ):
        self.config_path = Path(config_path)
        self.limit = limit
        self.dry_run = dry_run

        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize state tracker
        state_file = Path(self.config['paths']['base']) / 'pipeline_state.json'
        self.state = PipelineState(str(state_file))

        # Initialize cost tracker
        self.cost_tracker = CostTracker(
            budget=self.config['costs']['budget'],
            warning_threshold=self.config['costs']['warning_threshold'],
            log_file=str(Path(self.config['paths']['audit']) / 'cost_log.jsonl')
        )

        # Setup logging
        self._setup_logging()

        # Load data
        self._load_data()

    def _setup_logging(self):
        """Configure logging."""
        log_dir = Path(self.config['paths']['audit'])
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _load_data(self):
        """Load input CSV and build study mapping."""
        logger.info("Loading input data...")

        csv_path = self.config['input']['csv_path']
        pdf_dir = self.config['input']['pdf_directory']

        self.rows = load_v81_csv(csv_path)
        self.studies = get_unique_studies(self.rows)
        self.study_pdf_map = build_study_pdf_mapping(pdf_dir, self.rows)

        # Apply limit if specified
        if self.limit:
            study_ids = list(self.studies.keys())[:self.limit]
            self.studies = {sid: self.studies[sid] for sid in study_ids}
            logger.info(f"Limited to {self.limit} studies for testing")

        self.state.update_studies(len(self.studies))

        logger.info(f"Loaded {len(self.studies)} studies, {len(self.rows)} total rows")

    def run_phase0(self) -> bool:
        """Phase 0: RAG Index Build"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 0: RAG Index Build")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would build RAG index for PDFs")
            return True

        try:
            self.state.mark_phase_start(0)

            # Import dynamically to avoid circular dependencies
            from recode_v11.phase0_rag_index import Phase0RAGBuilder

            builder = Phase0RAGBuilder(self.config)
            builder.build_index(self.study_pdf_map)

            self.state.mark_phase_complete(0)
            logger.info("✓ Phase 0 complete: RAG index built")
            return True

        except Exception as e:
            logger.error(f"✗ Phase 0 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(0, str(e))
            return False

    def run_phase1(self) -> bool:
        """Phase 1: Claude Extraction"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 1: Claude Extraction")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would extract fields with Claude")
            return True

        try:
            self.state.mark_phase_start(1)

            from recode_v11.phase1_extract import Phase1Extractor

            extractor = Phase1Extractor(self.config, self.cost_tracker)
            extractor.extract_all_studies(self.studies, self.study_pdf_map)

            self.state.update_cost(self.cost_tracker.total_cost)
            self.state.mark_phase_complete(1)
            logger.info("✓ Phase 1 complete: Claude extraction done")
            return True

        except Exception as e:
            logger.error(f"✗ Phase 1 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(1, str(e))
            return False

    def run_effect_size_fill(self) -> bool:
        """Effect Size Fill (parallel with Phase 1 conceptually)"""
        logger.info("\n" + "="*60)
        logger.info("EFFECT SIZE FILL: 4-Tier Calculation")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would fill missing effect sizes")
            return True

        try:
            from recode_v11.effect_size_filler import EffectSizeFiller

            filler = EffectSizeFiller(self.config, self.cost_tracker)
            filler.fill_effect_sizes(self.rows)

            self.state.update_cost(self.cost_tracker.total_cost)
            logger.info("✓ Effect size fill complete")
            return True

        except Exception as e:
            logger.error(f"✗ Effect size fill failed: {e}", exc_info=True)
            return False

    def run_phase2(self) -> bool:
        """Phase 2: Multi-Model Consensus"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 2: Multi-Model Consensus")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would run 3-model consensus")
            return True

        try:
            self.state.mark_phase_start(2)

            from recode_v11.phase2_consensus import Phase2Consensus

            consensus = Phase2Consensus(self.config, self.cost_tracker)
            consensus.run_consensus(self.studies, self.study_pdf_map)

            self.state.update_cost(self.cost_tracker.total_cost)
            self.state.mark_phase_complete(2)
            logger.info("✓ Phase 2 complete: 3-model consensus achieved")
            return True

        except Exception as e:
            logger.error(f"✗ Phase 2 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(2, str(e))
            return False

    def run_phase3(self) -> bool:
        """Phase 3: Human Verification Sampling"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 3: Human Verification Sampling")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would generate human coding template")
            return True

        try:
            self.state.mark_phase_start(3)

            from recode_v11.phase3_sampling import StratifiedSampler

            sampler = StratifiedSampler(self.config)
            template_path = sampler.generate_sample()

            self.state.mark_phase_complete(3)

            # Print human pause message
            self._print_human_pause_message(template_path)

            return True

        except Exception as e:
            logger.error(f"✗ Phase 3 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(3, str(e))
            return False

    def _print_human_pause_message(self, template_path: str):
        """Print message for human verification pause."""
        print("\n" + "="*60)
        print("PHASE 3 COMPLETE: Human Verification Required")
        print("="*60)
        print(f"A human coding template has been generated at:")
        print(f"  {template_path}")
        print()
        print("INSTRUCTIONS:")
        print("  1. Open the CSV template")
        print("  2. For each row, code the 'human_value' column independently")
        print("  3. Do NOT reference the 'ai_consensus_value' while coding")
        print("  4. Save the completed template")
        print("  5. Re-run with: python run_pipeline.py --phase 4-6")
        print()
        print("Pipeline paused. Phases 4-6 require human coding data.")
        print("="*60 + "\n")

    def run_phase4(self) -> bool:
        """Phase 4: ICR Calculation"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 4: Inter-Coder Reliability")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would calculate ICR metrics")
            return True

        try:
            self.state.mark_phase_start(4)

            from recode_v11.phase4_reliability import Phase4Reliability

            reliability = Phase4Reliability(self.config)
            reliability.calculate_reliability()

            self.state.mark_phase_complete(4)
            logger.info("✓ Phase 4 complete: ICR calculated")
            return True

        except Exception as e:
            logger.error(f"✗ Phase 4 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(4, str(e))
            return False

    def run_phase5(self) -> bool:
        """Phase 5: Discrepancy Resolution"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 5: Discrepancy Resolution")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would resolve discrepancies")
            return True

        try:
            self.state.mark_phase_start(5)

            from recode_v11.phase5_resolution import DiscrepancyResolver

            resolver = DiscrepancyResolver(self.config)
            resolver.resolve_discrepancies()

            self.state.mark_phase_complete(5)
            logger.info("✓ Phase 5 complete: Discrepancies resolved")
            return True

        except Exception as e:
            logger.error(f"✗ Phase 5 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(5, str(e))
            return False

    def run_phase6(self) -> bool:
        """Phase 6: QA Gates + Final CSV"""
        logger.info("\n" + "="*60)
        logger.info("PHASE 6: QA Gates + Final CSV")
        logger.info("="*60)

        if self.dry_run:
            logger.info("[DRY RUN] Would run QA gates and generate final CSV")
            return True

        try:
            self.state.mark_phase_start(6)

            from recode_v11.phase6_qa import Phase6QA

            qa = Phase6QA(self.config)
            qa_results = qa.run_qa_gates()

            self.state.mark_phase_complete(6)
            logger.info("✓ Phase 6 complete: Final CSV generated")

            return qa_results['all_gates_passed']

        except Exception as e:
            logger.error(f"✗ Phase 6 failed: {e}", exc_info=True)
            self.state.mark_phase_failed(6, str(e))
            return False

    def run_phases(self, phase_range: List[int]) -> bool:
        """Run specified phases in order."""
        logger.info(f"\nRunning phases: {phase_range}")

        phase_methods = {
            0: self.run_phase0,
            1: self.run_phase1,
            2: self.run_phase2,
            3: self.run_phase3,
            4: self.run_phase4,
            5: self.run_phase5,
            6: self.run_phase6,
        }

        for phase_num in phase_range:
            # Check budget before each phase
            if not self.dry_run:
                if not self.cost_tracker.check_budget(estimated_cost=5.0):
                    logger.error(f"Insufficient budget for Phase {phase_num}")
                    return False

            # Run phase
            phase_method = phase_methods.get(phase_num)
            if not phase_method:
                logger.error(f"Invalid phase number: {phase_num}")
                return False

            success = phase_method()

            if not success:
                logger.error(f"Phase {phase_num} failed. Pipeline stopped.")
                self._print_recovery_suggestion(phase_num)
                return False

            # Run effect size fill after Phase 0 or Phase 1
            if phase_num == 1 and not self.dry_run:
                if not self.run_effect_size_fill():
                    logger.warning("Effect size fill had issues, but continuing...")

        return True

    def _print_recovery_suggestion(self, failed_phase: int):
        """Print recovery suggestions after failure."""
        print("\n" + "="*60)
        print("RECOVERY SUGGESTIONS")
        print("="*60)
        print(f"Phase {failed_phase} failed.")
        print()
        print("To recover:")
        print(f"  1. Check the error logs above")
        print(f"  2. Fix any data or configuration issues")
        print(f"  3. Re-run with: python run_pipeline.py --phase {failed_phase}-6")
        print()
        print(f"State file: {self.state.state_file}")
        print("="*60 + "\n")

    def print_summary(self, all_phases_passed: bool):
        """Print comprehensive pipeline summary."""
        cost_summary = self.cost_tracker.get_summary()

        print("\n" + "="*60)
        print("PIPELINE COMPLETE: GenAI Meta-Analysis v11")
        print("="*60)

        # Phases completed
        completed_phases = [
            p for p, data in self.state.state['phases'].items()
            if data['status'] == 'complete'
        ]
        print(f"Phases completed: {', '.join(completed_phases)}")

        # Studies processed
        print(f"Studies processed: {self.state.state['studies_processed']}")

        # Effect sizes (if available)
        effect_size_file = Path(self.config['effect_sizes']['output_dir']) / 'effect_sizes_filled.csv'
        if effect_size_file.exists():
            import csv
            with open(effect_size_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                filled = sum(1 for r in rows if r.get('Hedges_g'))
                print(f"Effect sizes filled: {filled}/{len(rows)}")

        # Final CSV
        final_csv = Path(self.config['phase6']['output_dir']) / self.config['phase6']['final_csv']
        if final_csv.exists():
            print(f"Final CSV: {final_csv}")

        # Cost
        print(f"Total cost: ${cost_summary['total_cost']:.2f} / ${cost_summary['budget']:.2f}")

        # Quality gates
        if all_phases_passed:
            print("Quality gates: ALL PASSED ✓")
        else:
            print("Quality gates: SOME FAILED ✗")

        print("="*60)

        # Cost breakdown
        if cost_summary['by_phase']:
            print("\nCost by Phase:")
            for phase, cost in sorted(cost_summary['by_phase'].items()):
                print(f"  Phase {phase}: ${cost:.2f}")

        if cost_summary['by_provider']:
            print("\nCost by Provider:")
            for provider, cost in sorted(cost_summary['by_provider'].items()):
                print(f"  {provider}: ${cost:.2f}")

        print("\n" + "="*60 + "\n")


def parse_phase_arg(phase_arg: str) -> List[int]:
    """Parse phase argument into list of phase numbers."""
    if '-' in phase_arg:
        # Range: "0-6"
        start, end = phase_arg.split('-')
        return list(range(int(start), int(end) + 1))
    else:
        # Single phase: "0"
        return [int(phase_arg)]


def main():
    parser = argparse.ArgumentParser(
        description='GenAI-HE Meta-Analysis v11: Master Pipeline Orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py --phase 0        # Only Phase 0
  python run_pipeline.py --phase 1        # Only Phase 1
  python run_pipeline.py --phase 0-2      # Phases 0 through 2
  python run_pipeline.py --phase 0-6      # Full pipeline
  python run_pipeline.py --full           # Same as 0-6
  python run_pipeline.py --smoke-test     # 5 studies, Phase 0-2
        """
    )

    parser.add_argument(
        '--phase',
        type=str,
        help='Phase(s) to run (e.g., "0", "0-2", "4-6")'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run full pipeline (phases 0-6)'
    )
    parser.add_argument(
        '--smoke-test',
        action='store_true',
        help='Run smoke test (5 studies, phases 0-2)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/recode_v11/pipeline_config.yaml',
        help='Path to pipeline config YAML'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of studies for testing'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate config and data without running'
    )

    args = parser.parse_args()

    # Determine phase range
    if args.smoke_test:
        phase_range = [0, 1, 2]
        limit = 5
    elif args.full:
        phase_range = list(range(7))
        limit = args.limit
    elif args.phase:
        phase_range = parse_phase_arg(args.phase)
        limit = args.limit
    else:
        parser.print_help()
        sys.exit(1)

    # Initialize orchestrator
    orchestrator = PipelineOrchestrator(
        config_path=args.config,
        limit=limit,
        dry_run=args.dry_run
    )

    # Run pipeline
    success = orchestrator.run_phases(phase_range)

    # Print summary
    orchestrator.print_summary(all_phases_passed=success)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
