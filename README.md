# Effectiveness of Generative AI on Learning Outcomes in Higher Education: A Three-Level Meta-Analysis

[![OSF](https://img.shields.io/badge/OSF-Open%20Science%20Framework-blue)](https://osf.io/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Author Information

**Hosung You**
College of Education, Pennsylvania State University
Email: hosung@psu.edu

## Abstract

This pre-registered three-level meta-analysis synthesized evidence on Generative AI (GenAI) effectiveness for learning outcomes in higher education. Systematic searches across seven databases identified **46 studies** (k = 251 effect sizes; N = 5,778 participants) published between November 2022 and December 2025. Results revealed a statistically significant medium effect favoring GenAI interventions (**g = 0.525**, 95% CI [0.303, 0.747], p < .001).

## Repository Structure

```
OSF/
├── data/
│   ├── raw/                          # Original unprocessed data
│   │   └── meta_analysis_effects_unified_with_moderators_refilled_tt.csv
│   └── processed/                    # Cleaned/corrected data for analysis
│       └── meta_analysis_HE_corrected.csv
│
├── analysis/
│   └── three_level_meta_analysis.R   # Main R analysis script
│
├── manuscript/
│   ├── GenAI_HE_MetaAnalysis_Manuscript_REVISED.docx  # Final manuscript
│   ├── figures/
│   │   ├── forest_plot_corrected.png
│   │   ├── funnel_plot_corrected.png
│   │   ├── forest_by_dimension_corrected.png
│   │   └── PRISMA_2020_FlowDiagram.png
│   └── tables/
│       └── Table3_Included_Studies.docx
│
├── supplementary/
│   ├── prisma/
│   │   ├── PRISMA_2020_FlowDiagram.pdf
│   │   └── PRISMA_2020_FlowDiagram.png
│   ├── codebook/
│   │   └── meta_analysis_codingbook.md
│   └── protocol/
│       └── META_ANALYSIS_EXTRACTION_PROTOCOL.md
│
└── README.md                         # This file
```

## Key Results

### Overall Effect
| Statistic | Value |
|-----------|-------|
| Pooled Hedges' g | 0.525 |
| 95% CI | [0.303, 0.747] |
| p-value | < .001 |
| Interpretation | Medium effect favoring GenAI |

### Heterogeneity
| Level | I² | τ² |
|-------|-----|-----|
| Total | 96.2% | - |
| Level 2 (within-study) | 44.8% | 0.230 |
| Level 3 (between-study) | 51.4% | 0.264 |

### Effects by Outcome Dimension
| Dimension | k | Hedges' g | 95% CI |
|-----------|---|-----------|--------|
| Behavioral | 23 | 0.765 | [0.412, 1.118] |
| Affective | 63 | 0.723 | [0.489, 0.957] |
| Cognitive | 148 | 0.599 | [0.341, 0.857] |
| Metacognitive | 17 | 0.216 | [-0.089, 0.521] |

### Publication Bias Assessment
- **PET Intercept:** -0.611 (95% CI: [-1.286, 0.064])
- **Interpretation:** No significant small-study bias detected

## Sample Characteristics
- **Studies screened:** 63 (met eligibility criteria)
- **Studies in quantitative synthesis:** 46 (with extractable effect sizes)
- **Effect sizes:** 251 (with valid Hedges' g and SE)
- **Total participants:** 5,778
- **Publication years:** 2023-2025

## Data Corrections Applied
1. **Winsorized outliers:** 14 effect sizes with |g| > 3 capped at ±3.0
2. **Study coding corrections:** 8 outcomes recoded from metacognitive to affective/behavioral
3. **Population filter:** K-12 studies excluded (higher education focus only)

## Software Requirements

### R (version 4.0+)
```r
install.packages(c("metafor", "clubSandwich", "ggplot2", "dplyr"))
```

### Required R Packages
| Package | Version | Purpose |
|---------|---------|---------|
| metafor | ≥4.0 | Meta-analysis models |
| clubSandwich | ≥0.5 | Robust variance estimation |
| ggplot2 | ≥3.4 | Visualization |
| dplyr | ≥1.1 | Data manipulation |

## Reproducing the Analysis

1. Clone this repository or download from OSF
2. Set working directory to `analysis/`
3. Run the R script:
```r
source("three_level_meta_analysis.R")
```

## Data Dictionary

See `supplementary/codebook/meta_analysis_codingbook.md` for complete variable descriptions.

### Key Variables in Dataset
| Variable | Description |
|----------|-------------|
| study_id | Unique study identifier (1-46) |
| outcome_id | Unique outcome identifier within study |
| hedges_g | Standardized mean difference (Hedges' g) |
| se_g | Standard error of effect size |
| outcome_dimension | Cognitive, Affective, Behavioral, or Metacognitive |
| blooms_category | Lower-order or Higher-order cognitive skills |
| n_treatment | Treatment group sample size |
| n_control | Control group sample size |

## Pre-registration

This study was pre-registered on OSF. The pre-registration protocol includes:
- Research questions and hypotheses
- Inclusion/exclusion criteria
- Search strategy
- Coding procedures
- Planned analyses

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Citation

```bibtex
@article{you2025genai,
  title={Effectiveness of Generative AI on Learning Outcomes in Higher Education: A Three-Level Meta-Analysis},
  author={You, Hosung},
  journal={[Journal TBD]},
  year={2025},
  institution={Pennsylvania State University}
}
```

## Contact

For questions about this research, please contact:

**Hosung You**
College of Education
Pennsylvania State University
Email: hosung@psu.edu

## Acknowledgments

This research was conducted at the College of Education, Pennsylvania State University.
