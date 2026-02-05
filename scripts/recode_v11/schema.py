"""
Schema v11: 11-Field Re-coding Schema for GenAI-HE Meta-Analysis
Based on v5 codebook + v8.1 data schema

Fields are organized into three categories:
- SUBJECTIVE (judgment required): blooms_level, outcome_dimension
- OPERATIONAL (structural extraction): study_design, control_condition, genai_tool,
  genai_tool_version, intervention_duration, education_level, discipline
- NUMERICAL (missing value imputation): hedges_g, se_g
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class FieldCategory(str, Enum):
    """Category of field for consensus and validation."""
    SUBJECTIVE = "subjective"
    OPERATIONAL = "operational"
    NUMERICAL = "numerical"


class FieldType(str, Enum):
    """Data type of field."""
    CATEGORICAL = "categorical"
    ORDINAL = "ordinal"
    FLOAT = "float"


class ConsensusMethod(str, Enum):
    """Method for reaching consensus."""
    EXACT_MAJORITY = "exact_majority"          # 2/3 exact match
    MAJORITY_WITH_TOLERANCE = "majority_tolerance"  # 2/3 with 1-level tolerance
    UNANIMOUS = "unanimous"                     # 3/3 required
    RELATIVE_TOLERANCE = "relative_tolerance"   # 5% relative difference


@dataclass
class FieldDefinition:
    """Complete definition of a re-coding field."""
    name: str
    category: FieldCategory
    field_type: FieldType
    allowed_values: Optional[List[str]] = None
    consensus_method: ConsensusMethod = ConsensusMethod.EXACT_MAJORITY
    is_critical: bool = False
    is_study_level: bool = True  # True = per-study, False = per-ES_ID
    ordinal_order: Optional[List[str]] = None  # For ordinal fields
    validation_min: Optional[float] = None
    validation_max: Optional[float] = None
    tolerance: Optional[float] = None  # For numerical/ordinal
    description: str = ""

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate a value against this field definition."""
        if value is None:
            return True, None  # None is allowed (missing)

        if self.field_type == FieldType.CATEGORICAL:
            if self.allowed_values and str(value).lower() not in [v.lower() for v in self.allowed_values]:
                return False, f"Invalid value '{value}'. Allowed: {self.allowed_values}"

        elif self.field_type == FieldType.ORDINAL:
            if self.allowed_values and str(value).lower() not in [v.lower() for v in self.allowed_values]:
                return False, f"Invalid ordinal value '{value}'. Allowed: {self.allowed_values}"

        elif self.field_type == FieldType.FLOAT:
            try:
                fval = float(value)
                if self.validation_min is not None and fval < self.validation_min:
                    return False, f"Value {fval} below minimum {self.validation_min}"
                if self.validation_max is not None and fval > self.validation_max:
                    return False, f"Value {fval} above maximum {self.validation_max}"
            except (ValueError, TypeError):
                return False, f"Cannot convert '{value}' to float"

        return True, None


# ============================================================================
# FIELD DEFINITIONS (11 fields)
# ============================================================================

RECODE_FIELDS: Dict[str, FieldDefinition] = {
    # --- SUBJECTIVE FIELDS (judgment required) ---
    "blooms_level": FieldDefinition(
        name="blooms_level",
        category=FieldCategory.SUBJECTIVE,
        field_type=FieldType.ORDINAL,
        allowed_values=["remember", "understand", "apply", "analyze", "evaluate", "create", "mixed"],
        ordinal_order=["remember", "understand", "apply", "analyze", "evaluate", "create"],
        consensus_method=ConsensusMethod.MAJORITY_WITH_TOLERANCE,
        is_critical=True,
        is_study_level=False,  # Per outcome (ES_ID)
        tolerance=1,  # 1-level tolerance
        description="Bloom's Revised Taxonomy level (Anderson & Krathwohl, 2001)"
    ),
    "outcome_dimension": FieldDefinition(
        name="outcome_dimension",
        category=FieldCategory.SUBJECTIVE,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["cognitive", "affective", "behavioral", "metacognitive", "mixed"],
        consensus_method=ConsensusMethod.EXACT_MAJORITY,
        is_critical=True,
        is_study_level=False,  # Per outcome (ES_ID)
        description="Outcome measurement dimension"
    ),

    # --- OPERATIONAL FIELDS (structural extraction) ---
    "study_design": FieldDefinition(
        name="study_design",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["RCT", "quasi-experimental", "pre-post", "crossover", "other"],
        consensus_method=ConsensusMethod.UNANIMOUS,
        is_critical=True,
        is_study_level=True,
        description="Research design methodology"
    ),
    "control_condition": FieldDefinition(
        name="control_condition",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["no_treatment", "traditional", "human_tutor", "alternative_tech",
                        "active_control", "waitlist", "not_reported"],
        consensus_method=ConsensusMethod.EXACT_MAJORITY,
        is_study_level=True,
        description="Control/comparison condition"
    ),
    "genai_tool": FieldDefinition(
        name="genai_tool",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["ChatGPT", "Claude", "Gemini", "Copilot", "Custom",
                        "Other", "Multiple", "not_reported"],
        consensus_method=ConsensusMethod.EXACT_MAJORITY,
        is_study_level=True,
        description="Generative AI tool used in intervention"
    ),
    "genai_tool_version": FieldDefinition(
        name="genai_tool_version",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["gpt-3.5", "gpt-4", "gpt-4o", "claude-3", "gemini-pro",
                        "other", "not_reported"],
        consensus_method=ConsensusMethod.EXACT_MAJORITY,
        is_study_level=True,
        description="Specific version of GenAI tool"
    ),
    "intervention_duration": FieldDefinition(
        name="intervention_duration",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.ORDINAL,
        allowed_values=["single_session", "<1_week", "1-4_weeks", "1-3_months",
                        ">3_months", "not_reported"],
        ordinal_order=["single_session", "<1_week", "1-4_weeks", "1-3_months", ">3_months"],
        consensus_method=ConsensusMethod.MAJORITY_WITH_TOLERANCE,
        is_study_level=True,
        tolerance=1,
        description="Duration of GenAI intervention"
    ),
    "education_level": FieldDefinition(
        name="education_level",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["K-12", "undergraduate", "graduate", "professional", "mixed"],
        consensus_method=ConsensusMethod.EXACT_MAJORITY,
        is_study_level=True,
        description="Education level of participants"
    ),
    "discipline": FieldDefinition(
        name="discipline",
        category=FieldCategory.OPERATIONAL,
        field_type=FieldType.CATEGORICAL,
        allowed_values=["STEM", "humanities", "social_sciences", "medicine", "business",
                        "education", "language", "CS", "engineering", "mixed"],
        consensus_method=ConsensusMethod.EXACT_MAJORITY,
        is_study_level=True,
        description="Academic discipline"
    ),

    # --- NUMERICAL FIELDS (missing value imputation) ---
    "hedges_g": FieldDefinition(
        name="hedges_g",
        category=FieldCategory.NUMERICAL,
        field_type=FieldType.FLOAT,
        consensus_method=ConsensusMethod.RELATIVE_TOLERANCE,
        validation_min=-5.0,
        validation_max=5.0,
        tolerance=0.05,  # 5% relative
        is_study_level=False,
        description="Hedges' g effect size"
    ),
    "se_g": FieldDefinition(
        name="se_g",
        category=FieldCategory.NUMERICAL,
        field_type=FieldType.FLOAT,
        consensus_method=ConsensusMethod.RELATIVE_TOLERANCE,
        validation_min=0.0,
        validation_max=3.0,
        tolerance=0.05,  # 5% relative
        is_study_level=False,
        description="Standard error of Hedges' g"
    ),
}


