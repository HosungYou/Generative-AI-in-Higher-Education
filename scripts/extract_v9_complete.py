#!/usr/bin/env python3
"""
GenAI-HE Meta-Analysis Data Extraction Pipeline v9.0 (Complete Edition)

Universal Codebook v2.2 + GenAI-HE Extension (47 columns)
Uses Groq LLM (llama-3.3-70b-versatile) for extraction
C6/C7 validation pipeline with full provenance tracking

Author: Claude Code
Date: 2026-01-27
"""

import os
import json
import logging
import math
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# GenAI-HE CODEBOOK SCHEMA (Universal Codebook v2.2 + GenAI-HE Extension)
# ============================================================================

GENAI_HE_SCHEMA = {
    # Layer 1: Identifiers + Metadata (12 fields)
    "layer1_identifiers": [
        "study_id", "es_id", "citation", "doi", "year", "authors",
        "title", "journal", "design_type", "timepoint", "sample_context", "country"
    ],

    # Layer 2: Core Statistical Values (12 fields)
    "layer2_statistics": [
        "outcome_name", "outcome_unit", "es_type", "analysis_type",
        "n_treatment", "n_control", "m_treatment", "sd_treatment",
        "m_control", "sd_control", "hedges_g", "se_g"
    ],

    # Layer 3: GenAI-HE Moderator Variables (15 fields)
    "layer3_moderators": [
        "genai_tool", "genai_tool_version", "genai_access_type",
        "blooms_level", "outcome_dimension", "learning_domain",
        "study_design", "intervention_duration", "intervention_type",
        "control_condition", "education_level", "discipline",
        "sample_size_total", "publication_type", "mod_country"
    ],

    # Layer 4: AI Extraction Provenance (4 fields)
    "layer4_provenance": [
        "ai_confidence_avg", "ai_method", "ai_conflicts", "ai_extraction_json"
    ],

    # Layer 5: Human Verification (8 fields)
    "layer5_verification": [
        "verified_status", "verified_by", "verified_date", "corrections_json",
        "disagreement_resolved", "final_values_json", "verification_notes", "sign_off"
    ]
}

# Moderator value constraints
MODERATOR_VALUES = {
    "genai_tool": ["ChatGPT", "Claude", "Gemini", "Llama", "Copilot", "Mistral", "Custom", "Other", "Multiple", "not_reported"],
    "genai_tool_version": ["gpt-3.5", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "claude-3-opus", "claude-3-sonnet", "gemini-pro", "llama-2", "llama-3", "other", "not_reported"],
    "genai_access_type": ["api", "web_interface", "custom_integration", "plugin", "embedded", "not_reported"],
    "blooms_level": ["remember", "understand", "apply", "analyze", "evaluate", "create", "mixed"],
    "outcome_dimension": ["cognitive", "affective", "behavioral", "metacognitive", "mixed"],
    "learning_domain": ["knowledge_acquisition", "skill_development", "problem_solving", "creativity", "writing", "critical_thinking", "self_regulation", "engagement", "other"],
    "study_design": ["RCT", "quasi-experimental", "pre-post", "crossover", "factorial", "other"],
    "intervention_duration": ["single_session", "<1_week", "1-4_weeks", "1-3_months", ">3_months", "not_reported"],
    "intervention_type": ["direct_instruction", "tutoring", "feedback", "writing_assistant", "problem_solving", "coding_assistant", "other"],
    "control_condition": ["no_treatment", "traditional", "human_tutor", "alternative_tech", "placebo", "waitlist", "not_reported"],
    "education_level": ["K-12", "undergraduate", "graduate", "professional", "adult_learner", "mixed"],
    "discipline": ["STEM", "humanities", "social_sciences", "medicine", "business", "education", "language", "CS", "engineering", "mixed", "other"],
    "publication_type": ["journal", "conference", "preprint", "thesis", "other"],
    "es_type": ["POST_BETWEEN", "ANCOVA", "CHANGE", "PRE_POST", "INDEPENDENT_TEST"]
}


# ============================================================================
# STAGE 1: Section-Aware PDF Parsing
# ============================================================================

