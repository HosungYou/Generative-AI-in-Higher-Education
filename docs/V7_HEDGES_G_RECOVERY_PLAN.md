# V7 Hedges' g Recovery Plan

**Date**: 2026-01-26
**Status**: Action Required
**Dataset**: GenAI_MetaAnalysis_v7.csv

## Executive Summary

V7 데이터셋 분석 결과, **155개 효과크기(42.5%)에서 Hedges_g가 누락**되어 있음.
**원인**: SD(표준편차) 값이 PDF에서 추출되지 않음
**해결책**: SD 재추출 시 계산 가능

**복구 가능 추정**: 45개 효과크기 (High priority - SD만 추출하면 계산 가능)
**추가 복구 가능**: 30개 효과크기 (Medium priority - M과 SD 재추출 필요)

---

## 1. 현황 분석

### 1.1 전체 데이터 현황

| 항목 | 수량 | 비율 |
|------|------|------|
| 총 효과크기 | 365 | 100% |
| Hedges_g 있음 | 210 | 57.5% |
| **Hedges_g 없음** | **155** | **42.5%** |

### 1.2 누락 데이터의 가용성 (155개 행 대상)

| 데이터 | 있음 | 비율 | 비고 |
|--------|------|------|------|
| n_Treatment | 96 | 61.9% | 표본크기는 대부분 추출됨 |
| M_Treatment | 102 | 65.8% | 평균값도 비교적 많음 |
| **SD_Treatment** | **40** | **25.8%** | **핵심 문제** |
| n_Control | 75 | 48.4% | - |
| M_Control | 89 | 57.4% | - |
| **SD_Control** | **28** | **18.1%** | **핵심 문제** |

**분석**: SD(표준편차)가 가장 많이 누락됨. 이는 PDF에서 표 추출 시 SD 컬럼이 인식되지 않았거나, 연구에서 SD 대신 SE(표준오차)를 보고했을 가능성이 있음.

### 1.3 복구 가능성 분류

| 분류 | 수량 | 조건 | 작업량 |
|------|------|------|--------|
| **즉시 계산 가능** | 0 | n, M, SD 모두 있음 | 없음 |
| **High Priority** | 45 | n, M은 있고 SD만 없음 | SD만 재추출 |
| **Medium Priority** | 30 | n은 있고 M, SD 없음 | M, SD 재추출 |
| **Low Priority** | 80 | n 또는 복잡한 경우 | 전체 재검토 |

---

## 2. 누락 연구 목록

**총 39개 연구**에서 일부 또는 전체 Hedges_g 누락:

```
Study IDs: 2, 6, 7, 10, 11, 12, 13, 14, 15, 17, 21, 22, 24, 26, 27, 28, 29, 30,
           31, 33, 35, 37, 38, 40, 44, 45, 49, 50, 52, 55, 57, 58, 59, 62, 64,
           65, 66, 67, 68
```

### 재추출 우선순위

1. **High Priority (45개 효과크기)**
   - 조건: n, M은 있지만 SD 없음
   - 작업: PDF에서 SD 컬럼만 추출
   - 예상 시간: 2-3시간

2. **Medium Priority (30개 효과크기)**
   - 조건: n은 있지만 M, SD 없음
   - 작업: PDF에서 평균과 SD 재추출
   - 예상 시간: 4-5시간

3. **Low Priority (80개 효과크기)**
   - 조건: 통계량 기반 변환 또는 원문 재검토 필요
   - 작업: t-통계량, F-통계량, η² 등 활용 또는 수동 확인
   - 예상 시간: 가변적

---

## 3. Hedges' g 계산 공식

### 3.1 방법 1: M, SD, n에서 계산 (권장)

```python
from math import sqrt

def calculate_hedges_g(m1, sd1, n1, m2, sd2, n2):
    """
    Calculate Hedges' g effect size from descriptive statistics

    Parameters:
    - m1, m2: Means of treatment and control groups
    - sd1, sd2: Standard deviations
    - n1, n2: Sample sizes

    Returns:
    - Hedges' g (bias-corrected effect size)
    """
    # Step 1: Calculate pooled standard deviation
    pooled_sd = sqrt(((n1-1)*sd1**2 + (n2-1)*sd2**2) / (n1 + n2 - 2))

    # Step 2: Calculate Cohen's d
    d = (m1 - m2) / pooled_sd

    # Step 3: Calculate Hedges' g correction factor (J)
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))

    # Step 4: Apply correction
    g = d * J

    return g
```

**검증 결과**: 기존 210개 Hedges_g 중 20개 샘플 재계산 → 19/20 일치 (95% 일치율)

### 3.2 방법 2: t-통계량에서 계산

