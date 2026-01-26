# Three-Level Meta-Analysis Results: GenAI in Higher Education (V7)

**Analysis Date:** 2026-01-26 18:33:32 
**Dataset:** GenAI_MetaAnalysis_v7.csv
**Analysis Script:** three_level_meta_analysis_v7.R

---

## Executive Summary

This V7 analysis includes methodological improvements from V6:
- Removed 10 pre-test effect sizes (methodological correction)
- Added ES_Type classification for effect size calculation methods
- Added verified SE and variance columns
- V7 dataset: 365 effect sizes from 66 studies

The analysis uses a three-level multilevel modeling approach to account for multiple effect sizes nested within studies.

---

## Sample Characteristics

| Metric | Value |
|--------|-------|
| Total Study IDs | 66 |
| Studies with valid ES | 40 |
| Total effect sizes | 365 |
| Valid effect sizes | 161 |
| Total participants | 20824 |
| Pre-test ES removed | 10 |

---

## Overall Effect Size

### Three-Level Random-Effects Model

| Statistic | Value |
|-----------|-------|
| **Hedges' g** | **0.747** |
| Standard Error | 0.173 |
| 95% CI | [0.409, 1.086] |
| p-value | 2.67e-05 |

---

## Heterogeneity

| Level | tau^2 | I^2 |
|-------|-------|-----|
| **Total** | - | **99.2%** |
| Level 2 (within-study) | 0.781 | 45.2% |
| Level 3 (between-study) | 0.9326 | 54% |

---

## Sensitivity Analysis

### Leave-One-Out Analysis

| Metric | Value |
|--------|-------|
| Range of estimates | 0.663 - 0.801 |
| Most influential study | Study 40 |

---

## Output Files Generated

| File | Description |
|------|-------------|
| `forest_plot_v7.png` | Forest plot of study-level effect sizes |
| `funnel_plot_v7.png` | Funnel plot for publication bias visualization |
| `meta_analysis_v7_results.rds` | R data object with full results |
| `meta_analysis_v7_results.md` | This summary file |

