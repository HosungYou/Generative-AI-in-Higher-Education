# Meta-Analysis Data Extraction Protocol
## GenAI Effectiveness in Higher Education (HE-GALF Framework)

**Created:** 2026-01-04
**Studies:** 69 experimental studies
**Framework:** Higher Education GenAI Learning Framework (HE-GALF)

---

## 1. Overview

This protocol guides the systematic extraction of effect size data and moderator variables from 69 experimental studies on Generative AI effectiveness in higher education. The extraction follows the theoretical framework outlined in `Theoretical_Framework_GenAI_HE.docx` and methodology from `Method_Section_HE.docx`.

---

## 2. Variables for Extraction

### 2.1 Study Identification Variables
| Variable | Description | Format |
|----------|-------------|--------|
| `study_id` | Unique identifier | 001-069 |
| `first_author` | First author's last name | Text |
| `year` | Publication year | 2020-2025 |
| `title` | Full title | Text |
| `source` | Database source | Semantic Scholar, OpenAlex, arXiv, ERIC |
| `doi` | Digital Object Identifier | 10.xxxx/xxxx |
| `journal` | Journal/venue name | Text |

### 2.2 Effect Size Variables (Primary)
| Variable | Description | Format | Priority |
|----------|-------------|--------|----------|
| `hedges_g` | Hedges' g effect size | Numeric | Calculate |
| `cohens_d` | Cohen's d effect size | Numeric | Extract/Calculate |
| `m_treatment` | Treatment group mean | Numeric | High |
| `sd_treatment` | Treatment group SD | Numeric | High |
| `n_treatment` | Treatment sample size | Integer | Critical |
| `m_control` | Control group mean | Numeric | High |
| `sd_control` | Control group SD | Numeric | High |
| `n_control` | Control sample size | Integer | Critical |
| `t_value` | t-statistic (if reported) | Numeric | Alternative |
| `f_value` | F-statistic (if reported) | Numeric | Alternative |
| `p_value` | p-value | Numeric | Supplementary |
| `ci_lower` | 95% CI lower bound | Numeric | If available |
| `ci_upper` | 95% CI upper bound | Numeric | If available |

### 2.3 Study Design Variables
| Variable | Description | Coding |
|----------|-------------|--------|
| `study_design` | Research design | RCT, quasi-experimental |
| `random_assignment` | Random allocation | Yes/No/Unclear |
| `pretest_posttest` | Pre-post measurement | Yes/No |
| `control_type` | Control condition type | no_AI, traditional, waitlist, active_control |
| `blinding` | Blinding procedure | none, single, double |

### 2.4 Moderator Variables (HE-GALF Framework)

#### 2.4.1 Intervention Characteristics
| Variable | Description | Coding |
|----------|-------------|--------|
| `genai_tool` | GenAI tool used | ChatGPT, GPT-4, Claude, Copilot, Custom |
| `gpt_version` | Specific GPT version | gpt-3.5-turbo, gpt-4, gpt-4o, etc. |
| `intervention_duration` | Length of intervention | <1week, 1-4weeks, 1-3months, >3months |
| `intervention_weeks` | Duration in weeks | Integer |
| `intervention_intensity` | Usage frequency | low, moderate, high |
| `ai_integration_type` | How AI was integrated | tutor, feedback, assistant, content_gen |

#### 2.4.2 Learner Characteristics
| Variable | Description | Coding |
|----------|-------------|--------|
| `academic_level` | Education level | undergraduate, graduate, mixed |
| `year_of_study` | Study year | 1, 2, 3, 4, graduate |
| `prior_knowledge` | Prior knowledge level | low, medium, high |
| `prior_ai_experience` | Prior AI experience | none, some, extensive |

#### 2.4.3 Educational Context
| Variable | Description | Coding |
|----------|-------------|--------|
| `discipline` | Academic discipline | STEM, humanities, social_science, medicine, education, language, business |
| `course_type` | Course type | lecture, lab, seminar, online, blended |
| `country` | Study location | Text (ISO code) |
| `institution_type` | Institution type | research_university, teaching_university, community_college |

