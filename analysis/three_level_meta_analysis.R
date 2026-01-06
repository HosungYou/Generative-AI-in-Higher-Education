# ============================================================================
# Three-Level Meta-Analysis: GenAI Effectiveness in Higher Education
# ============================================================================
# Author: Hosung You
# Affiliation: College of Education, Pennsylvania State University
# Date: January 2025
# ============================================================================

# Load required packages
library(metafor)
library(clubSandwich)
library(ggplot2)
library(dplyr)

# ============================================================================
# 1. DATA PREPARATION
# ============================================================================

# Load the corrected dataset
data <- read.csv("../data/processed/meta_analysis_HE_corrected.csv")

# Filter to valid effect sizes (with both g and SE)
data_valid <- data %>%
  filter(!is.na(hedges_g) & !is.na(se_g))

cat("="*60, "\n")
cat("DATA SUMMARY\n")
cat("="*60, "\n")
cat("Total effect sizes:", nrow(data_valid), "\n")
cat("Unique studies:", length(unique(data_valid$study_id)), "\n")
cat("Total participants:", sum(data_valid$n_treatment, na.rm=TRUE) +
                           sum(data_valid$n_control, na.rm=TRUE), "\n")

# ============================================================================
# 2. THREE-LEVEL RANDOM-EFFECTS MODEL
# ============================================================================

cat("\n", "="*60, "\n")
cat("THREE-LEVEL RANDOM-EFFECTS META-ANALYSIS\n")
cat("="*60, "\n")

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

# Calculate I² for each level
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
cat("I² Total:", round(I2_total, 1), "%\n")
cat("I² Level 2 (within-study):", round(I2_level2, 1), "%\n")
cat("I² Level 3 (between-study):", round(I2_level3, 1), "%\n")
cat("τ² Level 2:", round(sigma2_1, 4), "\n")
cat("τ² Level 3:", round(sigma2_2, 4), "\n")

# ============================================================================
# 3. ROBUST VARIANCE ESTIMATION
# ============================================================================

cat("\n", "="*60, "\n")
cat("ROBUST VARIANCE ESTIMATION (RVE)\n")
cat("="*60, "\n")

# Apply cluster-robust standard errors
rve_results <- coef_test(model_3level, vcov = "CR2", cluster = data_valid$study_id)
print(rve_results)

# ============================================================================
# 4. MODERATOR ANALYSES
# ============================================================================

cat("\n", "="*60, "\n")
cat("MODERATOR ANALYSIS: OUTCOME DIMENSION\n")
cat("="*60, "\n")

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

cat("\n", "="*60, "\n")
cat("MODERATOR ANALYSIS: BLOOM'S TAXONOMY\n")
cat("="*60, "\n")

# Filter to classified cognitive outcomes
data_blooms <- data_valid %>%
  filter(blooms_category %in% c("lower_order", "higher_order"))

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
# 6. PUBLICATION BIAS ASSESSMENT
# ============================================================================

cat("\n", "="*60, "\n")
cat("PUBLICATION BIAS ASSESSMENT\n")
cat("="*60, "\n")

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
}

# ============================================================================
# 7. SENSITIVITY ANALYSES
# ============================================================================

cat("\n", "="*60, "\n")
cat("SENSITIVITY ANALYSES\n")
cat("="*60, "\n")

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

# ============================================================================
# 8. FOREST PLOT
# ============================================================================

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
png("../output/forest_plot.png", width = 12, height = max(8, nrow(study_summary) * 0.3),
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
  main = "Forest Plot: GenAI Effects on Learning Outcomes in Higher Education"
)

# Add pooled effect
abline(v = coef(model_3level), lty = 2, col = "red", lwd = 2)
text(coef(model_3level), -1, paste0("Pooled g = ", round(coef(model_3level), 3)),
     col = "red", pos = 4)

dev.off()

cat("\nForest plot saved to: ../output/forest_plot.png\n")

# ============================================================================
# 9. FUNNEL PLOT
# ============================================================================

png("../output/funnel_plot.png", width = 10, height = 8, units = "in", res = 150)

plot(data_valid$hedges_g, data_valid$se_g,
     xlim = c(-4, 5),
     ylim = c(max(data_valid$se_g) * 1.1, 0),
     xlab = "Hedges' g",
     ylab = "Standard Error",
     main = "Funnel Plot: Publication Bias Assessment",
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

cat("Funnel plot saved to: ../output/funnel_plot.png\n")

# ============================================================================
# 10. SAVE RESULTS
# ============================================================================

results_summary <- list(
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
    n_studies = length(unique(data_valid$study_id)),
    n_effects = nrow(data_valid),
    n_participants = sum(data_valid$n_treatment, na.rm=TRUE) +
                     sum(data_valid$n_control, na.rm=TRUE)
  )
)

saveRDS(results_summary, "../output/meta_analysis_results.rds")

cat("\n", "="*60, "\n")
cat("ANALYSIS COMPLETE\n")
cat("="*60, "\n")
cat("Results saved to: ../output/meta_analysis_results.rds\n")
