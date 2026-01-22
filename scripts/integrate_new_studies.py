#!/usr/bin/env python3
"""
Integrate new studies into existing meta-analysis dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Paths
BASE_DIR = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness")
EXISTING_DATA = BASE_DIR / "Final/meta_analysis_HE_corrected.csv"
EXTRACTED_DATA = BASE_DIR / "Generative-AI-in-Higher-Education/data/extracted_effect_sizes.json"
OUTPUT_DIR = BASE_DIR / "Generative-AI-in-Higher-Education/data"

def load_extracted_data():
    """Load extracted effect size data"""
    with open(EXTRACTED_DATA, 'r') as f:
        return json.load(f)

def eta_to_d(eta_squared):
    """Convert eta squared to Cohen's d"""
    if eta_squared is None or eta_squared >= 1:
        return None
    return 2 * np.sqrt(eta_squared / (1 - eta_squared))

def calculate_hedges_g(d, n_total):
    """Calculate Hedges' g from Cohen's d"""
    if d is None or n_total is None:
        return None
    # Correction factor
    df = n_total - 2
    j = 1 - (3 / (4 * df - 1))
    return d * j

def calculate_se(g, n1, n2):
    """Calculate standard error of Hedges' g"""
    if g is None or n1 is None or n2 is None:
        return None
    n_total = n1 + n2
    return np.sqrt((n_total / (n1 * n2)) + (g**2 / (2 * (n_total - 2))))

# Study mapping with metadata
STUDY_MAPPING = {
    "20250711-273024-ln0ri4.pdf": {
        "study_id": 47,
        "title": "Knowledge Retention and AI Assistance",
        "year": 2025,
        "authors": "Unknown (2025)",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Cognitive dependency evidence - retention lower with AI"
    },
    "jmir-2024-1-e57037.pdf": {
        "study_id": 48,
        "title": "JMIR Medical Education Study",
        "year": 2024,
        "authors": "JMIR Authors",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Medical education context"
    },
    "s43031-025-00125-z.pdf": {
        "study_id": 49,
        "title": "Morocco STEM Education Study",
        "year": 2025,
        "authors": "Morocco STEM Team",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "STEM education in Morocco"
    },
    "1-s2.0-S0360131524000459-main.pdf": {
        "study_id": 50,
        "title": "Cognitive Skills and Flipped Learning",
        "year": 2024,
        "authors": "Essel et al.",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "C&E publication - cognitive skills"
    },
    "s41599-024-02751-w.pdf": {
        "study_id": 51,
        "title": "Humanities and Social Sciences Study",
        "year": 2024,
        "authors": "Unknown",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Humanities context"
    },
    "s44217-025-00700-6.pdf": {
        "study_id": 52,
        "title": "ESP Writing with AI",
        "year": 2025,
        "authors": "ESP Writing Team",
        "outcome_dimension": "behavioral",
        "genai_tool": "ChatGPT",
        "notes": "Writing skills - ESP context"
    },
    "Can ChatGPT enhance business student creativity  Evidence from a randomised controlled trial.pdf": {
        "study_id": 53,
        "title": "ChatGPT and Business Student Creativity",
        "year": 2025,
        "authors": "Geng & Razali",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Largest sample (N=534), creativity RCT"
    },
    "qgae170.pdf": {
        "study_id": 54,
        "title": "Oxford Academic Medical Study",
        "year": 2024,
        "authors": "Oxford Authors",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Medical education"
    },
    "Using_a_Chatbot_to_Provide_Formative_Feedback_A_Longitudinal_Study_of_Intrinsic_Motivation_Cognitive_Load_and_Learning_Performance.pdf": {
        "study_id": 55,
        "title": "Formative Feedback Chatbot Longitudinal Study",
        "year": 2024,
        "authors": "Yin et al.",
        "outcome_dimension": "affective",
        "genai_tool": "AI Chatbot",
        "notes": "Longitudinal design, motivation and cognitive load"
    },
    "s41598-025-97652-6.pdf": {
        "study_id": 56,
        "title": "Harvard AI Tutoring Study",
        "year": 2025,
        "authors": "Harvard Team",
        "outcome_dimension": "cognitive",
        "genai_tool": "AI Tutor",
        "notes": "Nature Scientific Reports publication"
    },
    "Brit J Educational Tech - 2025 - Urban - ChatGPT can make mistakes  Check important info   Epistemic beliefs and.pdf": {
        "study_id": 57,
        "title": "Epistemic Beliefs and ChatGPT Mistakes",
        "year": 2025,
        "authors": "Urban et al.",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "BJET 2025, epistemic beliefs focus"
    },
    "s10639-024-12705-z.pdf": {
        "study_id": 58,
        "title": "Education IT Programming Study",
        "year": 2024,
        "authors": "Education IT Authors",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Programming education - verify d=3.0"
    },
    "Comp Applic In Engineering - 2025 - Liu - Who Is the Best Helper for University Students  Mathematical Creativity  A.pdf": {
        "study_id": 59,
        "title": "Mathematical Creativity AI Comparison",
        "year": 2025,
        "authors": "Liu et al.",
        "outcome_dimension": "cognitive",
        "genai_tool": "Multiple AI",
        "notes": "Math creativity, multiple AI tools compared"
    },
    "s10639-025-13733-z.pdf": {
        "study_id": 60,
        "title": "Python Programming with AI",
        "year": 2025,
        "authors": "Python Programming Team",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Programming education"
    },
    "1-s2.0-S2666920X23000772-main.pdf": {
        "study_id": 61,
        "title": "Medical Education RCT",
        "year": 2024,
        "authors": "Gan et al.",
        "outcome_dimension": "cognitive",
        "genai_tool": "ChatGPT",
        "notes": "Medical education - verify d=2.98"
    },
    "Comparing the effects of ChatGPT and automated writing evaluation on students  writing and ideal L2 writing self.pdf": {
        "study_id": 62,
        "title": "ChatGPT vs AWE Writing Study",
        "year": 2025,
        "authors": "ChatGPT vs AWE Team",
        "outcome_dimension": "behavioral",
        "genai_tool": "ChatGPT",
        "notes": "Writing comparison study"
    }
}

