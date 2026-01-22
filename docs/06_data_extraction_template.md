# Data Extraction Template for Additional Studies

## Overview

This document provides a structured template for extracting effect size data from the 16 confirmed studies to be added to the meta-analysis.

---

## Extraction Status Summary

| Status | Count |
|--------|-------|
| ✅ Include (confirmed) | 16 |
| ⏸️ Conditional | 2 |
| 📝 Full-text review | 1 |
| ❌ Exclude | 4 |
| **Total reviewed** | **23** |

---

## Data Extraction Template

### Required Fields (per effect size)

```
study_id: [Auto-generated, e.g., "urban_2024_01"]
author: [Last name of first author]
year: [Publication year]
title: [Full title]
journal: [Journal name]
doi: [DOI if available]

# Sample Information
n_treatment: [Treatment group N]
n_control: [Control group N]
n_total: [Total N]

# Effect Size Data
effect_size_type: [d / g / r / eta_squared / other]
effect_size_value: [Numeric value]
se: [Standard error, if reported]
ci_lower: [95% CI lower bound]
ci_upper: [95% CI upper bound]
p_value: [p-value if reported]

# Outcome Classification
outcome_type: [cognitive / metacognitive / affective / performance]
outcome_measure: [Specific measure name]
outcome_timing: [immediate / delayed / follow-up]

# Moderator Variables
genai_tool: [ChatGPT-3.5 / ChatGPT-4 / Claude / Other]
discipline: [STEM / Social Sciences / Arts / Medicine / Other]
academic_level: [undergraduate / graduate / mixed]
study_design: [RCT / quasi-experimental]
intervention_duration: [weeks]
country: [Country of study]
prior_knowledge_controlled: [yes / no / not reported]
```

---

## Studies to Extract

### Part A: From Existing Meta-Analyses (5 studies)

#### 1. Urban et al. (2024) - Creative Problem-Solving
```yaml
study_id: urban_2024
author: Urban
year: 2024
title: "ChatGPT Improves Creative Problem-Solving Performance in University Students"
journal: Computers & Education
doi: 10.1016/j.compedu.2024.105031

n_treatment: 77
n_control: 68
n_total: 145

# Effect Size 1: Self-efficacy
effect_size_type: d
effect_size_value: 0.65
outcome_type: affective
outcome_measure: creative self-efficacy

# Effect Size 2: Quality
effect_size_type: d
effect_size_value: 0.69
outcome_type: cognitive
outcome_measure: solution quality

# Effect Size 3: Elaboration
effect_size_type: d
effect_size_value: 0.61
outcome_type: cognitive
outcome_measure: elaboration

# Effect Size 4: Originality
effect_size_type: d
effect_size_value: 0.55
outcome_type: cognitive
outcome_measure: originality

genai_tool: ChatGPT
discipline: General/Psychology
academic_level: undergraduate
study_design: RCT
country: Czech Republic
```

#### 2. Yin et al. (2024) - Formative Feedback
```yaml
study_id: yin_2024
author: Yin
year: 2024
title: [To be extracted from full-text]
journal: IEEE Transactions on Learning Technologies
doi: 10.1109/TLT.2024.3364015

n_total: [TBD]
effect_size_type: [TBD]
effect_size_value: [TBD]

outcome_type: cognitive
genai_tool: ChatGPT
study_design: longitudinal
```

#### 3. Essel et al. (2024) - Cognitive Skills
```yaml
study_id: essel_2024
author: Essel
year: 2024
title: "ChatGPT effects on cognitive skills of undergraduate students"
journal: Computers and Education: Artificial Intelligence
doi: 10.1016/j.caeai.2023.100198

n_treatment: 60
n_control: 65
n_total: 125

outcome_type: cognitive
outcome_measure: critical thinking, creative thinking, reflective thinking
genai_tool: ChatGPT
discipline: Research Methods
academic_level: undergraduate
study_design: RCT
country: Ghana
intervention_duration: [TBD]
```

