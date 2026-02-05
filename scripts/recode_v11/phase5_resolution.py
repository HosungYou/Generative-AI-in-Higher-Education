#!/usr/bin/env python3
"""
Phase 5: Discrepancy Resolution
Resolve coding discrepancies flagged during Phase 2 consensus or Phase 4 reliability check.

Resolution priority:
1. Human value (gold standard) when available
2. AI-AI discrepancy:
   - Categorical → Claude value as tiebreaker
   - Ordinal → median of 3 model values
   - Numerical → mean of concordant models; if >10% difference, flag for human review
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import Counter
import statistics

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from recode_v11.schema import (
    RECODE_FIELDS, FieldType, FieldCategory,
    get_ordinal_distance
)
from recode_v11.utils.audit import AuditLogger


class DiscrepancyResolver:
    """Resolve coding discrepancies using human gold standard or AI consensus."""

    def __init__(self, config: Dict[str, Any], audit_logger: AuditLogger):
        """
        Initialize resolver.

        Args:
            config: Phase 5 configuration
            audit_logger: Audit logger instance
        """
        self.config = config
        self.audit = audit_logger
        self.numerical_threshold = config.get("numerical_review_threshold", 0.10)
        self.priority = config.get("priority", [
            "human_gold_standard",
            "ai_consensus_majority",
            "claude_tiebreaker"
        ])

    def resolve_categorical(
        self,
        field_name: str,
        model_values: Dict[str, Dict[str, Any]],
        human_value: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resolve categorical field discrepancy.

        Args:
            field_name: Field name
            model_values: Dict of {model_name: {value, confidence}}
            human_value: Human-coded value if available

        Returns:
            Resolution result with resolved_value, method, rationale, needs_human_review
        """
        # Priority 1: Human value
        if human_value is not None:
            return {
                "resolved_value": human_value,
                "method": "human_gold_standard",
                "rationale": "Human coding takes priority as gold standard",
                "needs_human_review": False
            }

        # Priority 2: AI consensus (majority vote)
        values = [v["value"] for v in model_values.values() if v["value"] is not None]
        if not values:
            return {
                "resolved_value": None,
                "method": "no_data",
                "rationale": "No valid values from any model",
                "needs_human_review": True
            }

        value_counts = Counter(values)
        most_common = value_counts.most_common(1)[0]

        # If 2+ models agree
        if most_common[1] >= 2:
            return {
                "resolved_value": most_common[0],
                "method": "ai_consensus_majority",
                "rationale": f"{most_common[1]}/3 models agreed on '{most_common[0]}'",
                "needs_human_review": False
            }

        # Priority 3: Claude tiebreaker
        if "claude" in model_values and model_values["claude"]["value"] is not None:
            claude_value = model_values["claude"]["value"]
            return {
                "resolved_value": claude_value,
                "method": "claude_tiebreaker",
                "rationale": "All models disagreed, using Claude as tiebreaker",
                "needs_human_review": False
            }

        # Fallback: Use first non-null value
        return {
            "resolved_value": values[0],
            "method": "fallback_first_value",
            "rationale": "No consensus or Claude value, using first available",
            "needs_human_review": True
        }

    def resolve_ordinal(
        self,
        field_name: str,
        model_values: Dict[str, Dict[str, Any]],
        human_value: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resolve ordinal field discrepancy.

        Args:
            field_name: Field name
            model_values: Dict of {model_name: {value, confidence}}
            human_value: Human-coded value if available

        Returns:
            Resolution result
        """
        # Priority 1: Human value
        if human_value is not None:
            return {
                "resolved_value": human_value,
                "method": "human_gold_standard",
                "rationale": "Human coding takes priority as gold standard",
                "needs_human_review": False
            }

        # Get valid values
        values = [v["value"] for v in model_values.values() if v["value"] is not None]
        if not values:
            return {
                "resolved_value": None,
                "method": "no_data",
                "rationale": "No valid values from any model",
                "needs_human_review": True
            }

        # Get field schema
        field_schema = RECODE_FIELDS.get(field_name, {})
        valid_values = field_schema.get("valid_values", [])

        if not valid_values:
            # No ordinal scale defined, treat as categorical
            return self.resolve_categorical(field_name, model_values, human_value)

        # Map to ordinal positions
        value_to_pos = {v: i for i, v in enumerate(valid_values)}
        positions = [value_to_pos[v] for v in values if v in value_to_pos]

        if not positions:
            return {
                "resolved_value": values[0],
                "method": "fallback_invalid_ordinal",
                "rationale": "Values not in valid ordinal scale",
                "needs_human_review": True
            }

        # Median position
        median_pos = int(statistics.median(positions))
        median_value = valid_values[median_pos]

        # Check agreement
        if all(p == median_pos for p in positions):
            method = "ai_consensus_unanimous"
            rationale = "All models agreed on same ordinal level"
        elif len(set(positions)) == 1:
            method = "ai_consensus_majority"
            rationale = "Majority agreed on ordinal level"
        else:
            method = "ai_consensus_median"
            rationale = f"Median of ordinal positions: {positions}"

        return {
            "resolved_value": median_value,
            "method": method,
            "rationale": rationale,
            "needs_human_review": False
        }

    def resolve_numerical(
        self,
        field_name: str,
        model_values: Dict[str, Dict[str, Any]],
        human_value: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Resolve numerical field discrepancy.

        Args:
            field_name: Field name
            model_values: Dict of {model_name: {value, confidence}}
            human_value: Human-coded value if available

        Returns:
            Resolution result
        """
        # Priority 1: Human value
        if human_value is not None:
            return {
                "resolved_value": human_value,
                "method": "human_gold_standard",
                "rationale": "Human coding takes priority as gold standard",
                "needs_human_review": False
            }

        # Get valid numerical values
        values = []
        for v in model_values.values():
            if v["value"] is not None:
                try:
                    values.append(float(v["value"]))
                except (ValueError, TypeError):
                    pass

        if not values:
            return {
                "resolved_value": None,
                "method": "no_data",
                "rationale": "No valid numerical values from any model",
                "needs_human_review": True
            }

        if len(values) == 1:
            return {
                "resolved_value": values[0],
                "method": "single_value",
                "rationale": "Only one model provided valid numerical value",
                "needs_human_review": False
            }

        # Check concordance (coefficient of variation)
        mean_value = statistics.mean(values)

        if mean_value == 0:
            # All zeros
            return {
                "resolved_value": 0.0,
                "method": "ai_consensus_zeros",
                "rationale": "All models returned zero",
                "needs_human_review": False
            }

        stdev = statistics.stdev(values) if len(values) > 1 else 0
        cv = stdev / abs(mean_value) if mean_value != 0 else 0

        # If coefficient of variation > threshold, flag for review
        needs_review = cv > self.numerical_threshold

        if needs_review:
            method = "ai_mean_flagged"
            rationale = f"High variance (CV={cv:.2%}), flagged for human review. Values: {values}"
        else:
            method = "ai_consensus_mean"
            rationale = f"Mean of concordant models (CV={cv:.2%}). Values: {values}"

        return {
            "resolved_value": mean_value,
            "method": method,
            "rationale": rationale,
            "needs_human_review": needs_review
        }

    def resolve_single_item(
        self,
        item: Dict[str, Any],
        human_codings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Resolve a single discrepancy item.

        Args:
            item: Discrepancy item from phase5_queue
            human_codings: Dict of human-coded values (optional)

        Returns:
            Resolution result
        """
        field_name = item["field_name"]
        model_values = item["model_values"]

        # Get human value if available
        human_value = None
        if human_codings:
            study_id = item.get("study_id")
            es_id = item.get("es_id")

            if es_id:
                # Effect size level
                key = f"{study_id}_{es_id}"
                human_value = human_codings.get(key, {}).get(field_name)
            elif study_id:
                # Study level
                human_value = human_codings.get(study_id, {}).get(field_name)

        # Get field type
        field_schema = RECODE_FIELDS.get(field_name, {})
        field_type = field_schema.get("type", FieldType.CATEGORICAL)

        # Route to appropriate resolver
        if field_type == FieldType.NUMERICAL:
            resolution = self.resolve_numerical(field_name, model_values, human_value)
        elif field_type == FieldType.ORDINAL:
            resolution = self.resolve_ordinal(field_name, model_values, human_value)
        else:  # CATEGORICAL or unknown
            resolution = self.resolve_categorical(field_name, model_values, human_value)

        # Add metadata
        resolution["field_name"] = field_name
        resolution["study_id"] = item.get("study_id")
        resolution["es_id"] = item.get("es_id")
        resolution["level"] = item.get("level", "study")
        resolution["timestamp"] = datetime.now().isoformat()

        return resolution

    def resolve_all(
        self,
        phase5_queue: List[Dict[str, Any]],
        human_codings: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Resolve all discrepancies in the queue.

        Args:
            phase5_queue: List of discrepancy items
            human_codings: Dict of human-coded values (optional)

        Returns:
            List of resolution results
        """
        resolutions = []

        for item in phase5_queue:
            resolution = self.resolve_single_item(item, human_codings)
            resolutions.append(resolution)

            # Log to audit
            self.audit.log(
                phase="phase5_resolution",
                action="resolve",
                paper_id=resolution.get("study_id"),
                field_name=resolution["field_name"],
                new_value=resolution.get("resolved_value"),
                reason=resolution.get("rationale", ""),
                actor="system",
                metadata={
                    "method": resolution["method"],
                    "needs_human_review": resolution["needs_human_review"],
                    "es_id": resolution.get("es_id")
                }
            )

        return resolutions


def load_phase5_queue(queue_path: Path) -> List[Dict[str, Any]]:
    """Load phase5_queue.json from Phase 2."""
    if not queue_path.exists():
        print(f"Warning: {queue_path} not found, returning empty queue")
        return []

    with open(queue_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data if isinstance(data, list) else data.get("items", [])


def load_human_codings(human_path: Optional[Path]) -> Optional[Dict[str, Any]]:
    """Load human coding results from Phase 3 if available."""
    if not human_path or not human_path.exists():
        return None

    with open(human_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_resolutions(resolutions: List[Dict[str, Any]], output_path: Path):
    """Save resolution results to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Separate flagged items
    flagged = [r for r in resolutions if r.get("needs_human_review")]
    resolved = [r for r in resolutions if not r.get("needs_human_review")]

    output_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_items": len(resolutions),
            "resolved_count": len(resolved),
            "flagged_for_review": len(flagged)
        },
        "resolutions": resolutions,
        "flagged_items": flagged
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"Saved {len(resolutions)} resolutions to {output_path}")
    print(f"  - Resolved: {len(resolved)}")
    print(f"  - Flagged for human review: {len(flagged)}")


def main():
    parser = argparse.ArgumentParser(description="Phase 5: Resolve coding discrepancies")
    parser.add_argument(
        "--queue",
        type=Path,
        default=Path("data/recode_v11/03_phase2_consensus/phase5_queue.json"),
        help="Path to phase5_queue.json"
    )
    parser.add_argument(
        "--human",
        type=Path,
        help="Path to human coding results (optional)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/recode_v11/06_phase5_resolutions/resolutions.json"),
        help="Output path for resolutions"
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
            config = full_config.get("phase5", {})
    else:
        config = {
            "output_dir": "data/recode_v11/06_phase5_resolutions",
            "priority": [
                "human_gold_standard",
                "ai_consensus_majority",
                "claude_tiebreaker"
            ],
            "numerical_review_threshold": 0.10
        }

    # Initialize audit logger
    audit_log_path = Path("audit/resolutions_log.jsonl")
    audit_logger = AuditLogger(
        log_file=str(audit_log_path),
        auto_flush=True
    )

    # Load data
    print("Loading phase5_queue...")
    phase5_queue = load_phase5_queue(args.queue)
    print(f"Loaded {len(phase5_queue)} discrepancy items")

    human_codings = None
    if args.human:
        print(f"Loading human codings from {args.human}...")
        human_codings = load_human_codings(args.human)
        if human_codings:
            print(f"Loaded human codings for {len(human_codings)} items")

    # Resolve discrepancies
    print("\nResolving discrepancies...")
    resolver = DiscrepancyResolver(config, audit_logger)
    resolutions = resolver.resolve_all(phase5_queue, human_codings)

    # Save results
    save_resolutions(resolutions, args.output)

    # Summary statistics
    methods = Counter(r["method"] for r in resolutions)
    print("\nResolution methods used:")
    for method, count in methods.most_common():
        print(f"  {method}: {count}")


if __name__ == "__main__":
    main()
