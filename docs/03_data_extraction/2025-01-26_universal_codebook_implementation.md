# Universal Meta-Analysis Codebook Implementation

## Project: GenAI in Higher Education Meta-Analysis

**Version**: V8 + Universal Codebook v2.1
**Date**: 2026-01-26
**Codex Review**: APPROVE WITH MINOR CHANGES

---

## Overview

This document describes the implementation of the Universal Meta-Analysis Codebook v2.1 for the GenAI in Higher Education meta-analysis project. The codebook enables AI-Human collaboration for data extraction and verification, ensuring 100% human-verified data.

---

## Architecture: Four-Layer Design

```
┌─────────────────────────────────────────────────────────────────────┐
│              UNIVERSAL META-ANALYSIS CODEBOOK v2.1                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LAYER 1: IDENTIFIERS + METADATA (10 fields)                        │
│  study_id, es_id, citation, doi, year, design_type,                │
│  timepoint, arm_label_treat, arm_label_control, unit_of_analysis   │
│                                                                     │
│  LAYER 2: CORE STATISTICAL VALUES (18 fields)                       │
│  - Primary: outcome_name → se_g (12)                                │
│  - Change-score: pre_mean_treat, pre_sd_treat, pre_post_corr (3)   │
│  - Cluster: cluster_size, icc, n_clusters (3)                      │
│                                                                     │
│  LAYER 3: AI EXTRACTION PROVENANCE                                  │
│  Per-value: ai_value, source, method, confidence, derived_from     │
│  Stored as: ai_extraction_json                                     │
│                                                                     │
│  LAYER 4: HUMAN VERIFICATION (8 fields)                             │
│  verified_status, verified_by, verified_date, corrections_json,    │
│  disagreement_resolved, final_values_json, verification_notes,     │
│  sign_off                                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow: AI-Human Collaboration

### Phase 1: AI Extraction (Automated)
- ScholaRAG builds RAG from PDFs
- C6-DataIntegrityGuard extracts statistical values
- Multiple methods (RAG, OCR) run in parallel
- Provenance recorded for all extractions
- Hedges' g calculated where inputs complete

### Phase 2: Triage (Automated)
- C7-ErrorPreventionEngine categorizes by confidence
- Categories: HIGH (≥90%), MEDIUM (70-89%), LOW (<70%), CONFLICT
- Priority queue generated for human review

### Phase 3: Human Review (Mandatory)
- **ALL rows require human verification**
- Priority: Conflicts → Low → Medium → High
- Verify AI extraction against PDF
- Correct errors, record reason
- Mark as VERIFIED or REJECTED

### Phase 4: Final Validation (C5)
- All gates pass
- All rows verified
- All sign-offs complete
- Result: 100% Human-Verified Dataset

---

## Field Specifications

### Layer 1: Identifiers + Metadata

| Field | Type | Description |
|-------|------|-------------|
| study_id | str | Unique study identifier |
| es_id | str | Effect size ID (study_id + sequence) |
| citation | str | Full APA citation |
| doi | str | Digital Object Identifier |
| year | int | Publication year |
| design_type | str | RCT, QUASI, PRE_POST |
| timepoint | str | post, follow_up_3m |
| arm_label_treat | str | Treatment group label |
| arm_label_control | str | Control group label |
| unit_of_analysis | str | individual, cluster |

### Layer 2: Core Statistical Values

#### Primary Statistics (12 fields)

| Field | Type | Required |
|-------|------|----------|
| outcome_name | str | Yes |
| outcome_unit | str | No |
| es_type | str | Yes |
| analysis_type | str | No |
| n_treatment | int | Yes |
| n_control | int | Yes |
| m_treatment | float | Conditional |
| sd_treatment | float | Conditional |
| m_control | float | Conditional |
| sd_control | float | Conditional |
| hedges_g | float | Derived |
| se_g | float | Derived |

#### Change-Score Fields (3 fields, conditional)

| Field | Type | When Used |
|-------|------|-----------|
| pre_mean_treat | float | es_type = CHANGE |
| pre_sd_treat | float | es_type = CHANGE |
| pre_post_corr | float | es_type = CHANGE |

#### Cluster Fields (3 fields, conditional)

| Field | Type | When Used |
|-------|------|-----------|
| cluster_size | float | unit_of_analysis = cluster |
| icc | float | unit_of_analysis = cluster |
| n_clusters | int | unit_of_analysis = cluster |

### Layer 3: AI Extraction Provenance

Stored in `ai_extraction_json`:

```json
{
  "n_treatment": {
    "ai_value": 43,
    "source": "Table 2, p.8",
    "method": "OCR",
    "confidence": 85,
    "derived_from": null
  }
}
```

### Layer 4: Human Verification

| Field | Type | Values |
|-------|------|--------|
| verified_status | str | PENDING, PROVISIONAL, VERIFIED, REJECTED |
| verified_by | str | Reviewer initials |
| verified_date | date | Review date |
| corrections_json | json | Corrections made |
| disagreement_resolved | bool | Conflict resolved? |
| final_values_json | json | Human-confirmed values |
| verification_notes | str | Free text notes |
| sign_off | bool | Final approval |

---

## Confidence Thresholds

### Per-Field Thresholds

| Field | HIGH | MEDIUM | LOW |
|-------|------|--------|-----|
| n (sample size) | ≥95% | 80-94% | <80% |
| M (mean) | ≥90% | 70-89% | <70% |
| SD | ≥85% | 65-84% | <65% |
| hedges_g (derived) | ≥92% | 75-91% | <75% |

### Per-Source Modifiers

| Source | Modifier |
|--------|----------|
| Structured table | +10% |
| Semi-structured figure | +5% |
| Unstructured text | 0% |
| Abstract only | -15% |
| OCR with artifacts | -20% |

---

## Conflict Resolution

### Extraction Hierarchy

| Priority | Source | Weight |
|----------|--------|--------|
| 1 | Table cell | 1.0 |
| 2 | Figure data | 0.9 |
| 3 | In-text stats | 0.8 |
| 4 | Abstract | 0.5 |

### Tolerance Thresholds

| Value Type | Relative | Absolute |
|------------|----------|----------|
| n (sample size) | 5% | 2 |
| M (mean) | 10% | 0.5 |
| SD | 15% | 0.5 |

---

## GenAI-HE Project Specifics

### Dataset Summary (V8)

- **Total Effect Sizes**: 365
- **With Hedges' g**: 243 (66.6%)
- **Missing Hedges' g**: 122 (33.4%)
- **Total Studies**: 66

### ES Type Distribution

| ES Type | Count | Percentage |
|---------|-------|------------|
| POST_BETWEEN | - | Primary |
| ANCOVA | - | Secondary |
| CHANGE | - | Tertiary |
| PRE_POST | - | Last resort |
| PRE_TEST | 0 | REJECTED |

### Data Tiers

| Tier | Completeness | Count | Action |
|------|--------------|-------|--------|
| 1 | ≥70% | - | Auto-provisional |
| 2 | 40-69% | - | Recommended review |
| 3 | <40% | - | Required review |

---

## Integration with Diverga

### C5-MetaAnalysisMaster
- Orchestrates workflow
- Final validation
- Gate progression decisions

### C6-DataIntegrityGuard
- Extraction with provenance
- Hedges' g calculation
- SD recovery strategies

### C7-ErrorPreventionEngine
- Triage functionality
- Conflict detection
- Review queue generation

---

## Files

| File | Description |
|------|-------------|
| `GenAI_MetaAnalysis_v8.csv` | Raw data |
| `GenAI_MetaAnalysis_v8.xlsx` | Excel version |
| `GenAI_MetaAnalysis_v8_VERIFICATION.xlsx` | Universal Codebook format |

---

## References

- Borenstein et al. (2021). Introduction to Meta-Analysis
- Cochrane Handbook Chapter 6: Extracting Data
- PRISMA 2020 Statement
- Diverga CLAUDE.md (v6.3.0)
- Universal Codebook Plan v2.1

---

*Created: 2026-01-26*
*Author: Claude Code*
