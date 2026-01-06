# Meta-Analysis Extraction Codingbook (HE-GALF)

**Applies to:**
- `/Volumes/External SSD/Projects/Research/GenAI_Effectiveness/ScholaRAG/projects/2025-12-05_GenAI-Learning-Effects-Meta/data/07_meta_analysis/Analysis from Codex/meta_analysis_effects_unified_with_moderators_refilled_tt.csv`

**Source documents:**
- `META_ANALYSIS_EXTRACTION_PROTOCOL.md`
- Study PDFs in `data/07_meta_analysis/pdfs`
- `meta_analysis_studies.csv` (study-level metadata)

---

## 1) General Rules

- **Unit of analysis:** one row = one outcome per study.
- **Primary evidence:** results tables, main text (Methods/Results), appendix tables.
- **Priority order (effect data):** reported effect size > group means/SDs/n > t/F/p > CI.
- **Post-test preference:** use post-test values when both pre/post are reported. If only change scores are reported, use those and note in `notes`.
- **Rounding:** keep reported precision; do not round to fewer decimals.
- **Multiple measures of the same construct:** choose the measure explicitly linked to the intervention outcome; otherwise pick the most common or primary measure and note the choice.
- **Missing numeric values:** leave blank.
- **Missing categorical values:** use `not_reported` (except where explicit options are given).
- **Notes:** always record ambiguity, assumptions, or table references in `notes`.

---

## 2) Missing/Unclear Coding

- Use **`not_reported`** for categorical fields when the paper does not state the value.
- Use **blank** for numeric fields that are not reported or cannot be derived.
- If a value is inferred (e.g., implied randomization without explicit statement), mark the field as `not_reported` and explain the inference in `notes`.

---

## 3) Variable Definitions and Criteria

### 3.1 Identifiers and Bibliographic Metadata

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `study_id` | Text/Integer | 1-69 | Match `meta_analysis_studies.csv` study ID. |
| `outcome_id` | Text/Integer | Sequential per study | Unique ID for each outcome row. |
| `title` | Text | Full title | Use study title from `meta_analysis_studies.csv`. |
| `year` | Integer | 2020-2025 | Publication year. |
| `authors` | Text | Author list | Use as in metadata file. |
| `source` | Text | Semantic Scholar, OpenAlex, arXiv, ERIC | Source in metadata. |
| `doi` | Text | 10.xxxx/xxxx | DOI if present, else blank. |

### 3.2 Outcome Classification

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `outcome_name` | Text | e.g., knowledge_test, motivation | Use the specific label from the paper; map to the list in protocol. |
| `outcome_dimension` | Text | cognitive, affective, behavioral, metacognitive | Use protocol mapping: test scores -> cognitive; motivation/attitudes -> affective; engagement/time-on-task -> behavioral; SRL -> metacognitive. |
| `blooms_level` | Text | remember, understand, apply, analyze, evaluate, create | Use the dominant cognitive demand of the outcome task. |

### 3.3 Sample and Descriptive Statistics

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `n_treatment` | Integer | >= 1 | Treatment/AI group sample size. |
| `n_control` | Integer | >= 1 | Control/traditional group sample size. |
| `m_treatment` | Numeric | Mean | Post-test mean (treatment). |
| `sd_treatment` | Numeric | SD | Post-test SD (treatment). |
| `m_control` | Numeric | Mean | Post-test mean (control). |
| `sd_control` | Numeric | SD | Post-test SD (control). |

### 3.4 Effect Size and Statistical Values

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `hedges_g` | Numeric | Effect size | Prefer reported g; otherwise compute from d. |
| `cohens_d` | Numeric | Effect size | Prefer reported d; otherwise compute from M/SD/n. |
| `se_g` | Numeric | Standard error | Compute when g and sample sizes are available. |
| `ci_lower` | Numeric | 95% CI lower | Use reported CI if available. |
| `ci_upper` | Numeric | 95% CI upper | Use reported CI if available. |
| `t_value` | Numeric | t-statistic | Use reported t for group comparison. |
| `f_value` | Numeric | F-statistic | Use reported F for 2-group comparisons. |
| `p_value` | Numeric | p | Reported p-value for outcome. |
| `eta_squared` | Numeric | eta^2 | Reported effect size if present. |

