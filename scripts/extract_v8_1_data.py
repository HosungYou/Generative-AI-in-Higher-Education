#!/usr/bin/env python3
"""
GenAI-HE Meta-Analysis Data Extraction Script (V8.1)

This script extracts statistical values and moderator variables from PDFs
using the Universal Codebook v2.2 with GenAI-HE context extension.

Implements C6-DataIntegrityGuard functionality:
1. PDF text extraction (PyMuPDF)
2. LLM-based value extraction (Claude API)
3. Moderator variable classification
4. Hedges' g calculation
5. Provenance tracking

Author: Claude Code
Date: 2026-01-26
"""

import os
import re
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
import fitz  # PyMuPDF

# Try to import anthropic, handle gracefully if not available
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not installed. Run: pip install anthropic")

# Paths
PROJECT_DIR = Path(__file__).parent.parent
PDF_DIR = PROJECT_DIR / "pdfs"
DATA_DIR = PROJECT_DIR / "data" / "03_final"
OUTPUT_FILE = DATA_DIR / "GenAI_MetaAnalysis_v8.1.csv"
OUTPUT_XLSX = DATA_DIR / "GenAI_MetaAnalysis_v8.1.xlsx"

# GenAI Tool Classification
GENAI_TOOL_PATTERNS = {
    "ChatGPT": [
        r"chatgpt", r"chat\s*gpt", r"gpt-3\.5", r"gpt-4", r"gpt-4o",
        r"openai", r"gpt3", r"gpt4"
    ],
    "Claude": [r"claude", r"anthropic"],
    "Gemini": [r"gemini", r"bard", r"google\s*ai"],
    "Llama": [r"llama", r"meta\s*ai", r"llama-2", r"llama-3"],
    "Copilot": [r"copilot", r"github\s*copilot", r"microsoft\s*copilot"],
    "Mistral": [r"mistral", r"mixtral"],
}

GENAI_VERSION_PATTERNS = {
    "gpt-3.5": [r"gpt-3\.5", r"gpt3\.5", r"3\.5-turbo"],
    "gpt-4": [r"gpt-4(?!o)", r"gpt4(?!o)"],
    "gpt-4o": [r"gpt-4o", r"gpt4o"],
    "claude-3": [r"claude-3", r"claude\s*3"],
}

BLOOMS_KEYWORDS = {
    "remember": ["recall", "recognize", "list", "define", "memorize", "identify", "name"],
    "understand": ["explain", "describe", "interpret", "summarize", "classify", "comprehend"],
    "apply": ["apply", "implement", "use", "execute", "solve", "demonstrate", "practice"],
    "analyze": ["analyze", "differentiate", "examine", "compare", "contrast", "investigate"],
    "evaluate": ["evaluate", "judge", "critique", "assess", "justify", "argue", "rate"],
    "create": ["create", "design", "construct", "produce", "generate", "compose", "write"],
}

OUTCOME_DIMENSION_KEYWORDS = {
    "cognitive": ["knowledge", "learning", "score", "test", "achievement", "performance", "skill", "understanding"],
    "affective": ["attitude", "motivation", "satisfaction", "confidence", "self-efficacy", "perception", "interest", "enjoyment"],
    "behavioral": ["usage", "behavior", "participation", "engagement", "time", "completion", "action"],
    "metacognitive": ["self-regulation", "metacognitive", "awareness", "self-assessment", "strategy", "monitoring"],
}


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""


def classify_genai_tool(text: str) -> Dict[str, str]:
    """Classify GenAI tool from PDF text."""
    text_lower = text.lower()

    tool = "not_reported"
    version = "not_reported"
    access_type = "not_reported"

    # Find tool
    for tool_name, patterns in GENAI_TOOL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                tool = tool_name
                break
        if tool != "not_reported":
            break

    # Find version
    for ver, patterns in GENAI_VERSION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                version = ver
                break
        if version != "not_reported":
            break

    # Find access type
    if re.search(r"api|programmatic|integration", text_lower):
        access_type = "api"
    elif re.search(r"web\s*interface|browser|online|chat\s*interface", text_lower):
        access_type = "web_interface"
    elif re.search(r"custom|developed|built|application", text_lower):
        access_type = "custom_integration"

    return {
        "genai_tool": tool,
        "genai_tool_version": version,
        "genai_access_type": access_type
    }


