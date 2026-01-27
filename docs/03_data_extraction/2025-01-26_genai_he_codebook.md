# GenAI in Higher Education Meta-Analysis Codebook

## Context-Specific Extension of Universal Codebook v2.1

**Version**: 1.0
**Date**: 2026-01-26
**Project**: Generative AI in Higher Education Meta-Analysis

---

## Overview

This codebook extends the Universal Meta-Analysis Codebook v2.1 with **GenAI-HE specific moderator variables**. It provides:
1. Standard statistical fields for Hedges' g calculation
2. GenAI-specific moderator variables for subgroup analysis
3. Educational outcome classification (Bloom's Taxonomy)
4. AI extraction prompts for each variable

---

## Five-Layer Structure (Extended)

```
┌─────────────────────────────────────────────────────────────────────┐
│         GENAI-HE META-ANALYSIS CODEBOOK (Extended v2.1)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LAYER 1: IDENTIFIERS + METADATA (12 fields)                        │
│  study_id, es_id, citation, doi, year, authors, title,             │
│  journal, design_type, timepoint, sample_context, country          │
│                                                                     │
│  LAYER 2: CORE STATISTICAL VALUES (12 fields)                       │
│  outcome_name, outcome_unit, es_type, analysis_type,               │
│  n_treatment, n_control, m_treatment, sd_treatment,                │
│  m_control, sd_control, hedges_g, se_g                             │
│                                                                     │
│  LAYER 3: GENAI-HE MODERATOR VARIABLES (15 fields) ← NEW           │
│  genai_tool, genai_tool_version, genai_access_type,                │
│  blooms_level, outcome_dimension, learning_domain,                 │
│  study_design, intervention_duration, intervention_type,           │
│  control_condition, education_level, discipline,                   │
│  sample_size_total, publication_type, country                      │
│                                                                     │
│  LAYER 4: AI EXTRACTION PROVENANCE                                  │
│  ai_confidence_avg, ai_method, ai_conflicts, ai_extraction_json    │
│                                                                     │
│  LAYER 5: HUMAN VERIFICATION (8 fields)                             │
│  verified_status, verified_by, verified_date, corrections_json,    │
│  disagreement_resolved, final_values_json, verification_notes,     │
│  sign_off                                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 3: GenAI-HE Moderator Variables (Detailed)

### 3.1 GenAI Tool Variables

| Field | Type | Values | AI Extraction Prompt |
|-------|------|--------|---------------------|
| `genai_tool` | str | ChatGPT, Claude, Gemini, Llama, Copilot, Custom, Other, not_reported | "What generative AI tool was used in this study? Look for mentions of ChatGPT, GPT-4, Claude, Gemini, Bard, Llama, Copilot, etc." |
| `genai_tool_version` | str | gpt-3.5, gpt-4, gpt-4o, claude-3, gemini-pro, etc. | "What specific version or model of the AI tool was used? Look for version numbers like GPT-3.5, GPT-4, GPT-4o, Claude-3, etc." |
| `genai_access_type` | str | api, web_interface, custom_integration, plugin, not_reported | "How did participants access the AI tool? Via API, web interface, custom app, plugin, or integrated platform?" |

**GenAI Tool Classification Rules:**

```
ChatGPT Family:
  - ChatGPT (any version) → "ChatGPT"
  - GPT-3.5, GPT-3.5-turbo → "ChatGPT", version="gpt-3.5"
  - GPT-4, GPT-4-turbo → "ChatGPT", version="gpt-4"
  - GPT-4o → "ChatGPT", version="gpt-4o"

Claude Family:
  - Claude (any version) → "Claude"
  - Claude-3-opus, Claude-3-sonnet → version accordingly

Gemini/Bard:
  - Bard → "Gemini" (rebranded)
  - Gemini Pro, Gemini Ultra → "Gemini"

Open Source:
  - Llama, Llama-2, Llama-3 → "Llama"
  - Mixtral, Mistral → "Mistral"

Local/Custom:
  - Fine-tuned models → "Custom"
  - Multiple tools → list all, primary first

Not Reported:
  - "AI-based feedback", "LLM", "ChatBot" without specifics → "not_reported"
```

### 3.2 Educational Outcome Variables

| Field | Type | Values | AI Extraction Prompt |
|-------|------|--------|---------------------|
| `blooms_level` | str | remember, understand, apply, analyze, evaluate, create | "Based on the outcome measured, which Bloom's Taxonomy level does this assess? Remember=recall facts, Understand=explain concepts, Apply=use knowledge, Analyze=examine components, Evaluate=judge/critique, Create=produce new work" |
| `outcome_dimension` | str | cognitive, affective, behavioral, metacognitive | "Is this outcome cognitive (knowledge/skills), affective (attitudes/motivation), behavioral (actions/practices), or metacognitive (self-regulation/awareness)?" |
| `learning_domain` | str | knowledge_acquisition, skill_development, problem_solving, creativity, writing, critical_thinking, self_regulation, engagement, other | "What learning domain does this outcome belong to?" |

**Bloom's Taxonomy Classification Rules:**

```
REMEMBER (recall facts):
  - Factual recall tests
  - Knowledge quiz scores
  - Definition matching

UNDERSTAND (explain concepts):
  - Comprehension tests
  - Explanation quality
  - Concept mapping accuracy

APPLY (use knowledge):
  - Problem-solving tasks
  - Practical exercises
  - Code implementation
  - Language use tasks

ANALYZE (examine components):
  - Analysis quality scores
  - Comparison tasks
  - Error detection

EVALUATE (judge/critique):
  - Critique writing
  - Assessment accuracy
  - Peer review quality

CREATE (produce new work):
  - Creative writing scores
  - Original design tasks
  - Innovation measures
  - Generative tasks
```

**Outcome Dimension Classification:**

```
COGNITIVE:
  - Test scores, knowledge assessments
  - Skill performance, task accuracy
  - Learning gains, achievement

AFFECTIVE:
  - Attitudes, motivation
  - Self-efficacy, confidence
  - Satisfaction, enjoyment
  - Interest, engagement (emotional)

BEHAVIORAL:
  - Usage patterns, participation
  - Time on task, completion rates
  - Behavioral changes

METACOGNITIVE:
  - Self-regulation measures
  - Metacognitive awareness
  - Learning strategies
  - Self-assessment accuracy
```

### 3.3 Study Design Variables

| Field | Type | Values | AI Extraction Prompt |
|-------|------|--------|---------------------|
| `study_design` | str | RCT, quasi-experimental, pre-post, crossover, factorial | "What is the study design? RCT=random assignment, Quasi-experimental=non-random groups, Pre-post=single group before/after, Crossover=participants switch conditions" |
| `intervention_duration` | str | single_session, <1_week, 1-4_weeks, 1-3_months, >3_months | "How long was the AI intervention period?" |
| `intervention_type` | str | direct_instruction, tutoring, feedback, writing_assistant, problem_solving, other | "What type of AI intervention was used?" |
| `control_condition` | str | no_treatment, traditional, human_tutor, alternative_tech, placebo | "What did the control group receive?" |

**Study Design Classification:**

```
RCT (Randomized Controlled Trial):
  - Random assignment explicitly stated
  - "randomly assigned", "randomized"

QUASI-EXPERIMENTAL:
  - Non-random group assignment
  - Intact groups (classes, sections)
  - "quasi-experimental", "non-equivalent groups"

PRE-POST (Single Group):
  - One group measured before and after
  - No control group

CROSSOVER:
  - All participants experience both conditions
  - Counterbalanced design

FACTORIAL:
  - Multiple independent variables
  - 2×2, 2×3 designs
```

### 3.4 Context Variables

| Field | Type | Values | AI Extraction Prompt |
|-------|------|--------|---------------------|
| `education_level` | str | undergraduate, graduate, K-12, professional, mixed | "What education level were the participants?" |
| `discipline` | str | STEM, humanities, medicine, business, education, language, CS, engineering, mixed | "What academic discipline or subject area?" |
| `country` | str | ISO country code | "In which country was this study conducted?" |
| `sample_size_total` | int | Total N | "What is the total sample size (treatment + control)?" |
| `publication_type` | str | journal, conference, preprint, thesis | "Publication type?" |

---

## Layer 2: Effect Size Type Classification

| ES_Type | Description | When to Use |
|---------|-------------|-------------|
| `POST_BETWEEN` | Post-test between groups | Control group exists, post-test only reported |
| `ANCOVA` | ANCOVA-adjusted means | Pre-test used as covariate |
| `CHANGE` | Change score comparison | Pre-post change compared between groups |
| `PRE_POST` | Single group pre-post | No control group |
| `INDEPENDENT_TEST` | Separate test scores | Treatment vs control on independent assessment |

**ES Type Selection Hierarchy:**
1. POST_BETWEEN (preferred)
2. ANCOVA (if adjusted)
3. CHANGE (if change scores reported)
4. PRE_POST (last resort)

---

## AI Extraction Prompts (C6 Agent)

### Statistical Values Extraction

```python
STAT_EXTRACTION_PROMPT = """
From this PDF, extract the following statistical values for the outcome "{outcome_name}":

For the TREATMENT GROUP (GenAI/AI intervention):
1. Sample size (n): Number of participants
2. Mean (M): Post-test mean score
3. Standard Deviation (SD): Post-test SD

For the CONTROL GROUP (Traditional/No AI):
4. Sample size (n): Number of participants
5. Mean (M): Post-test mean score
6. Standard Deviation (SD): Post-test SD

Look in:
- Tables (especially results tables)
- Results section text
- Supplementary materials

For each value, provide:
- The extracted value
- Exact location (page, table, paragraph)
- Confidence (0-100%)

If SD is not directly reported, look for:
- Standard Error (SE) → SD = SE × √n
- 95% CI → SE = (upper - lower) / 3.92
"""
```

### Moderator Variables Extraction

```python
MODERATOR_EXTRACTION_PROMPT = """
From this PDF, extract the following moderator variables:

1. GenAI Tool:
   - What AI tool was used? (ChatGPT, Claude, Gemini, Llama, etc.)
   - What version? (GPT-3.5, GPT-4, GPT-4o, etc.)
   - How was it accessed? (web, API, custom app)

2. Bloom's Taxonomy Level:
   - What cognitive level does the outcome measure?
   - Remember, Understand, Apply, Analyze, Evaluate, Create

3. Study Design:
   - RCT, quasi-experimental, pre-post, crossover?
   - Was random assignment used?

4. Context:
   - Education level (undergraduate, graduate, K-12)
   - Discipline/Subject area
   - Country
   - Intervention duration

Look for these in:
- Abstract, Methods, Participants sections
- Intervention description
- Study design statements
"""
```

---

## Data Quality Rules

### Required Fields (Must Have)

| Field | Criticality |
|-------|-------------|
| study_id | CRITICAL |
| es_id | CRITICAL |
| outcome_name | CRITICAL |
| n_treatment | HIGH |
| n_control | HIGH |
| m_treatment | HIGH (for Hedges' g) |
| sd_treatment | HIGH (for Hedges' g) |
| m_control | HIGH (for Hedges' g) |
| sd_control | HIGH (for Hedges' g) |

### Moderator Completeness Targets

| Variable | Target | Current (V8) |
|----------|--------|--------------|
| genai_tool | ≥90% | 48% known |
| blooms_level | ≥80% | 59% coded |
| study_design | ≥95% | 44% known |
| outcome_dimension | ≥95% | 98% coded |

---

## V8 → V8.1 Migration

### Changes

| Aspect | V8 | V8.1 |
|--------|----|----|
| Structure | 26 columns | 47 columns (5-layer) |
| GenAI Tool | 48% known | Target ≥90% |
| Blooms Level | 59% coded | Target ≥80% |
| Study Design | 44% known | Target ≥95% |
| AI Provenance | None | Full tracking |
| Human Verification | Basic | Structured workflow |

### New Columns in V8.1

```
ADDED:
- genai_tool_version
- genai_access_type
- learning_domain
- intervention_duration
- intervention_type
- control_condition
- discipline
- country
- publication_type
- ai_confidence_avg
- ai_method
- ai_conflicts
- ai_extraction_json
- verified_status
- verified_by
- verified_date
- corrections_json
- final_values_json
- sign_off
```

---

## Integration with Diverga

### C5-MetaAnalysisMaster

```python
# Context-specific configuration
c5.configure(
    project_type="genai_he",
    moderator_schema=GENAI_HE_MODERATORS,
    extraction_prompts=GENAI_HE_PROMPTS,
    blooms_taxonomy=True,
    genai_tool_classification=True
)
```

### C6-DataIntegrityGuard

```python
# Extract with GenAI-HE schema
c6.extract_with_schema(
    pdf_folder="./pdfs",
    schema="genai_he_v8.1",
    include_moderators=True,
    blooms_classification=True
)
```

### C7-ErrorPreventionEngine

```python
# GenAI-HE specific validation
c7.validate_moderators(
    required=["genai_tool", "blooms_level", "study_design"],
    optional=["genai_tool_version", "learning_domain"]
)
```

---

## References

- Anderson & Krathwohl (2001). A Taxonomy for Learning, Teaching, and Assessing
- Bloom et al. (1956). Taxonomy of Educational Objectives
- Universal Meta-Analysis Codebook v2.1
- Diverga v6.3.0 C5/C6/C7 Agent Specifications

---

*Created: 2026-01-26*
*Author: Claude Code*
