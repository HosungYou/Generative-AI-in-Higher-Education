# Detailed Rationale for Inclusion/Exclusion Decisions

## Date: January 2025
## Reviewer: Claude Code (AI-assisted systematic review)

---

## Pre-Registered Inclusion Criteria

Based on PRISMA 2020 guidelines and meta-analysis protocol:

| Criterion | Requirement |
|-----------|-------------|
| **P** (Population) | Higher education students (undergraduate, graduate, postgraduate) |
| **I** (Intervention) | Generative AI tools (ChatGPT, GPT-3.5, GPT-4, Claude, Gemini, etc.) |
| **C** (Comparison) | Control group without GenAI OR traditional instruction |
| **O** (Outcome) | Quantitative learning outcomes with effect size calculable |
| **S** (Study Design) | Experimental or quasi-experimental |
| **T** (Time) | Published November 2022 - December 2025 |
| **L** (Language) | English |

### Additional Quality Criteria
- Minimum sample size: N ≥ 20 (per group preferred)
- Effect size: Must be reported or calculable from statistics
- Peer-reviewed or preprint with rigorous methodology

---

## ⏸️ Conditional Inclusion: Detailed Rationale

### 1. Georgetown Medical Study (2025)

**Citation**: Georgetown University Medical Education Study (2025)
**DOI**: 10.7759/cureus.85767
**Journal**: Cureus

| Criterion | Assessment |
|-----------|------------|
| Population | ✅ Medical students (higher education) |
| Intervention | ✅ ChatGPT |
| Comparison | ✅ Control group |
| Outcome | ✅ Knowledge assessment |
| Study Design | ✅ RCT |
| Time | ✅ 2025 |

**Issue Identified**: **Small Sample Size (N=33)**

```
┌─────────────────────────────────────────────────────────────┐
│                    SAMPLE SIZE CONCERN                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Total N = 33                                                │
│  Treatment: ~16-17 participants                              │
│  Control:   ~16-17 participants                              │
│                                                              │
│  Statistical Power Analysis:                                 │
│  - For d = 0.5 (medium effect), power = 0.34 (inadequate)   │
│  - For d = 0.8 (large effect), power = 0.56 (marginal)      │
│  - Recommended minimum: N = 64 per group for d = 0.5        │
│                                                              │
│  Risk: Inflated effect size estimates due to small sample   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Decision**: CONDITIONAL INCLUSION

**Rationale**:
1. Study meets all PICOS criteria
2. Small sample doesn't disqualify per protocol (no minimum N specified)
3. However, small samples can inflate effect sizes (small study effects)
4. Medical education context is valuable for generalizability

**Resolution Plan**:
- Include in main analysis
- Flag in sensitivity analysis as "small sample" (N < 50)
- Report results with and without this study
- Document in limitations section

---

### 2. Mahapatra (2024)

**Citation**: Mahapatra, S. (2024)
**Journal**: [To be verified]

| Criterion | Assessment |
|-----------|------------|
| Population | ✅ Higher education |
| Intervention | ✅ ChatGPT |
| Comparison | ⚠️ Needs verification |
| Outcome | ⚠️ Quantitative data availability unclear |
| Study Design | ⚠️ Needs verification |
| Time | ✅ 2024 |

**Issue Identified**: **Quantitative Data Verification Needed**

```
┌─────────────────────────────────────────────────────────────┐
│                DATA AVAILABILITY CONCERN                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Information from secondary source (other meta-analyses)    │
│  Primary source not yet reviewed                            │
│                                                              │
│  Uncertainties:                                              │
│  1. Are means and SDs reported for both groups?             │
│  2. Is the comparison group truly a control?                │
│  3. What specific outcomes were measured?                   │
│  4. Is the design truly experimental?                       │
│                                                              │
│  Without full-text verification, cannot confirm eligibility │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Decision**: CONDITIONAL INCLUSION

**Rationale**:
1. Appeared in multiple prior meta-analyses (Sun & Zhou, Liu et al.)
2. Likely meets criteria based on prior inclusion
3. However, independent verification required for rigor
4. Cannot assume prior meta-analyses applied identical criteria

**Resolution Plan**:
- Retrieve full-text PDF
- Verify experimental design with control group
- Confirm effect size data availability (M, SD, N or F, t, p)
- If criteria met: Include
- If criteria not met: Exclude with documented reason

---

## 📝 Full-Text Review Required: Detailed Rationale

### Jing et al. (2024)

**Citation**: Jing, Y., et al. (2024)
**DOI**: 10.1057/s41599-024-02751-w
**Journal**: Humanities and Social Sciences Communications (Nature)

| Criterion | Assessment |
|-----------|------------|
| Population | ⚠️ Likely higher education (needs confirmation) |
| Intervention | ⚠️ AI/Programming focus - GenAI component unclear |
| Comparison | ⚠️ Needs verification |
| Outcome | ⚠️ Programming + AI literacy - specific measures unclear |
| Study Design | ⚠️ Needs verification |
| Time | ✅ 2024 |

**Issue Identified**: **Intervention and Outcome Clarity**

