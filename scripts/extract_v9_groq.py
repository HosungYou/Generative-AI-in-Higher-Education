#!/usr/bin/env python3
"""
GenAI-HE Meta-Analysis Data Extraction Pipeline v9.0 (Groq Edition)

Modern extraction pipeline using:
- Stage 1: PyMuPDF for section-aware PDF parsing
- Stage 2: Groq LLM (llama-3.3-70b) for structured extraction
- Stage 3: C6/C7 validation with provenance tracking

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
# STAGE 1: PyMuPDF Section-Aware Parsing
# ============================================================================

def extract_sections_pymupdf(pdf_path: Path) -> Dict[str, str]:
    """
    Extract sections using PyMuPDF with section detection.
    """
    import fitz  # PyMuPDF

    sections = {
        "title": "",
        "abstract": "",
        "introduction": "",
        "methods": "",
        "results": "",
        "discussion": "",
        "tables": "",
        "full_text": ""
    }

    try:
        doc = fitz.open(str(pdf_path))
        full_text = ""

        for page in doc:
            full_text += page.get_text()

        sections["full_text"] = full_text

        # Simple section detection by keywords
        text_lower = full_text.lower()

        # Find section boundaries
        section_markers = [
            ("abstract", ["abstract", "요약"]),
            ("methods", ["method", "methodology", "연구방법", "연구 방법", "participants", "procedure"]),
            ("results", ["result", "finding", "결과"]),
            ("discussion", ["discussion", "conclusion", "논의", "결론"])
        ]

        positions = []
        for section_name, keywords in section_markers:
            for kw in keywords:
                pos = text_lower.find(kw)
                if pos != -1:
                    positions.append((pos, section_name))
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
# STAGE 2: Groq LLM Extraction
# ============================================================================

@dataclass
class ModeratorExtraction:
    """Extracted moderator variable with provenance."""
    field: str
    value: Any
    confidence: int  # 0-100
    source: str  # e.g., "Methods section, p.5"
    method: str  # e.g., "LLM_EXTRACTION", "TABLE_OCR", "MANUAL"


@dataclass
class StatisticalExtraction:
    """Extracted statistical value with provenance."""
    outcome_name: str
    n_treatment: Optional[int] = None
    n_control: Optional[int] = None
    m_treatment: Optional[float] = None
    sd_treatment: Optional[float] = None
    m_control: Optional[float] = None
    sd_control: Optional[float] = None
    hedges_g: Optional[float] = None
    se_g: Optional[float] = None
    confidence: int = 0
    source: str = ""
    method: str = "LLM_EXTRACTION"


@dataclass
class ExtractionResult:
    """Complete extraction result for a study."""
    study_id: str
    pdf_path: str
    extraction_timestamp: str
    moderators: List[ModeratorExtraction] = field(default_factory=list)
    statistics: List[StatisticalExtraction] = field(default_factory=list)
    validation_status: str = "PENDING"
    validation_notes: List[str] = field(default_factory=list)


# GenAI-HE specific moderator schema (Universal Codebook v2.2)
GENAI_HE_MODERATOR_SCHEMA = {
    "genai_tool": {
        "type": "categorical",
        "values": ["ChatGPT", "ChatGPT-3.5", "ChatGPT-4", "Claude", "Bard/Gemini", "Copilot", "Other", "Multiple", "Not Reported"],
        "extraction_prompt": "What GenAI tool was used in this study? Look for specific mentions of ChatGPT, GPT-3.5, GPT-4, Claude, Gemini, Bard, Copilot, or other AI assistants in the Methods section. Be specific about the version if mentioned."
    },
    "education_level": {
        "type": "categorical",
        "values": ["K-12", "Undergraduate", "Graduate", "Professional", "Mixed"],
        "extraction_prompt": "What education level were the participants? Look for undergraduate, graduate, K-12, professional students, etc."
    },
    "study_design": {
        "type": "categorical",
        "values": ["RCT", "Quasi-experimental", "Pre-post", "Other"],
        "extraction_prompt": "What was the study design? Was it a randomized controlled trial (RCT), quasi-experimental, or pre-post design?"
    },
    "blooms_level": {
        "type": "ordinal",
        "values": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"],
        "extraction_prompt": "What cognitive level was assessed according to Bloom's taxonomy? Look for learning outcomes described."
    },
    "intervention_duration": {
        "type": "continuous",
        "unit": "weeks",
        "extraction_prompt": "How long was the intervention in weeks? Look for duration mentioned in the Methods section."
    },
    "discipline": {
        "type": "categorical",
        "values": ["STEM", "Humanities", "Social Sciences", "Health", "Business", "Education", "Language Learning", "Mixed"],
        "extraction_prompt": "What discipline or subject area was studied? Look for mentions of the course or subject."
    },
    "country": {
        "type": "categorical",
        "extraction_prompt": "In which country was the study conducted? Look for location information in the Methods section or author affiliations."
    },
    "sample_size_total": {
        "type": "continuous",
        "extraction_prompt": "What was the total sample size? Add treatment and control group sizes."
    }
}


def create_extraction_prompt(sections: Dict[str, str], moderator_schema: Dict) -> str:
    """
    Create a structured extraction prompt for Groq.
    """
    prompt = f"""You are a meta-analysis data extraction expert. Extract the following information from this academic paper.