def extract_sections_pymupdf(pdf_path: Path) -> Dict[str, str]:
    """Extract sections using PyMuPDF with enhanced section detection."""
    import fitz

    sections = {
        "title": "",
        "abstract": "",
        "introduction": "",
        "methods": "",
        "results": "",
        "discussion": "",
        "tables": "",
        "references": "",
        "full_text": ""
    }

    try:
        doc = fitz.open(str(pdf_path))
        full_text = ""

        # Extract text from all pages
        for page in doc:
            full_text += page.get_text() + "\n"

        sections["full_text"] = full_text
        text_lower = full_text.lower()

        # Enhanced section detection with multiple keywords
        section_patterns = [
            ("abstract", ["abstract", "요약", "summary"]),
            ("introduction", ["introduction", "서론", "background"]),
            ("methods", ["method", "methodology", "연구방법", "participants", "procedure", "data collection", "materials"]),
            ("results", ["result", "finding", "결과", "data analysis"]),
            ("discussion", ["discussion", "conclusion", "논의", "결론", "implications", "limitations"]),
            ("references", ["reference", "참고문헌", "bibliography"])
        ]

        # Find positions of section headers
        positions = []
        for section_name, keywords in section_patterns:
            for kw in keywords:
                # Look for section header patterns
                patterns = [
                    f"\n{kw}\n",
                    f"\n{kw.upper()}\n",
                    f"\n{kw.title()}\n",
                    f"\n{kw}:",
                    f"\n{kw.upper()}:",
                ]
                for pattern in patterns:
                    pos = text_lower.find(pattern.lower())
                    if pos != -1:
                        positions.append((pos, section_name))
                        break
                if positions and positions[-1][1] == section_name:
                    break

        positions.sort(key=lambda x: x[0])

        # Extract sections based on positions
        for i, (pos, section_name) in enumerate(positions):
            end_pos = positions[i+1][0] if i+1 < len(positions) else len(full_text)
            sections[section_name] = full_text[pos:end_pos]

        doc.close()

    except Exception as e:
        logger.error(f"PyMuPDF extraction failed for {pdf_path}: {e}")

    return sections


# ============================================================================
# STAGE 2: Groq LLM Extraction (C6 Agent Pattern)
# ============================================================================