```
┌─────────────────────────────────────────────────────────────┐
│                INTERVENTION CLARITY CONCERN                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Study Focus: Programming education + AI literacy           │
│                                                              │
│  Questions requiring full-text review:                      │
│                                                              │
│  1. INTERVENTION TYPE                                        │
│     - Is this GenAI (ChatGPT, GPT) or general AI tools?     │
│     - Does it involve LLM-based code generation?            │
│     - Or is it AI literacy education ABOUT GenAI?           │
│                                                              │
│  2. OUTCOME MEASURES                                         │
│     - Programming skills: cognitive outcome ✓               │
│     - AI literacy: depends on how measured                  │
│     - Are these learning outcomes or attitudes?             │
│                                                              │
│  3. STUDY DESIGN                                             │
│     - Experimental with control?                            │
│     - Pre-post comparison?                                  │
│     - Correlation study?                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Decision**: FULL-TEXT REVIEW REQUIRED

**Rationale**:
1. Nature portfolio journal (high quality indicator)
2. Programming education is relevant to GenAI meta-analysis
3. However, "AI literacy" could be conceptual knowledge, not GenAI intervention
4. Need to distinguish: Learning WITH GenAI vs. Learning ABOUT GenAI
5. Only the former meets our inclusion criteria

**Resolution Plan**:
- Retrieve full-text from DOI
- Verify intervention is GenAI tool use (not AI education)
- Confirm experimental/quasi-experimental design
- Check for quantitative learning outcomes
- Decision after review:
  - If GenAI intervention + experimental + learning outcomes: Include
  - If AI education about GenAI (not using it): Exclude
  - If correlational/qualitative only: Exclude

---

## ❌ Excluded Studies: Detailed Rationale

### 1. Kim & Lee (2023)

**Citation**: Kim, J., & Lee, H. (2023)
**DOI**: 10.1007/s11528-022-00788-9
**Journal**: TechTrends

| Criterion | Assessment | Result |
|-----------|------------|--------|
| Population | ✅ Higher education | Pass |
| Intervention | ❌ Pre-ChatGPT chatbot | **FAIL** |
| Time | ❌ Published before Nov 2022 scope | **FAIL** |

**Exclusion Reason**: **Intervention Type - Not Generative AI**

```
┌─────────────────────────────────────────────────────────────┐
│                    EXCLUSION RATIONALE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Publication Date: 2023 (but research conducted pre-2022)   │
│  DOI timestamp: 10.1007/s11528-022-00788-9                  │
│                      ^^^^                                    │
│                   Published 2022                             │
│                                                              │
│  Technology Used: Rule-based or retrieval chatbot           │
│  NOT: Large Language Model (GPT-3.5, GPT-4, etc.)          │
│                                                              │
│  ChatGPT Release: November 30, 2022                         │
│  This study: Pre-dates ChatGPT availability                 │
│                                                              │
│  Our Focus: Generative AI (LLM-based tools)                 │
│  This Study: Traditional chatbot technology                 │
│                                                              │
│  CONCLUSION: Does not represent GenAI intervention          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Final Decision**: EXCLUDE
**Criterion Violated**: Intervention (not GenAI), Time (pre-ChatGPT era)

---

### 2. Hobert et al. (2023)

**Citation**: Hobert, S., et al. (2023)
**DOI**: 10.1016/j.ijhcs.2023.103108
**Journal**: International Journal of Human-Computer Studies

| Criterion | Assessment | Result |
|-----------|------------|--------|
| Population | ✅ Higher education | Pass |
| Intervention | ❌ General chatbot (not GenAI) | **FAIL** |
| Comparison | ✅ Control group | Pass |
| Outcome | ✅ Active learning (ICAP framework) | Pass |

**Exclusion Reason**: **Intervention Type - Not Generative AI**

