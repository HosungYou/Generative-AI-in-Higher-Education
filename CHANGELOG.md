# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [11.0.0] - 2026-02-05

### 6-Phase Validated Re-coding Pipeline

Major feature release: AI-Ethics-HR-Review's 6-Phase Validated Coding Pipeline adapted for GenAI-HE meta-analysis to improve SUBJECTIVE/OPERATIONAL coding accuracy to 85%+.

### Added

#### Pipeline Scripts (`scripts/recode_v11/`)

| File | Purpose |
|------|---------|
| `run_pipeline.py` | Master orchestrator (--phase 0-6, --smoke-test, --dry-run) |
| `schema.py` | 11-field schema: 2 subjective, 7 operational, 2 numerical |
| `phase0_rag_index.py` | ChromaDB RAG index from 71 PDFs (all-MiniLM-L6-v2) |
| `phase1_extract.py` | RAG-based Claude Sonnet extraction (9 categorical fields) |
| `effect_size_filler.py` | 4-tier missing Hedges' g / SE_g imputation |
| `phase2_consensus.py` | 3-model consensus (Claude + GPT-4o + Groq Llama 3.3) |
| `phase3_sampling.py` | Stratified 20% human verification sampling |
| `phase4_reliability.py` | ICR: Cohen's κ, Weighted κ, ICC(2,1), MAE |
| `phase5_resolution.py` | Discrepancy resolution (human > AI > tiebreaker) |
| `phase6_qa.py` | QA gates + GenAI_MetaAnalysis_v11_FINAL.csv generation |

#### Utility Modules (`scripts/recode_v11/utils/`)

| File | Source |
|------|--------|
| `metrics.py` | AI-Ethics-HR-Review + MAE/RMSE/accuracy extensions |
| `audit.py` | JSONL audit trail (from AI-Ethics-HR-Review) |
| `confidence.py` | Confidence calibration (from AI-Ethics-HR-Review) |
| `llm_clients.py` | Unified Claude/GPT-4o/Groq client with retry logic |
| `data_loader.py` | v8.1 CSV loader + Study_ID-PDF mapping |
| `cost_tracker.py` | API cost tracking ($50 budget enforcement) |

#### Field-Specific Prompts (`scripts/recode_v11/prompts/`)

9 extraction prompts: blooms_level, outcome_dimension, study_design, control_condition, genai_tool, genai_tool_version, intervention_duration, education_level, discipline

#### Configuration

- `configs/recode_v11/pipeline_config.yaml` - Master pipeline configuration

#### Data Structure

```
data/recode_v11/
├── 00_input/          # v8.1 CSV (365 rows, 70 studies)
├── 01_rag_index/      # ChromaDB vector store
├── 02_phase1_raw/     # Per-study Phase 1 JSON
├── 03_phase2_consensus/ # 3-model consensus results
├── 04_phase3_human/   # Human verification templates
├── 05_phase4_reliability/ # ICR reports
├── 06_phase5_resolutions/ # Resolution logs
├── 07_phase6_final/   # Final CSV + quality report
├── 08_effect_sizes/   # Effect size imputation results
└── audit/             # Pipeline audit trail (JSONL)
```

### Re-coding Fields (11)

| Category | Field | Type | Consensus Rule |
|----------|-------|------|----------------|
| Subjective | blooms_level | ordinal | 2/3 with 1-level tolerance |
| Subjective | outcome_dimension | categorical | 2/3 exact match |
| Operational | study_design | categorical | 3/3 unanimous (critical) |
| Operational | control_condition | categorical | 2/3 exact match |
| Operational | genai_tool | categorical | 2/3 exact match |
| Operational | genai_tool_version | categorical | 2/3 exact match |
| Operational | intervention_duration | ordinal | 2/3 with 1-level tolerance |
| Operational | education_level | categorical | 2/3 exact match |
| Operational | discipline | categorical | 2/3 exact match |
| Numerical | hedges_g | float | 5% relative tolerance |
| Numerical | se_g | float | 5% relative tolerance |

### Quality Targets

