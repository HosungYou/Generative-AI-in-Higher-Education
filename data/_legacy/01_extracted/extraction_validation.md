# Effect Size Extraction Validation Report

## Automated Extraction Summary
- **Total PDFs**: 16
- **Cohen's d extracted**: 10 (62.5%)
- **Eta squared extracted**: 4 (25.0%)
- **Sample size extracted**: 15 (93.8%)

---

## ⚠️ Values Requiring Verification

### Unusually Large Effect Sizes (d > 2.0)

| Filename | Extracted d | Issue | Action |
|----------|-------------|-------|--------|
| s10639-024-12705-z.pdf | 3.00 | Unusually large | Manual verification required |
| 1-s2.0-S2666920X23000772-main.pdf | 2.98 | Unusually large | Manual verification required |

> **Note**: Effect sizes > 2.0 are rare in educational research. These may be:
> - Misextracted values (e.g., t-values captured as d)
> - Actually correct but represent extreme interventions
> - Different effect size metrics

### Missing Effect Sizes

| Filename | N | Available Statistics | Conversion Possible? |
|----------|---|---------------------|---------------------|
| jmir-2024-1-e57037.pdf | 1051 | None extracted | Needs manual review |
| s41599-024-02751-w.pdf | 100 | t=0.599, F=7.039 | ✅ Can convert from F |
| qgae170.pdf | 115 | p=0.57 | ❌ Insufficient |
| Using_a_Chatbot...pdf | - | t=2.66, F=0.778 | ⚠️ Need N for conversion |

---

## ✅ Validated Extractions (Reasonable Values)

| Study | N | Cohen's d | η² | Status |
|-------|---|-----------|-----|--------|
| 20250711-273024-ln0ri4.pdf | 198 | 1.07 | - | ✅ Large but plausible |
| s43031-025-00125-z.pdf | 60 | 0.61 | - | ✅ Medium effect |
| 1-s2.0-S0360131524000459-main.pdf | 77 | 0.53 | - | ✅ Medium effect |
| s44217-025-00700-6.pdf | 117 | - | 0.789 | ⚠️ Very large η² - verify |
| Can ChatGPT enhance...pdf | 534 | - | 0.04 | ✅ Small effect |
| s41598-025-97652-6.pdf | 316 | 0.98 | - | ✅ Large effect |
| Brit J Educational Tech...pdf | 49 | 0.62 | - | ✅ Medium effect |
| Liu Mathematical Creativity...pdf | 110 | 1.36 | - | ✅ Large effect |
| s10639-025-13733-z.pdf | 79 | 0.53 | 0.111 | ✅ Medium effect |
| ChatGPT vs AWE...pdf | 118 | 0.71 | 0.10 | ✅ Medium effect |

---

## Effect Size Conversion Formulas

For studies with statistics but no effect size:

### From F-value (one-way ANOVA):
```
η² = (F × df₁) / (F × df₁ + df₂)
d = √(4η² / (1 - η²))
```

### From t-value:
```
d = 2t / √(df)
```

### From η² (partial eta squared):
```
d = 2 × √(η² / (1 - η²))
```

---

## Study-by-Study Mapping

| PDF Filename | Study Name | Year | Domain |
|--------------|------------|------|--------|
| 20250711-273024-ln0ri4.pdf | Knowledge Retention Study | 2025 | Cognitive dependency |
| jmir-2024-1-e57037.pdf | JMIR Study | 2024 | Medical education |
| s43031-025-00125-z.pdf | Morocco STEM | 2025 | STEM education |
| 1-s2.0-S0360131524000459-main.pdf | Essel et al. | 2024 | Cognitive skills |
| s41599-024-02751-w.pdf | Humanities & Social Sciences | 2024 | General |
| s44217-025-00700-6.pdf | ESP Writing | 2025 | Writing |
| Can ChatGPT enhance...pdf | Geng & Razali | 2025 | Creativity |
| qgae170.pdf | Oxford Academic | 2024 | Medical |
| Using_a_Chatbot...pdf | Yin et al. | 2024 | Formative feedback |
| s41598-025-97652-6.pdf | Harvard AI Tutoring | 2025 | Learning |
| Brit J Educational Tech...pdf | Urban et al. | 2025 | Epistemic beliefs |
| s10639-024-12705-z.pdf | Education IT | 2024 | Programming |
| Liu Mathematical Creativity...pdf | Liu et al. | 2025 | Math creativity |
| s10639-025-13733-z.pdf | Python Programming | 2025 | Programming |
| 1-s2.0-S2666920X23000772-main.pdf | Gan et al. | 2024 | Medical education |
| ChatGPT vs AWE...pdf | ChatGPT vs AWE | 2025 | Writing |

---

## Next Steps

1. **Manual verification** of d > 2.0 values
2. **Convert statistics** for studies without effect sizes
3. **Fill missing N** for Using_a_Chatbot...pdf
4. **Verify η² = 0.789** in ESP Writing study (seems too high)
5. **Integrate** all effect sizes into meta-analysis dataset
