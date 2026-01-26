# ============================================================================
# Extended Sensitivity Analysis: Metacognition & Bayesian Meta-Analysis
# ============================================================================
# Author: Hosung You (extended by Claude Code)
# Affiliation: College of Education, Pennsylvania State University
# Date: January 2026
# Version: 2.3
# ============================================================================

# Load required packages
required_packages <- c("metafor", "clubSandwich", "dplyr", "ggplot2")

# Check and install missing packages
for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org")
    library(pkg, character.only = TRUE)
  }
}

# Try to load brms/bayestestR (optional for Bayesian analysis)
bayesian_available <- FALSE
tryCatch({
  library(brms)
  library(bayestestR)
  bayesian_available <- TRUE
  cat("Bayesian packages loaded successfully.\n")
}, error = function(e) {
  cat("Note: brms/bayestestR not available. Bayesian analysis will be skipped.\n")
  cat("To enable: install.packages(c('brms', 'bayestestR'))\n\n")
})

# ============================================================================
# 1. LOAD DATA
# ============================================================================

# Try multiple data paths
data_paths <- c(
  "../data/processed/meta_analysis_HE_corrected.csv",
  "../data/processed/meta_analysis_46studies_with_moderators.csv",
  "../data/raw/meta_analysis_effects_unified_with_moderators_refilled_tt.csv"
)

data <- NULL
for(path in data_paths) {
  if(file.exists(path)) {
    data <- read.csv(path)
    cat("Data loaded from:", path, "\n")
    break
  }
}

if(is.null(data)) {
  stop("No data file found!")
}

# Filter valid effect sizes
data_valid <- data %>%
  filter(!is.na(hedges_g) & !is.na(se_g))

cat("\n========================================\n")
cat("DATA SUMMARY\n")
cat("========================================\n")
cat("Total effect sizes:", nrow(data_valid), "\n")
cat("Unique studies:", length(unique(data_valid$study_id)), "\n")

# ============================================================================
# 2. WINSORIZATION SENSITIVITY ANALYSIS
# ============================================================================

cat("\n========================================\n")
cat("WINSORIZATION SENSITIVITY ANALYSIS\n")
cat("========================================\n")

# Define winsorization function
winsorize_effect <- function(g, lower = -3.0, upper = 3.0) {
  pmax(pmin(g, upper), lower)
}

# Create winsorized variable
data_valid$hedges_g_winsorized <- winsorize_effect(data_valid$hedges_g)

# Count winsorized values
n_winsorized <- sum(abs(data_valid$hedges_g) > 3.0)
cat("Effect sizes winsorized (|g| > 3.0):", n_winsorized, "\n")

# Model 1: Original (no treatment)
model_original <- rma.mv(
  yi = hedges_g,
  V = se_g^2,
  random = ~ 1 | study_id/outcome_id,
  data = data_valid,
  method = "REML"
)

# Model 2: Winsorized
model_winsorized <- rma.mv(
  yi = hedges_g_winsorized,
  V = se_g^2,
  random = ~ 1 | study_id/outcome_id,
  data = data_valid,
  method = "REML"
)

# Model 3: Outliers excluded
data_no_outliers <- data_valid %>% filter(abs(hedges_g) <= 3.0)
model_excluded <- rma.mv(
  yi = hedges_g,
  V = se_g^2,
  random = ~ 1 | study_id/outcome_id,
  data = data_no_outliers,
  method = "REML"
)

# Compare results
winsor_comparison <- data.frame(
  Approach = c("Full dataset (no treatment)", "Winsorized (Primary)", "Outliers excluded"),
  g = c(coef(model_original), coef(model_winsorized), coef(model_excluded)),
  SE = c(sqrt(vcov(model_original)), sqrt(vcov(model_winsorized)), sqrt(vcov(model_excluded))),
  p = c(summary(model_original)$pval, summary(model_winsorized)$pval, summary(model_excluded)$pval)
)

winsor_comparison$CI_lower <- winsor_comparison$g - 1.96 * winsor_comparison$SE
winsor_comparison$CI_upper <- winsor_comparison$g + 1.96 * winsor_comparison$SE

cat("\nSensitivity Analysis Results:\n")
print(winsor_comparison)

# ============================================================================
# 3. METACOGNITIVE OUTCOMES SUBGROUP ANALYSIS
# ============================================================================

cat("\n========================================\n")
cat("METACOGNITIVE OUTCOMES ANALYSIS\n")
cat("========================================\n")