```python
def hedges_g_from_t(t, n1, n2):
    """
    Calculate Hedges' g from t-statistic
    Useful when only t-test results are reported
    """
    # Step 1: Calculate Cohen's d
    d = t * sqrt(1/n1 + 1/n2)

    # Step 2: Apply Hedges' correction
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))
    g = d * J

    return g
```

### 3.3 방법 3: F-통계량에서 계산 (df1=1인 경우)

```python
def hedges_g_from_F(F, n1, n2):
    """
    Calculate Hedges' g from F-statistic (for two groups only)
    """
    # Step 1: Calculate Cohen's d
    d = sqrt(F * (n1 + n2) / (n1 * n2))

    # Step 2: Apply Hedges' correction
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))
    g = d * J

    return g
```

### 3.4 SE(표준오차)에서 SD 변환

만약 PDF에서 SE(Standard Error)가 보고된 경우:

```python
SD = SE * sqrt(n)
```

---

## 4. 다음 단계

### Phase 1: High Priority 처리 (1-2일)

1. **작업 파일 준비**
   - `V7_SD_EXTRACTION_CHECKLIST.csv` 생성 완료
   - High priority 45개 행 필터링

2. **SD 재추출**
   - PDF에서 SD 컬럼만 수동 확인
   - SE로 보고된 경우 SD로 변환
   - 추출 결과를 checklist에 업데이트

3. **Hedges_g 자동 계산**
   ```python
   # 예시 스크립트
   for idx, row in high_priority.iterrows():
       if row['has_n'] and row['has_M'] and row['SD_Treatment'] and row['SD_Control']:
           g = calculate_hedges_g(
               row['M_Treatment'], row['SD_Treatment'], row['n_Treatment'],
               row['M_Control'], row['SD_Control'], row['n_Control']
           )
           df.at[idx, 'Hedges_g'] = g
   ```

4. **V8 데이터셋 생성**
   - 45개 효과크기 복구 후 V8로 버전업
   - 총 효과크기: 210 + 45 = **255개 (70%)**

### Phase 2: Medium Priority 처리 (3-5일)

1. PDF에서 M, SD 재추출 (30개 행)
2. Hedges_g 계산
3. V9 데이터셋 생성: **285개 (78%)**

### Phase 3: Low Priority 처리 (가변)

1. 통계량(t, F, η²) 활용 가능 여부 확인
2. 변환 가능한 경우 계산
3. 불가능한 경우 "Insufficient Data" 문서화
4. 최종 V10 데이터셋: **예상 ~310개 (85%)**

---

## 5. 예상 결과

| 단계 | 복구 가능 ES | 누적 유효 ES | 비율 | 소요 시간 |
|------|-------------|--------------|------|----------|
| 현재 (V7) | 0 | 210 | 57.5% | - |
| Phase 1 (V8) | +45 | 255 | 69.9% | 1-2일 |
| Phase 2 (V9) | +30 | 285 | 78.1% | 3-5일 |
| Phase 3 (V10) | +25 | 310 | 84.9% | 가변 |
| **최대 가능** | **+100** | **~310** | **~85%** | **1-2주** |

---

## 6. 품질 관리

### 6.1 재추출 체크리스트
- [ ] PDF 원문과 추출값 일치 확인
- [ ] SD vs SE 구분 확인
- [ ] 소수점 자릿수 일관성 유지
- [ ] 극단값(outlier) 검토

### 6.2 계산 검증
- [ ] 무작위 20% 샘플 수동 재계산
- [ ] 기존 Hedges_g와 비교 (있는 경우)
- [ ] 효과크기 범위 타당성 확인 (-3 < g < 3 일반적)

### 6.3 메타분석 영향 평가
- [ ] V7 vs V8 메타분석 결과 비교
- [ ] 이질성(I²) 변화 확인
- [ ] 출판 편향(funnel plot) 재검토

---

## 7. 참고문헌

- Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size and related estimators. *Journal of Educational Statistics*, 6(2), 107-128.
- Borenstein, M., Hedges, L. V., Higgins, J. P., & Rothstein, H. R. (2021). *Introduction to Meta-Analysis* (2nd ed.). Wiley.
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs. *Frontiers in Psychology*, 4, 863.

---

## 부록: 파일 위치

- **Recovery Plan**: `docs/V7_HEDGES_G_RECOVERY_PLAN.md` (이 문서)
- **Extraction Checklist**: `data/03_final/V7_SD_EXTRACTION_CHECKLIST.csv`
- **Current Dataset**: `data/03_final/GenAI_MetaAnalysis_v7.csv`
- **Changelog**: `data/03_final/V7_CHANGELOG.md`

---

**다음 작업**: High priority 45개 행에 대한 SD 재추출 시작
