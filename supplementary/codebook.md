# Codebook for Meta-Analysis Data Extraction

## Variable Definitions

### Study Identification

| Variable | Description | Values |
|----------|-------------|--------|
| Study_ID | Unique study identifier | Integer (1-70) |
| ES_ID | Effect size identifier | String (XXX_YY format) |
| Title | Full study title | Text |
| Year | Publication year | Integer (2022-2025) |
| Authors | Author names | Text (semicolon separated) |

### Outcome Variables

| Variable | Description | Values |
|----------|-------------|--------|
| Outcome_Name | Name of measured outcome | Text |
| Outcome_Dimension | AIMC classification | cognitive, affective, metacognitive, behavioral |
| Blooms_Level | Bloom's taxonomy level | remember, understand, apply, analyze, evaluate, create |

### Sample Information

| Variable | Description | Values |
|----------|-------------|--------|
| n_Treatment | Treatment group sample size | Integer |
| n_Control | Control group sample size | Integer |

### Effect Size Data

| Variable | Description | Values |
|----------|-------------|--------|
| M_Treatment | Treatment group mean | Numeric |
| SD_Treatment | Treatment group SD | Numeric |
| M_Control | Control group mean | Numeric |
| SD_Control | Control group SD | Numeric |
| Hedges_g | Standardized effect size (Hedges' g) | Numeric |
| SE_g | Standard error of g | Numeric |

### Data Quality

| Variable | Description | Values |
|----------|-------------|--------|
| Verification_Status | Data verification level | NOT_CHECKED, PARTIALLY_VERIFIED, OCR_VERIFIED, MANUAL_VERIFIED |
| Verification_Confidence | Confidence percentage | 0-100 |
| Data_Tier | Data quality tier | 1 (highest) - 3 (lowest) |

### Moderator Variables

| Variable | Description | Values |
|----------|-------------|--------|
| Discipline | Academic discipline | STEM, Health Sciences, Social Sciences, Humanities, etc. |
| GenAI_Tool | AI tool used | ChatGPT, Bard, Claude, Custom, etc. |
| Study_Design | Research design | RCT, Quasi-experimental |
| Duration_Weeks | Intervention duration | Integer |
| Country | Study location | Country name |

---

*Last updated: 2025-01-26*
