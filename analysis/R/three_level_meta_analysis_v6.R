# ============================================================================
# Three-Level Meta-Analysis: GenAI Effectiveness in Higher Education (V6)
# ============================================================================
# Author: Hosung You
# Affiliation: College of Education, Pennsylvania State University
# Date: January 2026
# Version: 6.0
# Changes from V5:
#   - Confirmed exclusion of 4 studies (IDs: 9, 18, 39, 61)
#   - 66 studies, 375 effect sizes total
#   - Recovered 5 studies (IDs: 10, 17, 20, 51, 56)
# ============================================================================

# Load required packages
library(metafor)
library(clubSandwich)
library(ggplot2)
library(dplyr)

# ============================================================================
# 1. DATA PREPARATION
# ============================================================================

# Load the V6 dataset (confirmed exclusions)
data <- read.csv("../../data/03_final/GenAI_MetaAnalysis_v6.csv")

# Normalize column names to lowercase for consistency
names(data) <- tolower(names(data))

# Create outcome_id from es_id for three-level nesting
data$outcome_id <- data$es_id

# Filter to valid effect sizes (with both g and SE)
data_valid <- data %>%
  filter(!is.na(hedges_g) & !is.na(se_g))

cat(rep("=", 70), "\n", sep="")
cat("V6 META-ANALYSIS: DATA SUMMARY\n")
cat(rep("=", 70), "\n", sep="")
cat("Dataset version: V6 (2025-01-26)\n")
cat("Total rows in dataset:", nrow(data), "\n")
cat("Valid effect sizes (with g and SE):", nrow(data_valid), "\n")
cat("Unique studies (total):", length(unique(data$study_id)), "\n")
cat("Unique studies (valid ES only):", length(unique(data_valid$study_id)), "\n")
cat("Total participants:", sum(data_valid$n_treatment, na.rm=TRUE) +
                           sum(data_valid$n_control, na.rm=TRUE), "\n")
cat("Excluded Study IDs: 9, 18, 39, 61 (not in dataset)\n")

# ============================================================================
# 2. THREE-LEVEL RANDOM-EFFECTS MODEL
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("THREE-LEVEL RANDOM-EFFECTS META-ANALYSIS\n")
cat(rep("=", 70), "\n", sep="")

# Fit three-level model
# Level 1: Sampling variance (known)
# Level 2: Within-study variance (outcomes within studies)
# Level 3: Between-study variance

model_3level <- rma.mv(
  yi = hedges_g,           # Effect size
  V = se_g^2,              # Sampling variance
  random = ~ 1 | study_id/outcome_id,  # Nested random effects
  data = data_valid,
  method = "REML",         # Restricted maximum likelihood
  test = "t"               # Use t-distribution for tests
)

# Print model results
print(summary(model_3level))

# Calculate I^2 for each level
W <- diag(1/data_valid$se_g^2)
X <- model.matrix(model_3level)
P <- W - W %*% X %*% solve(t(X) %*% W %*% X) %*% t(X) %*% W
sigma2_1 <- model_3level$sigma2[1]  # Level 2 variance
sigma2_2 <- model_3level$sigma2[2]  # Level 3 variance
typical_v <- sum(diag(P)) / sum(P^2)  # Typical sampling variance

I2_total <- 100 * (sigma2_1 + sigma2_2) / (sigma2_1 + sigma2_2 + typical_v)
I2_level2 <- 100 * sigma2_1 / (sigma2_1 + sigma2_2 + typical_v)
I2_level3 <- 100 * sigma2_2 / (sigma2_1 + sigma2_2 + typical_v)

cat("\nHETEROGENEITY DECOMPOSITION:\n")
cat("I^2 Total:", round(I2_total, 1), "%\n")
cat("I^2 Level 2 (within-study):", round(I2_level2, 1), "%\n")
cat("I^2 Level 3 (between-study):", round(I2_level3, 1), "%\n")
cat("tau^2 Level 2:", round(sigma2_1, 4), "\n")
cat("tau^2 Level 3:", round(sigma2_2, 4), "\n")

