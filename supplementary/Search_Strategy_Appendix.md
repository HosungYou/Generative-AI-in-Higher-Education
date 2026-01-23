# Appendix: Complete Search Strategy

## GenAI Effectiveness in Higher Education Meta-Analysis

**Search Dates**: November 2025 – January 2026
**Date Range of Publications**: November 2022 – January 2026

---

## 1. Database Search Strategies

### 1.1 PsycINFO (via Penn State Libraries - EBSCOhost)

**Search Date**: November 15, 2025
**Interface**: EBSCOhost

```
S1: TI ("generative AI" OR "generative artificial intelligence" OR "ChatGPT"
    OR "GPT-3" OR "GPT-4" OR "large language model*" OR "LLM" OR "AI chatbot*"
    OR "Claude" OR "Gemini" OR "Bard") OR AB ("generative AI" OR "generative
    artificial intelligence" OR "ChatGPT" OR "GPT-3" OR "GPT-4" OR "large
    language model*" OR "LLM" OR "AI chatbot*" OR "Claude" OR "Gemini" OR "Bard")

S2: TI ("learning outcome*" OR "academic achievement" OR "student performance"
    OR "learning gain*" OR "academic performance" OR "educational outcome*"
    OR "knowledge acquisition" OR "skill development") OR AB ("learning outcome*"
    OR "academic achievement" OR "student performance" OR "learning gain*"
    OR "academic performance" OR "educational outcome*" OR "knowledge acquisition"
    OR "skill development")

S3: TI ("higher education" OR "university" OR "universit*" OR "college*"
    OR "undergraduate*" OR "graduate student*" OR "postsecondary"
    OR "tertiary education") OR AB ("higher education" OR "university"
    OR "universit*" OR "college*" OR "undergraduate*" OR "graduate student*"
    OR "postsecondary" OR "tertiary education")

S4: S1 AND S2 AND S3

S5: S4 NOT (TI ("K-12" OR "primary school*" OR "secondary school*"
    OR "elementary" OR "high school" OR "middle school"))

Limiters: Publication Year: 2022-2026; Language: English
```

**Records Retrieved**: 412

---

### 1.2 ERIC (via Penn State Libraries - EBSCOhost)

**Search Date**: November 15, 2025
**Interface**: EBSCOhost

```
S1: TI ("generative AI" OR "ChatGPT" OR "GPT-3" OR "GPT-4" OR "large language
    model*" OR "LLM" OR "AI chatbot*" OR "Claude" OR "Gemini") OR AB ("generative
    AI" OR "ChatGPT" OR "GPT-3" OR "GPT-4" OR "large language model*" OR "LLM"
    OR "AI chatbot*" OR "Claude" OR "Gemini")

S2: DE "Higher Education" OR DE "Postsecondary Education" OR DE "College Students"
    OR DE "Undergraduate Students" OR DE "Graduate Students"

S3: DE "Academic Achievement" OR DE "Learning" OR DE "Student Achievement"
    OR DE "Educational Outcomes" OR TI ("learning outcome*" OR "academic
    achievement" OR "student performance")

S4: S1 AND S2 AND S3

S5: S4 NOT DE "Elementary Education" NOT DE "Secondary Education"

Limiters: Publication Date: Nov 2022-Jan 2026; Language: English
```

**Records Retrieved**: 287

---

### 1.3 Education Source (via Penn State Libraries - EBSCOhost)

**Search Date**: November 16, 2025
**Interface**: EBSCOhost

```
S1: TI ("generative AI" OR "ChatGPT" OR "GPT*" OR "large language model*"
    OR "LLM" OR "AI chatbot*" OR "Claude" OR "Gemini" OR "artificial intelligence")
    OR AB ("generative AI" OR "ChatGPT" OR "GPT*" OR "large language model*"
    OR "LLM" OR "AI chatbot*")

S2: TI ("higher education" OR "university" OR "college" OR "undergraduate"
    OR "graduate") OR AB ("higher education" OR "university" OR "college")

S3: TI ("learning" OR "achievement" OR "performance" OR "outcome*" OR "effect*")
    OR AB ("learning outcome*" OR "academic achievement" OR "effect*")

S4: S1 AND S2 AND S3

Limiters: Publication Date: 2022-2026; Source Types: Academic Journals;
          Language: English
```

**Records Retrieved**: 534

---

### 1.4 ProQuest Dissertations & Theses Global

**Search Date**: November 17, 2025
**Interface**: ProQuest

```
Query: (ti("generative AI" OR "ChatGPT" OR "GPT" OR "large language model")
        OR ab("generative AI" OR "ChatGPT" OR "GPT" OR "large language model"))
       AND (ti("higher education" OR "university" OR "college")
        OR ab("higher education" OR "university" OR "college"))
       AND (ti("learning" OR "achievement" OR "performance" OR "effect")
        OR ab("learning outcome" OR "academic achievement" OR "effect"))

Filters: Date range: Nov 2022 - Jan 2026
         Document type: Dissertation/Thesis
         Language: English
```