def create_new_study_entries():
    """Create new study entries in meta-analysis format"""
    extracted = load_extracted_data()

    new_entries = []

    for study in extracted:
        filename = study['filename']
        if filename not in STUDY_MAPPING:
            continue

        metadata = STUDY_MAPPING[filename]

        # Get or calculate effect sizes
        d = study.get('cohens_d')
        eta = study.get('partial_eta_squared') or study.get('eta_squared')
        n_total = study.get('n_total')

        # Convert eta to d if needed
        if d is None and eta is not None:
            d = eta_to_d(eta)

        # Assume equal groups if n_total available
        n1 = n2 = None
        if n_total:
            n1 = n_total // 2
            n2 = n_total - n1

        # Calculate Hedges' g and SE
        g = calculate_hedges_g(d, n_total) if d and n_total else None
        se = calculate_se(g, n1, n2) if g and n1 and n2 else None

        entry = {
            'study_id': metadata['study_id'],
            'outcome_id': f"{metadata['study_id']:03d}_01",
            'title': metadata['title'],
            'year': metadata['year'],
            'authors': metadata['authors'],
            'outcome_name': 'Primary Outcome',
            'outcome_dimension': metadata['outcome_dimension'],
            'blooms_level': 'not_reported',
            'n_treatment': n1,
            'n_control': n2,
            'm_treatment': study.get('mean_treatment'),
            'sd_treatment': study.get('sd_treatment'),
            'm_control': study.get('mean_control'),
            'sd_control': study.get('sd_control'),
            'hedges_g': round(g, 4) if g else None,
            'se_g': round(se, 4) if se else None,
            'ci_lower': round(g - 1.96 * se, 4) if g and se else None,
            'ci_upper': round(g + 1.96 * se, 4) if g and se else None,
            'cohens_d': round(d, 4) if d else None,
            't_value': study.get('t_value'),
            'f_value': study.get('f_value'),
            'p_value': study.get('p_value'),
            'eta_squared': eta,
            'study_design': 'RCT',
            'genai_tool': metadata['genai_tool'],
            'source': 'New Addition 2025',
            'doi': '',
            'extraction_confidence': 'medium' if d else 'low',
            'notes': metadata['notes'],
            'blooms_category': 'not_classified',
            'academic_level': 'mixed',
            'hedges_g_original': round(g, 4) if g else None,
            'needs_manual_review': 'Yes' if d is None or (d and abs(d) > 2.0) else 'No'
        }

        new_entries.append(entry)

    return new_entries

def main():
    # Load existing data
    existing_df = pd.read_csv(EXISTING_DATA)
    print(f"Existing studies: {existing_df['study_id'].nunique()}")
    print(f"Existing effect sizes: {len(existing_df)}")

    # Create new entries
    new_entries = create_new_study_entries()
    new_df = pd.DataFrame(new_entries)

    # Fill missing columns
    for col in existing_df.columns:
        if col not in new_df.columns:
            new_df[col] = None

    # Reorder columns to match existing
    new_df = new_df[existing_df.columns.tolist() + ['needs_manual_review']]

    # Save new studies separately
    new_studies_path = OUTPUT_DIR / "new_studies_to_add.csv"
    new_df.to_csv(new_studies_path, index=False)
    print(f"\nSaved new studies: {new_studies_path}")
    print(f"New studies: {len(new_df)}")

    # Create summary
    summary = {
        "total_new_studies": len(new_df),
        "with_effect_size": len(new_df[new_df['hedges_g'].notna()]),
        "needs_manual_review": len(new_df[new_df['needs_manual_review'] == 'Yes']),
        "studies": []
    }

    for _, row in new_df.iterrows():
        summary["studies"].append({
            "study_id": int(row['study_id']),
            "title": row['title'],
            "n": int(row['n_treatment'] + row['n_control']) if pd.notna(row['n_treatment']) else None,
            "hedges_g": float(row['hedges_g']) if pd.notna(row['hedges_g']) else None,
            "needs_review": row['needs_manual_review']
        })

    summary_path = OUTPUT_DIR / "integration_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary: {summary_path}")

    # Combined dataset (for preview only - needs manual review)
    combined_df = pd.concat([existing_df, new_df.drop('needs_manual_review', axis=1)], ignore_index=True)
    combined_path = OUTPUT_DIR / "meta_analysis_combined_DRAFT.csv"
    combined_df.to_csv(combined_path, index=False)
    print(f"\nSaved combined DRAFT: {combined_path}")
    print(f"Total studies in combined: {combined_df['study_id'].nunique()}")
    print(f"Total effect sizes: {len(combined_df)}")

    # Print review needed
    print("\n" + "="*50)
    print("STUDIES REQUIRING MANUAL REVIEW:")
    print("="*50)
    for _, row in new_df[new_df['needs_manual_review'] == 'Yes'].iterrows():
        print(f"  - {row['title']}: g={row['hedges_g']}, d={row['cohens_d']}")

if __name__ == "__main__":
    main()