## Paper Content

### Methods Section
{sections.get('methods', 'Not available')[:6000]}

### Results Section
{sections.get('results', 'Not available')[:6000]}

### Full Text (for reference)
{sections.get('full_text', 'Not available')[:4000]}

## Extraction Task

Extract the following moderator variables. For each, provide:
1. The extracted value
2. Confidence score (0-100)
3. Source location (e.g., "Methods section, paragraph 3")

### Moderator Variables to Extract:

"""
    for field, schema in moderator_schema.items():
        prompt += f"\n**{field}**:\n"
        prompt += f"- Prompt: {schema['extraction_prompt']}\n"
        if 'values' in schema:
            prompt += f"- Valid values: {', '.join(schema['values'])}\n"

    prompt += """

### Statistical Values to Extract:

For each outcome measure reported, extract:
- outcome_name: Name of the outcome measure
- n_treatment: Sample size in treatment group
- n_control: Sample size in control group
- m_treatment: Mean in treatment group
- sd_treatment: Standard deviation in treatment group
- m_control: Mean in control group
- sd_control: Standard deviation in control group

Look for these values in tables, results text, or statistical reports.

## Output Format

Respond ONLY with a JSON object (no markdown code blocks, no explanation) in this exact structure:
{
  "moderators": [
    {
      "field": "genai_tool",
      "value": "ChatGPT-4",
      "confidence": 95,
      "source": "Methods section: 'Participants used ChatGPT-4...'"
    }
  ],
  "statistics": [
    {
      "outcome_name": "Critical thinking score",
      "n_treatment": 45,
      "n_control": 42,
      "m_treatment": 78.5,
      "sd_treatment": 12.3,
      "m_control": 72.1,
      "sd_control": 11.8,
      "confidence": 90,
      "source": "Table 3, p.8"
    }
  ],
  "extraction_notes": ["Any issues or uncertainties noted during extraction"]
}