# Check for outcome_dimension variable
if("outcome_dimension" %in% names(data_valid)) {

  # Filter metacognitive outcomes
  metacog_data <- data_valid %>%
    filter(tolower(outcome_dimension) %in% c("metacognitive", "metacog", "meta-cognitive"))

  cat("Metacognitive effect sizes found:", nrow(metacog_data), "\n")
  cat("Metacognitive studies:", length(unique(metacog_data$study_id)), "\n")

  if(nrow(metacog_data) >= 5) {
    # Metacognitive-specific model
    model_metacog <- rma.mv(
      yi = hedges_g_winsorized,
      V = se_g^2,
      random = ~ 1 | study_id/outcome_id,
      data = metacog_data,
      method = "REML"
    )

    cat("\nMetacognitive Outcomes Only:\n")
    cat("Pooled g:", round(coef(model_metacog), 3), "\n")
    cat("95% CI: [", round(coef(model_metacog) - 1.96*sqrt(vcov(model_metacog)), 3), ", ",
        round(coef(model_metacog) + 1.96*sqrt(vcov(model_metacog)), 3), "]\n")
    cat("p-value:", round(summary(model_metacog)$pval, 4), "\n")

    # Power analysis for metacognitive detection
    # Approximate power calculation for detecting g = 0.40
    metacog_k <- length(unique(metacog_data$study_id))
    metacog_n <- nrow(metacog_data)
    avg_n <- mean(metacog_data$n_treatment + metacog_data$n_control, na.rm = TRUE)

    # Rough power estimate (simplified)
    se_expected <- sqrt(vcov(model_metacog))
    power_approx <- pnorm(0.40 / se_expected - 1.96)

    cat("\nPower Analysis:\n")
    cat("Studies (k):", metacog_k, "\n")
    cat("Effect sizes (n):", metacog_n, "\n")
    cat("Estimated power for detecting g=0.40:", round(power_approx * 100, 1), "%\n")

    # Check for measurement method variable
    if("measurement_method" %in% names(metacog_data) | "outcome_measure" %in% names(metacog_data)) {
      measure_var <- ifelse("measurement_method" %in% names(metacog_data),
                            "measurement_method", "outcome_measure")

      cat("\nSubgroup by Measurement Method:\n")
      print(table(metacog_data[[measure_var]]))

      # Try subgroup analysis if enough variation
      if(length(unique(metacog_data[[measure_var]])) > 1) {
        metacog_data$measure_factor <- as.factor(metacog_data[[measure_var]])

        tryCatch({
          model_measure <- rma.mv(
            yi = hedges_g_winsorized,
            V = se_g^2,
            mods = ~ measure_factor - 1,
            random = ~ 1 | study_id/outcome_id,
            data = metacog_data,
            method = "REML"
          )
          cat("\nMetacognition by Measurement Type:\n")
          print(summary(model_measure))
        }, error = function(e) {
          cat("Note: Subgroup analysis failed (likely due to small sample):", e$message, "\n")
        })
      }
    }
  } else {
    cat("Insufficient metacognitive effect sizes for separate analysis.\n")
  }

  # Full subgroup comparison
  cat("\n========================================\n")
  cat("OUTCOME DIMENSION COMPARISON\n")
  cat("========================================\n")

  data_valid$outcome_factor <- as.factor(tolower(data_valid$outcome_dimension))

  model_by_dimension <- rma.mv(
    yi = hedges_g_winsorized,
    V = se_g^2,
    mods = ~ outcome_factor - 1,
    random = ~ 1 | study_id/outcome_id,
    data = data_valid,
    method = "REML"
  )

  print(summary(model_by_dimension))

} else {
  cat("outcome_dimension variable not found in dataset.\n")
}

# ============================================================================
# 4. BAYESIAN META-ANALYSIS (if packages available)
# ============================================================================

