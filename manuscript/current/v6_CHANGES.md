# V6 Analysis Changes Summary

**Date:** 2026-01-26
**Analysis Script:** three_level_meta_analysis_v6.R
**Dataset:** GenAI_MetaAnalysis_v6.csv

---

## V5 vs V6 Comparison

| Metric | V5 | V6 | Change |
|--------|----|----|--------|
| **Dataset** | | | |
| Total Study IDs | 61 | 66 | +5 |
| Total effect sizes (rows) | 346 | 375 | +29 |
| Valid effect sizes (with g & SE) | 155 | 168 | +13 |
| Studies with valid ES | 38 | 41 | +3 |
| Total participants | 18,691 | 21,580 | +2,889 |
| **Overall Effect** | | | |
| Hedges' g | 0.770 | 0.719 | -0.051 |
| Standard Error | 0.167 | 0.169 | +0.002 |
| 95% CI Lower | 0.439 | 0.389 | -0.050 |
| 95% CI Upper | 1.101 | 1.050 | -0.051 |
| p-value | < .0001 | < .0001 | (same) |
| **Heterogeneity** | | | |
| I^2 Total | 99.1% | 99.2% | +0.1% |
| tau^2 Level 2 (within-study) | 0.697 | 0.749 | +0.052 |
| tau^2 Level 3 (between-study) | 0.814 | 0.980 | +0.166 |
| I^2 Level 2 | 45.7% | 42.9% | -2.8% |
| I^2 Level 3 | 53.4% | 56.2% | +2.8% |
| **Sensitivity** | | | |
| LOO Range Min | 0.682 | 0.642 | -0.040 |
| LOO Range Max | 0.816 | 0.772 | -0.044 |
| Most Influential Study | 8 | 40 | changed |

---

## Study Changes

### Confirmed Exclusions (4 studies)
These Study IDs were confirmed as NOT in the V5/V6 datasets:
- Study 9
- Study 18
- Study 39
- Study 61

### Recovered Studies (5 studies)
New studies added to V5 that are now in V6:
- Study 10: Differential Effects of GPT-Based Tools on Comprehension
- Study 17: Exploring the Role of AI Technology in Shaping College Students' English Writing Development
- Study 20: How Students Use AI Feedback Matters
- Study 51: (details in dataset)
- Study 56: (details in dataset)

---

## Moderator Analysis Updates (V6)

### Outcome Dimension

| Dimension | g (V6) | SE | 95% CI | p |
|-----------|--------|-------|---------|------|
| Affective | 0.913 | 0.261 | [0.40, 1.42] | < .001 |
| Behavioral | 0.678 | 0.346 | [0.00, 1.36] | .050 |
| Cognitive | 0.699 | 0.183 | [0.34, 1.06] | < .001 |
| Metacognitive | 0.513 | 0.371 | [-0.21, 1.24] | .167 |

Test of Moderation: QM(4) = 19.07, p = .0008

### Bloom's Taxonomy (k = 86)

| Category | g (V6) | SE | 95% CI | p |
|----------|--------|-------|---------|------|
| Higher-Order | 0.989 | 0.269 | [0.46, 1.52] | < .001 |
| Lower-Order | 0.736 | 0.236 | [0.27, 1.20] | .002 |

### Publication Bias

| Test | V5 | V6 |
|------|----|----|
| PET Intercept | -1.011 | -1.084 |
| PET 95% CI | [-1.65, -0.37] | [-1.72, -0.45] |
| PEESE Estimate | 0.241 | 0.202 |
| PEESE 95% CI | [-0.11, 0.60] | [-0.15, 0.56] |

**Note:** PET slope significant (p < .0001), indicating potential publication bias.

### RCT-Only Sensitivity

| Metric | V6 |
|--------|-----|
| RCT effect sizes | 22 |
| RCT studies | 5 |
| Pooled g | 0.114 |
| 95% CI | [-0.79, 1.02] |

---

## Key Interpretation

1. **Overall effect remains significant and positive** (g = 0.72, p < .0001)
   - Slightly smaller than V5 (g = 0.77) but within expected variation
   - Effect size still represents a medium-to-large positive effect

2. **Cognitive dependency hypothesis still supported**
   - Metacognitive outcomes: g = 0.51, non-significant (p = .167)
   - Affective outcomes: g = 0.91, significant (p < .001)
   - Cognitive outcomes: g = 0.70, significant (p < .001)

3. **Increased heterogeneity**
   - More between-study variance (56.2% vs 53.4%)
   - Suggests greater variation across different study contexts

4. **Publication bias concerns persist**
   - PET intercept negative and significant
   - PEESE-adjusted estimate (g = 0.20) substantially smaller

5. **RCT-only analysis is notably weaker**
   - Only 5 RCT studies with valid ES
   - Non-significant pooled effect (g = 0.11)
   - Suggests quasi-experimental designs may inflate estimates

---

## Files Updated

1. `data/03_final/GenAI_MetaAnalysis_v6.csv` - V6 dataset
2. `analysis/R/three_level_meta_analysis_v6.R` - V6 analysis script
3. `analysis/output/v6_results/` - All V6 outputs:
   - `forest_plot_v6.png`
   - `funnel_plot_v6.png`
   - `meta_analysis_v6_results.rds`
   - `meta_analysis_v6_results.md`

---

## Manuscript Update Recommendations

The following values should be updated in the manuscript:

### Abstract
- "38 studies with valid effect sizes (*k* = 155 effect sizes; *N* = 18,691 participants)"
  -> "41 studies with valid effect sizes (*k* = 168 effect sizes; *N* = 21,580 participants)"
- "*g* = 0.770, 95% CI [0.439, 1.101]"
  -> "*g* = 0.719, 95% CI [0.389, 1.050]"

### Results Section
- Update Overall Effect: g = 0.770 -> g = 0.719
- Update CI: [0.439, 1.101] -> [0.389, 1.050]
- Update sample sizes: 155 -> 168 ES, 38 -> 41 studies, 18,691 -> 21,580 participants
- Update heterogeneity: tau2_L2 = 0.697 -> 0.749, tau2_L3 = 0.814 -> 0.980

### Tables
- Table 3: Update tau2 and I2 values
- Table 4-6: Update moderator results

**Note:** The cognitive dependency hypothesis conclusion remains supported - metacognitive outcomes still show smallest, non-significant effect.