def create_c6_extraction_prompt(sections: Dict[str, str], study_id: str) -> str:
    """
    Create comprehensive extraction prompt following C6-DataIntegrityGuard pattern.
    Extracts all 47 columns from Universal Codebook v2.2 + GenAI-HE Extension.
    """

    # Truncate sections to fit context
    methods_text = sections.get('methods', '')[:8000]
    results_text = sections.get('results', '')[:8000]
    abstract_text = sections.get('abstract', '')[:2000]
    full_text = sections.get('full_text', '')[:6000]

    prompt = f"""You are C6-DataIntegrityGuard, a specialized meta-analysis data extraction agent.
Extract ALL variables from this academic paper following the Universal Codebook v2.2 + GenAI-HE Extension schema.

## STUDY INFORMATION
Study ID: {study_id}

## PAPER CONTENT

### Abstract
{abstract_text}

### Methods Section
{methods_text}

### Results Section
{results_text}

### Additional Text (for reference)
{full_text}

## EXTRACTION TASK

Extract the following variables organized by layer. For each value, provide confidence (0-100).

### LAYER 1: Identifiers & Metadata
- authors: First author's last name + et al.
- year: Publication year
- title: Full paper title
- journal: Journal name
- country: Country where study was conducted (ISO code preferred)
- design_type: RCT, QUASI, PRE_POST

### LAYER 2: Statistical Values
For EACH outcome measure, extract:
- outcome_name: Name of the outcome (e.g., "Writing quality", "Test score")
- es_type: POST_BETWEEN, ANCOVA, CHANGE, PRE_POST, INDEPENDENT_TEST
- n_treatment: Sample size in treatment/AI group
- n_control: Sample size in control group
- m_treatment: Mean in treatment group (post-test)
- sd_treatment: Standard deviation in treatment group
- m_control: Mean in control group (post-test)
- sd_control: Standard deviation in control group

If SD not directly reported, look for:
- Standard Error (SE) → SD = SE × √n
- 95% CI → SE = (upper - lower) / 3.92, then SD = SE × √n

### LAYER 3: GenAI-HE Moderator Variables

**GenAI Tool:**
- genai_tool: {', '.join(MODERATOR_VALUES['genai_tool'])}
  CLASSIFICATION RULES:
  - "ChatGPT", "GPT-3.5", "GPT-4" → ChatGPT
  - "Claude" → Claude
  - "Bard", "Gemini" → Gemini
  - "Llama", "Llama-2", "Llama-3" → Llama
  - Generic "AI chatbot", "LLM" without specifics → not_reported
- genai_tool_version: {', '.join(MODERATOR_VALUES['genai_tool_version'])}
- genai_access_type: {', '.join(MODERATOR_VALUES['genai_access_type'])}

**Educational Outcome:**
- blooms_level: {', '.join(MODERATOR_VALUES['blooms_level'])}
  CLASSIFICATION:
  - Factual recall, definitions → remember
  - Comprehension, explanation → understand
  - Problem-solving, implementation → apply
  - Comparison, analysis → analyze
  - Critique, evaluation → evaluate
  - Creative writing, design → create
- outcome_dimension: {', '.join(MODERATOR_VALUES['outcome_dimension'])}
- learning_domain: {', '.join(MODERATOR_VALUES['learning_domain'])}

**Study Design:**
- study_design: {', '.join(MODERATOR_VALUES['study_design'])}
  - "randomly assigned", "randomized" → RCT
  - "intact groups", "existing classes" → quasi-experimental
  - "one group", "no control" → pre-post
- intervention_duration: {', '.join(MODERATOR_VALUES['intervention_duration'])}
- intervention_type: {', '.join(MODERATOR_VALUES['intervention_type'])}
- control_condition: {', '.join(MODERATOR_VALUES['control_condition'])}

**Context:**
- education_level: {', '.join(MODERATOR_VALUES['education_level'])}
- discipline: {', '.join(MODERATOR_VALUES['discipline'])}
- sample_size_total: Total N (treatment + control)
- publication_type: {', '.join(MODERATOR_VALUES['publication_type'])}

## OUTPUT FORMAT

Respond ONLY with valid JSON (no markdown code blocks):

{{
  "layer1": {{
    "authors": {{"value": "string", "confidence": 0-100}},
    "year": {{"value": number, "confidence": 0-100}},
    "title": {{"value": "string", "confidence": 0-100}},
    "journal": {{"value": "string", "confidence": 0-100}},
    "country": {{"value": "ISO code", "confidence": 0-100}},
    "design_type": {{"value": "RCT|QUASI|PRE_POST", "confidence": 0-100}}
  }},
  "layer2_statistics": [
    {{
      "outcome_name": {{"value": "string", "confidence": 0-100}},
      "es_type": {{"value": "POST_BETWEEN|ANCOVA|CHANGE", "confidence": 0-100}},
      "n_treatment": {{"value": number, "confidence": 0-100, "source": "Table X / p.Y"}},
      "n_control": {{"value": number, "confidence": 0-100, "source": "Table X / p.Y"}},
      "m_treatment": {{"value": number, "confidence": 0-100, "source": "Table X / p.Y"}},
      "sd_treatment": {{"value": number, "confidence": 0-100, "source": "Table X / p.Y", "derived_from": null or "SE" or "CI"}},
      "m_control": {{"value": number, "confidence": 0-100, "source": "Table X / p.Y"}},
      "sd_control": {{"value": number, "confidence": 0-100, "source": "Table X / p.Y", "derived_from": null or "SE" or "CI"}}
    }}
  ],
  "layer3_moderators": {{
    "genai_tool": {{"value": "string", "confidence": 0-100, "source": "Methods section"}},
    "genai_tool_version": {{"value": "string or null", "confidence": 0-100}},
    "genai_access_type": {{"value": "string", "confidence": 0-100}},
    "blooms_level": {{"value": "string", "confidence": 0-100, "rationale": "brief explanation"}},
    "outcome_dimension": {{"value": "string", "confidence": 0-100}},
    "learning_domain": {{"value": "string", "confidence": 0-100}},
    "study_design": {{"value": "string", "confidence": 0-100, "source": "evidence"}},
    "intervention_duration": {{"value": "string", "confidence": 0-100}},
    "intervention_type": {{"value": "string", "confidence": 0-100}},
    "control_condition": {{"value": "string", "confidence": 0-100}},
    "education_level": {{"value": "string", "confidence": 0-100}},
    "discipline": {{"value": "string", "confidence": 0-100}},
    "sample_size_total": {{"value": number, "confidence": 0-100}},
    "publication_type": {{"value": "string", "confidence": 0-100}}
  }},
  "extraction_notes": ["List any issues, uncertainties, or missing data"]
}}

IMPORTANT:
- Only extract values you can find with evidence
- Use null for values not found
- Provide source locations for statistical values
- Be specific about GenAI tool (not just "AI tool")
"""
    return prompt


