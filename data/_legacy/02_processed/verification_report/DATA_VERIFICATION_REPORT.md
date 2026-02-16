# Meta-Analysis Data Verification Report

**Project:** GenAI Effectiveness in Higher Education Meta-Analysis
**Verification Date:** 2026-01-26
**Verified By:** Automated Script + Manual Review
**Report Version:** 1.0

---

## Executive Summary

This report documents the verification of 25 studies that lacked prior OCR extraction evidence in the meta-analysis dataset. The verification process cross-referenced extracted effect size data against original PDF documents.

### Key Findings

| Status | Count | Percentage |
|--------|-------|------------|
| **VERIFIED** | 7 | 28% |
| **PARTIALLY_VERIFIED** | 2 | 8% |
| **STATISTICS_FOUND_NO_MATCH** | 15 | 60% |
| **NO_STATISTICS_FOUND** | 1 | 4% |

**⚠️ CRITICAL: 64% of unverified studies (16/25) have data that could not be matched to PDF content.**

---

## Methodology

### Verification Process

1. **PDF Text Extraction**: Used PyMuPDF (fitz) to extract text from each PDF
2. **Statistical Pattern Recognition**: Applied regex patterns to identify:
   - Means (M = X.XX)
   - Standard Deviations (SD = X.XX)
   - Sample sizes (N = XX)
   - F-values, t-values, p-values
   - Cohen's d, Hedges' g, eta squared
3. **Comparison**: Matched extracted values against CSV data within 10% tolerance
4. **Confidence Calculation**: (Matched values / Total checked values) × 100

### Tolerance Criteria

- **Exact match**: Difference < 0.1
- **Close match**: Relative difference < 10%

---

## Detailed Results by Study

### ✅ VERIFIED Studies (7)

These studies have high confidence that CSV data matches PDF content.

| Study ID | Authors | Year | Confidence | Notes |
|----------|---------|------|------------|-------|
| 032 | Ching-Yi Chang; Wen-Song Su | 2025 | 100.0% | All values matched |
| 041 | Jin‐Hee Han; Ruqin Ren | 2025 | 91.7% | Most values matched |
| 043 | Haixin Liu | 2024 | 100.0% | All values matched |
| 048 | Sumie Chan; N. Lo; Alan Wong | 2024 | 75.0% | Good match |
| 054 | Santosh Mahapatra | 2024 | 100.0% | All values matched |
| 060 | Unknown | 2024 | 75.0% | Good match |
| 069 | Unknown | N/A | 100.0% | All values matched |

### ⚠️ PARTIALLY_VERIFIED Studies (2)

These studies have moderate confidence with some matching values.

| Study ID | Authors | Year | Confidence | Notes |
|----------|---------|------|------------|-------|
| 008 | Litian Hong | 2025 | 50.0% | Half of values matched |
| 023 | Viktor Taneski; Sašo Karakatič | 2025 | 57.1% | Some values matched |

### ❌ STATISTICS_FOUND_NO_MATCH Studies (15)

These studies have statistics in PDFs but extracted CSV values don't match.

| Study ID | Authors | Year | Confidence | Issue Description |
|----------|---------|------|------------|-------------------|
| 010 | Hudson K. Etkin | 2025 | 0% | PDF has N=195, but no M/SD; CSV has specific M/SD values |
| 016 | Yabing Jiang | 2025 | 28.6% | PDF means (8.43, 7.78) ≠ CSV means (7.33, 8.43) |
| 017 | Wang Jian | 2025 | 0% | CSV has all NaN values; PDF has some means |
| 019 | Guoqing Zhao | 2025 | 25.0% | Partial match only |
| 020 | Xusheng Dai | 2025 | 0% | CSV has all NaN; PDF has SDs but no means |
| 022 | Larissa I. Velez | 2025 | 0% | No matching values |
| 025 | Ting-Ting Wu | 2025 | 12.5% | Very low match rate |
| 034 | Nataliya Kasimovskaya | 2025 | 0% | No matching values |
| 036 | Wafa Muhammad | 2025 | 25.0% | Partial match only |
| 042 | Atakan Coban | 2024 | 0% | No matching values |
| 046 | Hsin-Yu Lee | 2024 | 0% | No matching values |
| 047 | Sireesha Prathigadapa | 2024 | 0% | No matching values |
| 051 | Seyyed Kazem Banihashem | 2024 | 0% | No matching values |
| 053 | Unknown | 2024 | 0% | No matching values |
| 056 | Joanne Leong | 2024 | 0% | No matching values |

### ❓ NO_STATISTICS_FOUND Studies (1)

| Study ID | Authors | Year | Notes |
|----------|---------|------|-------|
| 063 | Unknown | 2023 | PDF may not contain extractable statistics |

---

## Detailed Issue Analysis

### Issue Type 1: CSV has NaN values while PDF has statistics

**Affected Studies:** 017, 020

The CSV file contains NaN (missing) values for M/SD, but the PDF clearly contains statistical information. This suggests:
- Data extraction was incomplete
- Manual data entry error
- Statistics in PDF were not in expected format

**Example (Study 017):**
- PDF contains: M=20.37, SD=0.53
- CSV shows: m_treatment=NaN, sd_treatment=NaN

### Issue Type 2: Statistics exist but values don't match

**Affected Studies:** 010, 016, 019, and others

The PDF contains clear statistical values, but they don't match the CSV data within tolerance.

**Example (Study 016):**
- PDF means: [8.43, 7.78, 3.98, 4.16, 3.58]
- CSV means: [7.33, 8.43, 3.63]
- Partial overlap suggests possible data entry errors

### Issue Type 3: No statistics extracted from PDF

**Affected Studies:** 063

The PDF may contain statistics in formats not captured by regex patterns (e.g., images, tables).

---

## Data Quality Classification

Based on verification results, the meta-analysis data should be classified as:

### Tier 1: Fully Verified (High Confidence)
- Studies with OCR cache evidence AND verification ≥70%
- **Count:** ~42 studies (35 with OCR + 7 newly verified)
- **Effect Sizes:** ~250

### Tier 2: Partially Verified (Medium Confidence)
- Studies with verification 40-69%
- **Count:** 2 studies
- **Effect Sizes:** ~12

### Tier 3: Unverified (Low Confidence)
- Studies with verification <40% or STATISTICS_FOUND_NO_MATCH
- **Count:** 16 studies
- **Effect Sizes:** ~110

---

## Recommendations

### Immediate Actions

1. **Manual Review Required:** All 16 Tier 3 studies should be manually reviewed against original PDFs
2. **Data Correction:** Studies 017, 020 with NaN values need re-extraction
3. **Sensitivity Analysis:** Run meta-analysis with/without Tier 3 studies

### Data File Updates

1. Add `verification_status` column to effect size data
2. Add `verification_confidence` column
3. Add `data_tier` classification (1, 2, or 3)

### Documentation

1. Include this verification report in supplementary materials
2. Disclose verification status in methods section
3. Report sensitivity analyses excluding unverified data

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-26 | Initial verification report |

---

## Appendix: Verification Script Output

See `verification_results.json` for detailed JSON output of all verification checks.
