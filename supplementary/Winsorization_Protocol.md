# Winsorization Protocol for Outlier Treatment

## GenAI Effectiveness in Higher Education Meta-Analysis

---

## 1. Rationale

Extreme effect sizes can disproportionately influence meta-analytic estimates. Following recommendations for meta-analysis with extreme values (Viechtbauer & Cheung, 2010), we applied winsorization rather than exclusion to preserve all studies while reducing undue influence of outliers.

## 2. Winsorization Criteria

### 2.1 Threshold Definition

| Parameter | Value | Justification |
|-----------|-------|---------------|
| **Upper Bound** | g = +3.0 | 99.7th percentile under normal distribution |
| **Lower Bound** | g = −3.0 | 0.3rd percentile under normal distribution |
| **Detection Method** | Absolute value > 3.0 | Symmetric treatment of positive and negative outliers |

### 2.2 Procedure

1. **Identification**: Effect sizes with |g| > 3.0 were flagged as potential outliers
2. **Verification**: Each flagged effect size was reviewed for data extraction accuracy
3. **Winsorization**: Confirmed outliers were replaced with the threshold value (±3.0)
4. **Documentation**: All winsorized values recorded in Appendix B

## 3. Outlier Identification Results

### 3.1 Distribution Summary (Pre-Winsorization)

| Statistic | Value |
|-----------|-------|
| Total effect sizes | 381 |
| Mean | 0.58 |
| Median | 0.52 |
| SD | 0.89 |
| Minimum | −2.45 |
| Maximum | 4.87 |
| Outliers identified | 14 |

### 3.2 Outliers Identified (|g| > 3.0)

| Study ID | Outcome ID | Original g | Winsorized g | Direction | Notes |
|----------|------------|------------|--------------|-----------|-------|
| 7 | 7-1 | 3.42 | 3.0 | Positive | Large behavioral effect |
| 7 | 7-2 | 3.28 | 3.0 | Positive | Large cognitive effect |
| 7 | 7-3 | 4.12 | 3.0 | Positive | Large cognitive effect |
| 7 | 7-4 | 3.67 | 3.0 | Positive | Large cognitive effect |
| 7 | 7-5 | 3.15 | 3.0 | Positive | Large behavioral effect |
| 7 | 7-6 | 4.87 | 3.0 | Positive | Largest effect in dataset |
| 23 | 23-8 | 3.21 | 3.0 | Positive | Medical education |
| 23 | 23-9 | 3.45 | 3.0 | Positive | Medical education |
| 23 | 23-10 | 3.08 | 3.0 | Positive | Medical education |
| 30 | 30-1 | 3.12 | 3.0 | Positive | Language learning |
| 30 | 30-2 | 3.54 | 3.0 | Positive | Language learning |
| 30 | 30-3 | 3.89 | 3.0 | Positive | Language learning |
| 39 | 39-1 | 3.35 | 3.0 | Positive | Programming education |
| 39 | 39-2 | 3.02 | 3.0 | Positive | Programming education |

**Note**: All outliers were positive (favoring GenAI), concentrated in 4 studies with notably large effects.

## 4. Sensitivity Analysis Results

### 4.1 Comparison of Analytic Approaches

| Approach | g | 95% CI | SE | p | Decision |
|----------|---|--------|----|----|----------|
| **Winsorized (Primary)** | 0.622 | [0.389, 0.855] | 0.119 | < .001 | Reported |
| Full dataset (no treatment) | 0.658 | [0.412, 0.904] | 0.125 | < .001 | Sensitivity |
| Outliers excluded | 0.598 | [0.371, 0.825] | 0.116 | < .001 | Sensitivity |

### 4.2 Interpretation

- **Effect on estimate**: Winsorization reduced the pooled effect by 0.036 (5.5%) compared to untreated data
- **Robustness**: Results remain significant and substantively similar across all approaches
- **Conclusion**: Outlier treatment does not meaningfully alter conclusions

## 5. Influence Diagnostics

### 5.1 Cook's Distance Analysis

| Study ID | Cook's D | Classification | Action |
|----------|----------|----------------|--------|
| 7 | 0.42 | Influential | Winsorized; results robust |
| 23 | 0.28 | Moderately influential | Winsorized; results robust |
| 30 | 0.19 | Moderately influential | Winsorized; results robust |
| 39 | 0.15 | Marginally influential | Winsorized; results robust |

**Threshold**: Cook's D > 4/n = 4/65 = 0.062

### 5.2 Leave-One-Out Analysis

After winsorization, leave-one-out analysis showed:
- **Range of estimates**: g = 0.598 to g = 0.648
- **Most influential study when removed**: Study 7 (Hong, 2025)
- **Estimate without Study 7**: g = 0.598, 95% CI [0.371, 0.825]

## 6. R Code for Winsorization

```r
# Winsorization function
winsorize_effect <- function(g, lower = -3.0, upper = 3.0) {
  pmax(pmin(g, upper), lower)
}

# Apply winsorization
data$hedges_g_winsorized <- winsorize_effect(data$hedges_g)

# Count winsorized values
n_winsorized <- sum(abs(data$hedges_g) > 3.0)
cat("Effect sizes winsorized:", n_winsorized, "\n")

# Compare models
model_original <- rma.mv(yi = hedges_g, V = se_g^2,
                          random = ~ 1 | study_id/outcome_id,
                          data = data)

model_winsorized <- rma.mv(yi = hedges_g_winsorized, V = se_g^2,
                            random = ~ 1 | study_id/outcome_id,
                            data = data)
```

## 7. Reporting Checklist

- [x] Winsorization threshold clearly specified (|g| > 3.0)
- [x] Number of winsorized values reported (n = 14)
- [x] Direction of outliers documented (all positive)
- [x] Studies containing outliers identified
- [x] Sensitivity analysis comparing approaches
- [x] Influence diagnostics reported
- [x] R code provided for reproducibility

---

## References

Viechtbauer, W., & Cheung, M. W. L. (2010). Outlier and influence diagnostics for meta-analysis. *Research Synthesis Methods*, 1(2), 112-125.

---

*Protocol Version 1.0 | Created: 2026-01-23*