def extract_with_groq(sections: Dict[str, str], study_id: str) -> Dict[str, Any]:
    """Extract data using Groq LLM."""
    from openai import OpenAI

    api_key = os.environ.get("GROQ_API_KEY")
    model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        raise ValueError("GROQ_API_KEY not set")

    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    prompt = create_c6_extraction_prompt(sections, study_id)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are C6-DataIntegrityGuard. Extract meta-analysis data precisely. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4096
        )

        content = response.choices[0].message.content.strip()

        # Clean up response
        if content.startswith("```"):
            content = re.sub(r'^```(?:json)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)

        result = json.loads(content)
        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        return {"layer1": {}, "layer2_statistics": [], "layer3_moderators": {}, "extraction_notes": [f"JSON parse error: {str(e)}"]}
    except Exception as e:
        logger.error(f"Groq extraction failed: {e}")
        return {"layer1": {}, "layer2_statistics": [], "layer3_moderators": {}, "extraction_notes": [str(e)]}


# ============================================================================
# STAGE 3: C6/C7 Validation Pipeline
# ============================================================================

def calculate_hedges_g(n1: int, n2: int, m1: float, sd1: float, m2: float, sd2: float) -> tuple:
    """Calculate Hedges' g and SE_g from means and SDs."""
    try:
        # Pooled SD
        pooled_sd = math.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))

        if pooled_sd == 0:
            return None, None

        # Cohen's d
        d = (m1 - m2) / pooled_sd

        # Hedges' g correction factor
        df = n1 + n2 - 2
        J = 1 - (3 / (4 * df - 1))
        g = d * J

        # SE of Hedges' g
        se_g = math.sqrt((n1 + n2) / (n1 * n2) + (g ** 2) / (2 * (n1 + n2)))

        return round(g, 4), round(se_g, 4)
    except Exception:
        return None, None


def validate_c7(extraction: Dict, study_id: str) -> List[str]:
    """C7-ErrorPreventionEngine validation checks."""
    warnings = []

    # Check required moderators
    required_mods = ["genai_tool", "study_design", "education_level", "blooms_level"]
    layer3 = extraction.get("layer3_moderators", {})

    for mod in required_mods:
        if mod not in layer3 or not layer3[mod].get("value"):
            warnings.append(f"MISSING_MODERATOR: {mod} not extracted")
        elif layer3[mod].get("confidence", 0) < 70:
            warnings.append(f"LOW_CONFIDENCE: {mod} has confidence {layer3[mod].get('confidence')}%")

    # Check statistics
    stats = extraction.get("layer2_statistics", [])
    if not stats:
        warnings.append("NO_STATISTICS: No outcome measures extracted")

    for stat in stats:
        outcome = stat.get("outcome_name", {}).get("value", "Unknown")

        # Check for required statistical values
        for field in ["n_treatment", "n_control"]:
            if not stat.get(field, {}).get("value"):
                warnings.append(f"MISSING_N: {outcome} - {field} not found")

        # Check for complete data for Hedges' g calculation
        complete = all([
            stat.get("m_treatment", {}).get("value"),
            stat.get("sd_treatment", {}).get("value"),
            stat.get("m_control", {}).get("value"),
            stat.get("sd_control", {}).get("value"),
            stat.get("n_treatment", {}).get("value"),
            stat.get("n_control", {}).get("value")
        ])
        if not complete:
            warnings.append(f"INCOMPLETE_STATS: {outcome} - cannot calculate Hedges' g")

    # Check GenAI tool classification
    genai_tool = layer3.get("genai_tool", {}).get("value", "")
    if genai_tool == "not_reported":
        warnings.append("GENAI_TOOL_NOT_REPORTED: GenAI tool not identified")

    return warnings