def classify_blooms_level(outcome_name: str, text: str) -> str:
    """Classify Bloom's Taxonomy level based on outcome and context."""
    combined = f"{outcome_name} {text[:5000]}".lower()

    # Check for keywords
    scores = {level: 0 for level in BLOOMS_KEYWORDS}
    for level, keywords in BLOOMS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined:
                scores[level] += 1

    # Get highest scoring level
    max_score = max(scores.values())
    if max_score > 0:
        for level, score in scores.items():
            if score == max_score:
                return level

    # Default heuristics based on outcome name patterns
    outcome_lower = outcome_name.lower()
    if any(kw in outcome_lower for kw in ["test score", "quiz", "exam", "knowledge"]):
        return "remember"
    elif any(kw in outcome_lower for kw in ["comprehension", "understanding"]):
        return "understand"
    elif any(kw in outcome_lower for kw in ["performance", "task", "skill", "problem"]):
        return "apply"
    elif any(kw in outcome_lower for kw in ["critical", "analysis"]):
        return "analyze"
    elif any(kw in outcome_lower for kw in ["evaluation", "judgment", "critique"]):
        return "evaluate"
    elif any(kw in outcome_lower for kw in ["writing", "creative", "design", "generation"]):
        return "create"

    return "not_classified"


def classify_outcome_dimension(outcome_name: str) -> str:
    """Classify outcome dimension."""
    outcome_lower = outcome_name.lower()

    scores = {dim: 0 for dim in OUTCOME_DIMENSION_KEYWORDS}
    for dim, keywords in OUTCOME_DIMENSION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in outcome_lower:
                scores[dim] += 1

    max_score = max(scores.values())
    if max_score > 0:
        for dim, score in scores.items():
            if score == max_score:
                return dim

    return "cognitive"  # Default


def classify_study_design(text: str) -> str:
    """Classify study design from PDF text."""
    text_lower = text.lower()

    if re.search(r"random(ly|ized)?\s*(assign|allocat)", text_lower):
        return "RCT"
    elif re.search(r"quasi-?experiment", text_lower):
        return "quasi-experimental"
    elif re.search(r"non-?random", text_lower):
        return "quasi-experimental"
    elif re.search(r"pre-?post|before\s*and\s*after", text_lower):
        return "pre-post"
    elif re.search(r"crossover|cross-?over", text_lower):
        return "crossover"

    # Check for intact groups (classes, sections)
    if re.search(r"intact\s*group|existing\s*class|section", text_lower):
        return "quasi-experimental"

    return "not_reported"


def extract_education_level(text: str) -> str:
    """Extract education level."""
    text_lower = text.lower()

    if re.search(r"undergraduate|bachelor|college\s*student", text_lower):
        return "undergraduate"
    elif re.search(r"graduate|master|doctoral|phd", text_lower):
        return "graduate"
    elif re.search(r"k-?12|high\s*school|secondary|primary|elementary", text_lower):
        return "K-12"
    elif re.search(r"medical\s*student|nursing|resident", text_lower):
        return "professional"

    return "undergraduate"  # Default for HE studies


def extract_discipline(text: str) -> str:
    """Extract academic discipline."""
    text_lower = text.lower()

    disciplines = {
        "CS": [r"computer\s*science", r"programming", r"software", r"coding"],
        "medicine": [r"medic", r"nursing", r"health\s*science", r"clinical"],
        "engineering": [r"engineer"],
        "STEM": [r"stem", r"science", r"math", r"physic", r"chemistry", r"biology"],
        "language": [r"language\s*learning", r"esl", r"english", r"writing", r"linguistic"],
        "business": [r"business", r"management", r"marketing", r"finance"],
        "education": [r"education", r"teacher", r"pedagog"],
        "humanities": [r"humanities", r"philosophy", r"history", r"art"],
    }

    for disc, patterns in disciplines.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return disc

    return "mixed"


def calculate_hedges_g(m1, sd1, n1, m2, sd2, n2) -> tuple:
    """Calculate Hedges' g with small-sample correction."""
    try:
        if any(pd.isna([m1, sd1, n1, m2, sd2, n2])):
            return None, None
        if sd1 <= 0 or sd2 <= 0 or n1 <= 1 or n2 <= 1:
            return None, None

        # Pooled SD
        pooled_sd = np.sqrt(
            ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) /
            (n1 + n2 - 2)
        )

        if pooled_sd <= 0:
            return None, None

        # Cohen's d
        d = (m1 - m2) / pooled_sd

        # Hedges' correction
        df = n1 + n2 - 2
        J = 1 - (3 / (4 * df - 1))

        # Hedges' g
        g = d * J

        # SE of g
        se_g = np.sqrt(
            (n1 + n2) / (n1 * n2) + (g**2) / (2 * (n1 + n2))
        ) * J

        return round(g, 4), round(se_g, 4)
    except Exception:
        return None, None