# ============================================================================
# CONVENIENCE ACCESSORS
# ============================================================================

def get_field(name: str) -> FieldDefinition:
    """Get field definition by name."""
    if name not in RECODE_FIELDS:
        raise KeyError(f"Unknown field: {name}. Available: {list(RECODE_FIELDS.keys())}")
    return RECODE_FIELDS[name]


def get_fields_by_category(category: FieldCategory) -> Dict[str, FieldDefinition]:
    """Get all fields of a given category."""
    return {k: v for k, v in RECODE_FIELDS.items() if v.category == category}


def get_study_level_fields() -> Dict[str, FieldDefinition]:
    """Get fields that are extracted per-study (not per-ES_ID)."""
    return {k: v for k, v in RECODE_FIELDS.items() if v.is_study_level}


def get_outcome_level_fields() -> Dict[str, FieldDefinition]:
    """Get fields that are extracted per-outcome (ES_ID)."""
    return {k: v for k, v in RECODE_FIELDS.items() if not v.is_study_level}


def get_critical_fields() -> Dict[str, FieldDefinition]:
    """Get fields that require unanimous or special consensus."""
    return {k: v for k, v in RECODE_FIELDS.items() if v.is_critical}


def get_categorical_fields() -> List[str]:
    """Get names of categorical fields (for Cohen's kappa)."""
    return [k for k, v in RECODE_FIELDS.items() if v.field_type == FieldType.CATEGORICAL]


def get_ordinal_fields() -> List[str]:
    """Get names of ordinal fields (for weighted kappa)."""
    return [k for k, v in RECODE_FIELDS.items() if v.field_type == FieldType.ORDINAL]


def get_numerical_fields() -> List[str]:
    """Get names of numerical fields (for ICC)."""
    return [k for k, v in RECODE_FIELDS.items() if v.field_type == FieldType.FLOAT]


def validate_extraction(extraction: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate an extraction result against the schema.

    Returns dict of field_name -> list of validation errors.
    Empty dict means all valid.
    """
    errors = {}
    for field_name, field_def in RECODE_FIELDS.items():
        value = extraction.get(field_name)
        if value is not None:
            is_valid, error_msg = field_def.validate(value)
            if not is_valid:
                errors.setdefault(field_name, []).append(error_msg)
    return errors


def get_ordinal_distance(field_name: str, val1: str, val2: str) -> int:
    """
    Get ordinal distance between two values for an ordinal field.
    Returns -1 if either value is not in the ordinal order.
    """
    field_def = get_field(field_name)
    if not field_def.ordinal_order:
        return 0 if val1 == val2 else -1

    order = [v.lower() for v in field_def.ordinal_order]
    v1 = str(val1).lower()
    v2 = str(val2).lower()

    if v1 not in order or v2 not in order:
        return -1

    return abs(order.index(v1) - order.index(v2))


# CSV output column order for final dataset
FINAL_CSV_COLUMNS = [
    "Study_ID", "ES_ID", "Title", "Year", "Authors", "Outcome_Name",
    "outcome_dimension", "blooms_level", "study_design", "control_condition",
    "genai_tool", "genai_tool_version", "education_level", "discipline",
    "intervention_duration", "n_Treatment", "n_Control", "M_Treatment", "SD_Treatment",
    "M_Control", "SD_Control", "Hedges_g", "SE_g", "Variance_g",
    "confidence_avg", "coding_method", "human_verified"
]
