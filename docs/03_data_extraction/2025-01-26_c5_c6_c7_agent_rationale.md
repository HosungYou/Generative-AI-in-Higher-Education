# C5/C6/C7 Meta-Analysis Agent Rationale

## Document Purpose
This document explains why new specialized agents (C5-MetaAnalysisMaster, C6-DataIntegrityGuard, C7-ErrorPreventionEngine) are necessary based on critical issues discovered during V7 development of the GenAI in Higher Education meta-analysis.

---

## Executive Summary

During V5→V6→V7 dataset evolution, several **systemic failures** were identified that existing Diverga agents could not prevent:

| Issue | Impact | Root Cause |
|-------|--------|------------|
| Pre-test effect sizes included | 10 invalid ES analyzed | No temporal classification gate |
| 42% missing Hedges' g | 155/365 ES unusable | SD extraction failure |
| SD data loss during processing | 15% values lost | No data integrity tracking |
| Study count confusion | Reported 40 vs actual 66 | Missing study-level validation |

**Conclusion**: Existing extraction agents (B2, B3) focus on individual values but lack **orchestration**, **integrity verification**, and **proactive error prevention**.

---

## Part 1: Problems Discovered in V7 Development

### 1.1 Pre-Test Effect Size Contamination

**What Happened**:
- V6 included 10 pre-test effect sizes as independent outcomes
- These measure baseline differences, not treatment effects
- Violates Effect Size Selection Hierarchy

**Example from Data**:
```
ES_ID: 45-1  Outcome: "Pre-test critical thinking"  ← INVALID
ES_ID: 45-2  Outcome: "Post-test critical thinking" ← VALID
```

**Why Existing Agents Failed**:
- B3-EffectSizeExtractor extracts what's in the paper
- No gate to classify temporal nature (pre/post/change)
- No auto-reject rule for pre-test outcomes

**Required Solution**: Gate 4a - Temporal Classification Validation

---

### 1.2 SD Extraction Failure (42% Missing Hedges' g)

**What Happened**:
- 155 of 365 effect sizes have missing Hedges' g
- Root cause: Missing SD values (only 18% available in missing rows)
- Original coding data had 72.8% SD → V5_VERIFICATION had 58.1%
- 15% of SD values lost during processing

**Why Existing Agents Failed**:
- B3-EffectSizeExtractor extracts if present
- No fallback mechanism for unreported SD
- No tracking of data completeness across versions

**Required Solution**:
- C6-DataIntegrityGuard: Track data completeness
- Multi-source SD recovery strategies

---

### 1.3 Study Count vs Effect Size Count Confusion

**What Happened**:
- Report claimed "40 studies" when actual count was 66
- Confusion between studies WITH valid Hedges' g (45) vs total studies (66)
- 21 studies have ALL effect sizes missing Hedges' g

**Why Existing Agents Failed**:
- No study-level aggregation validation
- Effect size validation doesn't bubble up to study level

**Required Solution**: C6 with study-level integrity checks

---

### 1.4 Effect Size Selection Hierarchy Violations

**Proper Hierarchy** (discovered through Copilot discussion):

| Priority | Type | Use When |
|----------|------|----------|
| 1 (Best) | Post-test between-groups | Control group exists |
| 2 | ANCOVA-adjusted | Pre-test as covariate |
| 3 | Change score | No between-group post |
| 4 (Last) | Single-group pre-post | No control group |
| NEVER | Pre-test as outcome | Never valid |

**Why Existing Agents Failed**:
- No classification of ES types
- No priority enforcement when multiple ES available from same study

---

## Part 2: Why New Agents Are Needed

### 2.1 Gap Analysis: Current vs Required Capabilities

| Capability | B2 | B3 | C4 | NEEDED |
|------------|----|----|----|----|
| Extract individual ES | - | ✓ | - | ✓ |
| Classify ES temporal type | - | - | - | **C5** |
| Track data completeness | - | - | - | **C6** |
| Multi-gate validation | - | - | - | **C5** |
| Proactive error detection | - | - | - | **C7** |
| Orchestrate full workflow | - | - | Partial | **C5** |
| SD recovery strategies | - | - | - | **C6** |
| Hedges' g calculation | - | ✓ | - | **C6** |

### 2.2 Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    C5-MetaAnalysisMaster                    │
│                   (7-Phase Orchestrator)                    │
├─────────────────────────────────────────────────────────────┤
│ Phase 1: Study Selection    → Uses existing B1/B2          │
│ Phase 2: Data Extraction    → Orchestrates B3 + C6         │
│ Phase 3: Effect Size Calc   → Multi-gate validation        │
│ Phase 4: Quality Assessment → Bias, heterogeneity          │
│ Phase 5: Analysis Execution → Model selection              │
│ Phase 6: Sensitivity        → Leave-one-out, subgroups     │
│ Phase 7: Reporting          → PRISMA, forest plots         │
└─────────────────────────────────────────────────────────────┘
         ↓                              ↓