#### 2.4.4 Baseline Participant Characteristics (Group-Specific)
Use group-specific fields when baseline tables report values separately for control/traditional vs AI/treatment groups. If only overall demographics are reported, store them in the control fields and note this in `notes`.

| Variable | Description | Coding |
|----------|-------------|--------|
| `group_label_control` | Label used for control/traditional group | Text (e.g., TLG, Control) |
| `group_label_treatment` | Label used for AI/treatment group | Text (e.g., ALG, Experimental) |
| `age_mean_control` | Mean age (control group) | Numeric |
| `age_sd_control` | SD of age (control group) | Numeric |
| `age_mean_treatment` | Mean age (treatment group) | Numeric |
| `age_sd_treatment` | SD of age (treatment group) | Numeric |
| `gpa_mean_control` | Mean GPA (control group) | Numeric |
| `gpa_sd_control` | SD GPA (control group) | Numeric |
| `gpa_mean_treatment` | Mean GPA (treatment group) | Numeric |
| `gpa_sd_treatment` | SD GPA (treatment group) | Numeric |
| `gender_female_n_control` | Female count (control group) | Integer |
| `gender_male_n_control` | Male count (control group) | Integer |
| `gender_female_n_treatment` | Female count (treatment group) | Integer |
| `gender_male_n_treatment` | Male count (treatment group) | Integer |
| `grade_level_control` | Grade/year level (control) | Text |
| `grade_level_treatment` | Grade/year level (treatment) | Text |
| `program_type_control` | Program type (control) | undergraduate, graduate, mixed |
| `program_type_treatment` | Program type (treatment) | undergraduate, graduate, mixed |
| `baseline_age_t` | t-statistic for baseline age difference | Numeric |
| `baseline_age_p` | p-value for baseline age difference | Numeric |
| `baseline_gpa_t` | t-statistic for baseline GPA difference | Numeric |
| `baseline_gpa_p` | p-value for baseline GPA difference | Numeric |
| `baseline_gender_chi2` | chi-square for gender distribution | Numeric |
| `baseline_gender_p` | p-value for gender distribution | Numeric |
| `notes` | Evidence snippet or table reference | Text |

**Deprecated (do not use going forward):** `age_mean`, `age_sd`, `age_min`, `age_max`, `age_text`, `gpa_mean`, `gpa_sd`, `gpa_text`, `gender_female_n`, `gender_male_n`, `gender_female_pct`, `gender_male_pct`, `gender_other_pct`, `gender_text`.

### 2.5 Learning Outcome Variables (Bloom's Taxonomy Aligned)

#### 2.5.1 Outcome Dimension (Theoretical Framework)
| Variable | Description | Coding |
|----------|-------------|--------|
| `outcome_dimension` | Learning dimension | cognitive, affective, behavioral, metacognitive |

#### 2.5.2 Cognitive Complexity Level
| Variable | Description | Coding |
|----------|-------------|--------|
| `blooms_level` | Bloom's taxonomy level | remember, understand, apply, analyze, evaluate, create |
| `cognitive_complexity` | Higher/Lower order | lower_order (1-3), higher_order (4-6) |

#### 2.5.3 Specific Outcome Types
| Outcome Type | Dimension | Bloom's Level |
|--------------|-----------|---------------|
| `knowledge_test` | Cognitive | Remember/Understand |
| `comprehension` | Cognitive | Understand |
| `problem_solving` | Cognitive | Apply/Analyze |
| `critical_thinking` | Cognitive | Analyze/Evaluate |
| `creativity` | Cognitive | Create |
| `writing_quality` | Cognitive | Apply/Create |
| `motivation` | Affective | - |
| `self_efficacy` | Affective | - |
| `engagement` | Behavioral | - |
| `learning_time` | Behavioral | - |
| `self_regulation` | Metacognitive | - |
| `metacognitive_monitoring` | Metacognitive | - |

---

## 3. RAG-Based Extraction Queries

### 3.1 Effect Size Queries
```
Query 1: "sample size participants treatment control group n="
Query 2: "mean standard deviation M SD pre-test post-test"
Query 3: "effect size Cohen d Hedges g eta squared"
Query 4: "t-test F-test ANOVA significance p < .05 p = .001"
Query 5: "confidence interval CI 95%"
```