# ============================================================================
# 3. ROBUST VARIANCE ESTIMATION
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("ROBUST VARIANCE ESTIMATION (RVE)\n")
cat(rep("=", 70), "\n", sep="")

# Apply cluster-robust standard errors
rve_results <- coef_test(model_3level, vcov = "CR2", cluster = data_valid$study_id)
print(rve_results)

# ============================================================================
# 4. MODERATOR ANALYSES
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("MODERATOR ANALYSIS: OUTCOME DIMENSION\n")
cat(rep("=", 70), "\n", sep="")

# Fit model with outcome dimension as moderator
model_dimension <- rma.mv(
  yi = hedges_g,
  V = se_g^2,
  mods = ~ outcome_dimension - 1,  # Remove intercept for group means
  random = ~ 1 | study_id/outcome_id,
  data = data_valid,
  method = "REML"
)

print(summary(model_dimension))

# Test for moderation
model_null <- rma.mv(
  yi = hedges_g,
  V = se_g^2,
  random = ~ 1 | study_id/outcome_id,
  data = data_valid,
  method = "REML"
)

anova_result <- anova(model_null, model_dimension)
print(anova_result)

# ============================================================================
# 5. BLOOM'S TAXONOMY ANALYSIS
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("MODERATOR ANALYSIS: BLOOM'S TAXONOMY\n")
cat(rep("=", 70), "\n", sep="")

# Create Bloom's category from blooms_level
# Lower order: remember, understand, apply
# Higher order: analyze, evaluate, create
data_valid <- data_valid %>%
  mutate(blooms_category = case_when(
    blooms_level %in% c("remember", "understand", "apply") ~ "lower_order",
    blooms_level %in% c("analyze", "evaluate", "create") ~ "higher_order",
    TRUE ~ NA_character_
  ))

# Filter to classified cognitive outcomes
data_blooms <- data_valid %>%
  filter(!is.na(blooms_category))

cat("\nBlooms classification counts:\n")
print(table(data_blooms$blooms_category))

if(nrow(data_blooms) > 10) {
  model_blooms <- rma.mv(
    yi = hedges_g,
    V = se_g^2,
    mods = ~ blooms_category - 1,
    random = ~ 1 | study_id/outcome_id,
    data = data_blooms,
    method = "REML"
  )
  print(summary(model_blooms))
}

# ============================================================================
# 6. ADDITIONAL MODERATOR ANALYSES
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("ADDITIONAL MODERATOR ANALYSES\n")
cat(rep("=", 70), "\n", sep="")

# GenAI Tool moderator (if available)
if("genai_tool" %in% names(data_valid)) {
  cat("\n--- GenAI Tool Moderator ---\n")
  cat("Tool distribution:\n")
  print(table(data_valid$genai_tool, useNA = "ifany"))

  # Filter to studies with known tool
  data_tool <- data_valid %>%
    filter(!is.na(genai_tool) & genai_tool != "not_reported")

  if(nrow(data_tool) > 10 && length(unique(data_tool$genai_tool)) > 1) {
    model_tool <- rma.mv(
      yi = hedges_g,
      V = se_g^2,
      mods = ~ genai_tool - 1,
      random = ~ 1 | study_id/outcome_id,
      data = data_tool,
      method = "REML"
    )
    print(summary(model_tool))
  }
}

# Study Design moderator (if available)
if("study_design" %in% names(data_valid)) {
  cat("\n--- Study Design Moderator ---\n")
  cat("Design distribution:\n")
  print(table(data_valid$study_design, useNA = "ifany"))

  data_design <- data_valid %>%
    filter(!is.na(study_design) & study_design != "not_reported")

  if(nrow(data_design) > 10 && length(unique(data_design$study_design)) > 1) {
    model_design <- rma.mv(
      yi = hedges_g,
      V = se_g^2,
      mods = ~ study_design - 1,
      random = ~ 1 | study_id/outcome_id,
      data = data_design,
      method = "REML"
    )
    print(summary(model_design))
  }
}

# ============================================================================
# 7. PUBLICATION BIAS ASSESSMENT
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("PUBLICATION BIAS ASSESSMENT\n")
cat(rep("=", 70), "\n", sep="")