#### 4. Gan et al. (2024) - Medical Education
```yaml
study_id: gan_2024
author: Gan
year: 2024
title: "Integrating ChatGPT in Orthopedic Education for Medical Undergraduates: RCT"
journal: Journal of Medical Internet Research
doi: 10.2196/57037

n_total: 129
study_design: RCT
trial_registration: ChiCTR2300071774

outcome_type: cognitive
outcome_measure: orthopedic knowledge (MCQ performance)
genai_tool: ChatGPT
discipline: Medicine
academic_level: undergraduate
country: China
```

#### 5. Zhou & Kim (2024) - Music Education
```yaml
study_id: zhou_kim_2024
author: Zhou
year: 2024
title: [To be extracted from full-text]
journal: Education and Information Technologies
doi: 10.1007/s10639-024-12705-z

outcome_type: [TBD]
discipline: Arts (Music)
genai_tool: [TBD]
```

---

### Part B: New 2025 Studies (11 studies)

#### 6. Geng & Razali (2025) - Creativity RCT ⭐ LARGEST SAMPLE
```yaml
study_id: geng_2025
author: Geng
year: 2025
title: "Can ChatGPT enhance business student creativity? Evidence from RCT"
journal: Studies in Higher Education
doi: 10.1080/03075079.2025.2515512

n_total: 1190  # LARGEST SAMPLE IN META-ANALYSIS!
study_design: RCT

# Key Finding: Effect varies by discipline
# Marketing/Management: Enhanced creativity
# Entrepreneurship: Little to no effect

outcome_type: cognitive
outcome_measure: creativity
genai_tool: ChatGPT
discipline: Business
academic_level: undergraduate
```

#### 7. Knowledge Retention (2025) ⭐ SUPPORTS COGNITIVE DEPENDENCY
```yaml
study_id: retention_2025
author: [TBD - Barcaui likely]
year: 2025
title: "ChatGPT as a cognitive crutch: Evidence from RCT on knowledge retention"
journal: Computers & Education: Artificial Intelligence
doi: [TBD]

n_total: 120
study_design: RCT

# CRITICAL FINDING - SUPPORTS COGNITIVE DEPENDENCY HYPOTHESIS!
# ChatGPT group: 57.5%
# Control group: 68.5%
effect_size_type: d
effect_size_value: 0.68
direction: NEGATIVE (control > treatment)

outcome_type: metacognitive
outcome_measure: knowledge retention
genai_tool: ChatGPT
```

#### 8. Harvard AI Tutoring (2025)
```yaml
study_id: harvard_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: Nature Scientific Reports
doi: 10.1038/s41598-025-97652-6

n_total: 194
study_design: RCT

outcome_type: cognitive
genai_tool: AI Tutor
discipline: [TBD]
```

#### 9. Urban et al. (2025)
```yaml
study_id: urban_2025
author: Urban
year: 2025
title: [To be extracted]
journal: British Journal of Educational Technology
doi: 10.1111/bjet.13591

n_total: 98
study_design: experimental

outcome_type: [TBD]
genai_tool: [TBD]
```

#### 10. Gazi University (2025) - Medical Education
```yaml
study_id: gazi_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: Postgraduate Medical Journal
doi: 10.1093/postmj/qgae170

n_total: 129
study_design: RCT

outcome_type: cognitive
discipline: Medicine
genai_tool: ChatGPT
```

#### 11. ChatGPT vs AWE Writing (2025)
```yaml
study_id: awe_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: Computer Assisted Language Learning
doi: 10.1080/09588221.2025.2454541

n_total: 150
study_design: RCT

effect_size_type: eta_squared
effect_size_value: 0.10  # Convert to d/g

outcome_type: cognitive
outcome_measure: writing performance
discipline: Language/Writing
genai_tool: ChatGPT
```

