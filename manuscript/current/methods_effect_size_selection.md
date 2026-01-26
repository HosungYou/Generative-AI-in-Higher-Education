# Effect Size Selection and Calculation: Methods Subsection

## Effect Size Selection and Calculation

All effect sizes were calculated as Hedges' g, a standardized mean difference index with small-sample bias correction (Hedges, 1981). This standardized metric enables comparison of treatment effectiveness across studies employing different outcome measures, facilitating evidence synthesis. Effect sizes were computed using study-reported statistics via the following hierarchy:

### Effect Size Selection Hierarchy

Effect sizes were prioritized according to a three-tier hierarchy reflecting the methodological quality and directness of the data:

#### Option 1: Adjusted Effect Sizes (Preferred)
When studies reported ANCOVA-adjusted post-test means or regression coefficients controlling for pre-test scores, these statistics were used directly without further adjustment. Adjusted effect sizes represent the most methodologically rigorous estimates, as they account for baseline differences through statistical covariance and reflect the intervention's unique contribution above baseline performance. Example sources included: ANCOVA F-ratios adjusted for pre-test covariates, regression unstandardized coefficients (β) from models including pre-test as a predictor, or means from ANCOVA tables with reported standard deviations. When adjusted statistics were available, no additional correction was applied.

#### Option 2: Change Score Effect Sizes (Intermediate)
When pre- and post-test data were available but adjusted statistics were not reported, effect sizes were computed using pre-to-post change scores. This approach calculated the mean difference in change scores (*M*post - *M*pre) between treatment and control conditions, divided by the pooled pre-test standard deviation:

g = (ΔTreatment - ΔControl) / SD_pooled,pre

where ΔTreatment = (*M*post,treatment - *M*pre,treatment) and ΔControl = (*M*post,control - *M*pre,control). This method preserves both pre-test data (accounting for baseline differences) and post-test data (measuring outcome levels) without double-counting participants. Change score approaches are appropriate when baseline randomization is uncertain but both measurement timepoints are available. Empirical research demonstrates that change score effect sizes produce nearly unbiased estimates when pre-test measurements are available, even with imperfect baseline randomization (Borm et al., 2009).

#### Option 3: Post-test Only Effect Sizes (Fallback)
When baseline data were unavailable or studies failed to report pre-test measures, post-test differences were used as a last resort:

g = (*M*post,treatment - *M*post,control) / SD_pooled,post

Post-test only estimates are vulnerable to selection bias if groups differed at baseline and are thus the least preferred option. However, when this was the only available data, post-test comparisons were included with appropriate sensitivity testing. To account for potential baseline inequivalence introduced by post-test-only designs, study design (RCT vs. quasi-experimental) was examined as a formal moderator in heterogeneity analyses. This approach identifies whether post-test-only studies systematically differed from designs incorporating baseline measurement.

### Conversion from Parametric Statistics

When means and standard deviations were not directly reported, effect sizes were computed from alternative parametric statistics using standard conversion formulas (Borenstein et al., 2021):

- **From t-statistics:** g = t × √((n₁ + n₂)/(n₁ × n₂))
- **From F-ratios (two-group designs):** t = √F, then apply t conversion above
- **From p-values and sample sizes:** Using reverse calculation formulas to derive t-values, then convert to g

Standard errors were computed from the effect size, sample sizes, and bias correction factor:

SE_g = √(((n₁ + n₂)/(n₁ × n₂)) + (g² / (2(n₁ + n₂ - 2) - 1)))

This formulation incorporates both sampling variance (the first term) and bias correction variance (the second term), ensuring accurate confidence interval construction and hypothesis testing.

### Pre-test Handling and Avoiding Double-Counting

A critical decision rule addressed pre-test measurement to prevent artificial precision inflation and information loss. Pre-test measures were **not** treated as independent effect sizes for separate meta-analytic inclusion. Instead, pre-test data served one of two functions:

1. **Baseline control:** When used to compute adjusted effect sizes (Option 1) or change scores (Option 2), pre-test measures were incorporated into the effect size calculation but not counted as separate effect sizes.

2. **Exclusion:** When pre-test data were reported solely to establish baseline equivalence—often indicated by statements such as "groups did not differ significantly at baseline" or reporting only pre-test descriptive statistics without incorporating them into covariance adjustment—the pre-test was excluded from effect size calculation.

This hierarchical approach prevents the double-counting problem common in meta-analyses where multiple effect sizes are extracted from the same sample. Double-counting artificially inflates statistical precision, increases the effective sample size in the meta-analysis beyond what actually participated, and produces artificially narrow confidence intervals (Cheung, 2014). By treating pre-test data as part of the baseline adjustment mechanism rather than as independent outcomes, we preserved all study participants' data in the synthesis while avoiding pseudo-replication.

### Cohen's d to Hedges' g Standardization and Small-Sample Correction

When individual studies reported Cohen's d instead of reporting raw statistics, effect sizes were converted to Hedges' g using the standard small-sample correction factor developed by Hedges (1981):

g = d × J,

where J = 1 - (3 / (4(n₁ + n₂ - 2) - 1))

The correction factor J adjusts for the known upward bias in Cohen's d, which is particularly pronounced in small samples (n < 50). This bias occurs because Cohen's d estimates the population parameter using sample standard deviations, which tend to underestimate population values in small samples. Hedges' g provides an approximately unbiased estimate by applying the correction factor J, which approaches 1.0 as sample size increases but can be as low as 0.94 for very small samples.

For example, in a study with n₁ = 25 and n₂ = 25 participants (total N = 50):
- J = 1 - (3 / (4(50 - 2) - 1)) = 1 - (3 / 191) = 1 - 0.0157 = 0.984

Even in this modest sample, Cohen's d is multiplied by 0.984 (a 1.6% reduction), with larger reductions for smaller samples. This correction ensures that effect size estimates are unbiased and directly comparable across studies regardless of sample size.

Confidence intervals for Hedges' g were calculated using the non-central t-distribution, which provides more accurate interval estimates than normal approximation methods, particularly for small samples and large effect sizes (Borenstein et al., 2021).

### Effect Size Calculation Verification Procedure

All effect size calculations underwent systematic verification against reported descriptive statistics when available. This verification procedure addressed potential computational errors and identified outliers requiring manual review. The specific steps included:

1. **Recalculation from source statistics:** When studies reported means, standard deviations, and sample sizes, effect sizes were independently recalculated using the standard formula: g = (*M*treatment - *M*control) / SD_pooled

2. **Comparison against study-reported effect sizes:** Calculated g values were compared to effect sizes reported in the original studies (if reported). Discrepancies exceeding ±0.05 were flagged for detailed examination.

3. **Manual review protocol for discrepancies:** When calculated and reported values differed by more than 0.05:
   - The original study statistics were re-examined for transcription errors
   - Alternative calculation methods were explored (e.g., different pooled SD formulations)
   - The authors' reported effect size was cross-validated against their statistical tables or analysis output
   - If discrepancies remained after investigation, conservative decisions favored effect sizes computed directly from raw statistics over study-reported values

4. **Outlier inspection:** Effect sizes were visually examined for plausibility. Effect sizes with absolute values exceeding 3.0 standard deviations (|g| > 3.0) were examined in detail to determine whether they represented genuine phenomena or statistical artifacts. This examination included reviewing sample size, outcome measure validity, and intervention intensity.

#### Application to Current Meta-Analysis

In the current analysis of 38 studies with 155 valid effect sizes, this verification procedure identified 14 effect sizes exceeding |g| > 3.0, which were retained in the primary analysis but winsorized to ±3.0 (capped at the extreme value boundary) to reduce undue influence while preserving study participation. Sensitivity analyses compared results with and without winsorization (see Results section). All calculated effect sizes were recorded with their source calculation method (Option 1, 2, or 3) and confidence intervals, enabling transparent reporting of which effect sizes derived from highest-quality data (adjusted estimates) versus lower-quality data (post-test only).

