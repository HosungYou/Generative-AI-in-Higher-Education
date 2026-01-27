#!/usr/bin/env python3
"""
GenAI-HE Meta-Analysis Data Extraction Pipeline v9.0

Modern extraction pipeline using:
- Stage 1: Docling for section-aware PDF parsing
- Stage 2: Claude Structured Outputs for LLM extraction
- Stage 3: C6/C7 validation with provenance tracking

Author: Claude Code
Date: 2026-01-27
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# STAGE 1: Docling Section-Aware Parsing
# ============================================================================

def check_docling_available() -> bool:
    """Check if Docling is installed."""
    try:
        from docling.document_converter import DocumentConverter
        return True
    except ImportError:
        logger.warning("Docling not installed. Using PyMuPDF fallback.")
        return False


def extract_sections_docling(pdf_path: Path) -> Dict[str, str]:
    """
    Extract sections from PDF using Docling.
    Returns dict with section names as keys and text as values.
    """
    try:
        from docling.document_converter import DocumentConverter
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions

        # Configure Docling pipeline
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True

        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))

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

        # Process document structure
        doc = result.document
        current_section = "introduction"

        for item in doc.iterate_items():
            text = item.text if hasattr(item, 'text') else str(item)
            text_lower = text.lower().strip()

            # Detect section headers
            if any(kw in text_lower for kw in ["abstract", "요약"]):
                current_section = "abstract"
            elif any(kw in text_lower for kw in ["method", "methodology", "연구방법"]):
                current_section = "methods"
            elif any(kw in text_lower for kw in ["result", "finding", "결과"]):
                current_section = "results"
            elif any(kw in text_lower for kw in ["discussion", "conclusion", "논의"]):
                current_section = "discussion"
            elif any(kw in text_lower for kw in ["table", "표"]):
                sections["tables"] += text + "\n"
            else:
                sections[current_section] += text + "\n"

            sections["full_text"] += text + "\n"

        # Extract tables separately
        for table in doc.tables:
            sections["tables"] += table.export_to_markdown() + "\n\n"

        return sections

    except Exception as e:
        logger.error(f"Docling extraction failed for {pdf_path}: {e}")
        return extract_sections_pymupdf(pdf_path)


def extract_sections_pymupdf(pdf_path: Path) -> Dict[str, str]:
    """
    Fallback: Extract sections using PyMuPDF with section detection.
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
            ("methods", ["method", "methodology", "연구방법", "연구 방법"]),
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
# STAGE 2: Claude Structured Outputs for LLM Extraction
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


# GenAI-HE specific moderator schema
GENAI_HE_MODERATOR_SCHEMA = {
    "genai_tool": {
        "type": "categorical",
        "values": ["ChatGPT", "Claude", "Bard/Gemini", "Copilot", "Other", "Multiple"],
        "extraction_prompt": "What GenAI tool was used in this study? Look for mentions of ChatGPT, GPT-4, Claude, Gemini, Bard, Copilot, or other AI assistants in the Methods section."
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
        "values": ["STEM", "Humanities", "Social Sciences", "Health", "Business", "Mixed"],
        "extraction_prompt": "What discipline or subject area was studied? Look for mentions of the course or subject."
    },
    "country": {
        "type": "categorical",
        "extraction_prompt": "In which country was the study conducted? Look for location information in the Methods section."
    },
    "sample_size_total": {
        "type": "continuous",
        "extraction_prompt": "What was the total sample size? Add treatment and control group sizes."
    }
}


def create_extraction_prompt(sections: Dict[str, str], moderator_schema: Dict) -> str:
    """
    Create a structured extraction prompt for Claude.
    """
    prompt = f"""You are a meta-analysis data extraction expert. Extract the following information from this academic paper.

## Paper Content

### Methods Section
{sections.get('methods', 'Not available')[:8000]}

### Results Section
{sections.get('results', 'Not available')[:8000]}

### Tables
{sections.get('tables', 'Not available')[:4000]}

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
- n_treatment: Sample size in treatment group
- n_control: Sample size in control group
- m_treatment: Mean in treatment group
- sd_treatment: Standard deviation in treatment group
- m_control: Mean in control group
- sd_control: Standard deviation in control group

Look for these values in tables, results text, or statistical reports.

## Output Format

Respond with a JSON object in this exact structure:
```json
{
  "moderators": [
    {
      "field": "genai_tool",
      "value": "ChatGPT",
      "confidence": 95,
      "source": "Methods section, paragraph 2: 'Participants used ChatGPT-4...'"
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
```

Be precise and only extract values you can find with high confidence. If a value is not found, omit it rather than guessing.
"""
    return prompt