#### 12. ESP Writing (2025)
```yaml
study_id: esp_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: Discover Education
doi: 10.1007/s44217-025-00700-6

n_total: 117
study_design: experimental

outcome_type: cognitive
outcome_measure: ESP writing
discipline: Language/Writing
genai_tool: ChatGPT
```

#### 13. Morocco STEM (2025)
```yaml
study_id: morocco_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: Disciplinary and Interdisciplinary Science Education Research
doi: 10.1186/s43031-025-00125-z

n_total: 120
study_design: quasi-experimental

outcome_type: cognitive
discipline: STEM
country: Morocco
genai_tool: ChatGPT
```

#### 14. Python Programming (2025)
```yaml
study_id: python_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: Education and Information Technologies
doi: 10.1007/s10639-025-13733-z

n_total: 79
study_design: quasi-experimental

outcome_type: cognitive
outcome_measure: programming skills
discipline: Computer Science
genai_tool: ChatGPT
```

#### 15. Liu Math Creativity (2025)
```yaml
study_id: liu_math_2025
author: Liu
year: 2025
title: [To be extracted]
journal: Computer Applications in Engineering Education
doi: 10.1002/cae.70100

study_design: quasi-experimental

outcome_type: cognitive
outcome_measure: mathematical creativity
discipline: Mathematics
genai_tool: ChatGPT
```

#### 16. Taiwan Chemistry (2025)
```yaml
study_id: taiwan_chem_2025
author: [TBD]
year: 2025
title: [To be extracted]
journal: [TBD]
doi: [TBD]

n_total: 61
study_design: [TBD]

outcome_type: cognitive
discipline: Chemistry
country: Taiwan
genai_tool: ChatGPT
```

---

## Conditional Studies (Need Verification)

#### Georgetown Medical (2025)
```yaml
study_id: georgetown_2025
status: CONDITIONAL - Small sample

n_total: 33  # Below typical threshold
action_needed: Include in sensitivity analysis as "small sample" subgroup
```

#### Mahapatra (2024)
```yaml
study_id: mahapatra_2024
status: CONDITIONAL - Verify quantitative data

action_needed: Confirm effect sizes reported in full-text
```

---

## Full-Text Review Needed

#### Jing et al. (2024)
```yaml
study_id: jing_2024
status: FULL-TEXT REVIEW NEEDED

doi: 10.1057/s41599-024-02751-w
focus: Programming, AI literacy
action_needed: Verify meets inclusion criteria
```

---

## Effect Size Conversion Formulas

### For studies reporting eta-squared (η²):
```
d = 2 * sqrt(η² / (1 - η²))
```

### For studies reporting F-statistics:
```
d = 2 * sqrt(F / df_error)
```

### For studies reporting t-statistics:
```
d = 2t / sqrt(df)
```

### Converting Cohen's d to Hedges' g:
```
g = d * (1 - 3 / (4 * (n1 + n2) - 9))
```

### Standard error of g:
```
se_g = sqrt((n1 + n2) / (n1 * n2) + g² / (2 * (n1 + n2)))
```

---

## Next Steps

1. [ ] Retrieve full-text PDFs for all 16 confirmed studies
2. [ ] Extract complete effect size data using this template
3. [ ] Convert all effect sizes to Hedges' g
4. [ ] Calculate standard errors
5. [ ] Add to meta_analysis_HE_corrected.csv
6. [ ] Add to moderator_coding_46studies_rag_final.csv
7. [ ] Re-run three-level meta-analysis
8. [ ] Update PRISMA flow diagram (46 → 62 studies)

---

## Updated Study Count Projection

| Category | Count |
|----------|-------|
| Current studies | 46 |
| New confirmed additions | +16 |
| Conditional (pending) | +2 |
| Full-text review | +1 |
| **Projected total** | **62-65** |

This would match the study count of Deng et al. (2024) while maintaining our unique contributions:
- Cognitive Dependency Hypothesis
- Three-level model
- Most current evidence (through December 2025)