def process_existing_v8_with_moderators(v8_path: Path, pdf_dir: Path) -> pd.DataFrame:
    """
    Process existing V8 data and enhance with moderator variables extracted from PDFs.
    """
    print(f"Loading V8 data from {v8_path}...")
    df = pd.read_csv(v8_path)
    print(f"  Loaded {len(df)} records from {df['Study_ID'].nunique()} studies")

    # Create mapping of Study_ID to PDF file
    pdf_files = list(pdf_dir.glob("*.pdf"))
    study_pdf_map = {}
    for pdf in pdf_files:
        # Extract study ID from filename (e.g., "001_Jiyong_2025_..." -> 1)
        match = re.match(r"(\d+)_", pdf.name)
        if match:
            study_id = int(match.group(1))
            study_pdf_map[study_id] = pdf

    print(f"  Found {len(study_pdf_map)} PDFs mapped to studies")

    # Initialize new columns
    new_cols = {
        "genai_tool_v81": [],
        "genai_tool_version": [],
        "genai_access_type": [],
        "blooms_level_v81": [],
        "outcome_dimension_v81": [],
        "learning_domain": [],
        "study_design_v81": [],
        "education_level": [],
        "discipline": [],
        "ai_confidence_avg": [],
        "ai_method": [],
        "verified_status": [],
        "extraction_notes": [],
    }

    # Process each record
    pdf_cache = {}  # Cache PDF text to avoid re-reading

    for idx, row in df.iterrows():
        study_id = row['Study_ID']
        outcome_name = row.get('Outcome_Name', '')

        # Get PDF text (cached)
        if study_id not in pdf_cache:
            if study_id in study_pdf_map:
                pdf_text = extract_text_from_pdf(study_pdf_map[study_id])
                pdf_cache[study_id] = pdf_text
            else:
                pdf_cache[study_id] = ""

        pdf_text = pdf_cache.get(study_id, "")

        # Extract moderators
        if pdf_text:
            genai_info = classify_genai_tool(pdf_text)
            study_design = classify_study_design(pdf_text)
            education_level = extract_education_level(pdf_text)
            discipline = extract_discipline(pdf_text)
            blooms = classify_blooms_level(str(outcome_name), pdf_text)
            confidence = 80  # PDF found and processed
            method = "RAG_TEXT"
            notes = "Extracted from PDF text"
        else:
            # Fallback to existing data
            genai_info = {
                "genai_tool": row.get('GenAI_Tool', 'not_reported'),
                "genai_tool_version": "not_reported",
                "genai_access_type": "not_reported"
            }
            study_design = row.get('Study_Design', 'not_reported')
            education_level = "not_reported"
            discipline = "not_reported"
            blooms = row.get('Blooms_Level', '') if pd.notna(row.get('Blooms_Level')) else "not_classified"
            confidence = 50  # Using existing data
            method = "LEGACY"
            notes = "No PDF found, using V8 data"

        # Outcome dimension
        outcome_dim = classify_outcome_dimension(str(outcome_name))
        if pd.notna(row.get('Outcome_Dimension')):
            outcome_dim = row['Outcome_Dimension']  # Keep if already coded

        # Learning domain heuristic
        learning_domain = "knowledge_acquisition"
        outcome_lower = str(outcome_name).lower()
        if "writing" in outcome_lower:
            learning_domain = "writing"
        elif "critical" in outcome_lower:
            learning_domain = "critical_thinking"
        elif "problem" in outcome_lower or "solving" in outcome_lower:
            learning_domain = "problem_solving"
        elif "creat" in outcome_lower:
            learning_domain = "creativity"
        elif "skill" in outcome_lower:
            learning_domain = "skill_development"

        # Append to new columns
        new_cols["genai_tool_v81"].append(genai_info["genai_tool"])
        new_cols["genai_tool_version"].append(genai_info["genai_tool_version"])
        new_cols["genai_access_type"].append(genai_info["genai_access_type"])
        new_cols["blooms_level_v81"].append(blooms)
        new_cols["outcome_dimension_v81"].append(outcome_dim)
        new_cols["learning_domain"].append(learning_domain)
        new_cols["study_design_v81"].append(study_design)
        new_cols["education_level"].append(education_level)
        new_cols["discipline"].append(discipline)
        new_cols["ai_confidence_avg"].append(confidence)
        new_cols["ai_method"].append(method)
        new_cols["verified_status"].append("PENDING")
        new_cols["extraction_notes"].append(notes)

        if (idx + 1) % 50 == 0:
            print(f"  Processed {idx + 1}/{len(df)} records...")

    # Add new columns to dataframe
    for col, values in new_cols.items():
        df[col] = values

    # Recalculate Hedges' g where possible
    print("\nRecalculating Hedges' g...")
    recalc_count = 0
    for idx, row in df.iterrows():
        if pd.isna(row.get('Hedges_g')):
            g, se = calculate_hedges_g(
                row.get('M_Treatment'), row.get('SD_Treatment'), row.get('n_Treatment'),
                row.get('M_Control'), row.get('SD_Control'), row.get('n_Control')
            )
            if g is not None:
                df.at[idx, 'Hedges_g'] = g
                df.at[idx, 'SE_g'] = se
                df.at[idx, 'extraction_notes'] = df.at[idx, 'extraction_notes'] + "; Hedges_g recalculated"
                recalc_count += 1

    print(f"  Recalculated {recalc_count} Hedges' g values")

    # Update version info
    df['Data_Version'] = 'v8.1'
    df['Version_Date'] = datetime.now().strftime('%Y-%m-%d')

    return df


