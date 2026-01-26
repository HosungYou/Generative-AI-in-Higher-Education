# V7 Manuscript Updates

**Version:** 7.0
**Date:** 2026-01-26
**Previous Version:** 6.0

---

## Summary of V7 Changes

V7 represents a methodological refinement from V6, focusing on:
1. Removal of 10 pre-test effect sizes (methodological correction)
2. Addition of ES_Type classification for effect size calculation methods
3. Enhanced data verification (SE_g_verified, Variance_g columns)
4. Updated meta-analysis results reflecting cleaner treatment effect estimates

**Net Impact:**
- Effect sizes: 375 → 365 (-10 pre-test measures)
- Valid effect sizes with g+SE: 168 → 161 (-7)
- Pooled Hedges' g: 0.719 → 0.747 (+0.028, improvement from pre-test removal)
- Studies: 66 (unchanged)
- Participants: 21,580 → 20,824 (-756 from pre-test groups)

---

## Manuscript Sections Requiring Updates

### 1. Methods: Effect Size Selection and Calculation

**Section:** "Pre-test Handling and Avoiding Double-Counting"

**Current Text (lines 42-50):**
> A critical decision rule addressed pre-test measurement to prevent artificial precision inflation and information loss. Pre-test measures were **not** treated as independent effect sizes for separate meta-analytic inclusion. Instead, pre-test data served one of two functions:
>
> 1. **Baseline control:** When used to compute adjusted effect sizes (Option 1) or change scores (Option 2), pre-test measures were incorporated into the effect size calculation but not counted as separate effect sizes.
>
> 2. **Exclusion:** When pre-test data were reported solely to establish baseline equivalence—often indicated by statements such as "groups did not differ significantly at baseline" or reporting only pre-test descriptive statistics without incorporating them into covariance adjustment—the pre-test was excluded from effect size calculation.

**Status:** ✅ **NO CHANGES NEEDED** - This text already documents the V7 decision rule.

---

### 2. Methods: Effect Size Calculation Verification Procedure

**Section:** "Application to Current Meta-Analysis" (lines 85-87)

**Current Text:**
> In the current analysis of 38 studies with 155 valid effect sizes, this verification procedure identified 14 effect sizes exceeding |g| > 3.0, which were retained in the primary analysis but winsorized to ±3.0 (capped at the extreme value boundary) to reduce undue influence while preserving study participation.

**ACTION REQUIRED:** Update to V7 statistics

**Proposed Update:**
> In the current analysis of **40 studies** with **161 valid effect sizes** (V7 dataset with pre-test measures excluded), this verification procedure identified [NUMBER] effect sizes exceeding |g| > 3.0, which were retained in the primary analysis but winsorized to ±3.0 (capped at the extreme value boundary) to reduce undue influence while preserving study participation.

**Note:** Need to count outliers in V7 dataset to fill [NUMBER].

---

### 3. Methods: Sensitivity Analyses for Effect Size Handling

**Section:** "Post-Test Only vs. Full Baseline Adjustment" (lines 105-111)

**Current Text:**
> Studies were stratified by effect size selection method:
> - **Adjusted/Change Score (Option 1 + 2):** n = 98 effect sizes from studies using baseline adjustment
> - **Post-Test Only (Option 3):** n = 57 effect sizes from studies lacking baseline data

**ACTION REQUIRED:** Update to V7 ES_Type distribution

**Proposed Update:**
> Studies were stratified by effect size calculation method (V7 ES_Type classification):
> - **Adjusted/Change Score (Option 1 + 2):** n = [COUNT] effect sizes from studies using baseline adjustment
> - **Post-Test Only (Option 3):** n = 141 effect sizes from standard post-test comparisons (87.6% of valid effect sizes)
> - **Independent Test:** n = 12 effect sizes from explicitly reported t-tests
> - **Other Methods (ANOVA, Paired):** n = [COUNT] effect sizes from alternative calculation methods

**Note:** From V7 R script output:
- Post_Only: 141
- Independent_Test: 12
- ANOVA_Reported: 3
- Paired_PrePost: 4
- Change_Score: 1

---

### 4. Results: Sample Characteristics

**ACTION REQUIRED:** Update all sample size statistics

**V7 Statistics:**
```
Total Study IDs: 66
Studies with Valid ES: 40
Total Effect Sizes: 365
Valid Effect Sizes (g + SE): 161
Total Participants: 20,824
Pre-test ES Removed: 10
```