def process_extraction_c6(extraction: Dict) -> Dict:
    """C6-DataIntegrityGuard: Calculate derived values and add provenance."""
    stats = extraction.get("layer2_statistics", [])

    for stat in stats:
        # Extract values
        n1 = stat.get("n_treatment", {}).get("value")
        n2 = stat.get("n_control", {}).get("value")
        m1 = stat.get("m_treatment", {}).get("value")
        sd1 = stat.get("sd_treatment", {}).get("value")
        m2 = stat.get("m_control", {}).get("value")
        sd2 = stat.get("sd_control", {}).get("value")

        # Calculate Hedges' g if all values present
        if all([n1, n2, m1, sd1, m2, sd2]):
            g, se_g = calculate_hedges_g(n1, n2, m1, sd1, m2, sd2)
            stat["hedges_g"] = {"value": g, "confidence": 95, "method": "CALCULATED_FROM_MEANS"}
            stat["se_g"] = {"value": se_g, "confidence": 95, "method": "CALCULATED_FROM_MEANS"}

            # Check for anomalous values
            if g and abs(g) > 3.0:
                extraction.setdefault("extraction_notes", []).append(f"ANOMALY: Hedges' g = {g} is extreme")

    return extraction


# ============================================================================
# Main Pipeline
# ============================================================================

def process_pdf(pdf_path: Path, output_dir: Path) -> Dict:
    """Full extraction pipeline for a single PDF."""
    study_id = pdf_path.stem
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing: {study_id}")

    # Stage 1: Section extraction
    logger.info("  Stage 1: Extracting sections from PDF...")
    sections = extract_sections_pymupdf(pdf_path)

    # Stage 2: LLM extraction
    logger.info("  Stage 2: C6 LLM extraction...")
    extraction = extract_with_groq(sections, study_id)

    # Stage 3a: C6 processing (calculate derived values)
    logger.info("  Stage 3a: C6 calculating Hedges' g...")
    extraction = process_extraction_c6(extraction)

    # Stage 3b: C7 validation
    logger.info("  Stage 3b: C7 validation...")
    warnings = validate_c7(extraction, study_id)
    extraction["validation_warnings"] = warnings
    extraction["validation_status"] = "VALIDATED" if not warnings else "NEEDS_REVIEW"

    # Add metadata
    extraction["study_id"] = study_id
    extraction["pdf_path"] = str(pdf_path)
    extraction["extraction_timestamp"] = datetime.now().isoformat()
    extraction["pipeline_version"] = "9.0-groq"

    # Save individual result
    output_file = output_dir / f"{study_id}_extraction.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extraction, f, indent=2, ensure_ascii=False)

    logger.info(f"  Status: {extraction['validation_status']} ({len(warnings)} warnings)")

    return extraction


