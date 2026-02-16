# Manuscript Version History — Two-Paper Strategy

**Author:** Hosung You, Pennsylvania State University

---

## Project Structure (Reorganized 2026-02-16)

This project produces two independent but complementary papers from a shared gold standard dataset:

| Paper | Title | Status | File |
|-------|-------|--------|------|
| **A** | Generative AI in Higher Education: A Three-Level Meta-Analysis Revealing Cognitive Dependency in Metacognitive Outcomes | Draft (v4.0, to be updated with re-coded data) | `Paper_A_MetaAnalysis_v4.0.md` |
| **B** | LLM-Assisted Coding for Systematic Reviews: A Three-Model Comparative Framework | Scaffold (v1.0, awaiting data collection) | `Paper_B_AI_Coding_Methodology_v1.0.md` |

### Relationship Between Papers

```
Paper A (Meta-Analysis)                    Paper B (Methodology)
    |                                           |
    +-- Gold standard human coding ----------->-+-- Benchmark for AI evaluation
    |                                           |
    +-- Substantive findings (no AI mention)    +-- AI vs. human comparison
    |                                           |
    +-- Independent submission                  +-- References Paper A dataset
```

- **Paper A** uses only human-coded data. It makes no reference to AI-assisted coding.
- **Paper B** compares LLM coding against Paper A's gold standard.
- Paper A must be completed first (gold standard required as benchmark).

---

## Current File Structure

```
manuscript/versions/
├── CHANGELOG.md                              # This file
├── Paper_A_MetaAnalysis_v4.0.md              # Paper A — meta-analysis
├── Paper_B_AI_Coding_Methodology_v1.0.md     # Paper B — AI coding methodology
└── archive/                                  # Superseded intermediate drafts
    ├── GenAI_HE_MetaAnalysis_v1.0_Original.docx
    ├── GenAI_HE_MetaAnalysis_v2.0_EPR_Revision.md
    ├── GenAI_HE_MetaAnalysis_v2.1_Outcome_Operationalization.md
    ├── GenAI_HE_MetaAnalysis_v2.2_Classification_Table.md
    ├── GenAI_HE_MetaAnalysis_v2.3.md
    ├── GenAI_HE_MetaAnalysis_v3.0_AIMC_Framework.md
    └── REVISION_DIFF_SUMMARY.md
```

---

## Paper A Version History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2025-01-21 | Original manuscript (archived) |
| v2.0 | 2025-01-22 | EPR submission revision — power analysis, PRISMA figures, metacognitive operationalization (archived) |
| v2.1 | 2026-01-22 | Comprehensive outcome dimension operationalization (archived) |
| v2.2 | 2026-01-22 | Effect size classification table, table renumbering (archived) |
| v2.3 | 2026-01-25 | Minor updates (archived) |
| v3.0 | 2026-01-26 | AIMC Framework integration — major theoretical revision (archived) |
| **v4.0** | **2026-02-16** | **Final dataset with study exclusions (60 studies, 343 ES). Current working version.** |

**Next for Paper A**: Updated systematic search (through Feb 2026) → complete re-coding with dual human coders → revised analysis with Bayesian meta-analysis addition.

## Paper B Version History

| Version | Date | Description |
|---------|------|-------------|
| **v1.0** | **2026-02-16** | **Scaffold — complete structure with placeholders for empirical sections** |

**Next for Paper B**: Finalize prompt library → run AI extractions (Claude, GPT-4o, Gemini) → compute accuracy metrics → populate results → write discussion.

---

## Restructuring Notes (2026-02-16)

### What Changed

1. **Archived v1.0–v3.0**: These intermediate drafts are superseded by v4.0. Moved to `archive/` to reduce directory clutter while preserving git history.

2. **Renamed v4.0**: `GenAI_HE_MetaAnalysis_v4.0_Final_Dataset.md` → `Paper_A_MetaAnalysis_v4.0.md` to clearly indicate its role as Paper A.

3. **Created Paper B scaffold**: `Paper_B_AI_Coding_Methodology_v1.0.md` — complete manuscript structure (Introduction, Method, Results, Discussion) with [PLACEHOLDER] markers for empirical content. All methodological decisions (models, metrics, consensus strategies, workflow comparisons) are finalized.

4. **Archived REVISION_DIFF_SUMMARY.md**: Technical diff details for v1→v2 changes, no longer needed for active development.

### What Was Preserved

- All archived files remain in `archive/` and in git history.
- Paper A content is unchanged (only filename changed).
- CHANGELOG simplified to reflect two-paper structure.

---

## Supporting Materials

| File | Location | Description |
|------|----------|-------------|
| Coding Manual | `docs/GenAI_MetaAnalysis_Coding_Manual_v10.docx` | 15-section Word document with all variable definitions |
| Excel Template | `data/GenAI_MetaAnalysis_v10_TEMPLATE.xlsx` | 9-sheet workbook for data collection |
| Coding Script | `scripts/create_coding_manual.py` | Python script to regenerate the Word manual |

---

## Target Journals

### Paper A
- **Primary**: BJET / Computers & Education / ETR&D (educational technology)
- **Alternative**: Educational Psychology Review, Internet and Higher Education

### Paper B
- **TBD** — candidates: JASIST, Systematic Reviews, Research Synthesis Methods

---

*Changelog maintained by: Claude Code*
*Last updated: 2026-02-16 (two-paper restructuring)*