┌─────────────────────┐    ┌─────────────────────────────────┐
│ C6-DataIntegrityGuard│    │   C7-ErrorPreventionEngine     │
├─────────────────────┤    ├─────────────────────────────────┤
│ • Version tracking  │    │ • Pre-extraction warnings       │
│ • Data completeness │    │ • Pattern-based error detect    │
│ • Hedges' g calc    │    │ • Anomaly detection             │
│ • SD recovery       │    │ • Checkpoint enforcement        │
│ • Study-level agg   │    │ • Error taxonomy application    │
└─────────────────────┘    └─────────────────────────────────┘
```

---

## Part 3: Agent Specifications

### 3.1 C5-MetaAnalysisMaster

**Purpose**: Orchestrate complete meta-analysis workflow with multi-gate validation

**Key Features**:
1. **Multi-Gate Validation Pipeline**
   - Gate 1: Extraction Validation (completeness check)
   - Gate 2: Classification Validation (ES hierarchy)
   - Gate 3: Statistical Validation (Hedges' g verification)
   - Gate 4: Independence Validation (pre-test exclusion)

2. **Phase-Based Orchestration**
   - Each phase has entry/exit criteria
   - Mandatory checkpoints at phase transitions
   - Automatic rollback on validation failure

3. **Integration Points**
   - Calls B1/B2/B3 for extraction
   - Calls C6 for data integrity
   - Calls C7 for error prevention

### 3.2 C6-DataIntegrityGuard

**Purpose**: Ensure data completeness and calculate derived statistics

**Key Features**:
1. **Version Tracking**
   - Track data changes across versions (V5→V6→V7→V8)
   - Flag unexpected data loss
   - Maintain audit trail

2. **Hedges' g Calculation**
   ```python
   def calculate_hedges_g(m1, sd1, n1, m2, sd2, n2):
       pooled_sd = sqrt(((n1-1)*sd1**2 + (n2-1)*sd2**2) / (n1+n2-2))
       d = (m1 - m2) / pooled_sd
       df = n1 + n2 - 2
       J = 1 - (3 / (4*df - 1))  # Hedges' correction
       return d * J
   ```

3. **SD Recovery Strategies**
   - Strategy 1: Extract from tables/figures
   - Strategy 2: Calculate from CI/SE
   - Strategy 3: Impute from similar studies
   - Strategy 4: Contact authors

4. **Study-Level Aggregation**
   - Validate study counts match ES counts
   - Flag studies with all missing Hedges' g
   - Report data tier distribution

### 3.3 C7-ErrorPreventionEngine

**Purpose**: Proactively prevent common meta-analysis errors

**Error Taxonomy**:

| Category | Examples | Prevention Strategy |
|----------|----------|---------------------|
| Data Errors | Missing SD, wrong n | Pre-extraction checklist |
| Methodological | Pre-test inclusion | Classification gate |
| Statistical | Wrong pooling formula | Formula verification |
| Interpretation | Confusing study/ES counts | Clear terminology |
| Reproducibility | Unreported decisions | Audit logging |

**Key Features**:
1. **Pre-Extraction Warnings**
   - Warn about common extraction pitfalls
   - Flag papers with complex designs

2. **Pattern-Based Detection**
   - Detect pre-test patterns in outcome names
   - Identify suspicious effect sizes (|g| > 3)
   - Flag duplicate effect sizes

3. **Checkpoint Enforcement**
   - Mandatory human review at data tiers
   - No auto-proceed on Tier 3 data (<40% confidence)

---

## Part 4: Implementation Plan

### Phase 1: Documentation (Current)
- [x] Document rationale (this file)
- [ ] Get Codex feedback via /review
- [ ] Finalize agent specifications

### Phase 2: Diverga Integration
- [ ] Add C5/C6/C7 to Diverga agents folder
- [ ] Update pipeline-templates.md with meta_analysis_multigate
- [ ] Add 5 new checkpoints to user-checkpoints.md

### Phase 3: Testing
- [ ] Test on V7→V8 transition
- [ ] Validate Hedges' g calculations
- [ ] Verify gate enforcement

### Phase 4: Deployment
- [ ] Integrate with existing B2/B3 agents
- [ ] Document workflow in Diverga README

---

## Part 5: Expected Impact

### Before C5/C6/C7
- Manual error detection (discovered late in V7)
- No systematic validation gates
- 42% missing Hedges' g went unnoticed until analysis
- Pre-test contamination not caught

### After C5/C6/C7
- Automated multi-gate validation
- Proactive error prevention before extraction
- Real-time data completeness tracking
- Clear study vs ES count reporting
- Audit trail for all decisions

### Metrics for Success
| Metric | Before | Target |
|--------|--------|--------|
| Missing Hedges' g | 42% | <15% |
| Pre-test contamination | 10 ES | 0 ES |
| Data loss between versions | 15% SD lost | 0% |
| Study count accuracy | Incorrect reports | 100% accurate |

---

## Appendix: V7 Issues Timeline

1. **V5 Created**: 66 studies, 375 ES, SD extraction incomplete
2. **V5 Verified**: Some studies recovered, 4 excluded
3. **V6 Created**: All 66 studies, 375 ES
4. **Copilot Discussion**: Pre-test methodology issue identified
5. **V7 Created**: 10 pre-test ES removed (365 ES)
6. **Error Discovered**: Only 45 studies have valid Hedges' g
7. **Root Cause**: SD extraction failure (42% missing)
8. **Recovery Plan**: V8 with SD recovery from original data

---

## Appendix B: Codex Review Feedback (2026-01-26)

### Review Summary: APPROVE WITH CHANGES

| Criterion | Score | Status |
|-----------|-------|--------|
| Architecture Clarity | 7/10 | 🟡 |
| Gap Analysis | 8/10 | 🟡 |
| Implementation Feasibility | 6/10 | 🟡 |
| Error Coverage | 7/10 | 🟡 |
| Integration Design | 6/10 | 🟡 |

### Concerns Addressed

**1. Authority Overlap Resolution**

C5 owns **gate progression** (decision authority), C7 provides **advisory signals only**.

```
C7 → Advisory: "Warning: pre-test pattern detected in ES_45-1"
C5 → Decision: "GATE 4a FAILED. Rejecting ES_45-1. Reason: pre-test"
```

**2. Concrete Operational Thresholds**

| Parameter | Threshold | Source |
|-----------|-----------|--------|
| Anomaly detection | \|g\| > 3.0 | Lipsey & Wilson guideline |
| Tier 1 confidence | ≥70% fields complete | Project-specific |
| Tier 2 confidence | 40-69% fields complete | Project-specific |
| Tier 3 (HUMAN REVIEW) | <40% fields complete | Project-specific |
| Duplicate detection | Title similarity > 0.9 | Jaccard index |
| SD outlier | SD > 3× median SD | Statistical convention |

**3. Integration Contracts**

```yaml
# B3 → C6 handoff schema
effect_size_record:
  required:
    - Study_ID: str
    - ES_ID: str
    - Outcome_Name: str
  optional_but_tracked:
    - M_Treatment: float
    - SD_Treatment: float
    - n_Treatment: int
    - M_Control: float
    - SD_Control: float
    - n_Control: int
  computed_by_C6:
    - Hedges_g: float
    - SE_g: float
    - Data_Tier: int [1,2,3]
    - Completeness_Score: float [0-1]

