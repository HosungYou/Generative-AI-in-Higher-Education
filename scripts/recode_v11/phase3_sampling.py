#!/usr/bin/env python3
"""
Phase 3: Stratified Sampling for Human Verification
GenAI-HE Meta-Analysis v11 Re-coding Pipeline

Selects a stratified sample of studies for human gold standard coding.
Stratification ensures coverage across:
- Bloom's taxonomy levels
- Study designs (RCT, quasi-experimental)
- Academic disciplines
- Low-confidence AI consensus (oversampled 60%)
"""

import sys
import json
import random
import argparse
import yaml
import csv
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from recode_v11.schema import RECODE_FIELDS, get_study_level_fields, get_outcome_level_fields
from recode_v11.utils.audit import AuditLogger


@dataclass
class SamplingConfig:
    """Configuration for Phase 3 stratified sampling."""
    output_dir: Path
    sampling_rate: float
    minimum_studies: int
    maximum_studies: int
    stratification: List[str]
    low_confidence_oversample: float
    random_seed: int

    @classmethod
    def from_yaml(cls, config_path: str) -> 'SamplingConfig':
        """Load configuration from YAML file."""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        phase3_config = config['phase3']
        return cls(
            output_dir=Path(phase3_config['output_dir']),
            sampling_rate=phase3_config['sampling_rate'],
            minimum_studies=phase3_config['minimum_studies'],
            maximum_studies=phase3_config['maximum_studies'],
            stratification=phase3_config['stratification'],
            low_confidence_oversample=phase3_config['low_confidence_oversample'],
            random_seed=phase3_config['random_seed']
        )


@dataclass
class StudySample:
    """Represents a study selected for human verification."""
    study_id: str
    phase2_data: Dict
    strata: Dict[str, str]
    confidence_score: float
    is_low_confidence: bool
    n_outcomes: int
    selection_reason: str


