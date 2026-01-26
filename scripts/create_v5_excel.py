#!/usr/bin/env python3
"""
Create GenAI_MetaAnalysis_v5.xlsx with 4-sheet codebook structure.

Sheets:
1. 1_Codebook - Variable definitions and coding rules
2. 2_Study_Characteristics - One row per study (k studies)
3. 3_Effect_Sizes - One row per effect size (from v5 CSV)
4. 4_Moderator_Summary - Summary statistics by moderator categories
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
BASE_DIR = Path("/Volumes/External SSD/Projects/GenAI-HE-Review-AIMC")
V5_CSV = BASE_DIR / "data/03_final/GenAI_MetaAnalysis_v5.csv"
CODEBOOK_XLSX = BASE_DIR / "data/GenAI_MetaAnalysis_Coding_Data.xlsx"
OUTPUT_XLSX = BASE_DIR / "data/03_final/GenAI_MetaAnalysis_v5.xlsx"

def load_data():
    """Load v5 CSV and existing codebook."""
    v5_data = pd.read_csv(V5_CSV)
    codebook_sheets = pd.read_excel(CODEBOOK_XLSX, sheet_name=None)
    return v5_data, codebook_sheets

def create_codebook_sheet(existing_codebook):
    """Create 1_Codebook sheet with variable definitions."""
    # Use existing codebook, add any new v5-specific variables
    codebook = existing_codebook['1_Codebook'].copy()

    # Add v5-specific variables if not present
    v5_vars = [
        {'Variable': 'Verification_Status',
         'Description': 'Verification status of effect size data',
         'Values/Coding Rules': 'OCR_VERIFIED, MANUAL_VERIFIED, PARTIALLY_VERIFIED, NOT_CHECKED',
         'Source': 'Verification pipeline'},
        {'Variable': 'Verification_Confidence',
         'Description': 'Confidence percentage in verification',
         'Values/Coding Rules': 'Numeric (0-100)',
         'Source': 'Verification pipeline'},
        {'Variable': 'Data_Tier',
         'Description': 'Data quality tier',
         'Values/Coding Rules': '1=verified, 2=partially verified, 3=not checked',
         'Source': 'Quality assessment'}
    ]

    existing_vars = set(codebook['Variable'].values)
    for var in v5_vars:
        if var['Variable'] not in existing_vars:
            codebook = pd.concat([codebook, pd.DataFrame([var])], ignore_index=True)

    return codebook

def create_study_characteristics(v5_data):
    """Create 2_Study_Characteristics sheet - one row per study."""
    # Group by Study_ID to get unique studies
    study_chars = v5_data.groupby('Study_ID').agg({
        'Title': 'first',
        'Year': 'first',
        'Authors': 'first',
        'ES_ID': 'count'  # n_Effects
    }).reset_index()

    study_chars.columns = ['Study_ID', 'Title', 'Year', 'Authors', 'n_Effects']

    # Calculate total sample size per study (max of treatment + control)
    sample_sizes = v5_data.groupby('Study_ID').apply(
        lambda x: (x['n_Treatment'].fillna(0) + x['n_Control'].fillna(0)).max()
    ).reset_index(name='Sample_Size')

    study_chars = study_chars.merge(sample_sizes, on='Study_ID')

    # Add placeholder columns matching codebook structure
    study_chars['Study_Design'] = ''
    study_chars['GenAI_Tool'] = ''
    study_chars['Database_Source'] = ''
    study_chars['DOI'] = ''

    # Reorder columns to match codebook
    column_order = ['Study_ID', 'Title', 'Year', 'Authors', 'Study_Design',
                    'GenAI_Tool', 'Database_Source', 'DOI', 'Sample_Size', 'n_Effects']
    study_chars = study_chars[column_order]

    return study_chars

def create_effect_sizes_sheet(v5_data):
    """Create 3_Effect_Sizes sheet with all effect sizes."""
    # Map v5 columns to codebook structure
    effect_sizes = v5_data.copy()

    # Add missing columns from codebook with NA values
    codebook_columns = [
        'Study_ID', 'ES_ID', 'Title', 'Year', 'Authors', 'Outcome_Name',
        'Outcome_Dimension', 'Blooms_Level', 'n_Treatment', 'n_Control',
        'M_Treatment', 'SD_Treatment', 'M_Control', 'SD_Control',
        'Hedges_g', 'SE_g', 'CI_Lower', 'CI_Upper', 'Cohens_d',
        't_value', 'F_value', 'p_value', 'Effect_Source', 'Extraction_Method',
        'Extraction_Confidence', 'Study_Design', 'GenAI_Tool', 'Measure_Type',
        'Measure_Instrument', 'Verification_Status', 'Verification_Confidence', 'Data_Tier'
    ]

    for col in codebook_columns:
        if col not in effect_sizes.columns:
            effect_sizes[col] = np.nan

    # Calculate CI if Hedges_g and SE_g are available
    mask = effect_sizes['Hedges_g'].notna() & effect_sizes['SE_g'].notna()
    effect_sizes.loc[mask, 'CI_Lower'] = effect_sizes.loc[mask, 'Hedges_g'] - 1.96 * effect_sizes.loc[mask, 'SE_g']
    effect_sizes.loc[mask, 'CI_Upper'] = effect_sizes.loc[mask, 'Hedges_g'] + 1.96 * effect_sizes.loc[mask, 'SE_g']

    # Reorder columns
    final_columns = [c for c in codebook_columns if c in effect_sizes.columns]
    effect_sizes = effect_sizes[final_columns]

    return effect_sizes

def create_moderator_summary(v5_data):
    """Create 4_Moderator_Summary sheet with summary statistics."""
    summaries = []

    # Filter to only rows with valid Hedges_g
    valid_data = v5_data[v5_data['Hedges_g'].notna()].copy()

    # Moderator: Outcome_Dimension
    for dim in valid_data['Outcome_Dimension'].dropna().unique():
        subset = valid_data[valid_data['Outcome_Dimension'] == dim]
        if len(subset) > 0:
            summaries.append({
                'Moderator': 'Outcome_Dimension',
                'Category': dim,
                'k_Studies': subset['Study_ID'].nunique(),
                'n_Effects': len(subset),
                'Mean_g': subset['Hedges_g'].mean(),
                'SD_g': subset['Hedges_g'].std(),
                'Min_g': subset['Hedges_g'].min(),
                'Max_g': subset['Hedges_g'].max()
            })

    # Moderator: Blooms_Level
    for level in valid_data['Blooms_Level'].dropna().unique():
        subset = valid_data[valid_data['Blooms_Level'] == level]
        if len(subset) > 0:
            summaries.append({
                'Moderator': 'Blooms_Level',
                'Category': level,
                'k_Studies': subset['Study_ID'].nunique(),
                'n_Effects': len(subset),
                'Mean_g': subset['Hedges_g'].mean(),
                'SD_g': subset['Hedges_g'].std(),
                'Min_g': subset['Hedges_g'].min(),
                'Max_g': subset['Hedges_g'].max()
            })

    # Moderator: Verification_Status
    for status in valid_data['Verification_Status'].dropna().unique():
        subset = valid_data[valid_data['Verification_Status'] == status]
        if len(subset) > 0:
            summaries.append({
                'Moderator': 'Verification_Status',
                'Category': status,
                'k_Studies': subset['Study_ID'].nunique(),
                'n_Effects': len(subset),
                'Mean_g': subset['Hedges_g'].mean(),
                'SD_g': subset['Hedges_g'].std(),
                'Min_g': subset['Hedges_g'].min(),
                'Max_g': subset['Hedges_g'].max()
            })

    # Moderator: Data_Tier
    for tier in valid_data['Data_Tier'].dropna().unique():
        subset = valid_data[valid_data['Data_Tier'] == tier]
        if len(subset) > 0:
            summaries.append({
                'Moderator': 'Data_Tier',
                'Category': f'Tier_{int(tier)}',
                'k_Studies': subset['Study_ID'].nunique(),
                'n_Effects': len(subset),
                'Mean_g': subset['Hedges_g'].mean(),
                'SD_g': subset['Hedges_g'].std(),
                'Min_g': subset['Hedges_g'].min(),
                'Max_g': subset['Hedges_g'].max()
            })

    # Overall summary
    summaries.append({
        'Moderator': 'Overall',
        'Category': 'All Studies',
        'k_Studies': valid_data['Study_ID'].nunique(),
        'n_Effects': len(valid_data),
        'Mean_g': valid_data['Hedges_g'].mean(),
        'SD_g': valid_data['Hedges_g'].std(),
        'Min_g': valid_data['Hedges_g'].min(),
        'Max_g': valid_data['Hedges_g'].max()
    })

    return pd.DataFrame(summaries)

def main():
    print("Loading data...")
    v5_data, codebook_sheets = load_data()
    print(f"  V5 data: {len(v5_data)} effect sizes from {v5_data['Study_ID'].nunique()} studies")

    print("\nCreating 4-sheet Excel workbook...")

    # Create sheets
    sheet_1_codebook = create_codebook_sheet(codebook_sheets)
    print(f"  1_Codebook: {len(sheet_1_codebook)} variables")

    sheet_2_studies = create_study_characteristics(v5_data)
    print(f"  2_Study_Characteristics: {len(sheet_2_studies)} studies")

    sheet_3_effects = create_effect_sizes_sheet(v5_data)
    print(f"  3_Effect_Sizes: {len(sheet_3_effects)} effect sizes")

    sheet_4_moderators = create_moderator_summary(v5_data)
    print(f"  4_Moderator_Summary: {len(sheet_4_moderators)} categories")

    # Write to Excel
    print(f"\nWriting to {OUTPUT_XLSX}...")
    with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
        sheet_1_codebook.to_excel(writer, sheet_name='1_Codebook', index=False)
        sheet_2_studies.to_excel(writer, sheet_name='2_Study_Characteristics', index=False)
        sheet_3_effects.to_excel(writer, sheet_name='3_Effect_Sizes', index=False)
        sheet_4_moderators.to_excel(writer, sheet_name='4_Moderator_Summary', index=False)

    print("Done!")

    # Verification
    print("\n=== Verification ===")
    verify = pd.ExcelFile(OUTPUT_XLSX)
    for sheet in verify.sheet_names:
        df = pd.read_excel(verify, sheet_name=sheet)
        print(f"  {sheet}: {df.shape[0]} rows, {df.shape[1]} columns")

if __name__ == "__main__":
    main()
