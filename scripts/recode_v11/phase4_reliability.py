#!/usr/bin/env python3
"""
Phase 4: Inter-Coder Reliability (ICR) Calculation
GenAI-HE Meta-Analysis v11 Re-coding Pipeline

Calculates reliability metrics between AI consensus (Phase 2) and human gold standard (Phase 3).

Metrics:
- Categorical fields: Cohen's κ (target ≥ 0.85, acceptable ≥ 0.80)
- Ordinal fields: Weighted κ quadratic (target ≥ 0.80, acceptable ≥ 0.75)
- Numerical fields: ICC(2,1) (target ≥ 0.95, acceptable ≥ 0.90) + MAE < 0.05
- Overall: Accuracy, Krippendorff's α for 3-model agreement
"""

import sys
import json
import csv
import argparse
import yaml
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from recode_v11.schema import (
    RECODE_FIELDS, FieldType, get_categorical_fields,
    get_ordinal_fields, get_numerical_fields, get_field
)
from recode_v11.utils.metrics import (
    cohens_kappa, weighted_kappa, krippendorff_alpha,
    intraclass_correlation, agreement_rate, interpret_kappa,
    mean_absolute_error, root_mean_squared_error, overall_accuracy
)
from recode_v11.utils.audit import AuditLogger


@dataclass
class ReliabilityTargets:
    """Target and acceptable thresholds for reliability metrics."""
    cohens_kappa: float
    weighted_kappa: float
    icc: float
    mae_hedges_g: float

    cohens_kappa_acceptable: float
    weighted_kappa_acceptable: float
    icc_acceptable: float


@dataclass
class FieldReliability:
    """Reliability metrics for a single field."""
    field_name: str
    field_type: FieldType
    n_compared: int
    metric_name: str
    metric_value: float
    target: float
    acceptable: float
    status: str  # "PASS", "ACCEPTABLE", "FAIL"
    interpretation: Optional[str] = None
    mae: Optional[float] = None  # For numerical fields
    rmse: Optional[float] = None  # For numerical fields
    simple_agreement: Optional[float] = None


@dataclass
class Phase4Report:
    """Complete Phase 4 reliability report."""
    date: str
    n_studies_verified: int
    n_fields_compared: int
    per_field: Dict[str, FieldReliability]
    overall_accuracy: float
    krippendorff_alpha_3model: Optional[float] = None
    all_gates_passed: bool = False
    failed_fields: List[str] = field(default_factory=list)
    summary: str = ""