### 3.5 Study Design

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `study_design` | Text | RCT, quasi-experimental, not_reported | **RCT:** explicit random assignment of participants or clusters. **Quasi-experimental:** non-random assignment with a comparison group (e.g., matched groups, pre/post with control). **Not_reported:** design not explicitly stated. |

### 3.6 Intervention (GenAI) Metadata

**Explicit decision rules for `study_design`:**
- **RCT** only if the paper **explicitly states random assignment/allocation**, e.g., "randomly assigned," "random allocation," "randomized controlled trial," "cluster randomized."
- **Quasi-experimental** if there is a comparison group but **no explicit random assignment**, e.g., "quasi-experimental," "nonrandom assignment," "non-equivalent groups," "matched groups," "intact/existing classes," or "pretest-posttest with control."
- **Not_reported** if the design is not stated and randomization is not explicitly described.
- If terms like "experimental/control" appear **without** a randomization statement, default to **quasi-experimental** and note the evidence in `notes`.

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `genai_tool` | Text | ChatGPT, GPT-4, Claude, Copilot, Custom | Use the named tool; if multiple tools, use the primary tool and note in `notes`. |

### 3.7 Baseline Participant Characteristics (Group-Specific)

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `group_label_control` | Text | e.g., Control, TLG | Use the group label from the paper. |
| `group_label_treatment` | Text | e.g., Experimental, ALG | Use the group label from the paper. |
| `age_mean_control` | Numeric | Mean age | Control group baseline. |
| `age_sd_control` | Numeric | SD age | Control group baseline. |
| `age_mean_treatment` | Numeric | Mean age | Treatment group baseline. |
| `age_sd_treatment` | Numeric | SD age | Treatment group baseline. |
| `gpa_mean_control` | Numeric | GPA mean | Control group baseline. |
| `gpa_sd_control` | Numeric | GPA SD | Control group baseline. |
| `gpa_mean_treatment` | Numeric | GPA mean | Treatment group baseline. |
| `gpa_sd_treatment` | Numeric | GPA SD | Treatment group baseline. |
| `gender_female_n_control` | Integer | Count | Control group baseline. |
| `gender_male_n_control` | Integer | Count | Control group baseline. |
| `gender_female_n_treatment` | Integer | Count | Treatment group baseline. |
| `gender_male_n_treatment` | Integer | Count | Treatment group baseline. |
| `grade_level_control` | Text | e.g., Year 3 | Use group-specific grade/year if reported. |
| `grade_level_treatment` | Text | e.g., Year 3 | Use group-specific grade/year if reported. |
| `program_type_control` | Text | undergraduate, graduate, mixed | Control group baseline. |
| `program_type_treatment` | Text | undergraduate, graduate, mixed | Treatment group baseline. |
| `baseline_age_t` | Numeric | t | t-test for baseline age difference. |
| `baseline_age_p` | Numeric | p | p-value for baseline age difference. |
| `baseline_gpa_t` | Numeric | t | t-test for baseline GPA difference. |
| `baseline_gpa_p` | Numeric | p | p-value for baseline GPA difference. |
| `baseline_gender_chi2` | Numeric | chi-square | Chi-square for gender distribution. |
| `baseline_gender_p` | Numeric | p | p-value for gender distribution. |

**Rule:** If only overall demographics are reported (not group-specific), place values in control fields and note in `notes`.

### 3.8 Quality/Traceability

| Variable | Type | Coding / Allowed Values | Decision Rule |
|---|---|---|---|
| `extraction_confidence` | Numeric | 0.0-1.0 | Leave blank unless a confidence score is explicitly computed. |
| `notes` | Text | Evidence | Include page/table references or short snippets supporting extracted values. |

---

## 4) Study Design Examples (Quick Reference)

- **RCT:** "participants were randomly assigned" or "randomized controlled trial".
- **Quasi-experimental:** "nonrandom assignment", "matched comparison", or "pretest-posttest with control".
- **Not_reported:** no explicit design statement.

---

## 5) Outcome Dimension Mapping Examples

- **Cognitive:** exam scores, knowledge tests, problem-solving scores.
- **Affective:** motivation, attitudes, self-efficacy.
- **Behavioral:** engagement, time-on-task, participation rate.
- **Metacognitive:** self-regulation, metacognitive monitoring.
