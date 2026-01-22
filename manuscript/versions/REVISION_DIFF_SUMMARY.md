# Revision Diff Summary: v1.0 → v2.0

## Detailed Change Log

This document provides a technical summary of all changes made during the v2.0 revision.

---

## New Text Added

### 1. Submission Checklist (Top of Document)
```markdown
<!--
===============================================================================
SUBMISSION CHECKLIST - Complete Before Submitting to Educational Psychology Review
===============================================================================

REQUIRED ACTIONS:
1. [ ] Replace [ORCID-ID] with your actual ORCID identifier
2. [ ] Register protocol with PROSPERO and replace [CRD-XXXXX] with registration number
3. [ ] Upload data and materials to OSF and replace [OSF Repository Link] with actual URL
4. [ ] Prepare Figure files as separate high-resolution images
5. [ ] Format according to APA 7th Edition (EPR requirement)
6. [ ] Prepare cover letter for submission

TARGET JOURNAL: Educational Psychology Review (Springer)
Word Count: ~11,500 words (within EPR limits)
Abstract: 237 words (within 250-word limit)
===============================================================================
-->
```

---

### 2. Citation Verification Section (Method)
**Location:** After Search Strategy paragraph

```markdown
**Citation Verification and Publication Status.** Given the rapidly evolving nature
of GenAI research, this meta-analysis includes studies and theoretical works published
through January 2026. All 2025 and 2026 citations were verified for publication status
at the time of manuscript preparation. Citations fall into three categories: (a) *Fully
published articles* with assigned volume and issue numbers represent peer-reviewed
publications that have completed the publication process; (b) *Advance online publications*
(marked as such in references) are peer-reviewed manuscripts accepted for publication and
assigned DOIs but awaiting final pagination—these meet standard inclusion criteria for
systematic reviews as they have completed peer review; (c) *Preprints and non-peer-reviewed
works* were excluded from the meta-analytic synthesis (though occasionally cited for
theoretical context when clearly identified as such). For primary studies included in
quantitative synthesis, we required peer-reviewed publication status; the 13 reports
excluded for "not peer-reviewed/unverified preprint" status (see PRISMA diagram) reflect
enforcement of this criterion.
```

---

### 3. Metacognitive Outcome Operationalization (Method)
**Location:** After outcome coding paragraph

```markdown
**Metacognitive Outcome Operationalization.** Given the central theoretical importance
of metacognitive outcomes to the cognitive dependency hypothesis, we describe their
operationalization in detail. Across the 11 studies (*n* = 40 effect sizes) reporting
metacognitive outcomes, measures fell into three categories: (a) *Self-report questionnaires*
(*k* = 7), including the Motivated Strategies for Learning Questionnaire metacognitive
self-regulation subscale (MSLQ; Pintrich et al., 1991), the Online Self-Regulated Learning
Questionnaire (OSLQ; Barnard et al., 2009), and custom self-regulation scales assessing
planning, monitoring, and evaluation behaviors; (b) *Think-aloud protocols and verbal
reports* (*k* = 2), wherein students verbalized their thinking during learning tasks and
utterances were coded for metacognitive statements (planning, monitoring, evaluating);
and (c) *Trace data and log analysis* (*k* = 2), examining behavioral indicators of
self-regulation such as help-seeking patterns, time allocation, and revision behaviors
within learning management systems.

Notably, the majority (7 of 11 studies; 64%) relied on self-report measures, which may be
subject to social desirability bias and retrospective recall limitations (Winne &
Jamieson-Noel, 2002). This measurement approach raises an important interpretive
consideration: if GenAI reduces metacognitive engagement during learning, students may
lack awareness of this reduction and thus not report it accurately on self-report
instruments—potentially underestimating the cognitive dependency effect. Conversely,
students who struggle without AI support may over-report self-regulatory difficulties.
The limited number of studies using behavioral or trace-based metacognitive measures
(*k* = 4) precludes a meaningful comparison between measurement approaches, but future
research should prioritize objective metacognitive indicators that are less susceptible
to self-report biases.
```

---

### 4. Power Analysis for Metacognitive Findings (Results)
**Location:** After metacognitive effect interpretation

```markdown
**Statistical Power Considerations for Metacognitive Findings.** The metacognitive
outcome analysis is based on a smaller evidence base (*k* = 11 studies, *n* = 40 effect
sizes) compared to cognitive (*k* = 58, *n* = 218) and affective (*k* = 27, *n* = 83)
outcomes. To assess whether the non-significant metacognitive effect (*g* = 0.28,
*p* = .287) reflects a true null finding or insufficient statistical power, we conducted
a post-hoc power analysis. Using the observed between-study variance (τ²₃ = 0.276) and
within-study variance (τ²₂ = 0.218), along with the average sampling variance of the
metacognitive effect sizes (*v̄* = 0.089), we estimated that with *k* = 11 studies, the
analysis had approximately 47% power to detect an effect of *g* = 0.40 at α = .05
(two-tailed). The minimum detectable effect size (MDES) with 80% power would require
*g* ≈ 0.65. The observed effect (*g* = 0.28) falls well below this threshold, indicating
that even if a small-to-medium true effect exists, this analysis would likely fail to
detect it. Consequently, the non-significant finding should be interpreted with appropriate
caution: while the point estimate is notably smaller than other outcome dimensions, the
wide confidence interval (−0.24 to 0.80) cannot definitively rule out either a null effect
or a moderate positive effect. Future research explicitly targeting metacognitive outcomes
is needed to provide more precise estimates.
```

---

### 5. Figure Insertion Markers
**Locations:** Throughout document