class StratifiedSampler:
    """Performs stratified sampling for human verification."""

    def __init__(
        self,
        config: SamplingConfig,
        audit_logger: AuditLogger
    ):
        self.config = config
        self.audit = audit_logger
        self.phase2_results: List[Dict] = []
        self.total_studies: int = 0

    def load_phase2_results(self, phase2_dir: Path) -> None:
        """Load all Phase 2 consensus results."""
        all_results_file = phase2_dir / "all_phase2_results.json"

        if not all_results_file.exists():
            raise FileNotFoundError(
                f"Phase 2 results not found: {all_results_file}\n"
                f"Run Phase 2 consensus first."
            )

        with open(all_results_file) as f:
            self.phase2_results = json.load(f)

        self.total_studies = len(self.phase2_results)

        print(f"✓ Loaded {self.total_studies} studies from Phase 2")
        self.audit.log(
            phase='phase3',
            action='load',
            reason=f"Loaded {self.total_studies} Phase 2 results",
            actor='system',
            metadata={'source': str(all_results_file)}
        )

    def extract_strata(self, study: Dict) -> Dict[str, str]:
        """Extract stratification variables from a study."""
        strata = {}

        # Study-level strata
        study_level = study.get('study_level', {})

        if 'study_design' in self.config.stratification:
            design = study_level.get('study_design', {})
            strata['study_design'] = design.get('consensus_value', 'unknown')

        if 'discipline' in self.config.stratification:
            discipline = study_level.get('discipline', {})
            strata['discipline'] = discipline.get('consensus_value', 'unknown')

        # Outcome-level strata (aggregate from all outcomes)
        if 'blooms_level' in self.config.stratification:
            outcome_level = study.get('outcome_level', {})
            blooms_levels = set()
            for outcome_id, outcome_data in outcome_level.items():
                if 'blooms_level' in outcome_data:
                    blooms = outcome_data['blooms_level'].get('consensus_value')
                    if blooms:
                        blooms_levels.add(blooms)

            # Store as sorted list for consistency
            strata['blooms_level'] = ','.join(sorted(blooms_levels)) if blooms_levels else 'unknown'

        return strata

    def calculate_confidence_score(self, study: Dict) -> float:
        """Calculate overall confidence score for a study."""
        return study.get('overall_agreement', 0.0)

    def is_low_confidence(self, confidence: float) -> bool:
        """Determine if a study is low confidence (below 0.85)."""
        return confidence < 0.85

    def build_strata_groups(self) -> Dict[str, List[StudySample]]:
        """Group studies by strata."""
        strata_groups = defaultdict(list)

        for study in self.phase2_results:
            strata = self.extract_strata(study)
            confidence = self.calculate_confidence_score(study)
            is_low_conf = self.is_low_confidence(confidence)

            # Count outcomes
            outcome_level = study.get('outcome_level', {})
            n_outcomes = len(outcome_level)

            sample = StudySample(
                study_id=study['study_id'],
                phase2_data=study,
                strata=strata,
                confidence_score=confidence,
                is_low_confidence=is_low_conf,
                n_outcomes=n_outcomes,
                selection_reason=""
            )

            # Create strata key (sorted for consistency)
            strata_key = '|'.join(f"{k}={v}" for k, v in sorted(strata.items()))
            strata_groups[strata_key].append(sample)

        return strata_groups

    def select_sample(self) -> List[StudySample]:
        """
        Perform stratified sampling with constraints.

        Returns list of StudySample objects selected for human verification.
        """
        random.seed(self.config.random_seed)

        # Calculate target sample size
        target_n = int(self.total_studies * self.config.sampling_rate)
        target_n = max(self.config.minimum_studies, min(target_n, self.config.maximum_studies))

        print(f"\nTarget sample size: {target_n} studies ({self.config.sampling_rate*100:.0f}% of {self.total_studies})")

        # Build strata groups
        strata_groups = self.build_strata_groups()

        print(f"Found {len(strata_groups)} unique strata combinations")

        # Track coverage requirements
        coverage_needed = {
            'blooms_level': set(['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']),
            'study_design': set(['RCT', 'quasi-experimental']),
            'discipline': set()  # Any discipline is fine
        }

        selected: List[StudySample] = []
        selected_ids: Set[str] = set()

        # Phase 1: Ensure minimum coverage (at least 1 per required stratum)
        print("\nPhase 1: Ensuring minimum coverage...")

        # Cover each Bloom's level
        for blooms in coverage_needed['blooms_level']:
            matching_groups = [
                (key, samples) for key, samples in strata_groups.items()
                if blooms in samples[0].strata.get('blooms_level', '')
            ]

            if matching_groups:
                # Pick from first matching group
                key, samples = matching_groups[0]
                # Prefer low-confidence
                samples_sorted = sorted(samples, key=lambda s: (not s.is_low_confidence, s.confidence_score))
                for sample in samples_sorted:
                    if sample.study_id not in selected_ids:
                        sample.selection_reason = f"Coverage: Bloom's level '{blooms}'"
                        selected.append(sample)
                        selected_ids.add(sample.study_id)
                        print(f"  ✓ Selected study {sample.study_id} for Bloom's '{blooms}'")
                        break

        # Cover each study design
        for design in coverage_needed['study_design']:
            matching_groups = [
                (key, samples) for key, samples in strata_groups.items()
                if samples[0].strata.get('study_design') == design
            ]

            if matching_groups:
                key, samples = matching_groups[0]
                samples_sorted = sorted(samples, key=lambda s: (not s.is_low_confidence, s.confidence_score))
                for sample in samples_sorted:
                    if sample.study_id not in selected_ids:
                        sample.selection_reason = f"Coverage: Study design '{design}'"
                        selected.append(sample)
                        selected_ids.add(sample.study_id)
                        print(f"  ✓ Selected study {sample.study_id} for design '{design}'")
                        break

        print(f"Coverage selection: {len(selected)} studies")

        # Phase 2: Oversample low-confidence studies
        print("\nPhase 2: Oversampling low-confidence studies...")

        all_samples = [s for group in strata_groups.values() for s in group]
        low_conf_samples = [s for s in all_samples if s.is_low_confidence and s.study_id not in selected_ids]

        # Calculate how many low-confidence to add
        remaining = target_n - len(selected)
        low_conf_target = int(remaining * self.config.low_confidence_oversample)
        low_conf_target = min(low_conf_target, len(low_conf_samples))

        if low_conf_samples and low_conf_target > 0:
            # Randomly sample from low-confidence
            sampled_low = random.sample(low_conf_samples, low_conf_target)
            for sample in sampled_low:
                sample.selection_reason = f"Low confidence (agreement={sample.confidence_score:.2f})"
                selected.append(sample)
                selected_ids.add(sample.study_id)

            print(f"Low-confidence selection: {low_conf_target} studies")

        # Phase 3: Fill remaining with stratified random sampling
        print("\nPhase 3: Random stratified sampling...")

        remaining = target_n - len(selected)

        if remaining > 0:
            remaining_samples = [s for s in all_samples if s.study_id not in selected_ids]

            if len(remaining_samples) <= remaining:
                # Take all remaining
                for sample in remaining_samples:
                    sample.selection_reason = "Random stratified sample"
                    selected.append(sample)
                    selected_ids.add(sample.study_id)
            else:
                # Stratified random sample
                # Distribute proportionally across strata
                strata_counts = Counter()
                for sample in remaining_samples:
                    strata_key = '|'.join(f"{k}={v}" for k, v in sorted(sample.strata.items()))
                    strata_counts[strata_key] += 1

                # Allocate samples to strata proportionally
                allocations = {}
                total_remaining = len(remaining_samples)
                for strata_key, count in strata_counts.items():
                    proportion = count / total_remaining
                    allocations[strata_key] = max(1, int(remaining * proportion))

                # Sample from each stratum
                for strata_key, n_to_sample in allocations.items():
                    group_samples = [s for s in remaining_samples
                                   if '|'.join(f"{k}={v}" for k, v in sorted(s.strata.items())) == strata_key
                                   and s.study_id not in selected_ids]

                    n_actual = min(n_to_sample, len(group_samples))
                    if n_actual > 0:
                        sampled = random.sample(group_samples, n_actual)
                        for sample in sampled:
                            if len(selected) >= target_n:
                                break
                            sample.selection_reason = "Random stratified sample"
                            selected.append(sample)
                            selected_ids.add(sample.study_id)

                    if len(selected) >= target_n:
                        break

            print(f"Random selection: {len(selected) - (len(selected) - remaining)} studies")

        print(f"\n✓ Final sample size: {len(selected)} studies")

        return selected

    def generate_human_template(self, selected: List[StudySample], output_dir: Path) -> Path:
        """
        Generate CSV template for human coding.

        One row per field per study (not just study-level).
        """
        template_path = output_dir / "human_coding_template.csv"

        rows = []

        for sample in selected:
            study_id = sample.study_id
            study_data = sample.phase2_data

            # Study-level fields
            study_level = study_data.get('study_level', {})
            for field_name, field_data in study_level.items():
                consensus_value = field_data.get('consensus_value')
                status = field_data.get('status', 'unknown')
                agreement = field_data.get('agreement', 0.0)

                rows.append({
                    'study_id': study_id,
                    'outcome_id': '',  # Empty for study-level
                    'field_name': field_name,
                    'ai_consensus_value': consensus_value,
                    'ai_confidence': f"{agreement:.2f}",
                    'ai_status': status,
                    'human_value': '',
                    'notes': '',
                    'coding_date': ''
                })

            # Outcome-level fields
            outcome_level = study_data.get('outcome_level', {})
            for outcome_id, outcome_data in outcome_level.items():
                for field_name, field_data in outcome_data.items():
                    consensus_value = field_data.get('consensus_value')
                    status = field_data.get('status', 'unknown')
                    agreement = field_data.get('agreement', 0.0)

                    rows.append({
                        'study_id': study_id,
                        'outcome_id': outcome_id,
                        'field_name': field_name,
                        'ai_consensus_value': consensus_value,
                        'ai_confidence': f"{agreement:.2f}",
                        'ai_status': status,
                        'human_value': '',
                        'notes': '',
                        'coding_date': ''
                    })

        # Write CSV
        with open(template_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['study_id', 'outcome_id', 'field_name', 'ai_consensus_value',
                         'ai_confidence', 'ai_status', 'human_value', 'notes', 'coding_date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\n✓ Human coding template: {template_path}")
        print(f"  {len(rows)} fields to verify")

        self.audit.log(
            phase='phase3',
            action='generate_template',
            reason=f"Generated human coding template with {len(rows)} fields",
            actor='system',
            metadata={
                'template_path': str(template_path),
                'n_fields': len(rows),
                'n_studies': len(selected)
            }
        )

        return template_path

    def save_sample(self, selected: List[StudySample], output_dir: Path) -> Path:
        """Save selected sample to JSON."""
        sample_path = output_dir / "human_verification_sample.json"

        output = {
            'metadata': {
                'sampling_date': datetime.now().isoformat(),
                'total_studies': self.total_studies,
                'sample_size': len(selected),
                'sampling_rate': len(selected) / self.total_studies,
                'random_seed': self.config.random_seed,
                'stratification': self.config.stratification
            },
            'samples': []
        }

        for sample in selected:
            output['samples'].append({
                'study_id': sample.study_id,
                'selection_reason': sample.selection_reason,
                'strata': sample.strata,
                'confidence_score': sample.confidence_score,
                'is_low_confidence': sample.is_low_confidence,
                'n_outcomes': sample.n_outcomes,
                'phase2_data': sample.phase2_data
            })

        with open(sample_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✓ Sample saved: {sample_path}")

        self.audit.log(
            phase='phase3',
            action='save_sample',
            reason=f"Saved {len(selected)} studies for human verification",
            actor='system',
            metadata={
                'sample_path': str(sample_path),
                'sample_size': len(selected)
            }
        )

        return sample_path

    def print_summary(self, selected: List[StudySample]) -> None:
        """Print sampling summary statistics."""
        print("\n" + "="*70)
        print("PHASE 3 SAMPLING SUMMARY")
        print("="*70)

        print(f"\nTotal studies: {self.total_studies}")
        print(f"Sample size: {len(selected)} ({len(selected)/self.total_studies*100:.1f}%)")

        # Confidence distribution
        low_conf = sum(1 for s in selected if s.is_low_confidence)
        print(f"\nLow confidence studies: {low_conf} ({low_conf/len(selected)*100:.1f}%)")

        avg_conf = sum(s.confidence_score for s in selected) / len(selected)
        print(f"Average confidence: {avg_conf:.3f}")

        # Strata coverage
        print("\nStrata Coverage:")

        # Bloom's levels
        blooms_counts = Counter()
        for sample in selected:
            levels = sample.strata.get('blooms_level', 'unknown').split(',')
            for level in levels:
                if level and level != 'unknown':
                    blooms_counts[level] += 1

        if blooms_counts:
            print("\n  Bloom's Levels:")
            for level, count in sorted(blooms_counts.items()):
                print(f"    {level}: {count}")

        # Study designs
        design_counts = Counter(s.strata.get('study_design', 'unknown') for s in selected)
        print("\n  Study Designs:")
        for design, count in sorted(design_counts.items()):
            print(f"    {design}: {count}")

        # Disciplines
        discipline_counts = Counter(s.strata.get('discipline', 'unknown') for s in selected)
        print("\n  Disciplines:")
        for discipline, count in sorted(discipline_counts.items()):
            print(f"    {discipline}: {count}")

        print("\n" + "="*70)


def main():
    parser = argparse.ArgumentParser(
        description="Phase 3: Stratified Sampling for Human Verification"
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to pipeline_config.yaml'
    )

    args = parser.parse_args()

    # Load configuration
    config = SamplingConfig.from_yaml(args.config)

    # Setup audit logger
    with open(args.config) as f:
        full_config = yaml.safe_load(f)

    audit_log_path = full_config['audit']['log_file']
    audit = AuditLogger(audit_log_path, auto_flush=True)

    # Create output directory
    config.output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("PHASE 3: STRATIFIED SAMPLING FOR HUMAN VERIFICATION")
    print("="*70)

    # Initialize sampler
    sampler = StratifiedSampler(config, audit)

    # Load Phase 2 results
    phase2_dir = Path(full_config['phase2']['output_dir'])
    sampler.load_phase2_results(phase2_dir)

    # Perform stratified sampling
    selected = sampler.select_sample()

    # Save outputs
    sampler.save_sample(selected, config.output_dir)
    sampler.generate_human_template(selected, config.output_dir)

    # Print summary
    sampler.print_summary(selected)

    print("\n✓ Phase 3 complete!")
    print(f"\nNext steps:")
    print(f"1. Open: {config.output_dir / 'human_coding_template.csv'}")
    print(f"2. Fill in 'human_value' column with gold standard coding")
    print(f"3. Add notes if needed")
    print(f"4. Save and run Phase 4: python phase4_reliability.py --config {args.config}")


if __name__ == "__main__":
    main()
