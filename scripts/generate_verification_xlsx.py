#!/usr/bin/env python3
"""
Generate V8_VERIFICATION.xlsx using Universal Meta-Analysis Codebook v2.1

This script transforms the V8 dataset into the 4-layer codebook structure
for AI-Human collaboration in data verification.

Author: Claude Code
Date: 2026-01-26
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "03_final"
INPUT_FILE = DATA_DIR / "GenAI_MetaAnalysis_v8.csv"
OUTPUT_FILE = DATA_DIR / "GenAI_MetaAnalysis_v8_VERIFICATION.xlsx"


def create_codebook_sheet():
    """Create the codebook reference sheet."""
    codebook_data = {
        "Layer": [],
        "Field": [],
        "Type": [],
        "Description": [],
        "Required": [],
        "AI_Extracts": [],
        "Human_Verifies": []
    }

    # Layer 1: Identifiers + Metadata
    layer1_fields = [
        ("study_id", "str", "Unique study identifier", "Yes", "No", "No"),
        ("es_id", "str", "Effect size ID (study_id + sequence)", "Yes", "No", "No"),
        ("citation", "str", "Full APA citation", "Yes", "Yes", "If LOW"),
        ("doi", "str", "Digital Object Identifier", "No", "Yes", "If LOW"),
        ("year", "int", "Publication year", "Yes", "Yes", "No"),
        ("design_type", "str", "RCT|QUASI|PRE_POST", "Yes", "Yes", "Yes"),
        ("timepoint", "str", "Measurement timing", "Yes", "Yes", "Yes"),
        ("arm_label_treat", "str", "Treatment group label", "No", "Yes", "If LOW"),
        ("arm_label_control", "str", "Control group label", "No", "Yes", "If LOW"),
        ("unit_of_analysis", "str", "individual|cluster", "Yes", "Yes", "Yes"),
    ]

    for field, dtype, desc, req, ai, human in layer1_fields:
        codebook_data["Layer"].append("1: Identifiers")
        codebook_data["Field"].append(field)
        codebook_data["Type"].append(dtype)
        codebook_data["Description"].append(desc)
        codebook_data["Required"].append(req)
        codebook_data["AI_Extracts"].append(ai)
        codebook_data["Human_Verifies"].append(human)

    # Layer 2: Core Statistical Values
    layer2_fields = [
        ("outcome_name", "str", "Measured outcome variable", "Yes", "Yes", "Yes"),
        ("outcome_unit", "str", "Measurement unit", "No", "Yes", "If LOW"),
        ("es_type", "str", "POST_BETWEEN|ANCOVA|CHANGE|PRE_POST", "Yes", "Yes", "Yes"),
        ("analysis_type", "str", "adjusted|unadjusted", "No", "Yes", "If LOW"),
        ("n_treatment", "int", "Treatment group sample size", "Yes", "Yes", "If LOW"),
        ("n_control", "int", "Control group sample size", "Yes", "Yes", "If LOW"),
        ("m_treatment", "float", "Treatment group mean", "Cond", "Yes", "If LOW"),
        ("sd_treatment", "float", "Treatment group SD", "Cond", "Yes", "If LOW"),
        ("m_control", "float", "Control group mean", "Cond", "Yes", "If LOW"),
        ("sd_control", "float", "Control group SD", "Cond", "Yes", "If LOW"),
        ("hedges_g", "float", "Calculated effect size", "Derived", "Calc", "Verify"),
        ("se_g", "float", "Standard error of g", "Derived", "Calc", "Verify"),
    ]

    for field, dtype, desc, req, ai, human in layer2_fields:
        codebook_data["Layer"].append("2: Statistics")
        codebook_data["Field"].append(field)
        codebook_data["Type"].append(dtype)
        codebook_data["Description"].append(desc)
        codebook_data["Required"].append(req)
        codebook_data["AI_Extracts"].append(ai)
        codebook_data["Human_Verifies"].append(human)

    # Layer 2b: Change-score fields
    layer2b_fields = [
        ("pre_mean_treat", "float", "Pre-test mean (treatment)", "Cond", "Yes", "If CHANGE"),
        ("pre_sd_treat", "float", "Pre-test SD (treatment)", "Cond", "Yes", "If CHANGE"),
        ("pre_post_corr", "float", "Pre-post correlation (0-1)", "Cond", "Yes", "If CHANGE"),
    ]

    for field, dtype, desc, req, ai, human in layer2b_fields:
        codebook_data["Layer"].append("2b: Change-Score")
        codebook_data["Field"].append(field)
        codebook_data["Type"].append(dtype)
        codebook_data["Description"].append(desc)
        codebook_data["Required"].append(req)
        codebook_data["AI_Extracts"].append(ai)
        codebook_data["Human_Verifies"].append(human)

    # Layer 2c: Cluster fields
    layer2c_fields = [
        ("cluster_size", "float", "Average cluster size", "Cond", "Yes", "If CLUSTER"),
        ("icc", "float", "Intra-class correlation", "Cond", "Yes", "If CLUSTER"),
        ("n_clusters", "int", "Number of clusters", "Cond", "Yes", "If CLUSTER"),
    ]

    for field, dtype, desc, req, ai, human in layer2c_fields:
        codebook_data["Layer"].append("2c: Cluster")
        codebook_data["Field"].append(field)
        codebook_data["Type"].append(dtype)
        codebook_data["Description"].append(desc)
        codebook_data["Required"].append(req)
        codebook_data["AI_Extracts"].append(ai)
        codebook_data["Human_Verifies"].append(human)

    # Layer 3: AI Extraction
    layer3_fields = [
        ("ai_confidence_avg", "float", "Average AI confidence (0-100)", "-", "-", "-"),
        ("ai_method", "str", "Primary extraction method", "-", "-", "-"),
        ("ai_conflicts", "bool", "Any extraction conflicts?", "-", "-", "-"),
        ("ai_extraction_json", "json", "Full provenance data", "-", "-", "-"),
    ]

    for field, dtype, desc, req, ai, human in layer3_fields:
        codebook_data["Layer"].append("3: AI Provenance")
        codebook_data["Field"].append(field)
        codebook_data["Type"].append(dtype)
        codebook_data["Description"].append(desc)
        codebook_data["Required"].append(req)
        codebook_data["AI_Extracts"].append(ai)
        codebook_data["Human_Verifies"].append(human)

    # Layer 4: Human Verification
    layer4_fields = [
        ("verified_status", "str", "PENDING|PROVISIONAL|VERIFIED|REJECTED", "Yes", "No", "Yes"),
        ("verified_by", "str", "Reviewer initials", "Yes", "No", "Yes"),
        ("verified_date", "date", "Review date", "Yes", "No", "Yes"),
        ("corrections_json", "json", "Any corrections made", "No", "No", "Yes"),
        ("disagreement_resolved", "bool", "Conflict resolved?", "No", "No", "Yes"),
        ("final_values_json", "json", "Human-confirmed values", "No", "No", "Yes"),
        ("verification_notes", "str", "Review notes", "No", "No", "Yes"),
        ("sign_off", "bool", "Final approval", "Yes", "No", "Yes"),
    ]

    for field, dtype, desc, req, ai, human in layer4_fields:
        codebook_data["Layer"].append("4: Verification")
        codebook_data["Field"].append(field)
        codebook_data["Type"].append(dtype)
        codebook_data["Description"].append(desc)
        codebook_data["Required"].append(req)
        codebook_data["AI_Extracts"].append(ai)
        codebook_data["Human_Verifies"].append(human)

    return pd.DataFrame(codebook_data)


def calculate_confidence(row):
    """Calculate AI confidence based on data completeness."""
    fields = ['M_Treatment', 'SD_Treatment', 'n_Treatment',
              'M_Control', 'SD_Control', 'n_Control']
    present = sum(1 for f in fields if pd.notna(row.get(f)))
    return int((present / len(fields)) * 100)


def determine_review_priority(confidence, has_hedges_g, tier):
    """Determine human review priority."""
    if tier == 3:
        return 1  # Highest priority
    if confidence < 70:
        return 2  # High priority
    if not has_hedges_g:
        return 2  # High priority
    if confidence < 85:
        return 3  # Medium priority
    return 4  # Low priority (spot check)


def create_data_sheet(df):
    """Create the main data sheet with Universal Codebook structure."""

    data_rows = []

    for idx, row in df.iterrows():
        # Calculate confidence
        confidence = calculate_confidence(row)
        has_hedges_g = pd.notna(row.get('Hedges_g'))
        tier = row.get('Data_Tier', 3) if pd.notna(row.get('Data_Tier')) else 3
        priority = determine_review_priority(confidence, has_hedges_g, int(tier))

        # Determine status based on confidence
        if confidence >= 90 and has_hedges_g:
            status = "PROVISIONAL"
        else:
            status = "PENDING"

        # Build record
        year_val = row.get('Year')
        year_str = str(int(year_val)) if pd.notna(year_val) else "n.d."
        year_int = int(year_val) if pd.notna(year_val) else None

        record = {
            # Layer 1: Identifiers + Metadata
            "study_id": row.get('Study_ID'),
            "es_id": row.get('ES_ID'),
            "citation": f"{row.get('Authors', '')} ({year_str}). {row.get('Title', '')}",
            "doi": "",  # Not in V8, needs extraction
            "year": year_int,
            "design_type": row.get('Study_Design', 'not_reported'),
            "timepoint": "post",  # Default for GenAI-HE
            "arm_label_treat": "GenAI",
            "arm_label_control": "Traditional",
            "unit_of_analysis": "individual",  # Default

            # Layer 2: Core Statistical Values
            "outcome_name": row.get('Outcome_Name'),
            "outcome_unit": "",
            "es_type": row.get('ES_Type', 'POST_BETWEEN'),
            "analysis_type": "unadjusted",
            "n_treatment": row.get('n_Treatment'),
            "n_control": row.get('n_Control'),
            "m_treatment": row.get('M_Treatment'),
            "sd_treatment": row.get('SD_Treatment'),
            "m_control": row.get('M_Control'),
            "sd_control": row.get('SD_Control'),
            "hedges_g": row.get('Hedges_g'),
            "se_g": row.get('SE_g'),

            # Layer 2b: Change-score (conditional)
            "pre_mean_treat": None,
            "pre_sd_treat": None,
            "pre_post_corr": None,

            # Layer 2c: Cluster (conditional)
            "cluster_size": None,
            "icc": None,
            "n_clusters": None,

            # Layer 3: AI Extraction Summary
            "ai_confidence_avg": confidence,
            "ai_method": "LEGACY",  # Existing data, not AI-extracted
            "ai_conflicts": False,

            # Layer 4: Human Verification
            "verified_status": status,
            "verified_by": "",
            "verified_date": "",
            "disagreement_resolved": True,  # No conflicts for legacy data
            "verification_notes": "",
            "sign_off": False,

            # Additional context
            "review_priority": priority,
            "data_tier": tier,
            "genai_tool": row.get('GenAI_Tool', ''),
        }

        data_rows.append(record)

    return pd.DataFrame(data_rows)


def create_review_queue(data_df):
    """Create prioritized review queue."""
    queue = data_df[data_df['verified_status'] == 'PENDING'].copy()
    queue = queue[['study_id', 'es_id', 'review_priority', 'ai_confidence_avg',
                   'outcome_name', 'data_tier', 'hedges_g', 'verified_status']]
    queue.columns = ['study_id', 'es_id', 'priority', 'ai_confidence',
                     'outcome', 'tier', 'hedges_g', 'status']
    queue['issue'] = queue.apply(
        lambda r: 'Missing Hedges_g' if pd.isna(r['hedges_g']) else
                  f"Tier {int(r['tier'])} data" if r['tier'] == 3 else
                  'Low confidence' if r['ai_confidence'] < 70 else 'Medium confidence',
        axis=1
    )
    queue = queue.sort_values(['priority', 'ai_confidence'])
    queue['status'] = 'pending'
    return queue[['study_id', 'es_id', 'priority', 'issue', 'ai_confidence', 'status']]


def create_study_summary(data_df):
    """Create study-level summary."""
    summary = data_df.groupby('study_id').agg({
        'es_id': 'count',
        'hedges_g': lambda x: x.notna().sum(),
        'ai_confidence_avg': 'mean',
        'data_tier': 'min',
        'verified_status': lambda x: (x == 'VERIFIED').sum()
    }).reset_index()

    summary.columns = ['study_id', 'effect_size_count', 'valid_g_count',
                       'avg_confidence', 'worst_tier', 'verified_count']
    summary['all_g_missing'] = summary['valid_g_count'] == 0
    summary['verification_rate'] = summary['verified_count'] / summary['effect_size_count'] * 100

    return summary


def create_confidence_thresholds():
    """Create confidence thresholds reference."""
    thresholds = {
        "Field": ["n (sample size)", "M (mean)", "SD", "hedges_g (derived)",
                  "se_g (derived)", "pre_post_corr", "icc"],
        "HIGH_threshold": [95, 90, 85, 92, 92, 85, 80],
        "MEDIUM_threshold": [80, 70, 65, 75, 75, 65, 60],
        "Action_HIGH": ["Auto-provisional"] * 7,
        "Action_MEDIUM": ["Recommend review"] * 7,
        "Action_LOW": ["Require review"] * 7
    }
    return pd.DataFrame(thresholds)


def create_extraction_protocol():
    """Create extraction protocol reference."""
    protocol = {
        "Phase": [1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
        "Step": [
            "Build RAG from PDFs",
            "Query RAG for statistical values",
            "Apply OCR fallback for tables",
            "Record provenance for all extractions",
            "Calculate effective confidence",
            "Generate review queue by priority",
            "Verify AI extraction against PDF",
            "Correct errors and record reason",
            "Mark as VERIFIED or REJECTED",
            "C5 validates all gates",
            "Final sign-off"
        ],
        "Agent": ["C6", "C6", "C6", "C6", "C7", "C7", "Human", "Human", "Human", "C5", "Human"],
        "Output": [
            "RAG index",
            "Extracted values",
            "Table data",
            "ai_extraction_json",
            "Confidence scores",
            "Priority queue",
            "Verification",
            "corrections_json",
            "verified_status",
            "Gate results",
            "100% verified"
        ]
    }
    return pd.DataFrame(protocol)


def main():
    print(f"Loading V8 data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"  Loaded {len(df)} records")

    print("\nCreating Universal Codebook sheets...")

    # Create all sheets
    codebook_df = create_codebook_sheet()
    print(f"  Codebook: {len(codebook_df)} fields")

    data_df = create_data_sheet(df)
    print(f"  Data: {len(data_df)} records")

    review_queue = create_review_queue(data_df)
    print(f"  Review Queue: {len(review_queue)} pending")

    study_summary = create_study_summary(data_df)
    print(f"  Study Summary: {len(study_summary)} studies")

    thresholds_df = create_confidence_thresholds()
    protocol_df = create_extraction_protocol()

    # Statistics
    stats = {
        "Metric": [
            "Total Effect Sizes",
            "With Hedges' g",
            "Missing Hedges' g",
            "Missing %",
            "Total Studies",
            "PROVISIONAL (auto)",
            "PENDING (need review)",
            "High Priority (P1-2)",
            "Medium Priority (P3)",
            "Low Priority (P4)"
        ],
        "Value": [
            len(data_df),
            data_df['hedges_g'].notna().sum(),
            data_df['hedges_g'].isna().sum(),
            f"{data_df['hedges_g'].isna().sum() / len(data_df) * 100:.1f}%",
            data_df['study_id'].nunique(),
            (data_df['verified_status'] == 'PROVISIONAL').sum(),
            (data_df['verified_status'] == 'PENDING').sum(),
            len(review_queue[review_queue['priority'] <= 2]),
            len(review_queue[review_queue['priority'] == 3]),
            len(review_queue[review_queue['priority'] == 4])
        ]
    }
    stats_df = pd.DataFrame(stats)

    print(f"\nWriting to {OUTPUT_FILE}...")

    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        codebook_df.to_excel(writer, sheet_name='Codebook', index=False)
        data_df.to_excel(writer, sheet_name='Data', index=False)
        review_queue.to_excel(writer, sheet_name='Review_Queue', index=False)
        study_summary.to_excel(writer, sheet_name='Study_Summary', index=False)
        thresholds_df.to_excel(writer, sheet_name='Confidence_Thresholds', index=False)
        protocol_df.to_excel(writer, sheet_name='Extraction_Protocol', index=False)
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)

    print("\n" + "="*60)
    print("Universal Codebook V8_VERIFICATION.xlsx created successfully!")
    print("="*60)
    print(f"\nSheets created:")
    print(f"  1. Codebook - Field definitions ({len(codebook_df)} fields)")
    print(f"  2. Data - Main worksheet ({len(data_df)} records, 37 columns)")
    print(f"  3. Review_Queue - Prioritized human review ({len(review_queue)} pending)")
    print(f"  4. Study_Summary - Study-level aggregation ({len(study_summary)} studies)")
    print(f"  5. Confidence_Thresholds - Configurable thresholds")
    print(f"  6. Extraction_Protocol - Workflow reference")
    print(f"  7. Statistics - Summary metrics")
    print(f"\nNext steps:")
    print(f"  1. Human reviewers work through Review_Queue by priority")
    print(f"  2. Update verified_status and sign_off in Data sheet")
    print(f"  3. Record corrections in corrections_json if needed")
    print(f"  4. Final validation when all sign_off = True")


if __name__ == "__main__":
    main()