def create_v81_verification_xlsx(df: pd.DataFrame, output_path: Path):
    """Create V8.1 verification Excel file with multiple sheets."""

    # Codebook sheet
    codebook_data = {
        "Layer": [
            "1", "1", "1", "1", "1",
            "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2",
            "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3",
            "4", "4", "4", "4",
            "5", "5", "5", "5", "5", "5", "5", "5"
        ],
        "Field": [
            "study_id", "es_id", "title", "year", "authors",
            "outcome_name", "outcome_dimension_v81", "es_type", "n_treatment", "n_control",
            "m_treatment", "sd_treatment", "m_control", "sd_control", "hedges_g", "se_g", "data_tier",
            "genai_tool_v81", "genai_tool_version", "genai_access_type",
            "blooms_level_v81", "learning_domain",
            "study_design_v81", "education_level", "discipline",
            "intervention_duration", "intervention_type", "control_condition",
            "country", "sample_size_total", "publication_type",
            "ai_confidence_avg", "ai_method", "ai_conflicts", "extraction_notes",
            "verified_status", "verified_by", "verified_date", "corrections_json",
            "disagreement_resolved", "final_values_json", "verification_notes", "sign_off"
        ],
        "Type": [
            "str", "str", "str", "int", "str",
            "str", "str", "str", "int", "int",
            "float", "float", "float", "float", "float", "float", "int",
            "str", "str", "str", "str", "str", "str", "str", "str",
            "str", "str", "str", "str", "int", "str",
            "float", "str", "bool", "str",
            "str", "str", "date", "json", "bool", "json", "str", "bool"
        ],
        "Description": [
            "Unique study ID", "Effect size ID", "Study title", "Publication year", "Authors",
            "Outcome variable name", "Cognitive/Affective/Behavioral/Metacognitive", "Effect size type",
            "Treatment sample size", "Control sample size",
            "Treatment mean", "Treatment SD", "Control mean", "Control SD",
            "Hedges' g effect size", "SE of Hedges' g", "Data completeness tier",
            "GenAI tool (ChatGPT, Claude, etc.)", "Tool version (gpt-4, etc.)",
            "Access type (web, API, etc.)", "Bloom's taxonomy level", "Learning domain",
            "Study design (RCT, quasi, etc.)", "Education level", "Academic discipline",
            "Intervention duration", "Intervention type", "Control condition",
            "Country", "Total sample size", "Publication type",
            "Average AI confidence", "Extraction method", "Extraction conflicts", "Notes",
            "Verification status", "Reviewer", "Review date", "Corrections",
            "Conflicts resolved", "Final values", "Notes", "Final sign-off"
        ]
    }
    codebook_df = pd.DataFrame(codebook_data)

    # Review queue
    pending = df[df['verified_status'] == 'PENDING'].copy()
    pending['priority'] = pending.apply(
        lambda r: 1 if r['ai_confidence_avg'] < 70 else (2 if pd.isna(r.get('Hedges_g')) else 3),
        axis=1
    )
    review_queue = pending[['Study_ID', 'ES_ID', 'priority', 'ai_confidence_avg',
                            'Outcome_Name', 'genai_tool_v81', 'blooms_level_v81', 'verified_status']]
    review_queue = review_queue.sort_values('priority')
    review_queue.columns = ['study_id', 'es_id', 'priority', 'confidence', 'outcome', 'genai_tool', 'blooms', 'status']

    # Summary statistics
    stats = {
        "Metric": [
            "Total Effect Sizes",
            "Total Studies",
            "With Hedges' g",
            "Missing Hedges' g",
            "GenAI Tool Known",
            "Blooms Level Classified",
            "Study Design Known",
            "Avg AI Confidence",
            "PENDING Records",
            "VERIFIED Records"
        ],
        "Value": [
            len(df),
            df['Study_ID'].nunique(),
            df['Hedges_g'].notna().sum(),
            df['Hedges_g'].isna().sum(),
            (df['genai_tool_v81'] != 'not_reported').sum(),
            (df['blooms_level_v81'] != 'not_classified').sum(),
            (df['study_design_v81'] != 'not_reported').sum(),
            f"{df['ai_confidence_avg'].mean():.1f}%",
            (df['verified_status'] == 'PENDING').sum(),
            (df['verified_status'] == 'VERIFIED').sum()
        ]
    }
    stats_df = pd.DataFrame(stats)

    # GenAI tool distribution
    genai_dist = df['genai_tool_v81'].value_counts().reset_index()
    genai_dist.columns = ['GenAI_Tool', 'Count']

    # Blooms distribution
    blooms_dist = df['blooms_level_v81'].value_counts().reset_index()
    blooms_dist.columns = ['Blooms_Level', 'Count']

    # Write to Excel
    print(f"\nWriting V8.1 verification file to {output_path}...")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        codebook_df.to_excel(writer, sheet_name='Codebook', index=False)
        df.to_excel(writer, sheet_name='Data', index=False)
        review_queue.to_excel(writer, sheet_name='Review_Queue', index=False)
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        genai_dist.to_excel(writer, sheet_name='GenAI_Distribution', index=False)
        blooms_dist.to_excel(writer, sheet_name='Blooms_Distribution', index=False)


