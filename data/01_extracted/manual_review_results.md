# Manual Review Results: 7 Studies Requiring Verification
## Date: January 2025

---

## Summary of Decisions

| Study | Original Issue | Corrected d | Decision |
|-------|---------------|-------------|----------|
| JMIR Medical Education | Missing effect size | **0.40** | ✅ Include |
| Humanities Study | Missing effect size | 1.45 | ⚠️ Exclude (no control) |
| Oxford Medical | Missing effect size | **0.21** | ✅ Include |
| Formative Feedback (Yin) | Missing effect size | **0.38** | ✅ Include |
| ESP Writing | η²=0.789 abnormal | 0.70 (pre-post only) | ❌ Exclude (no control) |
| Education IT | d=3.0 abnormal | ~0.10 | ❌ Exclude (data inconsistent) |
| Medical Education (Gan) | d=2.98 abnormal | **1.20** | ✅ Include (corrected) |

**Final count: 4 included, 3 excluded**

---

## Detailed Review Results

### 1. JMIR Medical Education (jmir-2024-1-e57037.pdf)
**Decision: ✅ INCLUDE**

| Item | Value |
|------|-------|
| N total | 110 |
| N treatment | 54 |
| N control | 56 |
| M treatment | 141.20 |
| SD treatment | 26.68 |
| M control | 130.80 |
| SD control | 25.56 |
| **Calculated Cohen's d** | **0.40** |
| Study design | RCT |
| Outcome | Orthopedics MCQ test performance |
| Notes | Medical students, 2-week intervention, ChatGPT vs traditional |

---

### 2. Humanities Study (s41599-024-02751-w.pdf)
**Decision: ⚠️ EXCLUDE (No control group)**

| Item | Value |
|------|-------|
| N total | 50 |
| N treatment | N/A |
| N control | N/A |
| Design | Single-group, high/low AI literacy comparison |
| Issue | No control group - all participants used ChatGPT |
| Notes | Quasi-experimental, cannot isolate treatment effect |

---

### 3. Oxford Medical (qgae170.pdf)
**Decision: ✅ INCLUDE**

| Item | Value |
|------|-------|
| N total | 115 |
| N treatment | 56 |
| N control | 59 |
| M treatment | 74.7 |
| SD treatment | 15.1 |
| M control | 78.5 |
| SD control | 20.6 |
| **Cohen's d (reported)** | **0.21** |
| p-value | 0.26 |
| Study design | RCT |
| Outcome | Clinical reasoning (Key-Features Questions) |
| Notes | ChatGPT feedback vs expert feedback; control group slightly better |

---

### 4. Formative Feedback - Yin et al.
**Decision: ✅ INCLUDE**

| Item | Value |
|------|-------|
| N total | 173 |
| N treatment | 88 |
| N control | 85 |
| t-value (Cognitive Load Ch4) | 2.523 |
| **Calculated Cohen's d** | **0.38** |
| Study design | Quasi-experimental longitudinal |
| Outcome | Learning performance, cognitive load |
| Notes | 36-day study; chatbot vs teacher feedback |

---

### 5. ESP Writing (s44217-025-00700-6.pdf)
**Decision: ❌ EXCLUDE (No control group)**

| Item | Value |
|------|-------|
| N total | 117 |
| N treatment | 117 |
| N control | 0 |
| η² (time effect) | 0.789 |
| Issue | Within-subjects time effect, NOT treatment effect |
| Pre-post d | ~0.70 (but confounded) |
| Limitation | Single-group pretest-posttest, no control |
| Notes | Cannot attribute change to ChatGPT vs maturation |

---

### 6. Education IT (s10639-024-12705-z.pdf)
**Decision: ❌ EXCLUDE (Data quality issues)**

| Item | Value |
|------|-------|
| N total | 74 |
| N treatment | 36 |
| N control | 38 |
| Reported t | 9.71 |
| M treatment | 4.69 |
| SD treatment | 8.03 |
| M control | 3.88 |
| SD control | 8.61 |
| Calculated d from M/SD | ~0.10 |
| Issue | t=9.71 mathematically impossible with these M/SD values |
| Notes | Internal inconsistency in reported statistics |

---

### 7. Medical Education - Gan et al. (1-s2.0-S2666920X23000772-main.pdf)
**Decision: ✅ INCLUDE (Corrected)**

| Item | Value |
|------|-------|
| N total | 125 |
| N treatment | 60 |
| N control | 65 |
| M treatment | 39.2 |
| SD treatment | 6.57 |
| M control | 30.6 |
| SD control | 7.64 |
| Partial η² | 0.229 |
| **Calculated Cohen's d** | **1.20** |
| Original misextraction | 2.98 (was CFA fit index, not d) |
| Study design | Quasi-experimental |
| Outcome | Critical thinking skills |
| Notes | Semester-long intervention, ChatGPT-assisted learning |

---

## Updated Effect Sizes for Meta-Analysis

```csv
filename,n_total,n_treatment,n_control,cohens_d,hedges_g,se_g,decision
jmir-2024-1-e57037.pdf,110,54,56,0.40,0.39,0.19,include
s41599-024-02751-w.pdf,50,NA,NA,NA,NA,NA,exclude_no_control
qgae170.pdf,115,56,59,0.21,0.21,0.19,include
Using_a_Chatbot...pdf,173,88,85,0.38,0.38,0.15,include
s44217-025-00700-6.pdf,117,117,0,NA,NA,NA,exclude_no_control
s10639-024-12705-z.pdf,74,36,38,NA,NA,NA,exclude_data_quality
1-s2.0-S2666920X23000772-main.pdf,125,60,65,1.20,1.19,0.19,include
```

---

## Impact on Meta-Analysis

### Before Review
- Total new studies: 16
- Studies with effect sizes: 9

### After Review
- Confirmed inclusions: 13 studies (9 original + 4 newly verified)
- Exclusions: 3 studies
- Corrected values: 1 study (Gan: 2.98 → 1.20)

### Updated Study Count
| Metric | Previous | Updated |
|--------|----------|---------|
| Existing studies | 63 | 63 |
| New studies (valid) | 16 | 13 |
| **Total studies** | 79 | **76** |