**Records Retrieved**: 89

---

### 1.5 Semantic Scholar (API)

**Search Date**: November 20, 2025
**Interface**: REST API v1

```python
# Python code for Semantic Scholar API query
import semanticscholar as sch

query = """
("generative AI" OR "ChatGPT" OR "GPT-4" OR "large language model" OR "LLM")
AND ("higher education" OR "university" OR "college")
AND ("learning outcome" OR "academic achievement" OR "student performance")
"""

params = {
    'query': query,
    'year': '2022-2026',
    'fieldsOfStudy': ['Education', 'Computer Science'],
    'openAccessPdf': True,  # Prioritize open access
    'limit': 1000
}

# API endpoint
# GET https://api.semanticscholar.org/graph/v1/paper/search

# Fields requested: paperId, title, abstract, year, authors,
#                   openAccessPdf, citationCount, fieldsOfStudy
```

**Records Retrieved**: 1,247

---

### 1.6 OpenAlex (API)

**Search Date**: November 22, 2025
**Interface**: REST API

```
# OpenAlex API query
GET https://api.openalex.org/works

Parameters:
  filter:
    - from_publication_date:2022-11-01
    - to_publication_date:2026-01-31
    - concepts.id:C41008148 (Computer Science) OR C15744967 (Education)
    - has_abstract:true

  search:
    "generative AI" OR "ChatGPT" OR "GPT" OR "large language model"

  per_page: 200
  mailto: hosung@psu.edu (for polite pool access)
```

**Records Retrieved**: 892

---

### 1.7 arXiv (API)

**Search Date**: November 25, 2025
**Interface**: Export API

```
# arXiv API query
GET http://export.arxiv.org/api/query

Query string:
  search_query: (all:"generative AI" OR all:"ChatGPT" OR all:"large language model")
                AND (all:"education" OR all:"learning" OR all:"student")

  start: 0
  max_results: 500
  sortBy: submittedDate
  sortOrder: descending

# Filtered to categories: cs.CL, cs.AI, cs.CY, cs.HC
```

**Records Retrieved**: 198

---

## 2. Supplementary Search Strategies

### 2.1 Backward Citation Searching

**Procedure**:
1. Identified 5 key review articles on AI in education
2. Screened reference lists for eligible studies
3. Searched citing articles of seminal works

**Key Seed Articles**:
- Zawacki-Richter et al. (2019) - Systematic review of AI in HE
- Chen et al. (2020) - AI in education review
- Hwang et al. (2020) - AI in education trends
- Crompton & Burke (2023) - AI in HE scoping review
- Mollick & Mollick (2023) - ChatGPT in education

**Additional Records**: 112

### 2.2 Forward Citation Searching

**Procedure**:
1. Used Google Scholar "Cited by" feature
2. Searched Semantic Scholar citation network
3. Identified new experimental studies citing key reviews

**Additional Records**: 75

### 2.3 Grey Literature Search

**Sources Searched**:
- SSRN (Social Science Research Network)
- EdArXiv (Education preprint server)
- OSF Preprints
- Conference proceedings (AERA, CHI, L@S, AIED)

**Records Retrieved**: 187 (combined)

---

## 3. Search Results Summary

| Database/Source | Records Retrieved |
|-----------------|-------------------|
| PsycINFO | 412 |
| ERIC | 287 |
| Education Source | 534 |
| ProQuest Dissertations | 89 |
| Semantic Scholar | 1,247 |
| OpenAlex | 892 |
| arXiv | 198 |
| Citation searching | 187 |
| Grey literature | 187 |
| **Total** | **4,033** |
| After deduplication | **3,247** |

---

## 4. Search Update

**Final Search Date**: January 15, 2026

An updated search was conducted across all databases to capture newly published studies between the initial search (November 2025) and manuscript preparation.

**Additional Records from Update**: 398
**New Studies Included**: 18 (Studies 48-65 in final dataset)

---

## 5. PRISMA-S Checklist Compliance

| Item | Status | Notes |
|------|--------|-------|
| Database name | ✓ | All 7 databases named |
| Multi-database searching | ✓ | Cross-platform searches documented |
| Study registries | ✓ | PROSPERO searched |
| Online resources | ✓ | Grey literature sources specified |
| Citation searching | ✓ | Backward and forward searches conducted |
| Contacts | N/A | No author contacts for unpublished data |
| Search strategies | ✓ | Full strategies provided above |
| Limits and restrictions | ✓ | Date and language limits specified |
| Search filters | ✓ | Subject filters documented |
| Prior work | N/A | No prior reviews by this team |
| Updates | ✓ | January 2026 update documented |
| Dates of searches | ✓ | All dates specified |

---

## 6. Reproducibility Statement

All search strategies are documented with sufficient detail for replication. Raw search results (prior to deduplication) are available upon request. The deduplicated reference list is provided in the supplementary data files.

---

*Appendix Version 1.0 | Created: 2026-01-23*
