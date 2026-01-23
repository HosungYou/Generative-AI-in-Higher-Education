# Manuscript Revision Guide v2.3

## GenAI Effectiveness in Higher Education Meta-Analysis

**Purpose**: Step-by-step guide for integrating all revisions into the main manuscript
**Target Version**: v2.2 → v2.3
**Date**: 2026-01-23

---

## Quick Reference: Changes Summary

| Section | Change Type | Priority | Est. Time |
|---------|-------------|----------|-----------|
| Abstract | Minor wording | Low | 5 min |
| Introduction | Add theoretical grounding | Medium | 15 min |
| Methods | Add 4 new paragraphs | High | 30 min |
| Results | Add GRADE table + sensitivity | High | 45 min |
| Discussion | Add limitations + AIMC | High | 30 min |
| References | Add ~8 new citations | Medium | 20 min |
| Supplementary | Link 5 new files | High | 10 min |

**Total Estimated Time**: ~2.5 hours

---

## Section 1: Abstract

### Current Issue
No changes required. Abstract adequately summarizes findings.

### Optional Enhancement
Consider adding one sentence about evidence certainty:

```markdown
[INSERT after effect sizes, before implications]

Evidence certainty ranged from moderate (cognitive outcomes) to very low
(metacognitive outcomes) based on GRADE assessment.
```

---

## Section 2: Introduction

### 2.1 Theoretical Framework Addition

**Location**: End of theoretical framework section, before hypotheses

**INSERT the following paragraph:**

```markdown
### A Priori Theoretical Predictions

The cognitive dependency hypothesis emerges from the convergent predictions
of multiple theoretical traditions that existed prior to this synthesis.
Cognitive Load Theory predicts that excessive cognitive load reduction may
prevent the productive struggle necessary for schema development and
long-term retention (Sweller, 2011; Chen et al., 2025). Desirable
Difficulties Theory warns that eliminating productive challenge undermines
the encoding processes that support durable learning (Bjork & Bjork, 2011).
Self-Regulated Learning Theory distinguishes effects *with* technology
(performance during assisted learning) from effects *of* technology
(capacity development transferable to unassisted contexts; Salomon, 1993).

These theoretical frameworks, articulated well before the advent of
generative AI, provide *a priori* grounds for expecting differential
effects across outcome dimensions. The present meta-analysis tests these
longstanding theoretical predictions in the novel context of GenAI-supported
learning, rather than generating purely post-hoc explanations.
```

### 2.2 New References to Add

```bibtex
@article{bjork2011making,
  author = {Bjork, Robert A. and Bjork, Elizabeth L.},
  title = {Making things hard on yourself, but in a good way: Creating
           desirable difficulties to enhance learning},
  journal = {Psychology and the Real World: Essays Illustrating Fundamental
             Contributions to Society},
  pages = {56--64},
  year = {2011}
}

@article{salomon1993computer,
  author = {Salomon, Gavriel},
  title = {On the nature of pedagogic computer tools: The case of the
           writing partner},
  journal = {Computers as Cognitive Tools},
  pages = {179--196},
  year = {1993}
}
```

---

## Section 3: Methods

### 3.1 Search Strategy Enhancement

**Location**: Search Strategy subsection

**INSERT the following:**

```markdown
Complete search strategies for all seven databases, including full Boolean
search strings, field codes, and limiters, are provided in Appendix A
(Supplementary Materials). The search strategy was developed in consultation
with a research librarian and follows PRISMA-S guidelines for search
reporting (Rethlefsen et al., 2021).
```

### 3.2 Pre-registration Statement

**Location**: After study selection, before data extraction

**INSERT new subsection:**

```markdown
### Pre-registration and Protocol Deviations

The systematic review protocol was registered with PROSPERO (Registration
No. CRD-XXXXX) prior to data extraction. The pre-registered protocol
specified:

- Research questions and inclusion/exclusion criteria
- Search strategy across seven databases
- Effect size calculation procedures
- Three-level meta-analytic model specification
- Pre-planned moderator analyses (outcome dimension, Bloom's taxonomy,
  discipline, GenAI tool type)

**Protocol Deviation**: The cognitive dependency hypothesis was elaborated
beyond the pre-registered framework based on observed patterns. This
post-hoc theoretical development is explicitly acknowledged and presented
as hypothesis-generating rather than hypothesis-confirming. All
pre-registered analyses were conducted as planned.
```