# Egger's regression test (using precision as predictor)
# PET: Regress effect size on SE
pet_model <- rma.mv(
  yi = hedges_g,
  V = se_g^2,
  mods = ~ se_g,
  random = ~ 1 | study_id/outcome_id,
  data = data_valid,
  method = "REML"
)

cat("\nPrecision-Effect Test (PET):\n")
print(summary(pet_model))

# Extract PET intercept (effect when SE = 0)
pet_intercept <- coef(pet_model)[1]
pet_se <- sqrt(vcov(pet_model)[1,1])
pet_ci_lower <- pet_intercept - 1.96 * pet_se
pet_ci_upper <- pet_intercept + 1.96 * pet_se

cat("\nPET Intercept:", round(pet_intercept, 3), "\n")
cat("95% CI: [", round(pet_ci_lower, 3), ", ", round(pet_ci_upper, 3), "]\n")

# PEESE: If PET is significant, use SE^2
if(summary(pet_model)$pval[2] < 0.10) {
  peese_model <- rma.mv(
    yi = hedges_g,
    V = se_g^2,
    mods = ~ I(se_g^2),
    random = ~ 1 | study_id/outcome_id,
    data = data_valid,
    method = "REML"
  )
  cat("\nPEESE Results (PET slope significant):\n")
  print(summary(peese_model))

  peese_intercept <- coef(peese_model)[1]
  peese_se <- sqrt(vcov(peese_model)[1,1])
  cat("\nPEESE Adjusted Estimate:", round(peese_intercept, 3), "\n")
  cat("95% CI: [", round(peese_intercept - 1.96*peese_se, 3), ", ",
      round(peese_intercept + 1.96*peese_se, 3), "]\n")
}

# ============================================================================
# 8. SENSITIVITY ANALYSES
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("SENSITIVITY ANALYSES\n")
cat(rep("=", 70), "\n", sep="")

# Leave-one-out analysis at study level
studies <- unique(data_valid$study_id)
loo_results <- data.frame(
  study_removed = studies,
  estimate = NA,
  se = NA
)

for(i in seq_along(studies)) {
  subset_data <- data_valid %>% filter(study_id != studies[i])
  loo_model <- rma.mv(
    yi = hedges_g,
    V = se_g^2,
    random = ~ 1 | study_id/outcome_id,
    data = subset_data,
    method = "REML"
  )
  loo_results$estimate[i] <- coef(loo_model)
  loo_results$se[i] <- sqrt(vcov(loo_model))
}

cat("\nLeave-One-Out Analysis:\n")
cat("Range of estimates:", round(min(loo_results$estimate), 3), "to",
    round(max(loo_results$estimate), 3), "\n")
cat("Most influential study when removed:",
    studies[which.max(abs(loo_results$estimate - coef(model_3level)))], "\n")

# RCT-only sensitivity analysis
if("study_design" %in% names(data_valid)) {
  data_rct <- data_valid %>% filter(tolower(study_design) == "rct")
  if(nrow(data_rct) > 5) {
    cat("\n--- RCT-Only Sensitivity Analysis ---\n")
    cat("RCT effect sizes:", nrow(data_rct), "\n")
    cat("RCT studies:", length(unique(data_rct$study_id)), "\n")

    model_rct <- rma.mv(
      yi = hedges_g,
      V = se_g^2,
      random = ~ 1 | study_id/outcome_id,
      data = data_rct,
      method = "REML"
    )
    cat("RCT-only pooled g:", round(coef(model_rct), 3), "\n")
    cat("95% CI: [", round(coef(model_rct) - 1.96*sqrt(vcov(model_rct)), 3), ", ",
        round(coef(model_rct) + 1.96*sqrt(vcov(model_rct)), 3), "]\n")
  }
}

# ============================================================================
# 9. FOREST PLOT
# ============================================================================

cat("\n", rep("=", 70), "\n", sep="")
cat("GENERATING VISUALIZATIONS\n")
cat(rep("=", 70), "\n", sep="")

# Aggregate to study level for forest plot
study_summary <- data_valid %>%
  group_by(study_id) %>%
  summarize(
    mean_g = mean(hedges_g),
    se_g = sqrt(mean(se_g^2)),
    n_effects = n(),
    title = first(title)
  ) %>%
  arrange(mean_g)