class Phase4Reliability:
    """Calculates inter-coder reliability between AI and human coding."""

    def __init__(
        self,
        config_path: str,
        audit_logger: AuditLogger
    ):
        # Load configuration
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.phase4_config = self.config['phase4']
        self.output_dir = Path(self.phase4_config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.targets = ReliabilityTargets(
            cohens_kappa=self.phase4_config['targets']['cohens_kappa'],
            weighted_kappa=self.phase4_config['targets']['weighted_kappa'],
            icc=self.phase4_config['targets']['icc'],
            mae_hedges_g=self.phase4_config['targets']['mae_hedges_g'],
            cohens_kappa_acceptable=self.phase4_config['acceptable']['cohens_kappa'],
            weighted_kappa_acceptable=self.phase4_config['acceptable']['weighted_kappa'],
            icc_acceptable=self.phase4_config['acceptable']['icc']
        )

        self.audit = audit_logger

        # Data storage
        self.human_coding: Dict[str, Dict[str, Any]] = {}  # {study_id: {field_name: value}}
        self.ai_consensus: Dict[str, Dict[str, Any]] = {}  # {study_id: {field_name: value}}
        self.phase2_full_data: Dict[str, Dict] = {}

    def load_human_coding(self, csv_path: Path) -> None:
        """
        Load human coding from filled template CSV.

        Expects columns: study_id, outcome_id, field_name, ai_consensus_value,
                        ai_confidence, ai_status, human_value, notes, coding_date
        """
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Human coding template not found: {csv_path}\n"
                f"Complete Phase 3 human verification first."
            )

        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Parse human coding
        for row in rows:
            study_id = row['study_id']
            outcome_id = row.get('outcome_id', '')
            field_name = row['field_name']
            human_value = row.get('human_value', '').strip()

            # Skip if human didn't code this field
            if not human_value:
                continue

            # Create unique key for study+outcome+field
            if outcome_id:
                key = f"{study_id}:{outcome_id}:{field_name}"
            else:
                key = f"{study_id}::{field_name}"

            if study_id not in self.human_coding:
                self.human_coding[study_id] = {}

            self.human_coding[study_id][key] = human_value

        n_fields = sum(len(fields) for fields in self.human_coding.values())
        print(f"✓ Loaded human coding for {len(self.human_coding)} studies, {n_fields} fields")

        self.audit.log(
            phase='phase4',
            action='load',
            reason=f"Loaded human coding from {csv_path.name}",
            actor='system',
            metadata={
                'n_studies': len(self.human_coding),
                'n_fields': n_fields
            }
        )

    def load_ai_consensus(self, phase3_sample_path: Path) -> None:
        """Load AI consensus values from Phase 3 sample JSON."""
        if not phase3_sample_path.exists():
            raise FileNotFoundError(f"Phase 3 sample not found: {phase3_sample_path}")

        with open(phase3_sample_path) as f:
            sample_data = json.load(f)

        for sample in sample_data['samples']:
            study_id = sample['study_id']
            phase2_data = sample['phase2_data']

            self.phase2_full_data[study_id] = phase2_data

            if study_id not in self.ai_consensus:
                self.ai_consensus[study_id] = {}

            # Extract study-level fields
            study_level = phase2_data.get('study_level', {})
            for field_name, field_data in study_level.items():
                consensus_value = field_data.get('consensus_value')
                key = f"{study_id}::{field_name}"
                self.ai_consensus[study_id][key] = consensus_value

            # Extract outcome-level fields
            outcome_level = phase2_data.get('outcome_level', {})
            for outcome_id, outcome_data in outcome_level.items():
                for field_name, field_data in outcome_data.items():
                    consensus_value = field_data.get('consensus_value')
                    key = f"{study_id}:{outcome_id}:{field_name}"
                    self.ai_consensus[study_id][key] = consensus_value

        n_fields = sum(len(fields) for fields in self.ai_consensus.values())
        print(f"✓ Loaded AI consensus for {len(self.ai_consensus)} studies, {n_fields} fields")

        self.audit.log(
            phase='phase4',
            action='load',
            reason=f"Loaded AI consensus from {phase3_sample_path.name}",
            actor='system',
            metadata={
                'n_studies': len(self.ai_consensus),
                'n_fields': n_fields
            }
        )

    def align_values(self, field_name: str) -> Tuple[List[Any], List[Any]]:
        """
        Align AI and human values for a specific field.

        Returns (ai_values, human_values) as parallel lists.
        """
        field_def = get_field(field_name)

        ai_values = []
        human_values = []

        # Iterate through all human-coded studies
        for study_id, human_fields in self.human_coding.items():
            for key, human_val in human_fields.items():
                # Extract field name from key
                parts = key.split(':')
                key_field = parts[2]

                if key_field != field_name:
                    continue

                # Get corresponding AI value
                if study_id in self.ai_consensus and key in self.ai_consensus[study_id]:
                    ai_val = self.ai_consensus[study_id][key]

                    # Convert values to appropriate type
                    if field_def.field_type == FieldType.FLOAT:
                        try:
                            ai_val = float(ai_val) if ai_val not in [None, '', 'None'] else None
                            human_val = float(human_val) if human_val not in [None, '', 'None'] else None

                            if ai_val is not None and human_val is not None:
                                ai_values.append(ai_val)
                                human_values.append(human_val)
                        except (ValueError, TypeError):
                            continue
                    else:
                        # Categorical/Ordinal: normalize to lowercase
                        if ai_val and human_val:
                            ai_values.append(str(ai_val).lower().strip())
                            human_values.append(str(human_val).lower().strip())

        return ai_values, human_values

    def compute_field_reliability(self, field_name: str) -> Optional[FieldReliability]:
        """
        Compute reliability metrics for a specific field.

        Returns FieldReliability object or None if insufficient data.
        """
        field_def = get_field(field_name)

        # Align values
        ai_values, human_values = self.align_values(field_name)

        if len(ai_values) < 5:
            # Insufficient data for reliability calculation
            return None

        n_compared = len(ai_values)

        # Compute metrics based on field type
        if field_def.field_type == FieldType.CATEGORICAL:
            # Cohen's Kappa
            kappa = cohens_kappa(ai_values, human_values)
            target = self.targets.cohens_kappa
            acceptable = self.targets.cohens_kappa_acceptable

            if kappa >= target:
                status = "PASS"
            elif kappa >= acceptable:
                status = "ACCEPTABLE"
            else:
                status = "FAIL"

            return FieldReliability(
                field_name=field_name,
                field_type=field_def.field_type,
                n_compared=n_compared,
                metric_name="cohen_kappa",
                metric_value=kappa,
                target=target,
                acceptable=acceptable,
                status=status,
                interpretation=interpret_kappa(kappa),
                simple_agreement=agreement_rate(ai_values, human_values)
            )

        elif field_def.field_type == FieldType.ORDINAL:
            # Weighted Kappa (quadratic)
            wkappa = weighted_kappa(ai_values, human_values, weights='quadratic')
            target = self.targets.weighted_kappa
            acceptable = self.targets.weighted_kappa_acceptable

            if wkappa >= target:
                status = "PASS"
            elif wkappa >= acceptable:
                status = "ACCEPTABLE"
            else:
                status = "FAIL"

            return FieldReliability(
                field_name=field_name,
                field_type=field_def.field_type,
                n_compared=n_compared,
                metric_name="weighted_kappa",
                metric_value=wkappa,
                target=target,
                acceptable=acceptable,
                status=status,
                interpretation=interpret_kappa(wkappa),
                simple_agreement=agreement_rate(ai_values, human_values)
            )

        elif field_def.field_type == FieldType.FLOAT:
            # ICC(2,1) + MAE + RMSE
            ratings = np.column_stack([ai_values, human_values])
            icc_value, (ci_lower, ci_upper) = intraclass_correlation(ratings, model='ICC(2,1)')

            mae = mean_absolute_error(ai_values, human_values)
            rmse = root_mean_squared_error(ai_values, human_values)

            target = self.targets.icc
            acceptable = self.targets.icc_acceptable

            # Status based on ICC and MAE
            if icc_value >= target and (field_name != 'hedges_g' or mae <= self.targets.mae_hedges_g):
                status = "PASS"
            elif icc_value >= acceptable:
                status = "ACCEPTABLE"
            else:
                status = "FAIL"

            return FieldReliability(
                field_name=field_name,
                field_type=field_def.field_type,
                n_compared=n_compared,
                metric_name="icc_2_1",
                metric_value=icc_value,
                target=target,
                acceptable=acceptable,
                status=status,
                mae=mae,
                rmse=rmse,
                simple_agreement=None  # Not applicable for continuous
            )

        return None

    def compute_all(self) -> Phase4Report:
        """
        Compute reliability for all fields and generate complete report.
        """
        print("\n" + "="*70)
        print("COMPUTING INTER-CODER RELIABILITY")
        print("="*70 + "\n")

        per_field_results = {}
        failed_fields = []

        # Get all unique fields from human coding
        all_fields_coded = set()
        for study_fields in self.human_coding.values():
            for key in study_fields.keys():
                field_name = key.split(':')[2]
                all_fields_coded.add(field_name)

        print(f"Fields with human verification: {len(all_fields_coded)}")
        print(f"Fields: {', '.join(sorted(all_fields_coded))}\n")

        # Compute reliability for each field
        for field_name in sorted(all_fields_coded):
            print(f"Computing reliability for: {field_name}")

            result = self.compute_field_reliability(field_name)

            if result is None:
                print(f"  ⚠ Insufficient data (< 5 comparisons)")
                continue

            per_field_results[field_name] = result

            # Print result
            print(f"  {result.metric_name}: {result.metric_value:.3f} (target: {result.target}, status: {result.status})")
            if result.interpretation:
                print(f"  Interpretation: {result.interpretation}")
            if result.mae is not None:
                print(f"  MAE: {result.mae:.4f}, RMSE: {result.rmse:.4f}")
            if result.simple_agreement is not None:
                print(f"  Simple agreement: {result.simple_agreement:.3f}")

            # Track failures
            if result.status == "FAIL":
                failed_fields.append(field_name)

            print()

            # Log to audit
            self.audit.log(
                phase='phase4',
                action='compute_reliability',
                field_name=field_name,
                reason=f"{result.metric_name}={result.metric_value:.3f}, status={result.status}",
                actor='system',
                metadata={
                    'metric_value': result.metric_value,
                    'n_compared': result.n_compared,
                    'status': result.status
                }
            )

        # Calculate overall accuracy
        all_ai = []
        all_human = []

        for field_name in all_fields_coded:
            ai_vals, human_vals = self.align_values(field_name)
            all_ai.extend([str(v) for v in ai_vals])
            all_human.extend([str(v) for v in human_vals])

        overall_acc = overall_accuracy(all_ai, all_human) if all_ai else 0.0

        print(f"Overall accuracy (all fields): {overall_acc:.3f}")

        # Calculate Krippendorff's alpha for 3-model agreement (if Phase 2 data available)
        kripp_alpha = self._compute_3model_krippendorff()
        if kripp_alpha is not None:
            print(f"Krippendorff's α (3-model agreement): {kripp_alpha:.3f}")

        # Check if all gates passed
        all_gates_passed = len(failed_fields) == 0

        # Generate summary
        if all_gates_passed:
            summary = f"✓ All {len(per_field_results)} fields passed reliability targets."
        else:
            summary = f"⚠ {len(failed_fields)} field(s) failed: {', '.join(failed_fields)}"

        print(f"\n{summary}")

        # Create report
        report = Phase4Report(
            date=datetime.now().isoformat(),
            n_studies_verified=len(self.human_coding),
            n_fields_compared=len(per_field_results),
            per_field=per_field_results,
            overall_accuracy=overall_acc,
            krippendorff_alpha_3model=kripp_alpha,
            all_gates_passed=all_gates_passed,
            failed_fields=failed_fields,
            summary=summary
        )

        return report

    def _compute_3model_krippendorff(self) -> Optional[float]:
        """
        Compute Krippendorff's alpha for 3-model agreement on Phase 2 data.

        Uses the original Phase 2 extractions (Claude, GPT-4, Groq) to measure
        inter-model agreement.
        """
        # This would require access to individual model extractions from Phase 1
        # For now, return None as placeholder
        # TODO: Implement if Phase 1 raw extractions are accessible
        return None

    def check_gates(self, report: Phase4Report) -> Dict[str, bool]:
        """
        Check if reliability gates are passed.

        Returns dict of {gate_name: passed}
        """
        gates = {}

        for field_name, result in report.per_field.items():
            gate_name = f"{field_name}_{result.metric_name}"
            gates[gate_name] = result.status in ["PASS", "ACCEPTABLE"]

        gates['overall_accuracy'] = report.overall_accuracy >= 0.85
        gates['all_fields'] = report.all_gates_passed

        return gates

    def save_report(self, report: Phase4Report) -> Path:
        """Save reliability report as JSON."""
        report_path = self.output_dir / "reliability_report.json"

        # Convert report to dict
        report_dict = {
            'date': report.date,
            'n_studies_verified': report.n_studies_verified,
            'n_fields_compared': report.n_fields_compared,
            'per_field': {},
            'overall_accuracy': report.overall_accuracy,
            'krippendorff_alpha_3model': report.krippendorff_alpha_3model,
            'all_gates_passed': report.all_gates_passed,
            'failed_fields': report.failed_fields,
            'summary': report.summary
        }

        # Convert FieldReliability objects to dicts
        for field_name, result in report.per_field.items():
            report_dict['per_field'][field_name] = {
                'field_type': result.field_type.value,
                'n_compared': result.n_compared,
                'metric': result.metric_name,
                'value': result.metric_value,
                'target': result.target,
                'acceptable': result.acceptable,
                'status': result.status,
                'interpretation': result.interpretation,
                'mae': result.mae,
                'rmse': result.rmse,
                'simple_agreement': result.simple_agreement
            }

        with open(report_path, 'w') as f:
            json.dump(report_dict, f, indent=2)

        print(f"\n✓ Report saved: {report_path}")

        self.audit.log(
            phase='phase4',
            action='save_report',
            reason=f"Saved reliability report: {report.summary}",
            actor='system',
            metadata={
                'report_path': str(report_path),
                'all_gates_passed': report.all_gates_passed
            }
        )

        return report_path

    def save_summary(self, report: Phase4Report) -> Path:
        """Save human-readable summary text."""
        summary_path = self.output_dir / "reliability_summary.txt"

        with open(summary_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("PHASE 4: INTER-CODER RELIABILITY REPORT\n")
            f.write("="*70 + "\n\n")

            f.write(f"Date: {report.date}\n")
            f.write(f"Studies verified: {report.n_studies_verified}\n")
            f.write(f"Fields compared: {report.n_fields_compared}\n\n")

            f.write("="*70 + "\n")
            f.write("FIELD-LEVEL RELIABILITY\n")
            f.write("="*70 + "\n\n")

            for field_name, result in sorted(report.per_field.items()):
                f.write(f"Field: {field_name}\n")
                f.write(f"  Type: {result.field_type.value}\n")
                f.write(f"  N compared: {result.n_compared}\n")
                f.write(f"  Metric: {result.metric_name} = {result.metric_value:.3f}\n")
                f.write(f"  Target: {result.target} | Acceptable: {result.acceptable}\n")
                f.write(f"  Status: {result.status}\n")

                if result.interpretation:
                    f.write(f"  Interpretation: {result.interpretation}\n")

                if result.mae is not None:
                    f.write(f"  MAE: {result.mae:.4f} | RMSE: {result.rmse:.4f}\n")

                if result.simple_agreement is not None:
                    f.write(f"  Simple agreement: {result.simple_agreement:.3f}\n")

                f.write("\n")

            f.write("="*70 + "\n")
            f.write("OVERALL METRICS\n")
            f.write("="*70 + "\n\n")

            f.write(f"Overall accuracy: {report.overall_accuracy:.3f}\n")

            if report.krippendorff_alpha_3model is not None:
                f.write(f"Krippendorff's α (3-model): {report.krippendorff_alpha_3model:.3f}\n")

            f.write(f"\nAll gates passed: {report.all_gates_passed}\n")

            if report.failed_fields:
                f.write(f"\nFailed fields ({len(report.failed_fields)}):\n")
                for field in report.failed_fields:
                    f.write(f"  - {field}\n")

            f.write(f"\n{report.summary}\n")

        print(f"✓ Summary saved: {summary_path}")

        return summary_path


def main():
    parser = argparse.ArgumentParser(
        description="Phase 4: Inter-Coder Reliability Calculation"
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to pipeline_config.yaml'
    )

    args = parser.parse_args()

    # Load configuration
    with open(args.config) as f:
        config = yaml.safe_load(f)

    # Setup audit logger
    audit_log_path = config['audit']['log_file']
    audit = AuditLogger(audit_log_path, auto_flush=True)

    print("="*70)
    print("PHASE 4: INTER-CODER RELIABILITY CALCULATION")
    print("="*70)

    # Initialize Phase 4
    phase4 = Phase4Reliability(args.config, audit)

    # Load data
    phase3_dir = Path(config['phase3']['output_dir'])
    human_template = phase3_dir / "human_coding_template.csv"
    sample_json = phase3_dir / "human_verification_sample.json"

    print("\nLoading data...")
    phase4.load_human_coding(human_template)
    phase4.load_ai_consensus(sample_json)

    # Compute reliability
    report = phase4.compute_all()

    # Save outputs
    phase4.save_report(report)
    phase4.save_summary(report)

    # Check gates
    gates = phase4.check_gates(report)

    print("\n" + "="*70)
    print("QUALITY GATES")
    print("="*70)

    for gate_name, passed in sorted(gates.items()):
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {gate_name}")

    print("\n" + "="*70)

    if report.all_gates_passed:
        print("✓ Phase 4 complete! All reliability targets met.")
        print(f"\nNext step: Run Phase 5 (Discrepancy Resolution)")
    else:
        print("⚠ Phase 4 complete with warnings.")
        print(f"\nSome fields did not meet target reliability.")
        print(f"Review failed fields: {', '.join(report.failed_fields)}")
        print(f"\nOptions:")
        print(f"1. Proceed to Phase 5 with acceptable reliability (≥ 0.80)")
        print(f"2. Re-code failed fields and re-run Phase 4")


if __name__ == "__main__":
    main()