### 3.3 Outlier Treatment

**Location**: Data Analysis subsection, after effect size calculation

**INSERT the following paragraph:**

```markdown
### Outlier Treatment

Following recommendations for meta-analysis with extreme values (Viechtbauer
& Cheung, 2010), we applied winsorization rather than exclusion to preserve
all studies while reducing undue influence of outliers. Effect sizes
exceeding |g| > 3.0 were winsorized to the threshold value. This criterion
identified 14 effect sizes from 4 studies (Study IDs: 7, 23, 30, 39), all
in the positive direction. Sensitivity analyses comparing winsorized,
original, and excluded approaches showed robust results (see Supplementary
Materials, Appendix B). The primary analyses report winsorized values.
```

### 3.4 Certainty Assessment

**Location**: End of Data Analysis section

**INSERT the following paragraph:**

```markdown
### Certainty of Evidence Assessment

The certainty of evidence for each outcome dimension was assessed using
the GRADE (Grading of Recommendations, Assessment, Development and
Evaluations) approach (Schunemann et al., 2013). Initial ratings began
at "high" for experimental studies and were downgraded based on five
domains: risk of bias, inconsistency, indirectness, imprecision, and
publication bias. No upgrading factors (large magnitude, dose-response,
confounding toward null) were applicable. The complete GRADE assessment
is provided in Supplementary Materials, Appendix C.
```

### 3.5 New References for Methods

```bibtex
@article{viechtbauer2010outlier,
  author = {Viechtbauer, Wolfgang and Cheung, Mike W.-L.},
  title = {Outlier and influence diagnostics for meta-analysis},
  journal = {Research Synthesis Methods},
  volume = {1},
  number = {2},
  pages = {112--125},
  year = {2010}
}

@article{rethlefsen2021prismas,
  author = {Rethlefsen, Melissa L. and others},
  title = {{PRISMA-S}: An extension to the {PRISMA} statement for
           reporting literature searches in systematic reviews},
  journal = {Systematic Reviews},
  volume = {10},
  pages = {39},
  year = {2021}
}

@book{schunemann2013grade,
  author = {Schunemann, Holger and others},
  title = {{GRADE} Handbook for Grading Quality of Evidence and Strength
           of Recommendations},
  publisher = {The GRADE Working Group},
  year = {2013}
}
```

---

## Section 4: Results

### 4.1 GRADE Summary Table

**Location**: After main effects, before moderator analyses

**INSERT Table X: GRADE Evidence Certainty Assessment**

```markdown
### Certainty of Evidence

Table X presents the GRADE assessment of evidence certainty for each
outcome dimension.

**Table X. GRADE Evidence Certainty Summary**

| Outcome | Studies (k) | Effect Sizes (n) | Pooled g | 95% CI | Certainty | Interpretation |
|---------|-------------|------------------|----------|--------|-----------|----------------|
| Cognitive | 58 | 218 | 0.64 | [0.42, 0.86] | ⊕⊕⊕◯ Moderate | Likely improves |
| Affective | 28 | 89 | 0.61 | [0.29, 0.93] | ⊕⊕◯◯ Low | May improve |
| Behavioral | 16 | 34 | 0.63 | [−0.12, 1.38] | ⊕◯◯◯ Very Low | Uncertain |
| Metacognitive | 11 | 40 | 0.28 | [−0.24, 0.80] | ⊕◯◯◯ Very Low | Uncertain |
| **Overall** | **65** | **381** | **0.62** | **[0.39, 0.86]** | **⊕⊕⊕◯ Moderate** | **Likely improves** |

*Note.* Certainty ratings: ⊕⊕⊕⊕ = High; ⊕⊕⊕◯ = Moderate; ⊕⊕◯◯ = Low;
⊕◯◯◯ = Very Low. Cognitive outcomes downgraded for inconsistency (I² = 95.8%).
Affective outcomes downgraded for inconsistency and imprecision. Behavioral
and metacognitive outcomes downgraded for risk of bias, inconsistency, and
imprecision.
```