# Create forest plot
png("../output/v6_results/forest_plot_v6.png", width = 12, height = max(8, nrow(study_summary) * 0.3),
    units = "in", res = 150)

forest_data <- data.frame(
  study = paste0("Study ", study_summary$study_id),
  yi = study_summary$mean_g,
  sei = study_summary$se_g
)

forest(
  x = forest_data$yi,
  sei = forest_data$sei,
  slab = forest_data$study,
  xlim = c(-4, 5),
  xlab = "Hedges' g",
  main = "Forest Plot: GenAI Effects on Learning Outcomes in Higher Education (V6)"
)

# Add pooled effect
abline(v = coef(model_3level), lty = 2, col = "red", lwd = 2)
text(coef(model_3level), -1, paste0("Pooled g = ", round(coef(model_3level), 3)),
     col = "red", pos = 4)

dev.off()

cat("Forest plot saved to: ../output/v6_results/forest_plot_v6.png\n")

# ============================================================================
# 10. FUNNEL PLOT
# ============================================================================

png("../output/v6_results/funnel_plot_v6.png", width = 10, height = 8, units = "in", res = 150)

plot(data_valid$hedges_g, data_valid$se_g,
     xlim = c(-4, 5),
     ylim = c(max(data_valid$se_g) * 1.1, 0),
     xlab = "Hedges' g",
     ylab = "Standard Error",
     main = "Funnel Plot: Publication Bias Assessment (V6)",
     pch = 19, col = rgb(0.2, 0.4, 0.6, 0.6))

abline(v = coef(model_3level), lty = 2, col = "red", lwd = 2)
abline(v = 0, lty = 1, col = "black")

# Add pseudo 95% CI
se_range <- seq(0, max(data_valid$se_g) * 1.1, length.out = 100)
ci_lower <- coef(model_3level) - 1.96 * se_range
ci_upper <- coef(model_3level) + 1.96 * se_range
lines(ci_lower, se_range, lty = 3, col = "gray")
lines(ci_upper, se_range, lty = 3, col = "gray")

legend("topright",
       legend = c(paste0("Pooled g = ", round(coef(model_3level), 3)),
                  "95% Pseudo CI"),
       lty = c(2, 3), col = c("red", "gray"), lwd = c(2, 1))

dev.off()

cat("Funnel plot saved to: ../output/v6_results/funnel_plot_v6.png\n")

# ============================================================================
# 11. SAVE RESULTS
# ============================================================================

results_summary <- list(
  version = "V6",
  analysis_date = Sys.time(),
  overall_effect = list(
    estimate = coef(model_3level),
    se = sqrt(vcov(model_3level)),
    ci_lower = coef(model_3level) - 1.96 * sqrt(vcov(model_3level)),
    ci_upper = coef(model_3level) + 1.96 * sqrt(vcov(model_3level)),
    p_value = summary(model_3level)$pval
  ),
  heterogeneity = list(
    I2_total = I2_total,
    I2_level2 = I2_level2,
    I2_level3 = I2_level3,
    tau2_level2 = sigma2_1,
    tau2_level3 = sigma2_2
  ),
  publication_bias = list(
    pet_intercept = pet_intercept,
    pet_ci = c(pet_ci_lower, pet_ci_upper)
  ),
  sample_info = list(
    n_studies_total = length(unique(data$study_id)),
    n_studies_valid = length(unique(data_valid$study_id)),
    n_effects_total = nrow(data),
    n_effects_valid = nrow(data_valid),
    n_participants = sum(data_valid$n_treatment, na.rm=TRUE) +
                     sum(data_valid$n_control, na.rm=TRUE)
  ),
  sensitivity = list(
    loo_range = c(min(loo_results$estimate), max(loo_results$estimate)),
    most_influential_study = studies[which.max(abs(loo_results$estimate - coef(model_3level)))]
  )
)

saveRDS(results_summary, "../output/v6_results/meta_analysis_v6_results.rds")

# ============================================================================
# 12. GENERATE MARKDOWN SUMMARY
# ============================================================================

sink("../output/v6_results/meta_analysis_v6_results.md")