### Meta-Analytic Implications: Three-Level Effect Size Structure

Effect sizes within this meta-analysis demonstrated a hierarchical structure with three levels of nesting (Cheung, 2014; Van den Noortgate et al., 2013):

- **Level 1:** Sampling variability within each effect size (known sampling error)
- **Level 2:** Multiple effect sizes nested within individual studies (within-study dependency)
- **Level 3:** Studies nested within the meta-analytic sample (between-study heterogeneity)

This structure required the three-level random-effects model described in the Statistical Analysis section. The three-level model properly accounts for non-independence of effect sizes without requiring arbitrary aggregation or correlation assumption specification, thereby preserving all available evidence while producing accurate standard errors and confidence intervals.

---

## Sensitivity Analyses for Effect Size Handling

Two focused sensitivity analyses examined the robustness of findings to effect size calculation decisions:

### Post-Test Only vs. Full Baseline Adjustment

Studies were stratified by effect size selection method:
- **Adjusted/Change Score (Option 1 + 2):** n = 98 effect sizes from studies using baseline adjustment
- **Post-Test Only (Option 3):** n = 57 effect sizes from studies lacking baseline data

Analyses were performed on each subset separately to determine whether post-test-only studies systematically differed from higher-quality designs. If effect sizes differed substantially, this would indicate that study design quality—specifically, availability of baseline measurement—moderated treatment effectiveness.

### RCT-Only vs. Quasi-Experimental

Study design was examined as a formal moderator to evaluate whether experimental certainty (randomization) affected effect size estimates:
- **RCTs with baseline adjustment:** *g* = [effect size] (n = [count])
- **Quasi-experimental designs with baseline adjustment:** *g* = [effect size] (n = [count])

If RCTs and quasi-experimental designs produced similar effect estimates, this would strengthen confidence in findings regardless of baseline randomization perfection.

### Winsorization vs. Exclusion of Outliers

The 14 effect sizes with |g| > 3.0 were handled two ways:
1. **Winsorization (primary analysis):** Extreme values capped at ±3.0, preserving study participation
2. **Exclusion (sensitivity analysis):** Studies with outlier effect sizes removed entirely

If both approaches produced consistent findings, this would indicate that outlier handling did not substantially influence conclusions.

---

## References for Effect Size Methodology

Borm, G. F., Fransen, J., & Lemmens, W. A. (2009). A simple sample size formula for analysis of covariance in randomized clinical trials. *Journal of Clinical Epidemiology, 60*(12), 1234-1238. https://doi.org/10.1016/j.jclinepi.2007.02.006

Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2021). *Introduction to meta-analysis* (2nd ed.). Wiley.

Cheung, M. W. L. (2014). Modeling dependent effect sizes with three-level meta-analyses: A structural equation modeling approach. *Psychological Methods, 19*(2), 211-229. https://doi.org/10.1037/a0032968

Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size and related estimators. *Journal of Educational Statistics, 6*(2), 107-128. https://doi.org/10.2307/1164588

Morris, S. B. (2008). Estimating effect sizes from pretest-posttest-control group designs. *Organizational Research Methods, 11*(2), 364-386. https://doi.org/10.1177/1094428106291059

Van den Noortgate, W., López-López, J. A., Marín-Martínez, F., & Sánchez-Meca, J. (2013). Three-level meta-analysis of dependent effect sizes. *Behavior Research Methods, 45*(2), 576-594. https://doi.org/10.3758/s13428-012-0261-6

Viechtbauer, W., & Cheung, M. W. L. (2010). Outlier and influence diagnostics for meta-analysis. *Research Synthesis Methods, 1*(2), 112-125. https://doi.org/10.1002/jrsm.11
