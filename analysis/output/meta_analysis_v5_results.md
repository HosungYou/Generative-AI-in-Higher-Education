# Three-Level Meta-Analysis Results: GenAI in Higher Education (v5)

**Analysis Date:** 2025-01-26
**Dataset:** GenAI_MetaAnalysis_v5.csv
**Analysis Script:** three_level_meta_analysis.R

---

## Executive Summary

This three-level meta-analysis examines the effectiveness of Generative AI tools in higher education. The analysis uses a multilevel modeling approach to account for the dependency of multiple effect sizes nested within studies.

---

## Sample Characteristics

| Metric | Value |
|--------|-------|
| Total effect sizes (k) | 155 |
| Unique studies | 38 |
| Total participants | 18,691 |
| Dataset rows (including missing ES) | 346 |

**Note:** 61 unique study IDs exist in the dataset, but only 38 studies contributed valid effect sizes (with both Hedges' g and SE).

---

## Overall Effect Size

### Three-Level Random-Effects Model

| Statistic | Value |
|-----------|-------|
| **Hedges' g** | **0.770** |
| Standard Error | 0.167 |
| 95% CI | [0.439, 1.101] |
| t-value | 4.60 |
| p-value | < .0001 |

**Interpretation:** A medium-to-large positive effect (g = 0.77) indicating that GenAI interventions significantly improve learning outcomes compared to control conditions.

### Robust Variance Estimation (RVE)

| Statistic | Value |
|-----------|-------|
| Estimate | 0.77 |
| Robust SE | 0.167 |
| df (Satterthwaite) | 34.5 |
| p-value | < .001 |

---

## Heterogeneity

### Variance Decomposition

| Level | Variance (tau^2) | I^2 |
|-------|-----------------|-----|
| **Total** | - | **99.1%** |
| Level 2 (within-study) | 0.6972 | 45.7% |
| Level 3 (between-study) | 0.8137 | 53.4% |

**Interpretation:**
- Extremely high heterogeneity (I^2 = 99.1%) indicates substantial variability in effect sizes
- Heterogeneity is distributed fairly evenly between within-study (45.7%) and between-study (53.4%) levels
- This suggests meaningful variation both across different outcomes within studies and across different studies

### Test for Heterogeneity

| Statistic | Value |
|-----------|-------|
| Q | 3709.04 |
| df | 154 |
| p-value | < .0001 |

---

## Moderator Analyses

### Outcome Dimension

| Dimension | g | SE | 95% CI | p |
|-----------|---|----|----|---|
| **Affective** | 0.925 | 0.248 | [0.44, 1.41] | < .001 |
| **Cognitive** | 0.799 | 0.178 | [0.45, 1.15] | < .001 |
| Metacognitive | 0.578 | 0.343 | [-0.10, 1.25] | .092 |
| Behavioral | 0.198 | 0.349 | [-0.49, 0.88] | .571 |

**Test of Moderation:** QM(4) = 26.15, p < .0001

**Interpretation:** GenAI shows strongest effects on affective outcomes (g = 0.93), followed by cognitive outcomes (g = 0.80). Effects on behavioral outcomes are not statistically significant.

### Bloom's Taxonomy Analysis (k = 80)

| Category | g | SE | 95% CI | p |
|----------|---|----|----|---|
| **Higher-Order** (analyze, evaluate, create) | 1.061 | 0.282 | [0.51, 1.61] | < .001 |
| **Lower-Order** (remember, understand, apply) | 0.813 | 0.250 | [0.32, 1.30] | .001 |

**Counts:** Higher-order = 38 effects, Lower-order = 42 effects

**Interpretation:** GenAI interventions show larger effects on higher-order cognitive skills (g = 1.06) compared to lower-order skills (g = 0.81), though both are significant.

---

## Publication Bias Assessment

### Precision-Effect Test (PET)

| Statistic | Value |
|-----------|-------|
| PET Intercept | -1.011 |
| 95% CI | [-1.653, -0.369] |
| p-value | .002 |
| SE coefficient | 6.661 (p < .0001) |

### PEESE Results (triggered by significant PET slope)

| Statistic | Value |
|-----------|-------|
| Intercept | 0.241 |
| 95% CI | [-0.113, 0.595] |
| p-value | .182 |

**Interpretation:**
- Significant PET slope suggests potential publication bias
- PET intercept is negative (-1.01), which is unusual and may indicate model misspecification or funnel plot asymmetry
- PEESE adjusted estimate (0.24) is substantially smaller but not significant
- Caution warranted in interpreting the overall effect size due to publication bias indicators

---

## Sensitivity Analysis

### Leave-One-Out Analysis

| Metric | Value |
|--------|-------|
| Range of estimates | 0.682 - 0.816 |
| Most influential study | Study 8 |

**Interpretation:** The overall effect estimate is relatively robust, ranging from g = 0.68 to g = 0.82 when individual studies are removed. Study 8 has the largest influence on the pooled estimate.

---

## Output Files Generated

| File | Description |
|------|-------------|
| `forest_plot.png` | Forest plot of study-level effect sizes |
| `funnel_plot.png` | Funnel plot for publication bias visualization |
| `meta_analysis_results.rds` | R data object with full results |

---

## Comparison with v4 Dataset

| Metric | v4 | v5 | Change |
|--------|----|----|--------|
| Total rows | 346 | 346 | 0 |
| Valid effect sizes | 155 | 155 | 0 |
| Unique studies (in data) | 61 | 61 | 0 |
| Studies with valid ES | 38 | 38 | 0 |
| Max Study ID | 70 | 70 | 0 |

**Note:** The v4 and v5 datasets appear structurally identical. Study 70 (Yilmaz & Yilmaz 2023) with 3 effect sizes is present in both versions.

---

## Technical Notes

1. **Model Specification:** Three-level random-effects model with effect sizes nested within studies
2. **Estimation Method:** REML (Restricted Maximum Likelihood)
3. **Test Statistics:** t-distribution for inference
4. **Software:** R 4.5.2, metafor 4.8-0, clubSandwich (for RVE)

---

## Key Findings Summary

1. **Overall Effect:** GenAI interventions show a significant medium-to-large effect (g = 0.77, p < .0001)
2. **Heterogeneity:** Very high (I^2 = 99.1%), warranting moderator exploration
3. **Outcome Types:** Affective (g = 0.93) and cognitive (g = 0.80) outcomes benefit most
4. **Bloom's Taxonomy:** Larger effects for higher-order thinking (g = 1.06) vs. lower-order (g = 0.81)
5. **Publication Bias:** Evidence suggests potential bias; adjusted estimates may be smaller
6. **Robustness:** Leave-one-out analysis shows stable results (g = 0.68-0.82)