cat("# Three-Level Meta-Analysis Results: GenAI in Higher Education (V6)\n\n")
cat("**Analysis Date:**", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
cat("**Dataset:** GenAI_MetaAnalysis_v6.csv\n")
cat("**Analysis Script:** three_level_meta_analysis_v6.R\n\n")

cat("---\n\n")

cat("## Executive Summary\n\n")
cat("This V6 analysis confirms the exclusion of 4 studies (IDs: 9, 18, 39, 61) and includes 5 recovered studies (IDs: 10, 17, 20, 51, 56). The analysis uses a three-level multilevel modeling approach to account for multiple effect sizes nested within studies.\n\n")

cat("---\n\n")

cat("## Sample Characteristics\n\n")
cat("| Metric | Value |\n")
cat("|--------|-------|\n")
cat("| Total Study IDs | ", length(unique(data$study_id)), " |\n", sep="")
cat("| Studies with valid ES | ", length(unique(data_valid$study_id)), " |\n", sep="")
cat("| Total effect sizes | ", nrow(data), " |\n", sep="")
cat("| Valid effect sizes | ", nrow(data_valid), " |\n", sep="")
cat("| Total participants | ", sum(data_valid$n_treatment, na.rm=TRUE) + sum(data_valid$n_control, na.rm=TRUE), " |\n", sep="")
cat("| Excluded Study IDs | 9, 18, 39, 61 |\n")
cat("| Recovered Study IDs | 10, 17, 20, 51, 56 |\n\n")

cat("---\n\n")

cat("## Overall Effect Size\n\n")
cat("### Three-Level Random-Effects Model\n\n")
cat("| Statistic | Value |\n")
cat("|-----------|-------|\n")
cat("| **Hedges' g** | **", round(coef(model_3level), 3), "** |\n", sep="")
cat("| Standard Error | ", round(sqrt(vcov(model_3level)), 3), " |\n", sep="")
cat("| 95% CI | [", round(coef(model_3level) - 1.96*sqrt(vcov(model_3level)), 3), ", ",
    round(coef(model_3level) + 1.96*sqrt(vcov(model_3level)), 3), "] |\n", sep="")
cat("| p-value | ", format(summary(model_3level)$pval, scientific = TRUE, digits = 3), " |\n\n", sep="")

cat("---\n\n")

cat("## Heterogeneity\n\n")
cat("| Level | tau^2 | I^2 |\n")
cat("|-------|-------|-----|\n")
cat("| **Total** | - | **", round(I2_total, 1), "%** |\n", sep="")
cat("| Level 2 (within-study) | ", round(sigma2_1, 4), " | ", round(I2_level2, 1), "% |\n", sep="")
cat("| Level 3 (between-study) | ", round(sigma2_2, 4), " | ", round(I2_level3, 1), "% |\n\n", sep="")

cat("---\n\n")

cat("## Sensitivity Analysis\n\n")
cat("### Leave-One-Out Analysis\n\n")
cat("| Metric | Value |\n")
cat("|--------|-------|\n")
cat("| Range of estimates | ", round(min(loo_results$estimate), 3), " - ", round(max(loo_results$estimate), 3), " |\n", sep="")
cat("| Most influential study | Study ", studies[which.max(abs(loo_results$estimate - coef(model_3level)))], " |\n\n", sep="")

cat("---\n\n")

cat("## Output Files Generated\n\n")
cat("| File | Description |\n")
cat("|------|-------------|\n")
cat("| `forest_plot_v6.png` | Forest plot of study-level effect sizes |\n")
cat("| `funnel_plot_v6.png` | Funnel plot for publication bias visualization |\n")
cat("| `meta_analysis_v6_results.rds` | R data object with full results |\n")
cat("| `meta_analysis_v6_results.md` | This summary file |\n\n")

sink()

cat("\nMarkdown summary saved to: ../output/v6_results/meta_analysis_v6_results.md\n")

cat("\n", rep("=", 70), "\n", sep="")
cat("V6 ANALYSIS COMPLETE\n")
cat(rep("=", 70), "\n", sep="")
cat("Results saved to: ../output/v6_results/\n")