```
┌─────────────────────────────────────────────────────────────┐
│                    EXCLUSION RATIONALE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Study Focus: Chatbots for active learning                  │
│  Framework: ICAP (Interactive, Constructive, Active, Passive)│
│                                                              │
│  Chatbot Type Analysis:                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Rule-based chatbot    │ ← Hobert et al. used this   │    │
│  │ - Scripted responses  │                             │    │
│  │ - Decision trees      │                             │    │
│  │ - Pattern matching    │                             │    │
│  ├───────────────────────┼─────────────────────────────┤    │
│  │ Generative AI chatbot │ ← Our inclusion criteria    │    │
│  │ - LLM-powered         │                             │    │
│  │ - ChatGPT, GPT-4      │                             │    │
│  │ - Novel text generation│                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  The study does NOT use LLM-based generative AI             │
│  Results not generalizable to GenAI interventions           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Final Decision**: EXCLUDE
**Criterion Violated**: Intervention (traditional chatbot, not LLM-based GenAI)

---

### 3. Chen & Chang (2024)

**Citation**: Chen, X., & Chang, Z. (2024)
**DOI**: 10.1007/s10639-024-12553-x
**Journal**: Education and Information Technologies

| Criterion | Assessment | Result |
|-----------|------------|--------|
| Population | ❌ K-12 students | **FAIL** |
| Intervention | ✅ AI game-based learning | Pass |
| Comparison | ✅ Control group | Pass |
| Outcome | ✅ Learning outcomes (N=202) | Pass |
| Study Design | ✅ Experimental | Pass |

**Exclusion Reason**: **Population - Not Higher Education**

```
┌─────────────────────────────────────────────────────────────┐
│                    EXCLUSION RATIONALE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Target Population: K-12 (Primary/Secondary)                │
│  Our Population:    Higher Education Only                   │
│                                                              │
│  Sample: N = 202 students                                   │
│  Grade Level: Elementary or Middle School                   │
│                                                              │
│  Why This Matters:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ K-12 Context          │ Higher Education Context   │    │
│  ├───────────────────────┼─────────────────────────────┤    │
│  │ Developmental stage   │ Adult learners             │    │
│  │ Scaffolded curriculum │ Self-directed learning     │    │
│  │ Teacher-centered      │ Learner autonomy           │    │
│  │ Basic skills focus    │ Complex problem-solving    │    │
│  │ Different GenAI use   │ Research/writing focus     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Findings may not generalize to university students         │
│  Mixing populations would increase heterogeneity            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Final Decision**: EXCLUDE
**Criterion Violated**: Population (K-12, not higher education)

**Note**: This study could be valuable for a K-12 focused meta-analysis.

---

### 4. Feng et al. (2025)

**Citation**: Feng, Y., et al. (2025)
**DOI**: 10.1111/bjet.13611
**Journal**: British Journal of Educational Technology

| Criterion | Assessment | Result |
|-----------|------------|--------|
| Population | ✅ Higher education | Pass |
| Intervention | ✅ GenAI | Pass |
| Comparison | ⚠️ Not applicable | N/A |
| Outcome | ❌ No quantitative effect size | **FAIL** |
| Study Design | ❌ Qualitative/Network analysis | **FAIL** |

**Exclusion Reason**: **Study Design - No Quantitative Effect Size**

```
┌─────────────────────────────────────────────────────────────┐
│                    EXCLUSION RATIONALE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Study Type: Qualitative Network Analysis                   │
│  Our Requirement: Quantitative Effect Sizes                 │
│                                                              │
│  What This Study Does:                                       │
│  - Analyzes relationships/patterns in GenAI use             │
│  - Network visualization of concepts                        │
│  - Qualitative thematic analysis                            │
│                                                              │
│  What Meta-Analysis Requires:                               │
│  - Mean differences (M₁ - M₂)                               │
│  - Standard deviations (SD₁, SD₂)                           │
│  - Sample sizes (n₁, n₂)                                    │
│  - OR: F-statistics, t-statistics, p-values                 │
│  - OR: Correlation coefficients (r)                         │
│                                                              │
│  This study provides: Network metrics, not effect sizes     │
│  Cannot calculate: Cohen's d, Hedges' g, or similar         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Study Output        │ Meta-Analysis Input Required │    │
│  ├─────────────────────┼─────────────────────────────────┤  │
│  │ Network centrality  │ Mean difference (d)           │    │
│  │ Thematic codes      │ Variance (SE)                 │    │
│  │ Qualitative themes  │ Sample size per group         │    │
│  │        ❌           │           ✓                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Final Decision**: EXCLUDE
**Criterion Violated**: Study design (qualitative), Outcome (no effect size calculable)

**Note**: This study may be valuable for the qualitative synthesis section of a mixed-methods systematic review.

---

## Summary Decision Matrix

| Study | P | I | C | O | S | T | Decision |
|-------|---|---|---|---|---|---|----------|
| Georgetown (2025) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⏸️ Conditional (small N) |
| Mahapatra (2024) | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⏸️ Conditional (verify) |
| Jing et al. (2024) | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | 📝 Full-text review |
| Kim & Lee (2023) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ Exclude |
| Hobert et al. (2023) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ Exclude |
| Chen & Chang (2024) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ Exclude |
| Feng et al. (2025) | ✅ | ✅ | N/A | ❌ | ❌ | ✅ | ❌ Exclude |

**Legend**: P=Population, I=Intervention, C=Comparison, O=Outcome, S=Study Design, T=Time

---

## Appendix: PRISMA 2020 Reporting

### Item 16b: Reasons for Exclusion

For PRISMA flow diagram, exclusion reasons should be reported as:

```
Records excluded after full-text review (n = 4):
  - Not generative AI intervention (n = 2)
  - K-12 population, not higher education (n = 1)
  - Qualitative design, no effect size (n = 1)
```

### Sensitivity Analysis Plan

For conditional inclusions, report:

```
Sensitivity Analysis 1: Excluding small samples (N < 50)
  - Main analysis: k = 62, g = [value]
  - Excluding Georgetown (2025): k = 61, g = [value]
  - Difference: Δg = [value]

Sensitivity Analysis 2: Studies requiring verification
  - Main analysis: k = 62
  - Excluding unverified Mahapatra: k = 61
  - Results: [report if substantially different]
```