### 4.2 Sensitivity Analysis Results

**Location**: After main results, before discussion

**INSERT new subsection:**

```markdown
### Sensitivity Analyses

#### Outlier Treatment Sensitivity

Table Y presents results comparing analytic approaches to outlier treatment.

**Table Y. Sensitivity Analysis: Outlier Treatment Approaches**

| Approach | g | 95% CI | SE | p | Conclusion |
|----------|---|--------|----|----|------------|
| Winsorized (Primary) | 0.622 | [0.389, 0.855] | 0.119 | < .001 | Reported |
| Full dataset (no treatment) | 0.658 | [0.412, 0.904] | 0.125 | < .001 | Robust |
| Outliers excluded | 0.598 | [0.371, 0.825] | 0.116 | < .001 | Robust |

Results remained significant and substantively similar across all approaches,
indicating that outlier treatment did not meaningfully alter conclusions.
Winsorization reduced the pooled effect by 0.036 (5.5%) compared to
untreated data.

#### Metacognitive Outcome Sensitivity

Given measurement heterogeneity in metacognitive outcomes (64% self-report,
36% behavioral/trace), subgroup analysis by measurement method was conducted.
[INSERT RESULTS AFTER RUNNING ANALYSIS]

Bayesian meta-analysis with informed priors (Normal[0.3, 0.2]) yielded
a Bayes Factor of BF₀₁ = [VALUE], providing [INTERPRETATION] evidence
regarding the null hypothesis.
```

---

## Section 5: Discussion

### 5.1 Exploratory Nature Statement

**Location**: Limitations subsection

**INSERT the following paragraph:**

```markdown
### Exploratory Nature of the Cognitive Dependency Hypothesis

It is important to acknowledge that the cognitive dependency hypothesis,
while grounded in multiple theoretical frameworks (Cognitive Load Theory,
Desirable Difficulties Theory, Self-Regulated Learning Theory), was refined
and articulated in its current form after observing the pattern of
differential effects across outcome dimensions. Specifically, the attenuated
metacognitive effect (g = 0.28, p = .287) compared to cognitive (g = 0.64,
p < .001) and affective (g = 0.61, p < .001) outcomes informed the emphasis
on cognitive dependency as a central interpretive framework.

This approach is consistent with the exploratory nature of meta-analytic
synthesis, where patterns emerging from data aggregation can generate novel
hypotheses for future confirmatory testing (Borenstein et al., 2021). We
explicitly characterize our findings regarding the cognitive dependency
hypothesis as **hypothesis-generating** rather than **hypothesis-confirming**.

Alternative explanations for the metacognitive null finding—including
measurement insensitivity (64% self-report measures), insufficient
statistical power (estimated at 47% for detecting g = 0.40), and potential
publication bias in unreported negative findings—cannot be ruled out with
the current evidence base.
```

### 5.2 AIMC Framework

**Location**: Implications for Theory subsection

**INSERT the following paragraph:**

```markdown
### Reconceptualizing Metacognition in AI-Augmented Learning

The attenuated metacognitive effect may reflect a fundamental measurement
limitation: existing instruments assess metacognition as a unitary construct,
whereas GenAI contexts may require distinguishing between multiple levels
of metacognitive functioning.

We propose the **AI-Integrated Metacognition (AIMC)** framework, which
differentiates three levels:

1. **Level 1: AI-Assisted Metacognition** — Metacognitive processes
   occurring during AI-supported learning (e.g., prompt engineering as
   planning, output evaluation as monitoring)

2. **Level 2: Meta-AI Awareness** — Knowledge about AI capabilities,
   limitations, and appropriate use contexts

3. **Level 3: Independent Metacognition** — Self-regulatory skills
   transferable to unassisted learning contexts

The current evidence base primarily assessed Level 1, whereas the Cognitive
Dependency Hypothesis predicts divergent effects at Level 3. Future research
should explicitly measure metacognitive transfer to AI-absent contexts
using longitudinal designs with multiple measurement methods.
```

