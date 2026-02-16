# V7 Changelog - GenAI Meta-Analysis Data

**Version**: 7.0
**Date**: 2026-01-26
**Previous Version**: 6.0

---

## Summary Statistics

| Metric | V6 | V7 | Change |
|--------|----|----|--------|
| Total Effect Sizes | 375 | 365 | -10 |
| Unique Studies | 66 | 66 | 0 |
| Valid Hedges_g | ~210 | 210 | - |
| Missing Hedges_g | ~165 | 155 | - |

---

## Changes in V7

### 1. Pre-test Effect Sizes Removed (10 records)

Pre-test measures were removed as they do not represent treatment effects. The following effect sizes were excluded:

| Study_ID | ES_ID | Outcome_Name | Hedges_g |
|----------|-------|--------------|----------|
| 1 | 001_01 | Pre-test | -0.1055 |
| 3 | 003_01 | Academic Writing Achievement Pre-Test | 0.0364 |
| 26 | 026_01 | Thermodynamics Knowledge - Pretest | -0.0444 |
| 34 | 034_01 | Academic Performance - Pre-Training | 0.5405 |
| 34 | 034_03 | Moral Behavior Level - Pre-Training | 2.9848 |
| 34 | 034_05 | Self-Efficacy - Pre-Training | 3.9797 |
| 50 | 050_01 | Baseline SDLS Score | NaN |
| 50 | 050_02 | Baseline CCTS Score | NaN |
| 50 | 050_03 | Baseline GFS Score | NaN |
| 60 | 060_01 | Academic Writing Pre-test | -0.2624 |

**Removal Criteria**: Outcome names containing:
- Pre-test, Pretest, Pre test
- Pre-Training, Pre-training
- Baseline

**Note**: Original estimate was 22 pre-test effect sizes. After refined pattern matching to avoid false positives (e.g., "comprehension" was incorrectly flagged), 10 true pre-test measures were identified and removed.

---

### 2. Hedges' g Verification

All Hedges' g values were verified using the standard formula:

```
Cohen's d = (M_Treatment - M_Control) / Pooled_SD
J = 1 - (3 / (4 * (n1 + n2 - 2) - 1))  # Hedges correction
Hedges_g = d * J
```

**Results**:
- 170 effect sizes had sufficient data for verification
- 159 matched original values (diff < 0.01)
- 11 discrepancies identified (likely due to different calculation methods in original studies)

**Discrepancies Noted** (for transparency, values retained from V6):
- Studies 6, 16, 26, 37, 49 showed minor differences
- Likely causes: Different pooled SD formulas, adjusted means, or extracted from figures

---

### 3. ES_Type Classification Added

New column `ES_Type` classifies effect size calculation method:

| ES_Type | Count | Description |
|---------|-------|-------------|
| Post_Only | 330 | Standard post-test comparison |
| Change_Score | 16 | Pre-post difference scores |
| Independent_Test | 12 | Explicitly reported t-test |
| Paired_PrePost | 4 | Within-group paired comparison |
| ANOVA_Reported | 3 | ANOVA-based effect size |

**Classification Logic**:
- `Adjusted`: Contains "ancova", "adjusted", "covariate"
- `Change_Score`: Contains "change", "gain", "improvement", "difference"
- `Paired_PrePost`: Contains "paired"
- `Independent_Test`: Contains "independent" or "t-test"
- `ANOVA_Reported`: Contains "anova"
- `Post_Only`: Default (standard post-test comparison)

---

### 4. SE and Variance Columns Added

New columns for meta-analysis:

- `SE_g_verified`: Standard error calculated from formula:
  ```
  SE_g = sqrt((n1 + n2)/(n1 * n2) + g^2/(2*(n1 + n2)))
  ```
- `Variance_g`: SE_g_verified squared

**Verification**: All 161 calculable SE values matched original `SE_g` within 0.01 tolerance.

---

### 5. Version Metadata

New columns added:
- `Data_Version`: "v7"
- `Version_Date`: "2026-01-26"

---

## Column Structure (V7)

| Column | Description |
|--------|-------------|
| Study_ID | Unique study identifier |
| ES_ID | Effect size identifier |
| Title | Study title |
| Year | Publication year |
| Authors | Author list |
| Outcome_Name | Specific outcome measured |
| Outcome_Dimension | cognitive/affective/behavioral/metacognitive |
| **ES_Type** | **NEW: Effect size type classification** |
| Blooms_Level | Bloom's taxonomy level |
| n_Treatment | Treatment group sample size |
| n_Control | Control group sample size |
| M_Treatment | Treatment group mean |
| SD_Treatment | Treatment group SD |
| M_Control | Control group mean |
| SD_Control | Control group SD |
| Hedges_g | Effect size (Hedges' g) |
| SE_g | Original standard error |
| **SE_g_verified** | **NEW: Verified SE calculation** |
| **Variance_g** | **NEW: Variance of effect size** |
| Verification_Status | Data verification status |
| Verification_Confidence | Confidence level |
| Data_Tier | Data quality tier |
| GenAI_Tool | AI tool used in study |
| Study_Design | Research design |
| **Data_Version** | **NEW: Version identifier** |
| **Version_Date** | **NEW: Version date** |

---

## Outcome Dimension Distribution (V7)

| Dimension | Count | Percentage |
|-----------|-------|------------|
| cognitive | 224 | 61.4% |
| affective | 78 | 21.4% |
| metacognitive | 30 | 8.2% |
| behavioral | 26 | 7.1% |
| missing | 7 | 1.9% |

---

## Files Generated

| File | Description |
|------|-------------|
| `GenAI_MetaAnalysis_v7.csv` | Main V7 dataset (CSV) |
| `GenAI_MetaAnalysis_v7.xlsx` | Main V7 dataset (Excel) |
| `V7_removed_pretest.csv` | Removed pre-test records |
| `V7_CHANGELOG.md` | This changelog |

---

## Recommendations for Analysis

1. **Use `Hedges_g` column** for meta-analysis (already bias-corrected)
2. **Filter by `ES_Type`** if analyzing specific methodologies
3. **Use `SE_g_verified`** for weighting calculations
4. **Check `Outcome_Dimension`** for moderator analyses
5. **Note**: 155 effect sizes have missing Hedges_g due to insufficient raw data

---

## Contact

For questions about this dataset, refer to the main project documentation.