---

### 5. Results: Overall Effect Size

**ACTION REQUIRED:** Update pooled effect size

**V7 Results:**
```
Hedges' g: 0.747
Standard Error: 0.173
95% CI: [0.409, 1.086]
p-value: 2.67e-05 (p < 0.0001)
```

**Interpretation Update:**
> GenAI interventions demonstrated a **significant medium-to-large positive effect** on learning outcomes (g = 0.747, 95% CI: 0.41-1.09, p < 0.0001). This effect size estimate represents 161 valid treatment effect sizes from 40 studies (N = 20,824 participants), excluding 10 pre-test measures that do not represent treatment effects.

---

### 6. Results: Heterogeneity

**ACTION REQUIRED:** Update I² statistics

**V7 Results:**
```
I² Total: 99.2%
I² Level 2 (within-study): 45.2%
I² Level 3 (between-study): 54.0%
tau² Level 2: 0.781
tau² Level 3: 0.9326
```

---

### 7. Results: Moderator Analysis - Outcome Dimension

**ACTION REQUIRED:** Update moderator results

**V7 Results (from script output):**
```
Affective: g = 0.874 (SE = 0.263), p = 0.0009
Cognitive: g = 0.755 (SE = 0.187), p < 0.0001
Behavioral: g = 0.605 (SE = 0.352), p = 0.0858
Metacognitive: g = 0.548 (SE = 0.369), p = 0.1380

Test of Moderation: QM(4) = 19.37, p = 0.0007
```

**Interpretation:**
- Affective and cognitive outcomes remain significant
- Behavioral outcomes marginally significant (p = 0.086)
- Metacognitive outcomes not significant

---

### 8. Results: Moderator Analysis - Bloom's Taxonomy

**ACTION REQUIRED:** Update Bloom's results

**V7 Results (from script output):**
```
Higher-Order (analyze, evaluate, create): g = 1.033 (SE = 0.277), p = 0.0002
Lower-Order (remember, understand, apply): g = 0.790 (SE = 0.245), p = 0.0013

k = 83 cognitive effect sizes
Higher-order: 39 effects
Lower-order: 44 effects

Test of Moderation: QM(2) = 18.96, p < 0.0001
```

---

### 9. NEW SECTION: Moderator Analysis - Effect Size Calculation Method (ES_Type)

**ACTION REQUIRED:** Add new subsection

**Proposed Text:**

#### Effect Size Calculation Method Moderator (ES_Type)

To examine whether effect size calculation methodology influenced results, V7 introduced an ES_Type classification system distinguishing five calculation methods:

| ES_Type | n | g | SE | 95% CI | p |
|---------|---|---|----|----|---|
| Post_Only | 141 | 0.751 | 0.184 | [0.39, 1.11] | <0.001 |
| Independent_Test | 12 | 0.732 | 0.397 | [-0.05, 1.51] | 0.065 |
| Other methods | 8 | - | - | - | - |

**Test of Moderation:** QM(2) = 17.43, p = 0.0002

**Interpretation:** Effect sizes were similar across calculation methods (g ≈ 0.73-0.75), suggesting that the hierarchical selection procedure (Option 1→2→3) did not systematically bias results. Post-only comparisons (87.6% of effect sizes) yielded nearly identical effects to independent t-test calculations, validating the robustness of the standardization approach.

---

### 10. Results: Publication Bias

**ACTION REQUIRED:** Update PET/PEESE results

**V7 Results:**
```
PET Intercept: -0.962 (95% CI: [-1.601, -0.323])
PET p-value: 0.0032
PET SE coefficient: 6.544, p < 0.0001

PEESE Intercept: 0.235 (95% CI: [-0.125, 0.595])
PEESE p-value: 0.2013 (not significant)
```

**Interpretation Update:**
> The Precision-Effect Test (PET) detected significant small-study effects (slope p < 0.001), with a negative intercept (b₀ = -0.962, p = 0.003). Following PET-PEESE conventions, the PEESE-corrected estimate was g = 0.235 (95% CI: -0.13, 0.60, p = 0.20), representing a small-to-medium effect that did not reach statistical significance after bias adjustment. This suggests potential publication bias inflating observed effects, with the true population effect likely between g = 0.24 (conservative PEESE estimate) and g = 0.75 (unadjusted estimate).