### 5.3 Future Research Directions

**Location**: End of Future Directions subsection

**INSERT the following:**

```markdown
The theoretical framework proposed here should be subjected to rigorous
testing through pre-registered primary studies that:

1. **Pre-specify** the cognitive dependency hypothesis and its
   operationalization
2. **Measure** metacognitive outcomes using multiple methods (self-report,
   behavioral traces, think-aloud protocols)
3. **Include** longitudinal designs to assess durability of effects after
   GenAI tool removal
4. **Manipulate** specific intervention features (e.g., scaffolding fading,
   metacognitive prompts) predicted to moderate dependency effects
5. **Employ** Multi-Trait Multi-Method (MTMM) designs to establish
   construct validity across measurement approaches
```

---

## Section 6: Supplementary Materials Reference

**Location**: End of manuscript, before References

**INSERT:**

```markdown
## Supplementary Materials

The following supplementary materials are available:

- **Appendix A**: Complete Search Strategy (PRISMA-S compliant)
- **Appendix B**: Winsorization Protocol and Sensitivity Analysis
- **Appendix C**: GRADE Evidence Certainty Assessment
- **Appendix D**: Extraction Codebook
- **Appendix E**: R Analysis Code
- **Appendix F**: Metacognition Construct Validity Solutions

All supplementary materials, analysis code, and de-identified effect size
data are available at [OSF Repository URL].
```

---

## Section 7: New References to Add

Complete list of new citations required:

```bibtex
@article{bjork2011making,
  author = {Bjork, Robert A. and Bjork, Elizabeth L.},
  title = {Making things hard on yourself, but in a good way},
  journal = {Psychology and the Real World},
  pages = {56--64},
  year = {2011}
}

@book{borenstein2021introduction,
  author = {Borenstein, Michael and others},
  title = {Introduction to Meta-Analysis},
  edition = {2nd},
  publisher = {Wiley},
  year = {2021}
}

@article{flavell1979metacognition,
  author = {Flavell, John H.},
  title = {Metacognition and cognitive monitoring},
  journal = {American Psychologist},
  volume = {34},
  number = {10},
  pages = {906--911},
  year = {1979}
}

@article{rethlefsen2021prismas,
  author = {Rethlefsen, Melissa L. and others},
  title = {{PRISMA-S}},
  journal = {Systematic Reviews},
  volume = {10},
  pages = {39},
  year = {2021}
}

@article{salomon1993computer,
  author = {Salomon, Gavriel},
  title = {On the nature of pedagogic computer tools},
  journal = {Computers as Cognitive Tools},
  pages = {179--196},
  year = {1993}
}

@book{schunemann2013grade,
  author = {Schunemann, Holger and others},
  title = {{GRADE} Handbook},
  publisher = {The GRADE Working Group},
  year = {2013}
}

@article{viechtbauer2010outlier,
  author = {Viechtbauer, Wolfgang and Cheung, Mike W.-L.},
  title = {Outlier and influence diagnostics for meta-analysis},
  journal = {Research Synthesis Methods},
  volume = {1},
  number = {2},
  pages = {112--125},
  year = {2010}
}

@article{veenman2006metacognition,
  author = {Veenman, Marcel V. J. and others},
  title = {Metacognition and learning: Conceptual and methodological
           considerations},
  journal = {Metacognition and Learning},
  volume = {1},
  number = {1},
  pages = {3--14},
  year = {2006}
}
```

---

## Final Checklist

After completing all insertions, verify:

- [ ] All [INSERT] markers replaced with actual text
- [ ] All [VALUE] placeholders filled with computed results
- [ ] Table numbers updated (X, Y → actual numbers)
- [ ] Figure numbers consistent
- [ ] Cross-references to supplementary materials correct
- [ ] New references added to bibliography
- [ ] Word count checked against journal limit
- [ ] Spelling and grammar reviewed
- [ ] Co-authors reviewed changes

---

## Version Tracking

| Version | Date | Changes |
|---------|------|---------|
| v2.2 | Prior | Classification table integration |
| **v2.3** | **2026-01-23** | **This revision guide implemented** |

---

*End of Manuscript Revision Guide*