if(bayesian_available) {
  cat("\n========================================\n")
  cat("BAYESIAN META-ANALYSIS\n")
  cat("========================================\n")

  # Prepare metacognitive data for Bayesian analysis
  if(exists("metacog_data") && nrow(metacog_data) >= 5) {

    cat("Running Bayesian meta-analysis for metacognitive outcomes...\n")
    cat("(This may take several minutes)\n\n")

    # Prior specification (informed by general educational interventions)
    prior_meta <- c(
      prior(normal(0.3, 0.2), class = "Intercept"),   # Informed prior: small-medium effect
      prior(cauchy(0, 0.5), class = "sd")             # Half-Cauchy for heterogeneity
    )

    tryCatch({
      # Bayesian random-effects meta-analysis
      bayes_model <- brm(
        hedges_g_winsorized | se(se_g) ~ 1 + (1 | study_id),
        data = metacog_data,
        prior = prior_meta,
        chains = 4,
        iter = 4000,
        warmup = 1000,
        seed = 42,
        silent = 2,
        refresh = 0
      )

      cat("Bayesian Model Summary:\n")
      print(summary(bayes_model))

      # Bayes Factor for null effect (ROPE: -0.2 to 0.2)
      bf_result <- bayesfactor_parameters(
        bayes_model,
        null = c(-0.2, 0.2)
      )

      cat("\nBayes Factor Analysis:\n")
      cat("ROPE: [-0.2, 0.2] (Region of Practical Equivalence)\n")
      print(bf_result)

      # Interpretation guide
      cat("\nInterpretation Guide:\n")
      cat("BF01 > 10: Strong evidence for null\n")
      cat("BF01 3-10: Moderate evidence for null\n")
      cat("BF01 1/3-3: Inconclusive\n")
      cat("BF01 < 1/3: Evidence for effect\n")

      # Save Bayesian results
      bayes_results <- list(
        model = bayes_model,
        bf = bf_result,
        posterior_summary = posterior_summary(bayes_model)
      )
      saveRDS(bayes_results, "../output/bayesian_metacog_results.rds")
      cat("\nBayesian results saved to: ../output/bayesian_metacog_results.rds\n")

    }, error = function(e) {
      cat("Bayesian analysis error:", e$message, "\n")
      cat("Consider running with more data or simpler priors.\n")
    })

  } else {
    cat("Insufficient metacognitive data for Bayesian analysis.\n")
  }

} else {
  cat("\n========================================\n")
  cat("BAYESIAN ANALYSIS SKIPPED\n")
  cat("========================================\n")
  cat("To enable Bayesian analysis, install:\n")
  cat("install.packages(c('brms', 'bayestestR'))\n")
  cat("\nAlternative: Use frequentist equivalence testing:\n")

  # Equivalence test using TOST procedure (frequentist alternative)
  if(exists("metacog_data") && nrow(metacog_data) >= 5) {
    metacog_est <- coef(model_metacog)
    metacog_se <- sqrt(vcov(model_metacog))

    # TOST bounds (ROPE equivalent)
    delta_L <- -0.2
    delta_U <- 0.2

    # Two one-sided tests
    t_lower <- (metacog_est - delta_L) / metacog_se
    t_upper <- (delta_U - metacog_est) / metacog_se

    p_lower <- pt(t_lower, df = nrow(metacog_data) - 1, lower.tail = FALSE)
    p_upper <- pt(t_upper, df = nrow(metacog_data) - 1, lower.tail = FALSE)
    p_tost <- max(p_lower, p_upper)

    cat("\nEquivalence Test (TOST):\n")
    cat("Bounds: [", delta_L, ", ", delta_U, "]\n")
    cat("Estimate:", round(metacog_est, 3), "\n")
    cat("p (lower bound):", round(p_lower, 4), "\n")
    cat("p (upper bound):", round(p_upper, 4), "\n")
    cat("TOST p-value:", round(p_tost, 4), "\n")

    if(p_tost < 0.05) {
      cat("Conclusion: Effect is statistically equivalent to null (within bounds).\n")
    } else {
      cat("Conclusion: Cannot conclude equivalence to null.\n")
    }
  }
}

# ============================================================================
# 5. SAVE EXTENDED RESULTS
# ============================================================================

cat("\n========================================\n")
cat("SAVING EXTENDED RESULTS\n")
cat("========================================\n")

# Create output directory if needed
if(!dir.exists("../output")) {
  dir.create("../output", recursive = TRUE)
}

extended_results <- list(
  winsorization = winsor_comparison,
  n_winsorized = n_winsorized,
  analysis_date = Sys.time(),
  r_version = R.version.string
)

if(exists("model_metacog")) {
  extended_results$metacognitive <- list(
    estimate = coef(model_metacog),
    se = sqrt(vcov(model_metacog)),
    ci = c(coef(model_metacog) - 1.96*sqrt(vcov(model_metacog)),
           coef(model_metacog) + 1.96*sqrt(vcov(model_metacog))),
    p = summary(model_metacog)$pval,
    k = length(unique(metacog_data$study_id)),
    n = nrow(metacog_data),
    power_est = power_approx
  )
}

saveRDS(extended_results, "../output/extended_sensitivity_results.rds")
cat("Extended results saved to: ../output/extended_sensitivity_results.rds\n")

# Generate summary table for manuscript
cat("\n========================================\n")
cat("SUMMARY TABLE FOR MANUSCRIPT\n")
cat("========================================\n")

summary_table <- rbind(
  winsor_comparison[, c("Approach", "g", "CI_lower", "CI_upper", "p")],
  if(exists("model_metacog")) {
    data.frame(
      Approach = "Metacognitive only",
      g = round(coef(model_metacog), 3),
      CI_lower = round(coef(model_metacog) - 1.96*sqrt(vcov(model_metacog)), 3),
      CI_upper = round(coef(model_metacog) + 1.96*sqrt(vcov(model_metacog)), 3),
      p = round(summary(model_metacog)$pval, 4)
    )
  }
)

print(summary_table)

write.csv(summary_table, "../output/sensitivity_summary_table.csv", row.names = FALSE)
cat("\nSummary table saved to: ../output/sensitivity_summary_table.csv\n")

cat("\n========================================\n")
cat("EXTENDED ANALYSIS COMPLETE\n")
cat("========================================\n")