Be precise and only extract values you can find with high confidence. If a value is not found, use null or omit it.
"""
    return prompt


def extract_with_groq(
    sections: Dict[str, str],
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract data using Groq LLM (OpenAI-compatible API).
    """
    from openai import OpenAI

    api_key = api_key or os.environ.get("GROQ_API_KEY")
    model = model or os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        raise ValueError("GROQ_API_KEY not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    prompt = create_extraction_prompt(sections, GENAI_HE_MODERATOR_SCHEMA)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a meta-analysis data extraction expert. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4096
        )

        content = response.choices[0].message.content

        # Clean up response - remove markdown code blocks if present
        content = content.strip()
        if content.startswith("```"):
            # Remove markdown code block
            content = re.sub(r'^```(?:json)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)

        # Parse JSON
        result = json.loads(content)
        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        logger.error(f"Raw response: {content[:500]}")
        return {"moderators": [], "statistics": [], "extraction_notes": [f"JSON parse error: {str(e)}"]}
    except Exception as e:
        logger.error(f"Groq extraction failed: {e}")
        return {"moderators": [], "statistics": [], "extraction_notes": [str(e)]}


# ============================================================================
# STAGE 3: C6/C7 Validation Pipeline
# ============================================================================

def validate_extraction_c7(extraction: ExtractionResult) -> List[str]:
    """
    C7-ErrorPreventionEngine validation checks.
    """
    warnings = []

    # Check for critical missing moderators
    required_moderators = ["genai_tool", "study_design", "education_level"]
    found_moderators = {m.field for m in extraction.moderators}

    for req in required_moderators:
        if req not in found_moderators:
            warnings.append(f"MISSING_MODERATOR: {req} not extracted")

    # Check for low confidence extractions
    for mod in extraction.moderators:
        if mod.confidence < 70:
            warnings.append(f"LOW_CONFIDENCE: {mod.field} has confidence {mod.confidence}%")

    # Check statistical value completeness
    for stat in extraction.statistics:
        if stat.n_treatment is None or stat.n_control is None:
            warnings.append(f"INCOMPLETE_STATS: {stat.outcome_name} missing sample sizes")

        if stat.m_treatment is not None and stat.sd_treatment is None:
            warnings.append(f"MISSING_SD: {stat.outcome_name} has mean but no SD")

    # Check for anomalous values
    for stat in extraction.statistics:
        if stat.hedges_g is not None and abs(stat.hedges_g) > 3.0:
            warnings.append(f"ANOMALY: {stat.outcome_name} has extreme g={stat.hedges_g}")

    return warnings


def calculate_hedges_g(stat: StatisticalExtraction) -> Optional[float]:
    """
    Calculate Hedges' g from means and SDs.
    """
    if None in [stat.m_treatment, stat.sd_treatment, stat.m_control,
                stat.sd_control, stat.n_treatment, stat.n_control]:
        return None

    n1, n2 = stat.n_treatment, stat.n_control
    m1, m2 = stat.m_treatment, stat.m_control
    sd1, sd2 = stat.sd_treatment, stat.sd_control

    # Pooled SD
    try:
        pooled_sd = math.sqrt(
            ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2)
        )

        if pooled_sd == 0:
            return None

        # Cohen's d
        d = (m1 - m2) / pooled_sd

        # Hedges' g correction factor
        df = n1 + n2 - 2
        J = 1 - (3 / (4 * df - 1))

        g = d * J
        return round(g, 4)
    except Exception:
        return None


def calculate_se_g(stat: StatisticalExtraction, g: float) -> Optional[float]:
    """Calculate SE of Hedges' g."""
    if stat.n_treatment is None or stat.n_control is None:
        return None

    n1, n2 = stat.n_treatment, stat.n_control

    try:
        se = math.sqrt(
            (n1 + n2) / (n1 * n2) + (g ** 2) / (2 * (n1 + n2))
        )
        return round(se, 4)
    except Exception:
        return None


def process_extraction_c6(extraction: ExtractionResult) -> ExtractionResult:
    """
    C6-DataIntegrityGuard processing.
    """
    for stat in extraction.statistics:
        if stat.hedges_g is None:
            stat.hedges_g = calculate_hedges_g(stat)
            if stat.hedges_g is not None:
                stat.method = "CALCULATED_FROM_MEANS"

        if stat.hedges_g is not None and stat.se_g is None:
            stat.se_g = calculate_se_g(stat, stat.hedges_g)

    return extraction


# ============================================================================
# Main Pipeline
# ============================================================================

