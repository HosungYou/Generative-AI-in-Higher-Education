# New Studies Review Report - January 26, 2025

## Overview

This report documents the screening of 3 PDF papers for inclusion in the GenAI-HE-Review-AIMC meta-analysis.

**Inclusion Criteria:**
1. Study design: RCT or quasi-experimental with control group
2. Outcome: Learning outcomes (knowledge, skills, performance) - NOT just satisfaction or perceptions
3. Intervention: Generative AI (ChatGPT, LLM-based tools) in higher education
4. Sufficient data to calculate effect size (M, SD, n for both groups OR t/F statistics)

---

## Summary Table

| Study | Design | Population | AI Tool | Outcome Type | Decision |
|-------|--------|------------|---------|--------------|----------|
| Yilmaz & Yilmaz (2023) | Quasi-experimental | Undergraduates (N=45) | ChatGPT (GPT-3.5) | Cognitive + Affective | **INCLUDE** |
| Huang (2025) | Correlational | Middle school (N=616) | ASR-based apps | Speaking performance | **EXCLUDE** |
| Yin, Goh & Hu (2024) | Quasi-experimental | Undergraduates (N=173) | Flow.ai (rule-based) | Cognitive + Affective | **EXCLUDE** |

---

## Detailed Study Extractions

### Study 1: Yilmaz & Yilmaz (2023) - INCLUDE

**Citation:**
Yilmaz, R., & Karaoglan Yilmaz, F. G. (2023). The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation. *Computers and Education: Artificial Intelligence*, 4, 100147. https://doi.org/10.1016/j.caeai.2023.100147

**Study Characteristics:**
- **Design:** Quasi-experimental pretest-posttest control group design
- **Setting:** Java OOP programming course at a university in Turkey
- **Duration:** 7-week intervention period
- **Sample:**
  - Experimental group: n = 21 undergraduates (ChatGPT-assisted)
  - Control group: n = 24 undergraduates (traditional instruction)
  - Total N = 45

**Intervention:**
- **GenAI Tool:** ChatGPT (GPT-3.5)
- **Implementation:** Students used ChatGPT to understand problems, design algorithms, learn syntax, detect/fix errors, refactor code, create test scenarios, and develop documentation

**Outcomes and Statistics:**

| Outcome | Group | Pretest M (SD) | Posttest M (SD) | n |
|---------|-------|----------------|-----------------|---|
| Computational Thinking | Experimental | 103.67 (16.35) | 126.73 (8.34) | 21 |
| Computational Thinking | Control | 103.08 (16.86) | 112.61 (15.32) | 24 |
| Programming Self-Efficacy | Experimental | 32.18 (8.01) | 41.32 (5.84) | 21 |
| Programming Self-Efficacy | Control | 32.96 (6.19) | 33.52 (7.64) | 24 |
| Learning Motivation | Experimental | 86.32 (14.28) | 96.50 (7.62) | 21 |
| Learning Motivation | Control | 87.42 (13.91) | 85.17 (13.84) | 24 |

**ANCOVA Results:**
- Computational Thinking: F(1,42) = 18.760, p < .001, partial eta-squared = .309
- Programming Self-Efficacy: F(1,42) = 15.144, p < .001, partial eta-squared = .265
- Learning Motivation: F(1,42) = 11.412, p = .002, partial eta-squared = .214