```markdown
[Insert Figure 1 about here]  <!-- After PRISMA description -->
[Insert Figure 2 about here]  <!-- After overall effect -->
[Insert Figure 3 about here]  <!-- After Table 3 -->
[Insert Figure 4 about here]  <!-- After publication bias -->
```

---

### 6. Measurement Quality Alternative Explanation (Discussion)
**Location:** After Design Failure Hypothesis

```markdown
**Alternative Interpretation: Measurement Quality and Sensitivity.** A second alternative
explanation concerns the measurement properties of metacognitive versus cognitive outcomes.
Cognitive outcomes were predominantly assessed using standardized achievement tests,
performance-based assessments, and validated disciplinary knowledge measures—instruments
with established psychometric properties optimized through decades of educational measurement
research. In contrast, metacognitive outcomes were primarily measured using self-report
questionnaires (64% of studies), which face well-documented limitations: retrospective
recall biases, social desirability effects, and limited correspondence with actual
metacognitive behaviors (Winne & Jamieson-Noel, 2002; Veenman et al., 2006). These
measurement challenges may create differential sensitivity to treatment effects. If
cognitive measures more accurately capture true learning gains than self-report metacognitive
measures capture true self-regulatory changes, the observed differential effects may
partially reflect measurement artifacts rather than—or in addition to—genuine cognitive
dependency. This interpretation does not invalidate the theoretical concern but suggests
caution in interpreting the magnitude of the difference. Future research should employ
behavioral and trace-based metacognitive measures that may provide more sensitive detection
of self-regulation changes.
```

---

### 7. Expanded Limitations (Seventh Limitation)
**Location:** End of limitations paragraph

```markdown
**Seventh, and most critically for interpreting our central hypothesis, the metacognitive
outcome analysis was based on only 11 studies with 40 effect sizes—substantially fewer
than other outcome dimensions. As detailed in our power analysis, this limited evidence
base provided only ~47% power to detect a medium effect (*g* = 0.40), meaning the
non-significant finding (*p* = .287) should not be interpreted as definitive evidence
for the null hypothesis. The wide confidence interval (−0.24 to 0.80) encompasses both
null and meaningful positive effects; we cannot determine whether GenAI truly fails to
enhance metacognition or whether our sample was simply underpowered. Readers should
therefore interpret the cognitive dependency hypothesis as theoretically motivated and
preliminarily supported, but requiring replication with larger samples specifically
designed to assess metacognitive outcomes.**
```

---

### 8. Figure Captions Section (End of Document)
**Location:** After References

```markdown
## Figure Captions

**Figure 1.** PRISMA 2020 flow diagram illustrating the systematic literature search
and screening process. Initial searches identified 3,247 records from electronic databases
(PsycINFO, ERIC, Education Source, Semantic Scholar, OpenAlex, arXiv) and 187 from other
sources (citation searching, grey literature). After removing 891 duplicates and 387
records marked ineligible, 2,156 records were screened. Following title/abstract screening
(1,847 excluded) and full-text assessment (221 excluded), 65 studies with 381 effect sizes
were included in quantitative synthesis.

**Figure 2.** Forest plot of effect sizes by outcome dimension. The plot displays Hedges'
*g* estimates with 95% confidence intervals for cognitive (*k* = 58, *n* = 218), affective
(*k* = 27, *n* = 83), behavioral (*k* = 12, *n* = 40), and metacognitive (*k* = 11,
*n* = 40) outcomes. The overall pooled effect is shown at the bottom (*g* = 0.622,
95% CI [0.389, 0.855]). The attenuated metacognitive effect (*g* = 0.28, *p* = .287)
supports the cognitive dependency hypothesis.

**Figure 3.** Forest plot of effect sizes by academic discipline. Effect sizes varied
significantly across disciplines, with Medicine/Health showing the largest effect
(*g* = 0.72), followed by STEM (*g* = 0.58), Humanities/Social Sciences (*g* = 0.55),
and Language/Writing (*g* = 0.42). All effects except Language/Writing exceeded the
medium effect size threshold (*g* > 0.50).

**Figure 4.** Funnel plot for publication bias assessment. The plot displays effect
sizes (Hedges' *g*) against their standard errors. Slight asymmetry is visible, but
statistical tests (PET intercept = -0.583, *p* = .064; trim-and-fill *k*₀ = 0) suggest
publication bias does not substantially threaten estimate validity.
```

---

### 9. Supplementary Materials Section
**Location:** After Figure Captions

```markdown
## Supplementary Materials

Supplementary Materials, including the complete coding manual, effect size calculation
formulas, full PRISMA checklist, sensitivity analysis details, and additional moderator
analyses, are available at [OSF Repository Link].
```

---

## New References Added

### Veenman et al. (2006)
```
Veenman, M. V. J., Van Hout-Wolters, B. H. A. M., & Afflerbach, P. (2006). Metacognition
and learning: Conceptual and methodological considerations. *Metacognition and Learning,
1*(1), 3-14. https://doi.org/10.1007/s11409-006-6893-0
```

### Winne & Jamieson-Noel (2002)
```
Winne, P. H., & Jamieson-Noel, D. (2002). Exploring students' calibration of self reports
about study tactics and achievement. *Contemporary Educational Psychology, 27*(4), 551-572.
https://doi.org/10.1016/S0361-476X(02)00006-1
```

---

## Statistics

| Metric | v1.0 | v2.0 | Change |
|--------|------|------|--------|
| Word count (approx.) | ~10,500 | ~11,500 | +1,000 |
| References | 68 | 70 | +2 |
| New sections | 0 | 4 | +4 |
| Figure markers | 0 | 4 | +4 |

---

*Generated: 2025-01-22*
