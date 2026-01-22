#!/usr/bin/env python3
"""
Create final integrated meta-analysis dataset
Combines existing 63 studies with 13 verified new studies
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
BASE_DIR = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness")
EXISTING_DATA = BASE_DIR / "Final/meta_analysis_HE_corrected.csv"
CORRECTED_DATA = BASE_DIR / "Generative-AI-in-Higher-Education/data/corrected_effect_sizes.csv"
OUTPUT_DIR = BASE_DIR / "Generative-AI-in-Higher-Education/data"

def calculate_hedges_g(d, n1, n2):
    """Calculate Hedges' g and SE from Cohen's d"""
    if pd.isna(d) or pd.isna(n1) or pd.isna(n2):
        return None, None
    n_total = n1 + n2
    df = n_total - 2
    j = 1 - (3 / (4 * df - 1))
    g = d * j
    se = np.sqrt((n_total / (n1 * n2)) + (g**2 / (2 * df)))
    return round(g, 4), round(se, 4)

def main():
    # Load existing data
    existing = pd.read_csv(EXISTING_DATA)
    print(f"Existing dataset: {existing['study_id'].nunique()} studies, {len(existing)} effect sizes")

    # Load corrected new studies
    new_studies = pd.read_csv(CORRECTED_DATA)
    new_studies = new_studies[new_studies['decision'] == 'include']
    print(f"New verified studies: {len(new_studies)}")

    # Create new entries in existing format
    new_entries = []
    for _, row in new_studies.iterrows():
        # Calculate Hedges' g if not provided
        if pd.isna(row.get('hedges_g')):
            g, se = calculate_hedges_g(row['cohens_d'], row['n_treatment'], row['n_control'])
        else:
            g, se = row['hedges_g'], row['se_g']

        entry = {
            'study_id': row['study_id'],
            'outcome_id': f"{int(row['study_id']):03d}_01",
            'title': row['title'],
            'year': row['year'],
            'authors': 'See manual_review_results.md',
            'outcome_name': 'Primary Outcome',
            'outcome_dimension': row['outcome_dimension'],
            'blooms_level': 'not_reported',
            'n_treatment': row['n_treatment'],
            'n_control': row['n_control'],
            'hedges_g': g,
            'se_g': se,
            'ci_lower': round(g - 1.96 * se, 4) if g and se else None,
            'ci_upper': round(g + 1.96 * se, 4) if g and se else None,
            'cohens_d': row['cohens_d'],
            'study_design': row['study_design'],
            'genai_tool': 'ChatGPT',
            'source': 'New Addition 2025',
            'extraction_confidence': 'high',
            'notes': row['notes'],
            'blooms_category': 'not_classified',
            'academic_level': 'mixed',
            'hedges_g_original': g
        }
        new_entries.append(entry)

    new_df = pd.DataFrame(new_entries)

    # Align columns
    for col in existing.columns:
        if col not in new_df.columns:
            new_df[col] = None

    new_df = new_df[existing.columns]

    # Combine datasets
    combined = pd.concat([existing, new_df], ignore_index=True)

    # Save final dataset
    final_path = OUTPUT_DIR / "meta_analysis_FINAL.csv"
    combined.to_csv(final_path, index=False)

    print(f"\n✅ Final dataset created: {final_path}")
    print(f"   Total studies: {combined['study_id'].nunique()}")
    print(f"   Total effect sizes: {len(combined)}")

    # Summary statistics
    print("\n📊 Effect Size Summary:")
    print(f"   Mean Hedges' g: {combined['hedges_g'].mean():.3f}")
    print(f"   Median Hedges' g: {combined['hedges_g'].median():.3f}")
    print(f"   SD: {combined['hedges_g'].std():.3f}")
    print(f"   Range: [{combined['hedges_g'].min():.3f}, {combined['hedges_g'].max():.3f}]")

    # By dimension
    print("\n📊 By Outcome Dimension:")
    for dim in combined['outcome_dimension'].dropna().unique():
        subset = combined[combined['outcome_dimension'] == dim]
        print(f"   {dim}: n={len(subset)}, g={subset['hedges_g'].mean():.3f}")

    # Save summary
    summary = {
        'total_studies': int(combined['study_id'].nunique()),
        'total_effect_sizes': len(combined),
        'mean_g': round(combined['hedges_g'].mean(), 3),
        'median_g': round(combined['hedges_g'].median(), 3),
        'sd_g': round(combined['hedges_g'].std(), 3),
        'new_studies_added': len(new_entries),
        'excluded_studies': 3
    }

    import json
    with open(OUTPUT_DIR / "final_dataset_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Summary saved to final_dataset_summary.json")

if __name__ == "__main__":
    main()