def extract_with_claude(
    sections: Dict[str, str],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract data using Claude with structured outputs.
    Uses anthropic-beta: structured-outputs-2025-11-13
    """
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = create_extraction_prompt(sections, GENAI_HE_MODERATOR_SCHEMA)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ],
            # Enable structured outputs beta
            extra_headers={
                "anthropic-beta": "structured-outputs-2025-11-13"
            }
        )

        # Parse response
        content = response.content[0].text

        # Extract JSON from response
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            # Try parsing entire response as JSON
            result = json.loads(content)

        return result

    except Exception as e:
        logger.error(f"Claude extraction failed: {e}")
        return {"moderators": [], "statistics": [], "extraction_notes": [str(e)]}


# ============================================================================
# STAGE 3: C6/C7 Validation Pipeline
# ============================================================================

def validate_extraction_c7(extraction: ExtractionResult) -> List[str]:
    """
    C7-ErrorPreventionEngine validation checks.
    Returns list of warnings/errors.
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
    C6-DataIntegrityGuard calculation.
    """
    if None in [stat.m_treatment, stat.sd_treatment, stat.m_control,
                stat.sd_control, stat.n_treatment, stat.n_control]:
        return None

    import math

    n1, n2 = stat.n_treatment, stat.n_control
    m1, m2 = stat.m_treatment, stat.m_control
    sd1, sd2 = stat.sd_treatment, stat.sd_control

    # Pooled SD
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


def calculate_se_g(stat: StatisticalExtraction, g: float) -> Optional[float]:
    """
    Calculate SE of Hedges' g.
    """
    if stat.n_treatment is None or stat.n_control is None:
        return None

    import math

    n1, n2 = stat.n_treatment, stat.n_control

    se = math.sqrt(
        (n1 + n2) / (n1 * n2) + (g ** 2) / (2 * (n1 + n2))
    )

    return round(se, 4)


def process_extraction_c6(extraction: ExtractionResult) -> ExtractionResult:
    """
    C6-DataIntegrityGuard processing.
    Calculate derived values and add provenance.
    """
    for stat in extraction.statistics:
        # Calculate Hedges' g if not provided
        if stat.hedges_g is None:
            stat.hedges_g = calculate_hedges_g(stat)
            if stat.hedges_g is not None:
                stat.method = "CALCULATED_FROM_MEANS"

        # Calculate SE_g
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
    if check_docling_available():
        sections = extract_sections_docling(pdf_path)
    else:
        sections = extract_sections_pymupdf(pdf_path)

    # Stage 2: LLM extraction
    logger.info("  Stage 2: Claude extraction...")
    raw_extraction = extract_with_claude(sections, api_key)

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

    # Stage 3a: C6 processing (calculate Hedges' g)
    logger.info("  Stage 3a: C6 processing...")
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

    for pdf_path in pdf_files:
        study_id = pdf_path.stem
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
        "total_pdfs": len(pdf_files),
        "successful": sum(1 for r in results if r.validation_status != "FAILED"),
        "needs_review": sum(1 for r in results if r.validation_status == "NEEDS_REVIEW"),
        "failed": sum(1 for r in results if r.validation_status == "FAILED"),
        "results": [asdict(r) for r in results]
    }

    summary_file = output_dir / "extraction_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"\nExtraction complete: {summary['successful']}/{summary['total_pdfs']} successful")

    return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="GenAI-HE Meta-Analysis Extraction Pipeline v9.0"
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

    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        return

    if args.single:
        result = process_pdf(
            args.single,
            args.single.stem,
            args.output_dir,
            api_key
        )
        print(json.dumps(asdict(result), indent=2))
    else:
        process_batch(args.pdf_dir, args.output_dir, api_key, args.limit)


if __name__ == "__main__":
    main()