### 3.2 Study Design Queries
```
Query 1: "randomized controlled trial RCT random assignment"
Query 2: "quasi-experimental pretest posttest design"
Query 3: "control group comparison condition traditional instruction"
Query 4: "experimental group treatment intervention ChatGPT"
```

### 3.3 Moderator Queries
```
Query 1: "undergraduate graduate students higher education university"
Query 2: "ChatGPT GPT-4 generative AI tool version model"
Query 3: "intervention duration weeks semester course"
Query 4: "STEM science mathematics engineering humanities language"
Query 5: "prior knowledge experience novice expert"
Query 6: "baseline characteristics demographics table age gender GPA t = p = chi-square"
```

### 3.4 Outcome Dimension Queries
```
Query 1: "knowledge test achievement exam scores learning outcomes"
Query 2: "critical thinking problem solving higher-order thinking"
Query 3: "motivation engagement attitude self-efficacy"
Query 4: "self-regulated learning metacognition strategy"
Query 5: "writing quality creativity essay performance"
```

---

## 4. Effect Size Calculation Formulas

### 4.1 Cohen's d (from M and SD)
```
d = (M_treatment - M_control) / SD_pooled
SD_pooled = sqrt(((n_t - 1) * SD_t^2 + (n_c - 1) * SD_c^2) / (n_t + n_c - 2))
```

### 4.2 Hedges' g (bias-corrected)
```
g = d * (1 - 3 / (4 * (n_t + n_c) - 9))
```

### 4.3 From t-statistic
```
d = t * sqrt(1/n_t + 1/n_c)
```

### 4.4 From F-statistic (2 groups)
```
d = sqrt(F * (1/n_t + 1/n_c))
```

### 4.5 Standard Error of g
```
SE_g = sqrt((n_t + n_c) / (n_t * n_c) + g^2 / (2 * (n_t + n_c)))
```

---

## 5. Extraction Priority Hierarchy

1. **Direct Effect Sizes**: Hedges' g or Cohen's d reported in paper
2. **Means and SDs**: Calculate d from M, SD, n for each group
3. **t/F Statistics**: Calculate d from inferential statistics
4. **p-values with n**: Approximate d from exact p-value
5. **Reported significance**: Code direction only (insufficient for meta-analysis)

---

## 6. Quality Checks

### 6.1 Data Verification
- Cross-check extracted values against tables/figures
- Verify n values match reported total sample
- Confirm effect direction (+/- for treatment benefit)
- Check SD plausibility (should be positive, typically 10-30% of mean)

### 6.2 Multiple Outcomes
- Extract each outcome separately (multiple rows per study)
- Code `outcome_id` for within-study clustering
- Note if outcomes are independent or correlated

### 6.3 Uncertainty Coding
- `extraction_confidence`: high, medium, low
- `notes`: Free text for ambiguities
- `author_contact_needed`: Yes/No

---

## 7. File Outputs

| File | Description |
|------|-------------|
| `meta_analysis_studies.csv` | Basic study info (69 rows) |
| `meta_analysis_effects.csv` | Effect sizes with moderators (multiple rows per study) |
| `extraction_log.json` | Processing log and errors |
| `codebook.csv` | Variable definitions and coding |

---

## 8. RAG System Configuration

- **Vector Database**: FAISS
- **Embedding Model**: all-mpnet-base-v2 (768 dimensions)
- **Chunk Size**: 1,500 characters
- **Chunk Overlap**: 300 characters
- **Total Chunks**: 4,010
- **Papers**: 69

---

## 9. Expected Meta-Analysis Outputs

Based on theoretical framework (HE-GALF), expected analyses:

1. **Overall Effect**: Pooled Hedges' g for GenAI vs control
2. **Subgroup by Outcome Dimension**: Cognitive vs Affective vs Behavioral vs Metacognitive
3. **Subgroup by Cognitive Complexity**: Lower-order vs Higher-order (Bloom's)
4. **Meta-Regression by Moderators**:
   - Prior knowledge level
   - Intervention duration
   - Academic discipline
   - GenAI tool type
5. **Publication Bias**: Funnel plot, Egger's test, trim-and-fill

---

*Protocol Version: 1.0*
*Last Updated: 2026-01-04*
