#!/usr/bin/env python3
"""
Phase 6: QA Gates + Final CSV Generation
Apply quality assurance gates and generate final merged dataset.

QA Gates:
- Cohen's κ (categorical) ≥ 0.85
- Weighted κ (ordinal) ≥ 0.80
- ICC (numerical) ≥ 0.90
- Overall accuracy ≥ 85%
- Completeness ≥ 95%
- Effect size outliers (|g| > 3.0) < 3%
"""

import sys
import json
import argparse
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import statistics

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from recode_v11.schema import RECODE_FIELDS, FINAL_CSV_COLUMNS
from recode_v11.utils.data_loader import load_v81_csv
from recode_v11.utils.audit import AuditLogger


class Phase6QA:
    """QA gates and final CSV generation."""

    def __init__(self, config: Dict[str, Any], audit_logger: AuditLogger):
        """
        Initialize QA processor.

        Args:
            config: Phase 6 configuration
            audit_logger: Audit logger instance
        """
        self.config = config
        self.audit = audit_logger
        self.gates = config.get("gates", {})

    def check_qa_gates(self, reliability_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check all QA gates against reliability report.

        Args:
            reliability_report: Phase 4 reliability report

        Returns:
            List of gate results with pass/fail status
        """
        gate_results = []

        # Gate 1: Cohen's κ for categorical fields
        cohens_kappa_min = self.gates.get("cohens_kappa_min", 0.85)
        categorical_kappas = []

        for field, metrics in reliability_report.get("by_field", {}).items():
            field_schema = RECODE_FIELDS.get(field, {})
            if field_schema.get("type") == "categorical":
                kappa = metrics.get("cohens_kappa")
                if kappa is not None:
                    categorical_kappas.append((field, kappa))

        if categorical_kappas:
            min_kappa = min(k for _, k in categorical_kappas)
            avg_kappa = statistics.mean(k for _, k in categorical_kappas)
            passed = min_kappa >= cohens_kappa_min

            gate_results.append({
                "gate": "cohens_kappa",
                "threshold": cohens_kappa_min,
                "min_value": min_kappa,
                "avg_value": avg_kappa,
                "passed": passed,
                "message": f"Categorical fields: min κ={min_kappa:.3f}, avg κ={avg_kappa:.3f}",
                "action": "OK" if passed else "Suggest codebook revision for low-agreement fields"
            })

        # Gate 2: Weighted κ for ordinal fields
        weighted_kappa_min = self.gates.get("weighted_kappa_min", 0.80)
        ordinal_kappas = []

        for field, metrics in reliability_report.get("by_field", {}).items():
            field_schema = RECODE_FIELDS.get(field, {})
            if field_schema.get("type") == "ordinal":
                kappa = metrics.get("weighted_kappa")
                if kappa is not None:
                    ordinal_kappas.append((field, kappa))

        if ordinal_kappas:
            min_kappa = min(k for _, k in ordinal_kappas)
            avg_kappa = statistics.mean(k for _, k in ordinal_kappas)
            passed = min_kappa >= weighted_kappa_min

            gate_results.append({
                "gate": "weighted_kappa",
                "threshold": weighted_kappa_min,
                "min_value": min_kappa,
                "avg_value": avg_kappa,
                "passed": passed,
                "message": f"Ordinal fields: min κ_w={min_kappa:.3f}, avg κ_w={avg_kappa:.3f}",
                "action": "OK" if passed else "Suggest level reduction for ordinal scales"
            })

        # Gate 3: ICC for numerical fields
        icc_min = self.gates.get("icc_min", 0.90)
        numerical_iccs = []

        for field, metrics in reliability_report.get("by_field", {}).items():
            field_schema = RECODE_FIELDS.get(field, {})
            if field_schema.get("type") == "numerical":
                icc = metrics.get("icc_absolute")
                if icc is not None:
                    numerical_iccs.append((field, icc))

        if numerical_iccs:
            min_icc = min(i for _, i in numerical_iccs)
            avg_icc = statistics.mean(i for _, i in numerical_iccs)
            passed = min_icc >= icc_min

            gate_results.append({
                "gate": "icc",
                "threshold": icc_min,
                "min_value": min_icc,
                "avg_value": avg_icc,
                "passed": passed,
                "message": f"Numerical fields: min ICC={min_icc:.3f}, avg ICC={avg_icc:.3f}",
                "action": "OK" if passed else "Expand human review for numerical extractions"
            })

        # Gate 4: Overall accuracy
        accuracy_min = self.gates.get("overall_accuracy_min", 0.85)
        overall_accuracy = reliability_report.get("overall_metrics", {}).get("accuracy")

        if overall_accuracy is not None:
            passed = overall_accuracy >= accuracy_min

            gate_results.append({
                "gate": "overall_accuracy",
                "threshold": accuracy_min,
                "value": overall_accuracy,
                "passed": passed,
                "message": f"Overall accuracy: {overall_accuracy:.1%}",
                "action": "OK" if passed else "Expand RAG context or improve prompts"
            })

        # Gate 5: Completeness
        completeness_min = self.gates.get("completeness_min", 0.95)
        completeness = reliability_report.get("overall_metrics", {}).get("completeness")

        if completeness is not None:
            passed = completeness >= completeness_min

            gate_results.append({
                "gate": "completeness",
                "threshold": completeness_min,
                "value": completeness,
                "passed": passed,
                "message": f"Data completeness: {completeness:.1%}",
                "action": "OK" if passed else "Manual input needed for missing values"
            })

        # Log results
        for gate in gate_results:
            self.audit.log(
                phase="phase6_qa",
                action="qa_gate",
                reason=gate["message"],
                actor="system",
                metadata={
                    "gate": gate["gate"],
                    "passed": gate["passed"],
                    "threshold": gate.get("threshold"),
                    "value": gate.get("value") or gate.get("min_value")
                }
            )

        return gate_results

    def check_effect_size_outliers(self, effect_sizes: pd.DataFrame) -> Dict[str, Any]:
        """
        Check for effect size outliers.

        Args:
            effect_sizes: DataFrame with Hedges_g column

        Returns:
            Outlier check result
        """
        outlier_threshold = self.gates.get("outlier_threshold", 3.0)
        outlier_max_pct = self.gates.get("outlier_max_pct", 0.03)

        if "Hedges_g" not in effect_sizes.columns:
            return {
                "gate": "effect_size_outliers",
                "passed": True,
                "message": "No effect sizes to check",
                "outliers": []
            }

        # Filter valid effect sizes
        valid_g = effect_sizes["Hedges_g"].dropna()
        if len(valid_g) == 0:
            return {
                "gate": "effect_size_outliers",
                "passed": True,
                "message": "No valid effect sizes",
                "outliers": []
            }

        # Find outliers
        outliers = valid_g[valid_g.abs() > outlier_threshold]
        outlier_pct = len(outliers) / len(valid_g)

        passed = outlier_pct <= outlier_max_pct

        result = {
            "gate": "effect_size_outliers",
            "threshold": outlier_threshold,
            "max_pct": outlier_max_pct,
            "outlier_count": len(outliers),
            "total_count": len(valid_g),
            "outlier_pct": outlier_pct,
            "passed": passed,
            "message": f"Effect size outliers (|g| > {outlier_threshold}): {len(outliers)}/{len(valid_g)} ({outlier_pct:.1%})",
            "action": "OK" if passed else "Winsorize or exclude extreme outliers",
            "outliers": outliers.index.tolist()
        }

        self.audit.log(
            phase="phase6_qa",
            action="qa_gate",
            reason=result["message"],
            actor="system",
            metadata={
                "gate": "effect_size_outliers",
                "passed": passed,
                "outlier_count": len(outliers),
                "outlier_pct": outlier_pct
            }
        )

        return result

    def merge_results(
        self,
        v81_rows: pd.DataFrame,
        consensus_results: Dict[str, Any],
        resolution_results: Dict[str, Any],
        effect_sizes: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge all coding results into final dataset.

        Args:
            v81_rows: Original v8.1 CSV data
            consensus_results: Phase 2 consensus results
            resolution_results: Phase 5 resolution results
            effect_sizes: Effect size calculations

        Returns:
            Merged DataFrame
        """
        print("Merging results...")

        # Start with v8.1 baseline
        merged = v81_rows.copy()

        # Add new columns
        merged["confidence_avg"] = None
        merged["coding_method"] = None
        merged["human_verified"] = False
        merged["Variance_g"] = None

        # Build lookup dictionaries from consensus
        consensus_by_study = {}
        consensus_by_es = {}

        for item in consensus_results.get("consensus_items", []):
            field = item["field_name"]
            value = item["consensus_value"]
            confidence = item.get("confidence_avg", 0.0)
            method = item.get("method", "ai_consensus")
            human_verified = method == "human_gold_standard"

            if item["level"] == "study":
                study_id = item["study_id"]
                if study_id not in consensus_by_study:
                    consensus_by_study[study_id] = {}
                consensus_by_study[study_id][field] = {
                    "value": value,
                    "confidence": confidence,
                    "method": method,
                    "human_verified": human_verified
                }
            elif item["level"] == "effect_size":
                es_id = item.get("es_id")
                study_id = item.get("study_id")
                key = f"{study_id}_{es_id}" if es_id else study_id
                if key not in consensus_by_es:
                    consensus_by_es[key] = {}
                consensus_by_es[key][field] = {
                    "value": value,
                    "confidence": confidence,
                    "method": method,
                    "human_verified": human_verified
                }

        # Build lookup from resolutions
        resolutions_by_study = {}
        resolutions_by_es = {}

        for item in resolution_results.get("resolutions", []):
            field = item["field_name"]
            value = item["resolved_value"]
            method = item.get("method", "ai_resolved")
            human_verified = method == "human_gold_standard"

            if item["level"] == "study":
                study_id = item["study_id"]
                if study_id not in resolutions_by_study:
                    resolutions_by_study[study_id] = {}
                resolutions_by_study[study_id][field] = {
                    "value": value,
                    "method": method,
                    "human_verified": human_verified
                }
            elif item["level"] == "effect_size":
                es_id = item.get("es_id")
                study_id = item.get("study_id")
                key = f"{study_id}_{es_id}" if es_id else study_id
                if key not in resolutions_by_es:
                    resolutions_by_es[key] = {}
                resolutions_by_es[key][field] = {
                    "value": value,
                    "method": method,
                    "human_verified": human_verified
                }

        # Merge effect sizes
        if not effect_sizes.empty and "Hedges_g" in effect_sizes.columns:
            # Match by index or ES_ID
            for idx, row in effect_sizes.iterrows():
                if idx in merged.index:
                    merged.loc[idx, "Hedges_g"] = row["Hedges_g"]
                    merged.loc[idx, "SE_g"] = row.get("SE_g")
                    if pd.notna(row.get("SE_g")):
                        merged.loc[idx, "Variance_g"] = row["SE_g"] ** 2

        # Apply consensus and resolution values row by row
        for idx, row in merged.iterrows():
            study_id = row.get("Study_ID")
            es_id = row.get("ES_ID")

            confidences = []
            methods = []
            human_flags = []

            # Study-level fields
            if study_id in consensus_by_study:
                for field, data in consensus_by_study[study_id].items():
                    if field in merged.columns:
                        merged.loc[idx, field] = data["value"]
                        confidences.append(data["confidence"])
                        methods.append(data["method"])
                        human_flags.append(data["human_verified"])

            if study_id in resolutions_by_study:
                for field, data in resolutions_by_study[study_id].items():
                    if field in merged.columns:
                        merged.loc[idx, field] = data["value"]
                        methods.append(data["method"])
                        human_flags.append(data["human_verified"])

            # Effect size-level fields
            es_key = f"{study_id}_{es_id}" if es_id else None
            if es_key and es_key in consensus_by_es:
                for field, data in consensus_by_es[es_key].items():
                    if field in merged.columns:
                        merged.loc[idx, field] = data["value"]
                        confidences.append(data["confidence"])
                        methods.append(data["method"])
                        human_flags.append(data["human_verified"])

            if es_key and es_key in resolutions_by_es:
                for field, data in resolutions_by_es[es_key].items():
                    if field in merged.columns:
                        merged.loc[idx, field] = data["value"]
                        methods.append(data["method"])
                        human_flags.append(data["human_verified"])

            # Set metadata
            if confidences:
                merged.loc[idx, "confidence_avg"] = statistics.mean(confidences)

            if methods:
                # Priority: human > ai_consensus > ai_resolved
                if any("human" in m for m in methods):
                    merged.loc[idx, "coding_method"] = "human_verified"
                elif any("consensus" in m for m in methods):
                    merged.loc[idx, "coding_method"] = "ai_consensus"
                else:
                    merged.loc[idx, "coding_method"] = "ai_resolved"

            if human_flags:
                merged.loc[idx, "human_verified"] = any(human_flags)

        return merged

    def generate_final_csv(self, merged_data: pd.DataFrame, output_path: Path):
        """
        Generate final CSV with standardized columns.

        Args:
            merged_data: Merged DataFrame
            output_path: Output CSV path
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Ensure all required columns exist
        for col in FINAL_CSV_COLUMNS:
            if col not in merged_data.columns:
                merged_data[col] = None

        # Reorder columns
        final_df = merged_data[FINAL_CSV_COLUMNS]

        # Save
        final_df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"\nFinal CSV saved to {output_path}")
        print(f"  Rows: {len(final_df)}")
        print(f"  Columns: {len(final_df.columns)}")

    def generate_quality_report(
        self,
        gate_results: List[Dict[str, Any]],
        outlier_result: Dict[str, Any],
        merged_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Generate quality assurance summary report.

        Args:
            gate_results: QA gate results
            outlier_result: Outlier check result
            merged_data: Final merged data

        Returns:
            Quality report dict
        """
        all_gates = gate_results + [outlier_result]
        passed_gates = [g for g in all_gates if g.get("passed", False)]

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_gates": len(all_gates),
                "passed_gates": len(passed_gates),
                "failed_gates": len(all_gates) - len(passed_gates),
                "overall_pass": len(passed_gates) == len(all_gates),
                "total_rows": len(merged_data),
                "total_studies": merged_data["Study_ID"].nunique() if "Study_ID" in merged_data.columns else 0
            },
            "gates": all_gates,
            "coding_methods": merged_data["coding_method"].value_counts().to_dict() if "coding_method" in merged_data.columns else {},
            "human_verified_count": int(merged_data["human_verified"].sum()) if "human_verified" in merged_data.columns else 0
        }

        return report