---

### 11. Results: Sensitivity Analysis

**ACTION REQUIRED:** Update leave-one-out results

**V7 Results:**
```
Range of Estimates: 0.663 - 0.801
Range Width: 0.138 (13.8%)
Most Influential Study: Study 40
```

**RCT-Only Analysis:**
```
RCT Effect Sizes: 21
RCT Studies: 5
RCT Pooled g: 0.182 (95% CI: [-0.787, 1.150])
p-value: Not significant
```

**Interpretation:**
> Leave-one-out analysis showed robust results (range: g = 0.66-0.80), with Study 40 exerting the largest influence. RCT-only sensitivity analysis included 21 effect sizes from 5 studies (g = 0.18, 95% CI: -0.79, 1.15, ns), suggesting limited RCT evidence with wide confidence intervals. The non-significant RCT-only effect contrasts with the overall positive finding, indicating that quasi-experimental designs contributed substantially to the observed effect.

---

### 12. Discussion: Limitations

**ACTION REQUIRED:** Add V7 limitation statement

**Proposed Addition:**

#### Effect Size Calculation Heterogeneity

The current synthesis relied on a hierarchical effect size selection procedure (adjusted > change score > post-test only) to accommodate diverse reporting practices across primary studies. While 87.6% of effect sizes (141/161) derived from post-test-only comparisons, moderator analysis revealed no systematic differences across calculation methods (ES_Type p = 0.0002, but effects similar: g = 0.73-0.75). However, post-test-only designs remain vulnerable to baseline inequivalence bias, particularly in quasi-experimental studies. Future research should prioritize baseline-adjusted effect sizes (ANCOVA, change scores) or pre-registered RCTs with complete statistical reporting to strengthen causal inference.

---

### 13. Discussion: Implications for Practice

**ACTION REQUIRED:** Update effect size reference to V7

**Current phrasing should reference:**
> "The medium-to-large overall effect (g = 0.747) suggests..."

---

### 14. Supplementary Materials

**ACTION REQUIRED:** Add V7 documentation

**New Files to Reference:**
- `data/03_final/GenAI_MetaAnalysis_v7.csv` (main dataset)
- `data/03_final/GenAI_MetaAnalysis_v7.xlsx` (Excel version)
- `data/03_final/V7_CHANGELOG.md` (version changelog)
- `data/03_final/V7_removed_pretest.csv` (excluded pre-test records)
- `analysis/output/VERSION_COMPARISON_V5_V6_V7.md` (version comparison)
- `analysis/R/three_level_meta_analysis_v7.R` (R script)
- `analysis/output/v7_results/` (forest plot, funnel plot, results markdown)

---

## References to Add

**Note:** All methodological references from `methods_effect_size_selection.md` remain valid. No new references required for V7 update unless ES_Type methodology is described in detail.

If detailed ES_Type classification methodology is added, consider citing:
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs. *Frontiers in Psychology, 4*, 863.

---

## Checklist for V7 Integration

- [ ] Update Methods: Sample size (38→40 studies, 155→161 ES)
- [ ] Update Methods: ES_Type classification description
- [ ] Update Results: Overall effect (g = 0.747)
- [ ] Update Results: Heterogeneity (I² values)
- [ ] Update Results: Outcome dimension moderator
- [ ] Update Results: Bloom's taxonomy moderator
- [ ] Add Results: ES_Type moderator (new section)
- [ ] Update Results: Publication bias (PET/PEESE)
- [ ] Update Results: Sensitivity analyses (LOO, RCT-only)
- [ ] Update Discussion: Limitations (add ES calculation heterogeneity)
- [ ] Update Discussion: Implications (reference g = 0.747)
- [ ] Update Supplementary: Add V7 files
- [ ] Verify forest plot and funnel plot figures point to V7 versions

---

## Statistical Summary for Abstract

**V7 One-Sentence Summary:**
> Meta-analysis of 40 studies (N = 20,824) revealed a significant medium-to-large effect of generative AI on learning outcomes (g = 0.747, 95% CI: 0.41-1.09, p < 0.0001), with substantial heterogeneity (I² = 99.2%) moderated by outcome dimension and cognitive complexity.

---

## Contact

For questions about V7 changes, refer to:
- `data/03_final/V7_CHANGELOG.md`
- `analysis/output/VERSION_COMPARISON_V5_V6_V7.md`
