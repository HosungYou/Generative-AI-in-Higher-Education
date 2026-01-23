# Effectiveness of Generative AI on Learning Outcomes in Higher Education: A Three-Level Meta-Analysis

[![PRISMA 2020](https://img.shields.io/badge/PRISMA-2020%20Compliant-green.svg)](http://prisma-statement.org/)
[![OSF](https://img.shields.io/badge/OSF-Open%20Science%20Framework-blue)](https://osf.io/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Author Information

**Hosung You**
College of Education, Pennsylvania State University
Email: hosung@psu.edu

## Abstract

This pre-registered three-level meta-analysis synthesized evidence on Generative AI (GenAI) effectiveness for learning outcomes in higher education. Systematic searches across seven databases identified **65 studies** (k = 381 effect sizes; N = 8,247 participants) published between November 2022 and January 2026. Results revealed a statistically significant medium effect favoring GenAI interventions (**g = 0.622**, 95% CI [0.389, 0.855], p < .001).

**Key Theoretical Contribution**: The *Cognitive Dependency Hypothesis* — GenAI demonstrates robust positive effects on immediate cognitive and affective outcomes but attenuated effects on metacognitive development, suggesting potential cognitive offloading that may impede self-regulatory skill acquisition.

---

## Repository Structure

```
Generative-AI-in-Higher-Education/
│
├── 📄 README.md                          # This file
├── 📄 MASTER_INTEGRATION_DOCUMENT.md     # Central coordination document
├── 📄 MANUSCRIPT_REVISION_GUIDE.md       # Section-by-section revision guide
├── 📄 VERSION_CONTROL_AND_CHECKLIST.md   # Quality assurance and tracking
│
├── 📁 data/
│   ├── raw/                              # Original unprocessed data
│   │   └── meta_analysis_effects_unified_with_moderators_refilled_tt.csv
│   └── processed/                        # Cleaned/corrected data for analysis
│       └── meta_analysis_HE_corrected.csv
│
├── 📁 analysis/
│   └── three_level_meta_analysis.R       # Main R analysis script
│
├── 📁 manuscript/
│   └── versions/
│       ├── GenAI_HE_MetaAnalysis_v2.2_Classification_Table.md
│       └── GenAI_HE_MetaAnalysis_v2.3.md  # (To be created)
│
└── 📁 supplementary/
    ├── GRADE_Evidence_Certainty_Assessment.md      # NEW: GRADE evaluation
    ├── Winsorization_Protocol.md                   # NEW: Outlier treatment
    ├── Search_Strategy_Appendix.md                 # NEW: Complete search strings
    ├── Exploratory_Study_Statement.md              # NEW: HARKing defense
    ├── Metacognition_Construct_Validity_Solutions.md # NEW: Validity framework
    ├── prisma/
    │   ├── PRISMA_2020_FlowDiagram.pdf
    │   └── PRISMA_2020_FlowDiagram.png
    ├── codebook/
    │   └── meta_analysis_codingbook.md
    └── protocol/
        └── META_ANALYSIS_EXTRACTION_PROTOCOL.md
```

---

## Key Results (Updated v2.3)

### Overall Effect
| Statistic | Value |
|-----------|-------|
| Pooled Hedges' g | 0.622 |
| 95% CI | [0.389, 0.855] |
| p-value | < .001 |
| Studies (k) | 65 |
| Effect Sizes (n) | 381 |
| Total N | 8,247 |

### Heterogeneity
| Level | I² | τ² |
|-------|-----|-----|
| Total | 96.2% | - |
| Level 2 (within-study) | - | 0.312 |
| Level 3 (between-study) | - | 0.089 |

### Effects by Outcome Dimension (with GRADE Certainty)
| Dimension | k | n | Hedges' g | 95% CI | p | Certainty |
|-----------|---|---|-----------|--------|---|-----------|
| Cognitive | 58 | 218 | 0.64 | [0.42, 0.86] | < .001 | ⊕⊕⊕◯ Moderate |
| Affective | 28 | 89 | 0.61 | [0.29, 0.93] | < .001 | ⊕⊕◯◯ Low |
| Behavioral | 16 | 34 | 0.63 | [−0.12, 1.38] | .098 | ⊕◯◯◯ Very Low |
| Metacognitive | 11 | 40 | 0.28 | [−0.24, 0.80] | .287 | ⊕◯◯◯ Very Low |

### Publication Bias Assessment
- **PET Intercept:** Non-significant (no evidence of small-study bias)
- **Funnel plot:** Symmetric distribution

---

## Supplementary Materials (v2.3 Additions)

| Document | Description | Purpose |
|----------|-------------|---------|
| [GRADE Assessment](supplementary/GRADE_Evidence_Certainty_Assessment.md) | Evidence certainty by outcome | PRISMA Items 21-22 |
| [Winsorization Protocol](supplementary/Winsorization_Protocol.md) | Outlier treatment (\|g\| > 3.0) | Transparency |
| [Search Strategy](supplementary/Search_Strategy_Appendix.md) | 7 database search strings | PRISMA Items 6-7 |
| [Exploratory Statement](supplementary/Exploratory_Study_Statement.md) | Hypothesis generation disclosure | Limitations |
| [Metacognition Solutions](supplementary/Metacognition_Construct_Validity_Solutions.md) | 4-Pillar validity framework | Construct validity |
| [Codebook](supplementary/codebook/meta_analysis_codingbook.md) | Extraction protocol | Data dictionary |

---

## Theoretical Framework: AI-Integrated Metacognition (AIMC) Model

```
┌─────────────────────────────────────────────────────────────────┐
│              AIMC: AI-Integrated Metacognition Model            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Level 1: AI-Assisted Metacognition (With-AI Context)          │
│      • Prompt engineering as planning                          │
│      • Output evaluation as monitoring                         │
│                                                                 │
│  Level 2: Meta-AI Awareness (About-AI Knowledge)               │
│      • Understanding AI capabilities/limitations               │
│      • Evaluating AI output reliability                        │
│                                                                 │
│  Level 3: Independent Metacognition (Without-AI Transfer)      │
│      • Self-regulated learning without AI support              │
│      • Internalized monitoring/evaluation skills               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Corrections Applied

1. **Winsorized outliers:** 14 effect sizes with |g| > 3.0 capped at ±3.0 (from 4 studies)
2. **Study coding corrections:** Outcomes recoded per Flavell taxonomy
3. **Population filter:** K-12 studies excluded (higher education focus only)

---

## Software Requirements

### R (version 4.3+)
```r
install.packages(c("metafor", "clubSandwich", "brms", "bayestestR", "ggplot2", "dplyr"))
```

### Required R Packages
| Package | Version | Purpose |
|---------|---------|---------|
| metafor | ≥4.0 | Meta-analysis models |
| clubSandwich | ≥0.5 | Robust variance estimation |
| brms | ≥2.20 | Bayesian meta-analysis |
| bayestestR | ≥0.13 | Bayes Factor calculation |
| ggplot2 | ≥3.4 | Visualization |

---

## Reproducing the Analysis

1. Clone this repository
2. Set working directory to `analysis/`
3. Run the R script:
```r
source("three_level_meta_analysis.R")
```

---

## Pre-registration

This study was pre-registered on PROSPERO (CRD-XXXXX). Protocol deviations are documented in `supplementary/Exploratory_Study_Statement.md`.

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

---

## Citation

```bibtex
@article{you2026genai,
  title={Effectiveness of Generative AI on Learning Outcomes in Higher Education:
         A Three-Level Meta-Analysis},
  author={You, Hosung},
  journal={[Journal TBD]},
  year={2026},
  institution={Pennsylvania State University}
}
```

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| v2.2 | 2026-01-XX | Classification table integration |
| **v2.3** | **2026-01-23** | **Supplements, GRADE, validity solutions, integration docs** |

---

## Contact

**Hosung You**
College of Education
Pennsylvania State University
Email: hosung@psu.edu

---

## Acknowledgments

This research was conducted at the College of Education, Pennsylvania State University.

---

*Last updated: 2026-01-23*
