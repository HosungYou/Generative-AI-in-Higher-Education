# 6-Phase Validated Re-coding Pipeline (v11.0)

**Date**: 2026-02-05
**Author**: Hosung You
**Based on**: AI-Ethics-HR-Review 6-Phase Architecture

---

## Overview

The v11 re-coding pipeline introduces a rigorous 6-phase validated coding approach adapted from the AI-Ethics-HR-Review project. It uses multi-model consensus (Claude Sonnet + GPT-4o + Groq Llama 3.3) with human verification to achieve ≥85% accuracy on 11 key fields.

## Pipeline Flow

```
Phase 0 (RAG Index) → Phase 1 (Claude Extract) + Effect Size Fill
    → Phase 2 (3-Model Consensus)
    → Phase 3 (Stratified Sampling for Human Verification)
    → [HUMAN PAUSE: Researcher codes 14-20 studies]
    → Phase 4 (Inter-Coder Reliability)
    → Phase 5 (Discrepancy Resolution)
    → Phase 6 (QA Gates + Final CSV)
```

## Usage

```bash
# Smoke test (5 studies, Phase 0-2)
python scripts/recode_v11/run_pipeline.py --smoke-test

# Full automated phases
python scripts/recode_v11/run_pipeline.py --phase 0-3

# After human coding template is filled
python scripts/recode_v11/run_pipeline.py --phase 4-6

# Full pipeline
python scripts/recode_v11/run_pipeline.py --full
```

## Phase Details

### Phase 0: RAG Index Build
- Processes 71 PDFs with PyMuPDF
- Creates ChromaDB vector store with all-MiniLM-L6-v2 embeddings
- Chunk size: 1000, overlap: 200
- Cost: $0 (local embeddings)

### Phase 1: RAG-based Claude Extraction
- Extracts 9 categorical fields using field-specific prompts
- Study-level fields (7): study_design, control_condition, genai_tool, genai_tool_version, intervention_duration, education_level, discipline
- Outcome-level fields (2): blooms_level, outcome_dimension
- Low confidence (<0.75) auto-flagged for Phase 5
- Estimated cost: ~$3.16

### Effect Size Filler (parallel with Phase 1)
- 4-tier imputation for missing Hedges' g and SE_g
- Tier 1: Direct calculation from M, SD, n (99%+ accuracy)
- Tier 2: RAG extraction from PDF statistics (85-90%)
- Tier 3: t/F/p conversion to Cohen's d → Hedges' g (80-85%)
- Tier 4: Flag as manual_needed
- Estimated cost: ~$3.60

### Phase 2: Multi-Model Consensus
- 3 models verify independently: Claude Sonnet, GPT-4o, Groq Llama 3.3
- Consensus rules by field type:
  - Categorical: 2/3 exact match (MAJORITY)
  - Ordinal: 2/3 with 1-level tolerance (NEAR_CONCORDANT)
  - Numerical: 5% relative tolerance (CONCORDANT)
  - Critical fields (study_design, blooms_level, outcome_dimension): 3/3 unanimous
- Discordant items queued for Phase 5
- Estimated cost: ~$3.23

### Phase 3: Human Verification Sampling
- 20% stratified sample (14-20 studies from 70)
- Stratification: Bloom's level coverage, study design, discipline
- 60% oversampling of low-confidence studies
- Generates CSV template for independent human coding

### Phase 4: Inter-Coder Reliability
- Categorical: Cohen's κ (target ≥ 0.85)
- Ordinal: Weighted κ quadratic (target ≥ 0.80)
- Numerical: ICC(2,1) (target ≥ 0.95) + MAE < 0.05
- Also computes Krippendorff's α for 3-model agreement

### Phase 5: Discrepancy Resolution
- Priority: Human gold standard > AI consensus > Claude tiebreaker
- Categorical: majority vote or Claude tiebreaker
- Ordinal: median of 3 models
- Numerical: mean of concordant; >10% diff → human review
- All decisions logged to audit trail

### Phase 6: QA Gates + Final CSV
- 6 quality gates must pass before CSV generation
- Generates GenAI_MetaAnalysis_v11_FINAL.csv (27 columns)
- R/metafor compatible format

## Configuration

All settings in `configs/recode_v11/pipeline_config.yaml`:
- Model selection and parameters
- RAG settings (chunk size, embedding model)
- Consensus rules and thresholds
- Quality gate thresholds
- Cost budget ($50)

## File Structure

```
scripts/recode_v11/
├── run_pipeline.py         # Master orchestrator
├── schema.py               # 11-field schema
├── phase0_rag_index.py     # RAG index build
├── phase1_extract.py       # Claude extraction
├── effect_size_filler.py   # 4-tier ES imputation
├── phase2_consensus.py     # 3-model consensus
├── phase3_sampling.py      # Human verification sampling
├── phase4_reliability.py   # ICR calculation
├── phase5_resolution.py    # Discrepancy resolution
├── phase6_qa.py            # QA gates + final CSV
├── prompts/                # 9 field-specific prompts
└── utils/                  # Shared utilities
    ├── metrics.py          # Statistical metrics
    ├── audit.py            # Audit trail
    ├── confidence.py       # Confidence calibration
    ├── llm_clients.py      # Unified LLM client
    ├── data_loader.py      # CSV loader
    └── cost_tracker.py     # Cost tracking
```

## Estimated Costs

| Phase | Cost |
|-------|------|
| Phase 0 (RAG) | $0 |
| Phase 1 (Claude) | ~$3.16 |
| Effect Size Fill | ~$3.60 |
| Phase 2 (3-model) | ~$3.23 |
| Phase 3-6 (local) | $0 |
| Buffer | ~$2.00 |
| **Total** | **~$12** |