**Calculated Effect Sizes (Cohen's d):**

| Outcome | Cohen's d | SE | 95% CI | Interpretation |
|---------|-----------|-----|--------|----------------|
| Computational Thinking | 1.12 | 0.32 | [0.49, 1.75] | Large |
| Programming Self-Efficacy | 1.14 | 0.32 | [0.51, 1.77] | Large |
| Learning Motivation | 1.00 | 0.31 | [0.39, 1.61] | Large |

**Effect Size Calculation Details:**

*Computational Thinking:*
- SD_pooled = sqrt[((21-1) x 8.34^2 + (24-1) x 15.32^2) / (21+24-2)] = 12.57
- d = (126.73 - 112.61) / 12.57 = 1.12

*Programming Self-Efficacy:*
- SD_pooled = sqrt[((21-1) x 5.84^2 + (24-1) x 7.64^2) / 43] = 6.86
- d = (41.32 - 33.52) / 6.86 = 1.14

*Learning Motivation:*
- SD_pooled = sqrt[((21-1) x 7.62^2 + (24-1) x 13.84^2) / 43] = 11.38
- d = (96.50 - 85.17) / 11.38 = 1.00

**Inclusion Rationale:**
- Quasi-experimental design with control group
- Higher education setting (university undergraduates)
- Generative AI intervention (ChatGPT GPT-3.5)
- Learning outcomes measured (computational thinking, self-efficacy, motivation)
- Sufficient statistics provided (M, SD, n for both groups)

---

### Study 2: Huang (2025) - EXCLUDE

**Citation:**
Huang, M. (2025). Student engagement and speaking performance in AI-assisted learning environments: A mixed-methods study from Chinese middle schools. *Education and Information Technologies*, 30, 7143-7165. https://doi.org/10.1007/s10639-024-12989-1

**Study Characteristics:**
- **Design:** Mixed-methods correlational study (NOT experimental)
- **Setting:** Chinese middle schools
- **Sample:** N = 616 middle school students (grades 7-9)

**Intervention:**
- **AI Tool:** AI-based speaking practice applications with Automatic Speech Recognition (ASR)
- **NOT Generative AI:** Uses ASR technology, not LLM-based generative AI

**Analysis:**
- Multiple regression analysis examining relationships between engagement dimensions and speaking performance
- No experimental manipulation or control group comparison

**Exclusion Rationale:**
1. **Not experimental design:** Correlational/regression study without control group
2. **Not higher education:** Middle school students (grades 7-9)
3. **Not generative AI:** Uses ASR-based speaking apps, not ChatGPT or LLM-based tools
4. **No effect size calculable:** No between-group comparison with M/SD/n

---

### Study 3: Yin, Goh & Hu (2024) - EXCLUDE

**Citation:**
Yin, J., Goh, T.-T., & Hu, Y. (2024). Using a chatbot to provide formative feedback: A longitudinal study of intrinsic motivation, cognitive load, and learning performance. *IEEE Transactions on Learning Technologies*, 17, 1378-1389. https://doi.org/10.1109/TLT.2024.3403645

**Study Characteristics:**
- **Design:** Longitudinal quasi-experimental with pretest-posttest
- **Setting:** Basic university computer course in China
- **Duration:** One semester (4 chapters)
- **Sample:**
  - Chatbot group: n = 88 undergraduates
  - Teacher feedback group: n = 85 undergraduates
  - Total N = 173

**Intervention:**
- **Tool:** Flow.ai chatbot platform
- **Technology:** Rule-based chatbot with scripted formative feedback
- **NOT Generative AI:** Paper explicitly states the chatbot uses a "knowledge base" with pre-programmed responses, not LLM-generated content

**Key Quote from Paper:**
> "The chatbot was designed using Flow.ai... The chatbot's knowledge base was constructed to provide scripted formative feedback based on student queries."

**Statistics Available:**
- Two-way ANCOVA results with mean differences
- Chapter 1: Mean Difference = 2.427, p < .05
- Chapter 4: Mean Difference = 0.815, p = .009

**Exclusion Rationale:**
1. **Not generative AI:** Flow.ai is a rule-based chatbot platform using scripted responses and a knowledge base, not an LLM/generative AI system
2. The intervention compares rule-based chatbot feedback vs. teacher feedback
3. While the study design and statistics would otherwise qualify, the intervention does not meet the "Generative AI" criterion

**Note:** If the inclusion criteria were expanded to include "AI-assisted feedback" regardless of generative vs. rule-based distinction, this study would be includable with the following effect sizes:
- Learning Performance (Chapter 1): d approximately 0.78 (estimated from mean difference and standard errors)
- Learning Performance (Chapter 4): d approximately 0.26

---

## Summary of Decisions

| Study | Decision | Primary Reason |
|-------|----------|----------------|
| Yilmaz & Yilmaz (2023) | **INCLUDE** | Meets all criteria: quasi-experimental, ChatGPT, higher education, learning outcomes |
| Huang (2025) | **EXCLUDE** | Not experimental, not higher education, not generative AI |
| Yin, Goh & Hu (2024) | **EXCLUDE** | Rule-based chatbot (Flow.ai), not generative AI |

---

## Data to Add to Effect Sizes Dataset

For Yilmaz & Yilmaz (2023), the following rows should be added to the meta-analysis dataset:

| Study_ID | ES_ID | Title | Year | Authors | Outcome_Name | Outcome_Dimension | Blooms_Level | n_Treatment | n_Control | M_Treatment | SD_Treatment | M_Control | SD_Control | Hedges_g | SE_g |
|----------|-------|-------|------|---------|--------------|-------------------|--------------|-------------|-----------|-------------|--------------|-----------|------------|----------|------|
| NEW | NEW_01 | The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation | 2023 | Ramazan Yilmaz; Fatma Gizem Karaoglan Yilmaz | Computational Thinking | cognitive | apply | 21 | 24 | 126.73 | 8.34 | 112.61 | 15.32 | 1.09 | 0.32 |
| NEW | NEW_02 | The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation | 2023 | Ramazan Yilmaz; Fatma Gizem Karaoglan Yilmaz | Programming Self-Efficacy | affective | - | 21 | 24 | 41.32 | 5.84 | 33.52 | 7.64 | 1.11 | 0.32 |
| NEW | NEW_03 | The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation | 2023 | Ramazan Yilmaz; Fatma Gizem Karaoglan Yilmaz | Learning Motivation | affective | - | 21 | 24 | 96.50 | 7.62 | 85.17 | 13.84 | 0.97 | 0.31 |

**Note:** Hedges' g values are slightly adjusted from Cohen's d using the small sample correction factor: g = d * (1 - 3/(4*df - 1)) where df = n1 + n2 - 2

---

## Recommendations

1. **Add Yilmaz & Yilmaz (2023)** to the meta-analysis dataset with three effect sizes (computational thinking, self-efficacy, motivation)

2. **Domain coding:** This study should be coded as:
   - Domain: Programming/Computer Science
   - GenAI Tool: ChatGPT
   - Setting: Higher Education (Undergraduate)

3. **Quality assessment:** The study has adequate methodological quality with:
   - Pretest-posttest control group design
   - ANCOVA controlling for pretest differences
   - Appropriate sample size for detecting large effects
   - Clear description of intervention

4. **Limitation note:** The sample size (N=45) is relatively small, which may affect generalizability

---

*Report generated: January 26, 2025*
*Reviewer: Claude Code (Automated Screening)*