def process_pdf(
    pdf_path: Path,
    study_id: str,
    output_dir: Path,
    api_key: Optional[str] = None
) -> ExtractionResult:
    """
    Full extraction pipeline for a single PDF.
    """
    logger.info(f"Processing: {study_id}")

    # Stage 1: Section extraction
    logger.info("  Stage 1: Extracting sections...")
    sections = extract_sections_pymupdf(pdf_path)

    # Stage 2: LLM extraction
    logger.info("  Stage 2: Groq LLM extraction...")
    raw_extraction = extract_with_groq(sections, api_key)

    # Convert to dataclass
    result = ExtractionResult(
        study_id=study_id,
        pdf_path=str(pdf_path),
        extraction_timestamp=datetime.now().isoformat(),
        moderators=[
            ModeratorExtraction(
                field=m["field"],
                value=m["value"],
                confidence=m.get("confidence", 0),
                source=m.get("source", ""),
                method="LLM_EXTRACTION"
            )
            for m in raw_extraction.get("moderators", [])
        ],
        statistics=[
            StatisticalExtraction(
                outcome_name=s.get("outcome_name", "Unknown"),
                n_treatment=s.get("n_treatment"),
                n_control=s.get("n_control"),
                m_treatment=s.get("m_treatment"),
                sd_treatment=s.get("sd_treatment"),
                m_control=s.get("m_control"),
                sd_control=s.get("sd_control"),
                confidence=s.get("confidence", 0),
                source=s.get("source", ""),
                method="LLM_EXTRACTION"
            )
            for s in raw_extraction.get("statistics", [])
        ]
    )

    # Stage 3a: C6 processing
    logger.info("  Stage 3a: C6 processing (Hedges' g)...")
    result = process_extraction_c6(result)

    # Stage 3b: C7 validation
    logger.info("  Stage 3b: C7 validation...")
    warnings = validate_extraction_c7(result)
    result.validation_notes = warnings
    result.validation_status = "VALIDATED" if len(warnings) == 0 else "NEEDS_REVIEW"

    # Save individual result
    output_file = output_dir / f"{study_id}_extraction.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(asdict(result), f, indent=2, ensure_ascii=False)

    logger.info(f"  Completed: {result.validation_status} ({len(warnings)} warnings)")

    return result


