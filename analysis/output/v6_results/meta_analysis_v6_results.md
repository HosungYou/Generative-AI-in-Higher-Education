# Three-Level Meta-Analysis Results: GenAI in Higher Education (V6)

**Analysis Date:** 2026-01-26 17:36:10 
**Dataset:** GenAI_MetaAnalysis_v6.csv
**Analysis Script:** three_level_meta_analysis_v6.R

---

## Executive Summary

This V6 analysis confirms the exclusion of 4 studies (IDs: 9, 18, 39, 61) and includes 5 recovered studies (IDs: 10, 17, 20, 51, 56). The analysis uses a three-level multilevel modeling approach to account for multiple effect sizes nested within studies.

---

## Sample Characteristics

| Metric | Value |
|--------|-------|
| Total Study IDs | 66 |
| Studies with valid ES | 41 |
| Total effect sizes | 375 |
| Valid effect sizes | 168 |
| Total participants | 21580 |
| Excluded Study IDs | 9, 18, 39, 61 |
| Recovered Study IDs | 10, 17, 20, 51, 56 |

---

## Overall Effect Size

### Three-Level Random-Effects Model

| Statistic | Value |
|-----------|-------|
| **Hedges' g** | **0.719** |
| Standard Error | 0.169 |
| 95% CI | [0.389, 1.05] |
| p-value | 3.31e-05 |

---

## Heterogeneity

| Level | tau^2 | I^2 |
|-------|-------|-----|
| **Total** | - | **99.2%** |
| Level 2 (within-study) | 0.7486 | 42.9% |
| Level 3 (between-study) | 0.9804 | 56.2% |

---

## Sensitivity Analysis

### Leave-One-Out Analysis

| Metric | Value |
|--------|-------|
| Range of estimates | 0.642 - 0.772 |
| Most influential study | Study 40 |

---

## Output Files Generated

| File | Description |
|------|-------------|
| `forest_plot_v6.png` | Forest plot of study-level effect sizes |
| `funnel_plot_v6.png` | Funnel plot for publication bias visualization |
| `meta_analysis_v6_results.rds` | R data object with full results |
| `meta_analysis_v6_results.md` | This summary file |