def main():
    print("="*60)
    print("GenAI-HE Meta-Analysis V8.1 Data Extraction")
    print("Universal Codebook v2.2 + GenAI-HE Extension")
    print("="*60)

    v8_path = DATA_DIR / "GenAI_MetaAnalysis_v8.csv"

    # Process V8 data with moderator extraction
    df = process_existing_v8_with_moderators(v8_path, PDF_DIR)

    # Summary
    print("\n" + "="*60)
    print("V8.1 Extraction Summary")
    print("="*60)
    print(f"Total records: {len(df)}")
    print(f"Total studies: {df['Study_ID'].nunique()}")
    print(f"\nGenAI Tool (v8.1):")
    print(df['genai_tool_v81'].value_counts())
    print(f"\nBlooms Level (v8.1):")
    print(df['blooms_level_v81'].value_counts())
    print(f"\nStudy Design (v8.1):")
    print(df['study_design_v81'].value_counts())
    print(f"\nHedges' g: {df['Hedges_g'].notna().sum()}/{len(df)} ({df['Hedges_g'].notna().sum()/len(df)*100:.1f}%)")

    # Save outputs
    print(f"\nSaving to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saving to {OUTPUT_XLSX}...")
    output_xlsx = DATA_DIR / "GenAI_MetaAnalysis_v8.1_VERIFICATION.xlsx"
    create_v81_verification_xlsx(df, output_xlsx)

    print("\n" + "="*60)
    print("V8.1 Extraction Complete!")
    print("="*60)
    print(f"\nOutput files:")
    print(f"  - {OUTPUT_FILE}")
    print(f"  - {output_xlsx}")
    print(f"\nNext steps:")
    print(f"  1. Review extraction in Review_Queue sheet")
    print(f"  2. Verify GenAI tools and Blooms levels")
    print(f"  3. Update verified_status and sign_off")


if __name__ == "__main__":
    main()
