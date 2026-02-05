# Documentation: GenAI Meta-Analysis Project

This folder contains all project documentation organized by category.

**Last Updated**: 2025-01-27
**Project**: Generative AI in Education Meta-Analysis

---

## Directory Structure

```
docs/
├── 01_literature_search/     # Literature review and search strategy
├── 02_study_selection/       # Inclusion/exclusion decisions
├── 03_data_extraction/       # Extraction templates, codebooks, pipelines
├── 04_methodology/           # Statistical methods, effect size recovery
├── 05_manuscript/            # Manuscript drafts and updates
├── 06_decisions/             # Key research decisions and rationale
└── README.md
```

---

## 01_literature_search/

Documents related to literature identification and search strategy.

| File | Description |
|------|-------------|
| `2025-01-26_literature_review_update.md` | Summary of related meta-analyses |
| `2025-01-26_search_strategy_revision.md` | Database search strategy |
| `2025-01-26_overlap_analysis.md` | Overlap analysis with existing meta-analyses |
| `2025-01-26_additional_studies.md` | Additional study candidates |
| `2025-01-26_missing_studies_analysis.md` | Analysis of missing studies |
| `2025-01-26_new_studies_review.md` | Review of newly identified studies |

---

## 02_study_selection/

Documents related to study screening and selection decisions.

| File | Description |
|------|-------------|
| `2025-01-26_differentiation_strategy.md` | Strategy for differentiating from prior meta-analyses |
| `2025-01-26_inclusion_decisions.md` | Final inclusion/exclusion decisions |
| `2025-01-26_exclusion_rationale.md` | Detailed rationale for exclusions |
| `2025-01-26_pdf_retrieval_list.md` | DOI links and retrieval instructions |

---

## 03_data_extraction/

Documents related to data extraction methodology and implementation.

| File | Description |
|------|-------------|
| `2025-01-26_extraction_template.md` | Data extraction template |
| `2025-01-26_genai_he_codebook.md` | GenAI-HE specific codebook extension |
| `2025-01-26_universal_codebook_implementation.md` | Universal Codebook v2.2 implementation |
| `2025-01-26_c5_c6_c7_agent_rationale.md` | Diverga agent rationale (C5, C6, C7) |
| `2025-01-27_extraction_pipeline_v9.md` | V9.0 extraction pipeline documentation |
| `2026-02-05_recode_pipeline_v11.md` | V11.0 6-Phase Validated Re-coding Pipeline documentation |

---

## 04_methodology/

Documents related to statistical methodology and analysis approaches.

| File | Description |
|------|-------------|
| `2025-01-26_hedges_g_recovery_plan.md` | Plan for recovering missing Hedges' g values |
| `2025-01-26_methodology_improvement_report.md` | V7 methodology improvements |
| `2025-01-26_meta_analysis_comparison.md` | Comparison with other meta-analyses |

---

## 05_manuscript/

Documents related to manuscript preparation and revisions.

| File | Description |
|------|-------------|
| `2025-01-26_manuscript_updates_v3.md` | Manuscript updates (V3) |
| `2025-01-26_manuscript_updates_v4.md` | Manuscript updates (V4) |
| `2025-01-26_discussion_text.md` | Discussion section text |

---

## 06_decisions/

Key research decisions with rationale and approval.

| File | Description |
|------|-------------|
| `2025-01-27_scope_expansion_k12_inclusion.md` | **Decision to include K-12 studies** with education level as moderator |

---

## Current Status

### Study Counts (V9.0 Extraction)

| Metric | Count |
|--------|-------|
| Total Studies | 70 |
| Effect Sizes | 146 |
| Higher Education | 63 |
| K-12 | 7 |

### Current Pipeline: V11.0 Re-coding

| Feature | Value |
|---------|-------|
| Re-coding Fields | 11 (2 subjective, 7 operational, 2 numerical) |
| Models | Claude Sonnet + GPT-4o + Groq Llama 3.3 |
| Human Verification | 20% stratified sample |
| Quality Target | Cohen's κ ≥ 0.85, Weighted κ ≥ 0.80 |

### Key Decisions

1. **2025-01-27**: Scope expanded to include K-12 studies
   - Education level added as moderator variable
   - Manuscript title revision required: "Higher Education" → "Education"
   - See `06_decisions/2025-01-27_scope_expansion_k12_inclusion.md`

### Pipeline Versions

| Version | Date | Description |
|---------|------|-------------|
| V11.0 | 2026-02-05 | 6-Phase Validated Re-coding with multi-model consensus |
| V9.0 | 2025-01-27 | Groq-based extraction with Universal Codebook v2.2 |
| V8.x | 2025-01-26 | Previous extraction with SD recovery |
| V7.x | 2025-01-26 | Methodology improvements |

---

## Related Directories

- `/data/extractions_v9/` - V9.0 extraction JSON files
- `/data/03_final/` - Final Excel outputs and analysis reports
- `/scripts/` - Extraction and analysis scripts
- `/manuscript/current/` - Current manuscript draft