def flatten_to_excel_rows(extractions: List[Dict]) -> List[Dict]:
    """Flatten extractions to Excel rows (one row per effect size)."""
    rows = []

    for ext in extractions:
        if ext.get("validation_status") == "FAILED":
            continue

        study_id = ext.get("study_id", "")
        layer1 = ext.get("layer1", {})
        layer3 = ext.get("layer3_moderators", {})
        stats = ext.get("layer2_statistics", [])

        # Helper to extract value
        def get_val(d, key, default=""):
            if isinstance(d, dict) and key in d:
                v = d[key]
                return v.get("value", default) if isinstance(v, dict) else v
            return default

        # If no statistics, create one row with moderators only
        if not stats:
            stats = [{}]

        for i, stat in enumerate(stats):
            row = {
                # Layer 1: Identifiers
                "Study_ID": study_id,
                "ES_ID": f"{study_id}_{i+1:02d}",
                "Authors": get_val(layer1, "authors"),
                "Year": get_val(layer1, "year"),
                "Title": get_val(layer1, "title"),
                "Journal": get_val(layer1, "journal"),
                "Country_Study": get_val(layer1, "country"),
                "Design_Type": get_val(layer1, "design_type"),

                # Layer 2: Statistics
                "Outcome_Name": get_val(stat, "outcome_name"),
                "ES_Type": get_val(stat, "es_type"),
                "n_Treatment": get_val(stat, "n_treatment"),
                "n_Control": get_val(stat, "n_control"),
                "M_Treatment": get_val(stat, "m_treatment"),
                "SD_Treatment": get_val(stat, "sd_treatment"),
                "M_Control": get_val(stat, "m_control"),
                "SD_Control": get_val(stat, "sd_control"),
                "Hedges_g": get_val(stat, "hedges_g"),
                "SE_g": get_val(stat, "se_g"),

                # Layer 3: GenAI-HE Moderators
                "GenAI_Tool": get_val(layer3, "genai_tool"),
                "GenAI_Tool_Version": get_val(layer3, "genai_tool_version"),
                "GenAI_Access_Type": get_val(layer3, "genai_access_type"),
                "Blooms_Level": get_val(layer3, "blooms_level"),
                "Outcome_Dimension": get_val(layer3, "outcome_dimension"),
                "Learning_Domain": get_val(layer3, "learning_domain"),
                "Study_Design": get_val(layer3, "study_design"),
                "Intervention_Duration": get_val(layer3, "intervention_duration"),
                "Intervention_Type": get_val(layer3, "intervention_type"),
                "Control_Condition": get_val(layer3, "control_condition"),
                "Education_Level": get_val(layer3, "education_level"),
                "Discipline": get_val(layer3, "discipline"),
                "Sample_Size_Total": get_val(layer3, "sample_size_total"),
                "Publication_Type": get_val(layer3, "publication_type"),

                # Layer 4: Provenance
                "AI_Confidence_Avg": calculate_avg_confidence(ext),
                "AI_Method": "GROQ_LLM",
                "Extraction_Timestamp": ext.get("extraction_timestamp", ""),

                # Layer 5: Verification
                "Validation_Status": ext.get("validation_status", "PENDING"),
                "Validation_Warnings": "; ".join(ext.get("validation_warnings", [])),
                "Verified_Status": "PENDING",
                "Sign_Off": False
            }
            rows.append(row)

    return rows


def calculate_avg_confidence(ext: Dict) -> float:
    """Calculate average confidence across all extracted values."""
    confidences = []

    # Layer 1
    for v in ext.get("layer1", {}).values():
        if isinstance(v, dict) and "confidence" in v:
            confidences.append(v["confidence"])

    # Layer 2
    for stat in ext.get("layer2_statistics", []):
        for v in stat.values():
            if isinstance(v, dict) and "confidence" in v:
                confidences.append(v["confidence"])

    # Layer 3
    for v in ext.get("layer3_moderators", {}).values():
        if isinstance(v, dict) and "confidence" in v:
            confidences.append(v["confidence"])

    return round(sum(confidences) / len(confidences), 1) if confidences else 0


