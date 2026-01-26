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

## Repository Structure (v5.0)

```
GenAI-HE-Review-AIMC/
│
├── README.md                              # This file
├── CHANGELOG.md                           # Version history
├── LICENSE                                # CC BY 4.0
├── MASTER_INTEGRATION_DOCUMENT.md         # Central coordination document
├── MANUSCRIPT_REVISION_GUIDE.md           # Section-by-section revision guide
├── VERSION_CONTROL_AND_CHECKLIST.md       # Quality assurance and tracking
│
├── data/
│   ├── 00_raw/                            # Original unmodified data
│   │   ├── GenAI_MetaAnalysis_Effects_Raw.csv
│   │   ├── GenAI_MetaAnalysis_Codebook.xlsx
│   │   ├── GenAI_MetaAnalysis_Coding_Data.xlsx
│   │   └── new_studies_to_add.csv
│   ├── 01_extracted/                      # Intermediate extraction files
│   │   ├── extracted_effect_sizes.csv
│   │   ├── extracted_effect_sizes.json
│   │   ├── corrected_effect_sizes.csv
│   │   └── extraction_summary.md
│   ├── 02_processed/                      # Cleaned/validated data
│   │   ├── meta_analysis_FINAL.csv
│   │   ├── GenAI_MetaAnalysis_Effects_Verified.csv
│   │   ├── GenAI_MetaAnalysis_FINAL_v4.xlsx
│   │   └── DATA_PROVENANCE.md
│   └── 03_final/                          # SINGLE SOURCE OF TRUTH
│       └── GenAI_MetaAnalysis_v5.csv      # 61 studies, 346 effect sizes
│
├── analysis/
│   ├── R/                                 # R analysis scripts
│   │   ├── three_level_meta_analysis.R
│   │   └── extended_sensitivity_analysis.R
│   └── output/                            # Analysis output (results, logs)
│
├── manuscript/
│   ├── current/                           # Active manuscript
│   ├── versions/                          # Historical versions
│   │   ├── GenAI_HE_MetaAnalysis_v2.2_Classification_Table.md
│   │   └── GenAI_HE_MetaAnalysis_v2.3.md
│   ├── figures/                           # Publication-ready figures
│   │   └── PRISMA_2020_FlowDiagram.png
│   └── tables/                            # Publication-ready tables
│       └── Table3_Included_Studies.docx
│
├── figures/
│   ├── source/                            # Source files (SVG, scripts)
│   │   └── AIMC_Framework_Organic.svg
│   ├── output/                            # Generated figures
│   ├── AIMC_Framework.png                 # Main framework figure
│   └── PRISMA_2020_Flow_Diagram.svg
│
├── scripts/
│   ├── data_processing/                   # Python data scripts
│   │   ├── convert_real_data_to_excel.py
│   │   ├── create_final_dataset.py
│   │   └── generate_coding_data.py
│   └── figure_generation/                 # Python figure scripts
│       ├── generate_aimc_framework.py
│       └── generate_aimc_organic.py
│
├── supplementary/                         # Supplementary materials
│   ├── GRADE_assessment.md
│   ├── search_strategy.md
│   └── codebook.md
│
├── docs/                                  # Documentation (01-10)
│   └── README.md
│
└── pdfs/                                  # Source PDFs (not in git)
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
| v2.3 | 2026-01-23 | Supplements, GRADE, validity solutions, integration docs |
| **v5.0** | **2026-01-26** | **Data update (Study 70: Yilmaz & Yilmaz 2023), folder reorganization** |

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

*Last updated: 2026-01-26*
