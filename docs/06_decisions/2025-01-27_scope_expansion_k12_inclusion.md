# Scope Expansion Decision: Including K-12 Studies

**Date**: 2025-01-27
**Decision**: Include K-12 studies with Education Level as moderator variable
**Impact**: Manuscript title and scope revision required

---

## 1. Background

### Original Manuscript Scope

The manuscript "Generative AI in Higher Education: A Three-Level Meta-Analysis" was originally scoped to include only higher education studies. The theoretical justification stated:

> "The decision to focus exclusively on higher education reflects both empirical and theoretical considerations... students possess greater metacognitive capabilities for self-regulated learning (Zimmerman, 2002), face complex disciplinary knowledge demands (Alexander, 2003), and operate with greater autonomy in learning decisions (Deci & Ryan, 2000). These factors may moderate GenAI effectiveness in ways distinct from K-12 settings."

### K-12 Studies Identified in V9.0 Extraction

During the v9.0 extraction pipeline, 7 studies were identified as K-12:

| Study ID | Author/Year | Education Level | GenAI Tool | Notes |
|----------|-------------|-----------------|------------|-------|
| 018 | Satoru_2025 | K-12 | ChatGPT | CEFR language assessment |
| 019 | Guoqing_2025 | K-12 | Custom | |
| 020 | Xusheng_2025 | K-12 | Custom | |
| 022 | Larissa_2025 | K-12 | ChatGPT | |
| 028 | Tuan_2025 | K-12 | ChatGPT | Teachers' professional development |
| 044 | Dadan_2024 | K-12 | ChatGPT | Didactical tetrahedron |
| 055 | Yousef_2024 | K-12 | ChatGPT | **Grade 12** Quantum Physics |

**Note**: Study 055 (Grade 12) and Study 028 (Teachers) may be closer to higher education/adult contexts.

---

## 2. Discussion Points

### Question Raised

> "HE 특성(metacognitive capabilities, autonomy)이 K-12에는 반영되기 어려운가?"

### Analysis

| Factor | K-12 | Higher Education | Difference Type |
|--------|------|------------------|-----------------|
| **Metacognitive capabilities** | Developing (high schoolers have substantial levels) | More developed | **Degree, not kind** |
| **Autonomy** | Structured environment, but increasing | Higher autonomy | **Continuous spectrum** |
| **Self-regulation** | Can be taught and develops (Veenman et al., 2006) | More mature | **Degree, not kind** |

### Key Insights

1. **Developmental continuity**: Metacognitive capabilities exist on a developmental continuum, not as a binary HE/K-12 distinction
2. **Grade 12 proximity**: High school seniors (Grade 12) have metacognitive capabilities similar to university freshmen
3. **Empirical opportunity**: Including both allows empirical testing of whether education level moderates GenAI effects
4. **Original justification was overly dichotomous**: The theoretical argument for HE-only scope oversimplified the developmental trajectory

---

## 3. Decision

### Final Decision: **Option A - Include K-12 with Education Level as Moderator**

**Rationale**:
1. Enables empirical comparison: "Does GenAI effect differ between K-12 and HE?"
2. More comprehensive synthesis of available evidence
3. Education level becomes a testable moderator hypothesis
4. Academically stronger contribution

### Alternative Considered (Rejected)

**Option B**: Exclude K-12, maintain HE-only scope
- Would maintain consistency with current manuscript
- Loses 7 studies (10% of sample)
- Misses opportunity for moderator analysis

---

## 4. Required Manuscript Changes

### High Priority

| Section | Current | Required Change |
|---------|---------|-----------------|
| **Title** | "Generative AI in Higher Education..." | "Generative AI in Education..." |
| **Abstract** | References "higher education" | Revise to "educational contexts" with HE/K-12 breakdown |
| **Keywords** | "higher education" | Add "K-12 education", "education level" |

### Theoretical Framework

| Location | Change Required |
|----------|-----------------|
| Line 70-71 | Remove exclusive HE justification |
| AIMC Framework | Extend to acknowledge developmental differences |
| Methods | Add Education Level (HE vs K-12) as planned moderator |

### Results Section

Add moderator analysis:
```
Education Level Moderator Analysis:
- Higher Education: k = 63, g = [value], 95% CI [x, y]
- K-12: k = 7, g = [value], 95% CI [x, y]
- Q_between = [value], p = [value]
```

### Discussion

Add paragraph discussing:
1. Whether effects differ by education level
2. Implications for developmental metacognition theory
3. Recommendations for K-12 vs HE implementation

---

## 5. Data Implications

### Updated Study Counts

| Category | Count |
|----------|-------|
| Total Studies | 70 |
| Higher Education | 63 |
| K-12 | 7 |

### Education Level Distribution (v9.0 Extraction)

```
undergraduate: 50 (71%)
K-12: 7 (10%)
graduate: 3 (4%)
not_reported: 3 (4%)
adult_learner: 2 (3%)
other: 5 (7%)
```

---

## 6. Timeline

| Task | Status | Target |
|------|--------|--------|
| Document decision | ✅ Complete | 2025-01-27 |
| Update extraction to include education level coding | ✅ Complete (v9.0) | 2025-01-27 |
| Revise manuscript title and abstract | Pending | TBD |
| Add moderator analysis code | Pending | TBD |
| Update theoretical framework | Pending | TBD |

---

## 7. References

- Veenman, M. V., Van Hout-Wolters, B. H., & Afflerbach, P. (2006). Metacognition and learning: Conceptual and methodological considerations. *Metacognition and learning*, 1(1), 3-14.
- Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview. *Theory into practice*, 41(2), 64-70.
- Alexander, P. A. (2003). The development of expertise: The journey from acclimation to proficiency. *Educational researcher*, 32(8), 10-14.
- Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological inquiry*, 11(4), 227-268.

---

## 8. Approval

**Decision approved by**: Hosung You
**Date**: 2025-01-27
**Implementation**: Proceed with Option A