def create_excel_output(rows: List[Dict], output_path: Path):
    """Create Excel file with full codebook schema."""
    import pandas as pd

    df = pd.DataFrame(rows)

    # Reorder columns to match codebook
    column_order = [
        # Layer 1
        "Study_ID", "ES_ID", "Authors", "Year", "Title", "Journal", "Country_Study", "Design_Type",
        # Layer 2
        "Outcome_Name", "ES_Type", "n_Treatment", "n_Control",
        "M_Treatment", "SD_Treatment", "M_Control", "SD_Control", "Hedges_g", "SE_g",
        # Layer 3
        "GenAI_Tool", "GenAI_Tool_Version", "GenAI_Access_Type",
        "Blooms_Level", "Outcome_Dimension", "Learning_Domain",
        "Study_Design", "Intervention_Duration", "Intervention_Type", "Control_Condition",
        "Education_Level", "Discipline", "Sample_Size_Total", "Publication_Type",
        # Layer 4
        "AI_Confidence_Avg", "AI_Method", "Extraction_Timestamp",
        # Layer 5
        "Validation_Status", "Validation_Warnings", "Verified_Status", "Sign_Off"
    ]

    # Ensure all columns exist
    for col in column_order:
        if col not in df.columns:
            df[col] = ""

    df = df[column_order]

    # Save to Excel with formatting
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)

        # Create codebook sheet
        codebook_data = [
            {"Layer": "Layer 1", "Field": "Study_ID", "Type": "str", "Description": "Unique study identifier"},
            {"Layer": "Layer 1", "Field": "ES_ID", "Type": "str", "Description": "Effect size ID"},
            {"Layer": "Layer 1", "Field": "Authors", "Type": "str", "Description": "First author + et al."},
            {"Layer": "Layer 1", "Field": "Year", "Type": "int", "Description": "Publication year"},
            {"Layer": "Layer 2", "Field": "Outcome_Name", "Type": "str", "Description": "Name of outcome measure"},
            {"Layer": "Layer 2", "Field": "Hedges_g", "Type": "float", "Description": "Hedges' g effect size"},
            {"Layer": "Layer 3", "Field": "GenAI_Tool", "Type": "cat", "Description": "ChatGPT, Claude, Gemini, etc."},
            {"Layer": "Layer 3", "Field": "Blooms_Level", "Type": "ord", "Description": "remember-create"},
            {"Layer": "Layer 3", "Field": "Study_Design", "Type": "cat", "Description": "RCT, quasi-experimental, etc."},
        ]
        pd.DataFrame(codebook_data).to_excel(writer, sheet_name='Codebook', index=False)

    logger.info(f"Excel file saved: {output_path}")
    return df


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="GenAI-HE Extraction Pipeline v9.0")
    parser.add_argument("--pdf-dir", type=Path, default=Path("pdfs"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/extractions_v9"))
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--single", type=Path, default=None)
    parser.add_argument("--excel", type=Path, default=None)

    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if not os.environ.get("GROQ_API_KEY"):
        logger.error("GROQ_API_KEY not set")
        return

    extractions = []

    if args.single:
        ext = process_pdf(args.single, args.output_dir)
        extractions.append(ext)
    else:
        pdf_files = sorted(args.pdf_dir.glob("*.pdf"))
        if args.limit:
            pdf_files = pdf_files[:args.limit]

        logger.info(f"Processing {len(pdf_files)} PDFs...")

        for pdf_path in pdf_files:
            try:
                ext = process_pdf(pdf_path, args.output_dir)
                extractions.append(ext)
            except Exception as e:
                logger.error(f"Failed: {pdf_path.name} - {e}")
                extractions.append({
                    "study_id": pdf_path.stem,
                    "validation_status": "FAILED",
                    "extraction_notes": [str(e)]
                })

    # Create Excel output
    rows = flatten_to_excel_rows(extractions)
    excel_path = args.excel or args.output_dir / "GenAI_MetaAnalysis_v9.xlsx"
    create_excel_output(rows, excel_path)

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("EXTRACTION SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total PDFs: {len(extractions)}")
    logger.info(f"Successful: {sum(1 for e in extractions if e.get('validation_status') != 'FAILED')}")
    logger.info(f"Needs Review: {sum(1 for e in extractions if e.get('validation_status') == 'NEEDS_REVIEW')}")
    logger.info(f"Failed: {sum(1 for e in extractions if e.get('validation_status') == 'FAILED')}")
    logger.info(f"Excel output: {excel_path}")


if __name__ == "__main__":
    main()