# C6 → C5 handoff
integrity_report:
  - total_records: int
  - tier_distribution: {1: int, 2: int, 3: int}
  - missing_fields_summary: dict
  - version_diff: list[str]  # Changes from previous version
  - anomalies_detected: list[AnomalyRecord]
```

**4. Phased Implementation (Narrow C5 Scope Initially)**

| Phase | C5 Scope | Timeline |
|-------|----------|----------|
| Phase 1 (MVP) | Gates 1-4 only | Week 1 |
| Phase 2 | + Quality Assessment | Week 2 |
| Phase 3 | + Sensitivity Analysis | Week 3 |
| Phase 4 | + Reporting | Week 4 |

### Integration Test Scenario

**Simulating V7 Failure: Pre-test Inclusion**

```
INPUT: ES record with Outcome_Name = "Pre-test critical thinking score"

Expected C7 Response:
  - Advisory: "PRE_TEST_PATTERN_DETECTED"
  - Severity: HIGH
  - Evidence: "Pattern 'pre-test' in Outcome_Name"

Expected C5 Response:
  - Gate: 4a (Temporal Classification)
  - Decision: REJECT
  - Reason: "Pre-test outcomes are not valid independent effect sizes"
  - Action: Remove from analysis dataset, log to exclusion audit
```

---

*Document created: 2026-01-26*
*Author: Claude Code with Diverga multi-agent orchestration*
*Codex Review: APPROVE WITH CHANGES (2026-01-26)*
*Related: V7_METHODOLOGY_IMPROVEMENT_REPORT.md, V7_HEDGES_G_RECOVERY_PLAN.md*