def process_batch(
    pdf_dir: Path,
    output_dir: Path,
    api_key: Optional[str] = None,
    limit: Optional[int] = None
) -> List[ExtractionResult]:
    """
    Process all PDFs in a directory.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if limit:
        pdf_files = pdf_files[:limit]

    results = []

    logger.info(f"Processing {len(pdf_files)} PDFs...")

    for i, pdf_path in enumerate(pdf_files):
        study_id = pdf_path.stem
        logger.info(f"\n[{i+1}/{len(pdf_files)}] {study_id}")
        try:
            result = process_pdf(pdf_path, study_id, output_dir, api_key)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {study_id}: {e}")
            results.append(ExtractionResult(
                study_id=study_id,
                pdf_path=str(pdf_path),
                extraction_timestamp=datetime.now().isoformat(),
                validation_status="FAILED",
                validation_notes=[str(e)]
            ))

    # Save summary
    summary = {
        "extraction_date": datetime.now().isoformat(),
        "pipeline_version": "9.0-groq",
        "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "total_pdfs": len(pdf_files),
        "successful": sum(1 for r in results if r.validation_status != "FAILED"),
        "needs_review": sum(1 for r in results if r.validation_status == "NEEDS_REVIEW"),
        "failed": sum(1 for r in results if r.validation_status == "FAILED"),
    }

    summary_file = output_dir / "extraction_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"\n{'='*60}")
    logger.info(f"Extraction complete: {summary['successful']}/{summary['total_pdfs']} successful")
    logger.info(f"Needs review: {summary['needs_review']}")
    logger.info(f"Failed: {summary['failed']}")

    return results


def create_excel_output(results: List[ExtractionResult], output_path: Path):
    """
    Create Excel file from extraction results (Universal Codebook v2.2 format).
    """
    import pandas as pd

    # Flatten results into rows
    rows = []

    for result in results:
        if result.validation_status == "FAILED":
            continue

        # Get moderator values as dict
        mod_dict = {m.field: m.value for m in result.moderators}
        mod_conf = {f"{m.field}_confidence": m.confidence for m in result.moderators}
        mod_source = {f"{m.field}_source": m.source for m in result.moderators}

        # Create row for each statistical outcome
        if result.statistics:
            for stat in result.statistics:
                row = {
                    "Study_ID": result.study_id,
                    "Extraction_Date": result.extraction_timestamp,
                    "Validation_Status": result.validation_status,
                    # Moderators
                    "GenAI_Tool": mod_dict.get("genai_tool", ""),
                    "GenAI_Tool_Confidence": mod_conf.get("genai_tool_confidence", ""),
                    "Education_Level": mod_dict.get("education_level", ""),
                    "Study_Design": mod_dict.get("study_design", ""),
                    "Blooms_Level": mod_dict.get("blooms_level", ""),
                    "Discipline": mod_dict.get("discipline", ""),
                    "Country": mod_dict.get("country", ""),
                    "Intervention_Duration_Weeks": mod_dict.get("intervention_duration", ""),
                    "Sample_Size_Total": mod_dict.get("sample_size_total", ""),
                    # Statistics
                    "Outcome_Name": stat.outcome_name,
                    "n_Treatment": stat.n_treatment,
                    "n_Control": stat.n_control,
                    "M_Treatment": stat.m_treatment,
                    "SD_Treatment": stat.sd_treatment,
                    "M_Control": stat.m_control,
                    "SD_Control": stat.sd_control,
                    "Hedges_g": stat.hedges_g,
                    "SE_g": stat.se_g,
                    "Stat_Confidence": stat.confidence,
                    "Stat_Source": stat.source,
                    "Stat_Method": stat.method,
                    # Validation
                    "Validation_Notes": "; ".join(result.validation_notes)
                }
                rows.append(row)
        else:
            # Study with no statistics extracted
            row = {
                "Study_ID": result.study_id,
                "Extraction_Date": result.extraction_timestamp,
                "Validation_Status": result.validation_status,
                "GenAI_Tool": mod_dict.get("genai_tool", ""),
                "GenAI_Tool_Confidence": mod_conf.get("genai_tool_confidence", ""),
                "Education_Level": mod_dict.get("education_level", ""),
                "Study_Design": mod_dict.get("study_design", ""),
                "Blooms_Level": mod_dict.get("blooms_level", ""),
                "Discipline": mod_dict.get("discipline", ""),
                "Country": mod_dict.get("country", ""),
                "Intervention_Duration_Weeks": mod_dict.get("intervention_duration", ""),
                "Sample_Size_Total": mod_dict.get("sample_size_total", ""),
                "Validation_Notes": "; ".join(result.validation_notes)
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False, engine='openpyxl')
    logger.info(f"Excel file saved: {output_path}")

    return df


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="GenAI-HE Meta-Analysis Extraction Pipeline v9.0 (Groq Edition)"
    )
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=Path("pdfs"),
        help="Directory containing PDF files"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/extractions_v9"),
        help="Output directory for extraction results"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of PDFs to process (for testing)"
    )
    parser.add_argument(
        "--single",
        type=Path,
        default=None,
        help="Process a single PDF file"
    )
    parser.add_argument(
        "--excel",
        type=Path,
        default=None,
        help="Output Excel file path"
    )

    args = parser.parse_args()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY environment variable not set")
        return

    if args.single:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        result = process_pdf(
            args.single,
            args.single.stem,
            args.output_dir,
            api_key
        )
        print(json.dumps(asdict(result), indent=2))
    else:
        results = process_batch(args.pdf_dir, args.output_dir, api_key, args.limit)

        # Create Excel output
        if args.excel:
            create_excel_output(results, args.excel)
        else:
            excel_path = args.output_dir / "GenAI_MetaAnalysis_v9.xlsx"
            create_excel_output(results, excel_path)


if __name__ == "__main__":
    main()