| Metric | Target | Acceptable |
|--------|--------|------------|
| Cohen's κ (categorical) | ≥ 0.85 | ≥ 0.80 |
| Weighted κ (ordinal) | ≥ 0.80 | ≥ 0.75 |
| ICC(2,1) (numerical) | ≥ 0.95 | ≥ 0.90 |
| MAE (Hedges' g) | < 0.05 | < 0.10 |
| Overall accuracy | ≥ 85% | ≥ 80% |
| Completeness | ≥ 95% | ≥ 90% |

### Architecture

- **Input**: v8.1 CSV (365 rows, 70 studies) + 71 PDFs
- **Output**: R/metafor compatible GenAI_MetaAnalysis_v11_FINAL.csv
- **Models**: Claude Sonnet 4.5 + GPT-4o + Groq Llama 3.3 70B
- **Estimated cost**: ~$12 (budget: $50)
- **Based on**: AI-Ethics-HR-Review 6-Phase Validated Coding Pipeline

---

## [6.0.0] - 2025-01-26

### V6 Meta-Analysis Update

Re-ran complete three-level meta-analysis with confirmed dataset.

### Dataset Statistics (V6)

| Metric | V5 | V6 | Change |
|--------|----|----|--------|
| Total Study IDs | 61 | 66 | +5 |
| Total effect sizes | 346 | 375 | +29 |
| Valid ES (with g & SE) | 155 | 168 | +13 |
| Studies with valid ES | 38 | 41 | +3 |
| Participants | 18,691 | 21,580 | +2,889 |

### Analysis Results (V6)

| Metric | V5 | V6 |
|--------|----|----|
| Overall g | 0.770 | 0.719 |
| 95% CI | [0.439, 1.101] | [0.389, 1.050] |
| I^2 Total | 99.1% | 99.2% |
| tau^2 Level 2 | 0.697 | 0.749 |
| tau^2 Level 3 | 0.814 | 0.980 |

### Key Findings Confirmed

- **Cognitive dependency hypothesis still supported**
  - Metacognitive outcomes: g = 0.51, non-significant (p = .167)
  - Cognitive outcomes: g = 0.70, significant (p < .001)
  - Affective outcomes: g = 0.91, significant (p < .001)
- Publication bias indicators persist (PET intercept significant)
- RCT-only analysis: g = 0.11, non-significant (k = 5 studies)

### Files Added

- `data/03_final/GenAI_MetaAnalysis_v6.csv`
- `analysis/R/three_level_meta_analysis_v6.R`
- `analysis/output/v6_results/forest_plot_v6.png`
- `analysis/output/v6_results/funnel_plot_v6.png`
- `analysis/output/v6_results/meta_analysis_v6_results.rds`
- `analysis/output/v6_results/meta_analysis_v6_results.md`
- `manuscript/current/v6_CHANGES.md`

### Confirmed Exclusions

Study IDs not in dataset: 9, 18, 39, 61

### Recovered Studies

Study IDs 10, 17, 20, 51, 56 included in V6

---

## [5.0.0] - 2025-01-26

### Data Update and Project Reorganization

Major reorganization of folder structure and final dataset verification.

### Added

#### Study 70: Yilmaz & Yilmaz (2023)
- **Title**: "The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation"
- **Effect sizes**: 3 (Computational Thinking, Programming Self-Efficacy, Learning Motivation)
- **Sample**: n=21 treatment, n=24 control
- **Verification**: MANUAL_VERIFIED, 100% confidence, Tier 1

#### New Folder Structure
```
data/
  00_raw/          - Original unmodified data
  01_extracted/    - Intermediate extraction files
  02_processed/    - Cleaned/validated data
  03_final/        - SINGLE SOURCE OF TRUTH (GenAI_MetaAnalysis_v5.csv)
analysis/
  R/               - R analysis scripts
  output/          - Analysis results
scripts/
  data_processing/ - Python data scripts
  figure_generation/ - Python figure scripts
manuscript/
  current/         - Active manuscript
  versions/        - Historical versions
  figures/         - Publication figures
  tables/          - Publication tables
figures/
  source/          - Source files (SVG, scripts)
  output/          - Generated figures
supplementary/     - GRADE, search strategy, codebook
```

### Changed

- Reorganized all data files into semantic subdirectories
- Moved Python scripts from data/ and figures/ to scripts/
- Moved R scripts to analysis/R/
- Created v5 final dataset as single source of truth

### Dataset Statistics (v5)

| Metric | Value |
|--------|-------|
| Total Studies | 61 (unique IDs) |
| Total Effect Sizes | 346 |
| Study ID Range | 1-70 (with gaps) |
| Verification Tiers | 1 (highest) to 3 |

---

## [1.1.0] - 2025-01-06

### Theoretical Framework Enhancement: Empirical Support for Cognitive Dependency Hypothesis

This release strengthens the manuscript's theoretical framework by integrating recent empirical research that directly supports the Cognitive Dependency Hypothesis—our central theoretical contribution.

### Added

#### New Citations in Theoretical Framework

| Paper | Section | Key Contribution |
|-------|---------|------------------|
| **Yan (2025)** | Introduction | Comprehensive review of GenAI's cognitive, metacognitive, and epistemic implications—identifies both positive effects (personalized guidance) and risks (diminished epistemic vigilance, superficial learning) |
| **Kos'myna (2025)** | Cognitive Load Theory | MIT Media Lab EEG study demonstrating neural evidence of "cognitive debt"—progressive decline in brain engagement over 4 months of ChatGPT use |
| **Fan et al. (2025)** | Self-Regulated Learning | Introduced "metacognitive laziness" concept—empirical evidence that GenAI reduces engagement in self-reflection, planning, and self-evaluation |
| **Tankelevitch et al. (2024)** | Self-Regulated Learning | CHI 2024 paper on metacognitive demands of GenAI—paradox that GenAI requires metacognition but may erode it through frequent use |
| **Gerlich (2025)** | Automation Bias | Large-scale study (n=666) finding r = -0.75 correlation between AI usage and critical thinking, with cognitive offloading as mediating mechanism |

#### New Citations in Discussion

| Location | Addition |
|----------|----------|
| SRL Perspective | Fan et al.'s "metacognitive laziness" as explanation for g = 0.23 metacognitive finding |
| Comparison with Prior Meta-Analyses | Bastani et al. (17% transfer failure) and Kos'myna (4-month cognitive decline) as mechanistic evidence |

#### New References Added

```
Fan, Y., Zhang, L., & Wang, M. (2025). Beware of metacognitive laziness: Effects of
    generative artificial intelligence on learning motivation, processes, and
    performance. British Journal of Educational Technology, 56(2), 456-478.

Gerlich, M. (2025). AI tools in society: Impacts on cognitive offloading and the
    future of critical thinking. Societies, 15(1), 6.

Kos'myna, N. (2025). Your brain on ChatGPT: Accumulation of cognitive debt when
    using an AI assistant for essay writing task. MIT Media Lab Working Paper.

Tankelevitch, L., Kewenig, V., Simkute, A., Scott, A. E., Sarkar, A., & Sellen, A.
    (2024). The metacognitive demands and opportunities of generative AI.
    Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems, 1-24.

Yan, L. (2025). Beyond efficiency: Empirical insights on generative AI's impact on
    cognition, metacognition and epistemic agency in learning. British Journal of
    Educational Technology. Advance online publication.
```

### Changed

- **Word count**: 10,376 → 10,930 words (+554 words)
- **Reference count**: ~85 → ~90 references (+5 new empirical studies)
- **File size**: 44.6KB → 46.0KB

### Theoretical Significance

These additions strengthen the manuscript by:

1. **Neural Evidence**: Kos'myna (2025) provides EEG-based neural evidence for the cognitive dependency hypothesis, demonstrating that the pattern is not merely behavioral but reflects measurable changes in brain activation patterns.

2. **Convergent Terminology**: The "metacognitive laziness" concept (Fan et al., 2025) provides independent terminological validation of our theoretical framework—different researchers arriving at similar conclusions through different methodologies.

3. **Effect Size Corroboration**: Gerlich's (2025) finding of r = -0.75 between AI use and critical thinking provides additional quantitative support for the cognitive dependency concern, with younger participants showing higher vulnerability.

4. **Temporal Dynamics**: Both Kos'myna (2025) and Bastani et al. (2024) demonstrate that cognitive dependency effects emerge and strengthen over time, supporting our recommendation for "strategic rather than continuous AI use."

5. **Metacognitive Paradox**: Tankelevitch et al. (2024) articulate the paradox that GenAI requires metacognition for effective use but may erode the very skills needed—a self-reinforcing dependency cycle.

---

## [1.0.0] - 2025-01-06

### Initial Release

First comprehensive release of the meta-analysis dataset, analysis code, and manuscript.

### Included

#### Data
- Raw meta-analysis data (251 effect sizes from 46 studies)
- Processed data with winsorized outliers and corrected codings
- Full moderator variables (outcome dimension, Bloom's taxonomy, discipline, GenAI tool)

#### Analysis
- Three-level meta-analysis R script using metafor and clubSandwich
- Robust variance estimation with CR2 small-sample corrections
- Publication bias assessment (PET, PET-PEESE, trim-and-fill)
- Sensitivity analyses (leave-one-out, RCT-only, outlier exclusion)

#### Manuscript
- Complete manuscript in APA 7th Edition format
- Theoretical framework integrating 6 theories:
  - Cognitive Load Theory
  - Desirable Difficulties Theory
  - Self-Regulated Learning Theory
  - Self-Determination Theory
  - Sociocultural Learning Theory
  - Automation Bias and Cognitive Offloading
- Cognitive Dependency Hypothesis as primary theoretical contribution
- 5 Tables (Study characteristics, Heterogeneity, Moderator analyses)
- 4 Figures (Forest plot, Funnel plot, Dimension forest, PRISMA diagram)

#### Supplementary Materials
- PRISMA 2020 flow diagram (PDF and PNG)
- Complete coding book
- Meta-analysis extraction protocol

### Key Findings

| Finding | Value | Interpretation |
|---------|-------|----------------|
| Overall effect | g = 0.525 | Medium positive effect |
| Metacognitive effect | g = 0.23 (ns) | Supports cognitive dependency hypothesis |
| Cognitive effect | g = 0.54* | Significant positive |
| Affective effect | g = 0.55* | Significant positive |
| Medicine/Health | g = 0.64* | Strongest discipline effect |
| ChatGPT | g = 0.63* | Most studied tool, significant |

---

## Version History Summary

| Version | Date | Focus |
|---------|------|-------|
| 5.0.0 | 2025-01-26 | Data update (Study 70) + folder reorganization |
| 1.1.0 | 2025-01-06 | Theoretical framework enhancement with 5 new empirical citations |
| 1.0.0 | 2025-01-06 | Initial comprehensive release |
