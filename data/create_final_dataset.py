#!/usr/bin/env python3
"""
Create Final Dataset with Excluded Studies
==========================================
Excludes 5 flagged studies and creates publication-ready dataset.

Author: Claude Code
Date: 2026-01-26
Version: 4.0
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

# Studies to exclude (design issues identified in manual review)
EXCLUDED_STUDIES = [10, 17, 20, 51, 56]

EXCLUSION_REASONS = {
    10: "Within-subject design without traditional control group",
    17: "No control group - pre-post design only",
    20: "Complex multi-group design not suitable for standard meta-analysis",
    51: "Measures feedback quality, not learning outcomes",
    56: "Measures engagement metrics, not learning performance"
}

def load_source_data():
    """Load the verified source data."""
    # Load the manual-reviewed data
    df = pd.read_csv("meta_analysis_effects_v3_manual_reviewed_20260126.csv")
    return df

def exclude_studies(df):
    """Exclude flagged studies from dataset."""
    print(f"\n=== Excluding {len(EXCLUDED_STUDIES)} Studies ===")

    # Count before exclusion
    n_studies_before = df['study_id'].nunique()
    n_effects_before = len(df)

    # Exclude studies
    df_excluded = df[~df['study_id'].isin(EXCLUDED_STUDIES)].copy()

    # Count after exclusion
    n_studies_after = df_excluded['study_id'].nunique()
    n_effects_after = len(df_excluded)

    print(f"  Before: {n_studies_before} studies, {n_effects_before} effect sizes")
    print(f"  After:  {n_studies_after} studies, {n_effects_after} effect sizes")
    print(f"  Excluded: {n_studies_before - n_studies_after} studies, {n_effects_before - n_effects_after} effect sizes")

    return df_excluded

def create_study_characteristics(df):
    """Create study characteristics sheet."""
    study_cols = ['study_id', 'title', 'year', 'authors']

    # Get unique studies
    studies = df.groupby('study_id').first().reset_index()

    # Calculate n_effects per study
    effect_counts = df.groupby('study_id').size().reset_index(name='n_Effects')
    studies = studies.merge(effect_counts, on='study_id')

    # Calculate total sample size
    sample_sizes = df.groupby('study_id').agg({
        'n_treatment': 'first',
        'n_control': 'first'
    }).reset_index()
    sample_sizes['Sample_Size'] = sample_sizes['n_treatment'] + sample_sizes['n_control']
    studies = studies.merge(sample_sizes[['study_id', 'Sample_Size']], on='study_id')

    # Add verification status
    verification = df.groupby('study_id')['verification_status'].first().reset_index()
    studies = studies.merge(verification, on='study_id')

    # Rename columns
    studies = studies.rename(columns={
        'study_id': 'Study_ID',
        'title': 'Title',
        'year': 'Year',
        'authors': 'Authors',
        'verification_status': 'Verification_Status'
    })

    # Select and order columns
    cols = ['Study_ID', 'Title', 'Year', 'Authors', 'Sample_Size', 'n_Effects', 'Verification_Status']
    available_cols = [c for c in cols if c in studies.columns]

    return studies[available_cols]

def create_effect_sizes_sheet(df):
    """Create effect sizes sheet with standardized columns."""
    # Map column names to Excel format
    column_mapping = {
        'study_id': 'Study_ID',
        'outcome_id': 'ES_ID',
        'title': 'Title',
        'year': 'Year',
        'authors': 'Authors',
        'outcome_name': 'Outcome_Name',
        'outcome_dimension': 'Outcome_Dimension',
        'blooms_level': 'Blooms_Level',
        'n_treatment': 'n_Treatment',
        'n_control': 'n_Control',
        'm_treatment': 'M_Treatment',
        'sd_treatment': 'SD_Treatment',
        'm_control': 'M_Control',
        'sd_control': 'SD_Control',
        'hedges_g': 'Hedges_g',
        'se_g': 'SE_g',
        'verification_status': 'Verification_Status',
        'verification_confidence': 'Verification_Confidence',
        'data_tier': 'Data_Tier'
    }

    # Rename columns
    df_excel = df.rename(columns=column_mapping)

    # Calculate SE if not present
    if 'SE_g' not in df_excel.columns:
        # SE = sqrt((n1+n2)/(n1*n2) + g^2/(2*(n1+n2)))
        n1 = df_excel['n_Treatment']
        n2 = df_excel['n_Control']
        g = df_excel['Hedges_g']
        df_excel['SE_g'] = np.sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))

    # Select columns
    cols = ['Study_ID', 'ES_ID', 'Title', 'Year', 'Authors', 'Outcome_Name',
            'Outcome_Dimension', 'Blooms_Level', 'n_Treatment', 'n_Control',
            'M_Treatment', 'SD_Treatment', 'M_Control', 'SD_Control',
            'Hedges_g', 'SE_g', 'Verification_Status', 'Verification_Confidence', 'Data_Tier']

    available_cols = [c for c in cols if c in df_excel.columns]

    return df_excel[available_cols]

def create_moderator_summary(df):
    """Create moderator summary statistics."""
    summaries = []

    # By Outcome Dimension
    if 'outcome_dimension' in df.columns:
        for dim in df['outcome_dimension'].dropna().unique():
            subset = df[df['outcome_dimension'] == dim]
            summaries.append({
                'Moderator': 'Outcome_Dimension',
                'Category': dim,
                'k_Studies': subset['study_id'].nunique(),
                'n_Effects': len(subset),
                'Mean_g': subset['hedges_g'].mean(),
                'SD_g': subset['hedges_g'].std(),
                'Min_g': subset['hedges_g'].min(),
                'Max_g': subset['hedges_g'].max()
            })

    # By Bloom's Level
    if 'blooms_level' in df.columns:
        for level in df['blooms_level'].dropna().unique():
            subset = df[df['blooms_level'] == level]
            summaries.append({
                'Moderator': 'Blooms_Level',
                'Category': level,
                'k_Studies': subset['study_id'].nunique(),
                'n_Effects': len(subset),
                'Mean_g': subset['hedges_g'].mean(),
                'SD_g': subset['hedges_g'].std(),
                'Min_g': subset['hedges_g'].min(),
                'Max_g': subset['hedges_g'].max()
            })

    # By Year
    for year in sorted(df['year'].dropna().unique()):
        subset = df[df['year'] == year]
        summaries.append({
            'Moderator': 'Publication_Year',
            'Category': int(year),
            'k_Studies': subset['study_id'].nunique(),
            'n_Effects': len(subset),
            'Mean_g': subset['hedges_g'].mean(),
            'SD_g': subset['hedges_g'].std(),
            'Min_g': subset['hedges_g'].min(),
            'Max_g': subset['hedges_g'].max()
        })

    # By Verification Status
    for status in df['verification_status'].unique():
        subset = df[df['verification_status'] == status]
        summaries.append({
            'Moderator': 'Verification_Status',
            'Category': status,
            'k_Studies': subset['study_id'].nunique(),
            'n_Effects': len(subset),
            'Mean_g': subset['hedges_g'].mean(),
            'SD_g': subset['hedges_g'].std(),
            'Min_g': subset['hedges_g'].min(),
            'Max_g': subset['hedges_g'].max()
        })

    return pd.DataFrame(summaries)

def create_codebook():
    """Create codebook sheet."""
    codebook_data = [
        ['Study_ID', 'Unique study identifier', 'Integer (1-69)', 'Assigned during screening'],
        ['ES_ID', 'Effect size identifier', 'Format: StudyID_##', 'Assigned during extraction'],
        ['Title', 'Full study title', 'Text', 'Primary study'],
        ['Year', 'Publication year', '2023-2025', 'Primary study'],
        ['Authors', 'Study authors', 'Text', 'Primary study'],
        ['Outcome_Name', 'Name of outcome measure', 'Text', 'Primary study'],
        ['Outcome_Dimension', 'Category of outcome', 'Cognitive/Affective/Behavioral', 'Coded'],
        ['Blooms_Level', 'Bloom\'s taxonomy level', 'Remember/Understand/Apply/Analyze/Evaluate/Create', 'Coded'],
        ['n_Treatment', 'Treatment group sample size', 'Integer', 'Primary study'],
        ['n_Control', 'Control group sample size', 'Integer', 'Primary study'],
        ['M_Treatment', 'Treatment group mean', 'Numeric', 'Primary study'],
        ['SD_Treatment', 'Treatment group SD', 'Numeric', 'Primary study'],
        ['M_Control', 'Control group mean', 'Numeric', 'Primary study'],
        ['SD_Control', 'Control group SD', 'Numeric', 'Primary study'],
        ['Hedges_g', 'Hedges\' g effect size', 'Numeric (bias-corrected)', 'Calculated'],
        ['SE_g', 'Standard error of Hedges\' g', 'Numeric', 'Calculated'],
        ['Verification_Status', 'Data verification status', 'OCR_VERIFIED/MANUAL_VERIFIED/PARTIALLY_VERIFIED', 'Verification process'],
        ['Verification_Confidence', 'Confidence level (0-100%)', 'Numeric', 'Verification process'],
        ['Data_Tier', 'Data quality tier', '1=High/2=Medium/3=Low', 'Verification process'],
        ['Sample_Size', 'Total sample size', 'n_Treatment + n_Control', 'Calculated'],
        ['n_Effects', 'Number of effect sizes per study', 'Integer', 'Counted']
    ]

    return pd.DataFrame(codebook_data, columns=['Variable', 'Description', 'Values/Coding Rules', 'Source'])

def create_exclusion_log():
    """Create exclusion log sheet."""
    log_data = []
    for study_id, reason in EXCLUSION_REASONS.items():
        log_data.append({
            'Study_ID': study_id,
            'Exclusion_Reason': reason,
            'Review_Date': '2026-01-26',
            'Reviewer': 'Manual PDF Review'
        })
    return pd.DataFrame(log_data)

def run_basic_meta_analysis(df):
    """Run basic meta-analysis calculations."""
    results = {}

    # Overall effect
    g = df['hedges_g'].dropna()
    n1 = df['n_treatment'].dropna()
    n2 = df['n_control'].dropna()

    # Calculate variance weights
    se = np.sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))
    var = se**2
    weights = 1 / var

    # Weighted mean
    weighted_mean = np.sum(weights * g) / np.sum(weights)
    weighted_se = np.sqrt(1 / np.sum(weights))

    # 95% CI
    ci_lower = weighted_mean - 1.96 * weighted_se
    ci_upper = weighted_mean + 1.96 * weighted_se

    # Heterogeneity (Q statistic)
    q = np.sum(weights * (g - weighted_mean)**2)
    df_q = len(g) - 1

    # I-squared
    if q > df_q:
        i_squared = (q - df_q) / q * 100
    else:
        i_squared = 0

    results['overall'] = {
        'k_studies': df['study_id'].nunique(),
        'n_effects': len(g),
        'mean_g': weighted_mean,
        'se_g': weighted_se,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'q_statistic': q,
        'df': df_q,
        'i_squared': i_squared
    }

    return results

def save_excel_workbook(study_chars, effect_sizes, moderator_summary, codebook, exclusion_log, output_path):
    """Save all sheets to Excel workbook."""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        codebook.to_excel(writer, sheet_name='1_Codebook', index=False)
        study_chars.to_excel(writer, sheet_name='2_Study_Characteristics', index=False)
        effect_sizes.to_excel(writer, sheet_name='3_Effect_Sizes', index=False)
        moderator_summary.to_excel(writer, sheet_name='4_Moderator_Summary', index=False)
        exclusion_log.to_excel(writer, sheet_name='5_Exclusion_Log', index=False)

    print(f"\n✅ Saved Excel workbook: {output_path}")

def main():
    print("=" * 70)
    print("CREATING FINAL DATASET v4.0")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Load and exclude
    df = load_source_data()
    df_final = exclude_studies(df)

    # Create sheets
    print("\n=== Creating Excel Sheets ===")
    codebook = create_codebook()
    print(f"  1_Codebook: {len(codebook)} variables")

    study_chars = create_study_characteristics(df_final)
    print(f"  2_Study_Characteristics: {len(study_chars)} studies")

    effect_sizes = create_effect_sizes_sheet(df_final)
    print(f"  3_Effect_Sizes: {len(effect_sizes)} effect sizes")

    moderator_summary = create_moderator_summary(df_final)
    print(f"  4_Moderator_Summary: {len(moderator_summary)} categories")

    exclusion_log = create_exclusion_log()
    print(f"  5_Exclusion_Log: {len(exclusion_log)} excluded studies")

    # Save Excel
    save_excel_workbook(
        study_chars, effect_sizes, moderator_summary, codebook, exclusion_log,
        "GenAI_MetaAnalysis_FINAL_v4.xlsx"
    )

    # Save CSV
    effect_sizes.to_csv("GenAI_MetaAnalysis_Effects_FINAL_v4.csv", index=False)
    print(f"✅ Saved CSV: GenAI_MetaAnalysis_Effects_FINAL_v4.csv")

    # Run meta-analysis
    print("\n=== Meta-Analysis Results ===")
    results = run_basic_meta_analysis(df_final)
    overall = results['overall']

    print(f"\n  Overall Effect (Random Effects):")
    print(f"    k = {overall['k_studies']} studies")
    print(f"    n = {overall['n_effects']} effect sizes")
    print(f"    g = {overall['mean_g']:.3f} [{overall['ci_lower']:.3f}, {overall['ci_upper']:.3f}]")
    print(f"    Q({overall['df']}) = {overall['q_statistic']:.2f}")
    print(f"    I² = {overall['i_squared']:.1f}%")

    # Save meta-analysis results
    with open("meta_analysis_results_v4.json", 'w') as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\n✅ Saved meta-analysis results: meta_analysis_results_v4.json")

    # Summary
    print("\n" + "=" * 70)
    print("FINAL DATASET SUMMARY")
    print("=" * 70)
    print(f"  Studies included: {overall['k_studies']}")
    print(f"  Studies excluded: {len(EXCLUDED_STUDIES)}")
    print(f"  Effect sizes: {overall['n_effects']}")
    print(f"  Overall effect: g = {overall['mean_g']:.3f}")

    # By tier
    tier_counts = df_final.groupby('data_tier')['study_id'].nunique()
    print("\n  By Data Tier:")
    for tier in sorted(tier_counts.index):
        print(f"    Tier {tier}: {tier_counts[tier]} studies")

    return df_final, results

if __name__ == "__main__":
    main()