def load_consensus_results(consensus_path: Path) -> Dict[str, Any]:
    """Load Phase 2 consensus results."""
    if not consensus_path.exists():
        print(f"Warning: {consensus_path} not found")
        return {"consensus_items": []}

    with open(consensus_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_resolution_results(resolution_path: Path) -> Dict[str, Any]:
    """Load Phase 5 resolution results."""
    if not resolution_path.exists():
        print(f"Warning: {resolution_path} not found")
        return {"resolutions": []}

    with open(resolution_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_effect_sizes(es_path: Path) -> pd.DataFrame:
    """Load effect size calculations."""
    if not es_path.exists():
        print(f"Warning: {es_path} not found")
        return pd.DataFrame()

    # Could be CSV or JSON
    if es_path.suffix == ".csv":
        return pd.read_csv(es_path)
    elif es_path.suffix == ".json":
        with open(es_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict) and "effect_sizes" in data:
                return pd.DataFrame(data["effect_sizes"])
    return pd.DataFrame()


def load_reliability_report(report_path: Path) -> Dict[str, Any]:
    """Load Phase 4 reliability report."""
    if not report_path.exists():
        print(f"Warning: {report_path} not found")
        return {}

    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Phase 6: QA gates and final CSV generation")
    parser.add_argument(
        "--v81-csv",
        type=Path,
        default=Path("data/v8.1/GenAI_MetaAnalysis_v8.1.csv"),
        help="Path to original v8.1 CSV"
    )
    parser.add_argument(
        "--reliability",
        type=Path,
        default=Path("data/recode_v11/05_phase4_reliability/reliability_report.json"),
        help="Path to Phase 4 reliability report"
    )
    parser.add_argument(
        "--consensus",
        type=Path,
        default=Path("data/recode_v11/03_phase2_consensus/consensus_results.json"),
        help="Path to Phase 2 consensus results"
    )
    parser.add_argument(
        "--resolutions",
        type=Path,
        default=Path("data/recode_v11/06_phase5_resolutions/resolutions.json"),
        help="Path to Phase 5 resolutions"
    )
    parser.add_argument(
        "--effect-sizes",
        type=Path,
        default=Path("data/recode_v11/effect_sizes.csv"),
        help="Path to effect size calculations"
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("data/recode_v11/07_phase6_final/GenAI_MetaAnalysis_v11_FINAL.csv"),
        help="Output path for final CSV"
    )
    parser.add_argument(
        "--output-report",
        type=Path,
        default=Path("data/recode_v11/07_phase6_final/quality_report.json"),
        help="Output path for quality report"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/recode_v11_config.yaml"),
        help="Path to configuration file"
    )

    args = parser.parse_args()

    # Load config
    import yaml
    if args.config.exists():
        with open(args.config, "r") as f:
            full_config = yaml.safe_load(f)
            config = full_config.get("phase6", {})
    else:
        config = {
            "output_dir": "data/recode_v11/07_phase6_final",
            "final_csv": "GenAI_MetaAnalysis_v11_FINAL.csv",
            "gates": {
                "cohens_kappa_min": 0.85,
                "weighted_kappa_min": 0.80,
                "icc_min": 0.90,
                "overall_accuracy_min": 0.85,
                "completeness_min": 0.95,
                "outlier_threshold": 3.0,
                "outlier_max_pct": 0.03
            }
        }

    # Initialize audit logger
    audit_log_path = Path("audit/phase6_qa_log.jsonl")
    audit_logger = AuditLogger(
        log_file=str(audit_log_path),
        auto_flush=True
    )

    # Initialize QA processor
    qa = Phase6QA(config, audit_logger)

    # Load all inputs
    print("Loading data...")
    v81_df = load_v81_csv(args.v81_csv)
    print(f"Loaded {len(v81_df)} rows from v8.1 CSV")

    reliability_report = load_reliability_report(args.reliability)
    consensus_results = load_consensus_results(args.consensus)
    resolution_results = load_resolution_results(args.resolutions)
    effect_sizes = load_effect_sizes(args.effect_sizes)

    # Check QA gates
    print("\nChecking QA gates...")
    gate_results = qa.check_qa_gates(reliability_report)

    for gate in gate_results:
        status = "✓ PASS" if gate["passed"] else "✗ FAIL"
        print(f"  {status}: {gate['message']}")
        if not gate["passed"]:
            print(f"    Action: {gate['action']}")

    # Check outliers
    print("\nChecking effect size outliers...")
    outlier_result = qa.check_effect_size_outliers(effect_sizes)
    status = "✓ PASS" if outlier_result["passed"] else "✗ FAIL"
    print(f"  {status}: {outlier_result['message']}")
    if not outlier_result["passed"]:
        print(f"    Action: {outlier_result['action']}")

    # Merge results
    merged_data = qa.merge_results(
        v81_df,
        consensus_results,
        resolution_results,
        effect_sizes
    )

    # Generate final CSV
    qa.generate_final_csv(merged_data, args.output_csv)

    # Generate quality report
    print("\nGenerating quality report...")
    quality_report = qa.generate_quality_report(gate_results, outlier_result, merged_data)

    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_report, "w", encoding="utf-8") as f:
        json.dump(quality_report, f, indent=2)

    print(f"Quality report saved to {args.output_report}")

    # Summary
    print("\n" + "="*60)
    print("PHASE 6 COMPLETE")
    print("="*60)
    print(f"QA Gates: {quality_report['summary']['passed_gates']}/{quality_report['summary']['total_gates']} passed")
    print(f"Overall: {'✓ PASS' if quality_report['summary']['overall_pass'] else '✗ FAIL'}")
    print(f"Final dataset: {quality_report['summary']['total_rows']} rows")
    print(f"Human verified: {quality_report['summary']['human_verified_count']} items")
    print("="*60)


if __name__ == "__main__":
    main()
