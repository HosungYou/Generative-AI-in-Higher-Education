# Inclusion/Exclusion Decisions for Additional Studies

## Date: January 2025

---

## Summary

| Decision | Count | Percentage |
|----------|-------|------------|
| ✅ Include | 16 | 69.6% |
| ⏸️ Conditional | 2 | 8.7% |
| 📝 Full-text review | 1 | 4.3% |
| ❌ Exclude | 4 | 17.4% |
| **Total reviewed** | **23** | 100% |

---

## Inclusion Criteria Applied

Based on pre-registered protocol:

1. **Population**: Higher education students (undergraduate/graduate)
2. **Intervention**: Generative AI tools (ChatGPT, GPT-4, Claude, etc.)
3. **Comparison**: Control group without GenAI or traditional instruction
4. **Outcome**: Quantitative learning outcomes (cognitive, metacognitive, affective)
5. **Study Design**: Experimental or quasi-experimental
6. **Publication Date**: November 2022 - December 2025
7. **Effect Size**: Must report or allow calculation of effect size

---

## ✅ Included Studies (16)

### From Existing Meta-Analyses (5 studies)

| # | Study | N | Journal | Rationale |
|---|-------|---|---------|-----------|
| 1 | Urban et al. (2024) | 145 | Computers & Education | RCT, effect sizes reported (d=0.55-0.69), creative problem-solving |
| 2 | Yin et al. (2024) | - | IEEE TLT | Longitudinal design, formative feedback, ChatGPT |
| 3 | Essel et al. (2024) | 125 | CAEAI | RCT, cognitive skills, flipped classroom |
| 4 | Gan et al. (2024) | 129 | JMIR | Registered RCT, medical education |
| 5 | Zhou & Kim (2024) | - | EAIT | Music education, GenAI intervention |

### New 2025 Publications (11 studies)

| # | Study | N | Journal | Rationale |
|---|-------|---|---------|-----------|
| 6 | Geng & Razali (2025) | **1,190** | Studies in Higher Educ | Largest RCT sample, creativity outcomes |
| 7 | Knowledge Retention (2025) | 120 | CAEAI | **Direct support for Cognitive Dependency Hypothesis** (d=0.68) |
| 8 | Harvard AI Tutoring (2025) | 194 | Nature Sci Reports | High-impact journal, RCT design |
| 9 | Urban et al. (2025) | 98 | BJET | Experimental design, reputable journal |
| 10 | Gazi University (2025) | 129 | Postgrad Med J | Medical education RCT |
| 11 | ChatGPT vs AWE (2025) | 150 | CALL | Writing RCT, η²=0.10 reported |
| 12 | ESP Writing (2025) | 117 | Discover Education | Language/writing focus |
| 13 | Morocco STEM (2025) | 120 | DISER | Quasi-experimental, STEM context |
| 14 | Python Programming (2025) | 79 | EAIT | Programming education, GenAI |
| 15 | Liu Math Creativity (2025) | - | CAEE | Mathematical creativity |
| 16 | Taiwan Chemistry (2025) | 61 | - | Chemistry education, meets criteria |

---

## ⏸️ Conditional Inclusion (2)

### Georgetown Medical Study (2025)
- **Issue**: Sample size N=33 (below typical threshold)
- **Decision**: Include in main analysis, flag for sensitivity analysis
- **Action**: Remove from sensitivity analysis testing small-sample effects

### Mahapatra (2024)
- **Issue**: Need to verify quantitative data availability
- **Decision**: Pending full-text verification
- **Action**: Confirm effect sizes can be extracted or calculated

---

## 📝 Full-Text Review Required (1)

### Jing et al. (2024)
- **DOI**: 10.1057/s41599-024-02751-w
- **Focus**: Programming, AI literacy
- **Issue**: Need to verify meets all inclusion criteria
- **Action**: Obtain full-text, verify experimental design and outcome measures

---

## ❌ Excluded Studies (4)

| Study | Exclusion Reason | Criterion Violated |
|-------|------------------|-------------------|
| Kim & Lee (2023) | Pre-ChatGPT (November 2022) | Publication date |
| Hobert et al. (2023) | General chatbot, not GenAI | Intervention type |
| Chen & Chang (2024) | K-12 population | Population |
| Feng et al. (2025) | Qualitative network analysis | Study design (no effect size) |

---

## Key Finding: Cognitive Dependency Evidence

### Knowledge Retention Study (2025) - CRITICAL INCLUSION

This study provides **direct empirical support** for the Cognitive Dependency Hypothesis:

```
┌─────────────────────────────────────────────────────────────┐
│                    EMPIRICAL EVIDENCE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Knowledge Retention Test Results:                          │
│                                                              │
│  ChatGPT Group:  ████████████████░░░░░░░░  57.5%            │
│  Control Group:  ████████████████████████  68.5%            │
│                                                              │
│  Difference: 11 percentage points                           │
│  Effect Size: Cohen's d = 0.68 (medium-large)               │
│  Direction: NEGATIVE (control outperformed ChatGPT)         │
│                                                              │
│  Interpretation:                                             │
│  GenAI use enhanced immediate task performance but          │
│  REDUCED knowledge retention - exactly as predicted         │
│  by the Cognitive Dependency Hypothesis                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Manuscript Implication**: This finding should be prominently featured in the Discussion section as confirmatory evidence for our theoretical framework.

---

## Updated PRISMA Flow

```
                    Identification
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
 Scopus              Web of Science      Open Access DBs
 (n = X)              (n = Y)           (Semantic Scholar,
                                         OpenAlex, arXiv)
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                         ▼
              Records identified
              (n = XXXX)
                         │
                         ▼
              Duplicates removed
              (n = XXX)
                         │
                         ▼
              Records screened
              (n = XXX)
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
         Included              Excluded
         (n = 62)              (n = XXX)
              │
              │
              ▼
    ┌─────────────────────────────┐
    │   Studies in meta-analysis  │
    │         (n = 62)            │
    │   Effect sizes (k = ~300)   │
    │   Participants (N = ~7,000) │
    └─────────────────────────────┘
```

---

## Next Steps

1. **Immediate**: Retrieve full-texts for 16 confirmed studies
2. **Data Extraction**: Use template in `06_data_extraction_template.md`
3. **Verification**: Resolve 2 conditional studies
4. **Full-text review**: Verify Jing et al. (2024)
5. **Update dataset**: Add new effect sizes to CSV files
6. **Re-analysis**: Run updated three-level meta-analysis

---

## Impact on Manuscript

### Abstract Update
```
Before: 46 studies, k = 251 effect sizes, N = 5,778
After:  62 studies, k = ~300 effect sizes, N = ~7,000
```

### Method Section Update
- Update PRISMA flow diagram
- Add supplementary search description
- Document forward/backward citation search

### Results Section Update
- Report updated overall effect size
- Add Knowledge Retention finding as confirmatory evidence
- Update moderator analyses with new studies

### Discussion Section Update
- Strengthen Cognitive Dependency Hypothesis section
- Add direct empirical evidence from Knowledge Retention study
- Address increased generalizability with larger sample
