# OSF 등록 및 GitHub 연동 To-Do List

## 완료된 작업 ✅

- [x] OSF 디렉토리 구조 생성
- [x] 데이터 파일 복사 (raw, processed)
- [x] R 분석 스크립트 복사
- [x] 원고 및 보충자료 복사
- [x] OSF용 README.md 생성
- [x] Git 저장소 초기화
- [x] CC BY 4.0 라이선스 추가
- [x] 초기 커밋 완료

---

## 실천적 To-Do List 📋

### 1단계: GitHub 저장소 생성 및 연동

**GitHub에서 수행할 작업:**

1. [ ] **GitHub 로그인** → https://github.com
2. [ ] **새 저장소 생성**
   - "New repository" 클릭
   - Repository name: `GenAI-HE-MetaAnalysis`
   - Description: `Three-level meta-analysis of GenAI effectiveness on learning outcomes in higher education`
   - **Public** 선택 (Open Science)
   - README 추가 **안함** (이미 있음)
   - License 추가 **안함** (이미 있음)
3. [ ] **생성 후 표시되는 명령어 복사**

**터미널에서 수행할 작업:**
```bash
cd "/Volumes/External SSD/Projects/Research/GenAI_Effectiveness/Final/OSF"

# GitHub 원격 저장소 연결 (YOUR_USERNAME을 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/YOUR_USERNAME/GenAI-HE-MetaAnalysis.git

# 메인 브랜치 이름 설정 및 푸시
git branch -M main
git push -u origin main
```

---

### 2단계: OSF 프로젝트 생성

1. [ ] **OSF 로그인** → https://osf.io
2. [ ] **새 프로젝트 생성**
   - "Create new project" 클릭
   - Title: `Effectiveness of Generative AI on Learning Outcomes in Higher Education: A Three-Level Meta-Analysis`
   - Storage location: `United States` 또는 선호하는 지역
3. [ ] **프로젝트 설명 추가**
   - Description에 Abstract 내용 붙여넣기
4. [ ] **라이선스 설정**
   - Settings → License → `CC BY 4.0`
5. [ ] **태그 추가**
   - `meta-analysis`, `generative AI`, `higher education`, `learning outcomes`, `ChatGPT`, `three-level model`

---

### 3단계: GitHub-OSF 연동

1. [ ] **OSF 프로젝트에서 Add-ons 클릭**
2. [ ] **GitHub 선택 → Enable**
3. [ ] **GitHub 계정 연결** (처음이면 인증 필요)
4. [ ] **저장소 선택**: `GenAI-HE-MetaAnalysis`
5. [ ] **Import 클릭**
   - GitHub 파일들이 OSF에 자동으로 동기화됨

---

### 4단계: Pre-registration (선택사항)

**이미 분석을 완료했으므로 Post-registration으로 등록:**

1. [ ] **Registrations 탭 클릭**
2. [ ] **New registration**
3. [ ] **템플릿 선택**: `Open-Ended Registration` 또는 `AsPredicted`
4. [ ] **필수 정보 입력**:
   - 연구 질문
   - 가설
   - 분석 계획
   - 변경 사항 (있을 경우)

---

### 5단계: DOI 발급 및 인용 준비

1. [ ] **OSF에서 DOI 생성**
   - Settings → Identifiers → Create DOI
2. [ ] **인용 형식 확인**
   - Citations 탭에서 APA, BibTeX 등 확인
3. [ ] **원고에 OSF DOI 추가**
   - Data Availability Statement에 OSF 링크 포함

---

### 6단계: 최종 확인 체크리스트

**데이터 및 코드:**
- [ ] 데이터 파일 열기 가능 확인 (CSV 인코딩)
- [ ] R 스크립트 실행 가능 확인
- [ ] 변수명이 codebook과 일치하는지 확인

**문서:**
- [ ] README.md가 모든 파일 설명하는지 확인
- [ ] 원고 파일 정상 열림 확인
- [ ] Figure 파일들 해상도 적절한지 확인

**메타데이터:**
- [ ] 저자 정보 정확한지 확인
- [ ] 라이선스 올바르게 설정되었는지 확인
- [ ] 키워드/태그 적절한지 확인

---

## 파일 구조 요약

```
OSF/
├── README.md                    ← 프로젝트 설명 (OSF 메인 페이지에 표시)
├── LICENSE                      ← CC BY 4.0 라이선스
├── .gitignore                   ← Git 무시 파일
├── TODO_OSF_SUBMISSION.md       ← 이 파일 (제출 후 삭제 가능)
│
├── data/
│   ├── raw/                     ← 원본 데이터
│   └── processed/               ← 분석용 정제 데이터
│
├── analysis/
│   └── three_level_meta_analysis.R  ← R 분석 코드
│
├── manuscript/
│   ├── GenAI_HE_MetaAnalysis_Manuscript_REVISED.docx
│   ├── figures/                 ← Forest plot, Funnel plot, PRISMA
│   └── tables/                  ← Table 3 (연구 특성)
│
└── supplementary/
    ├── prisma/                  ← PRISMA 2020 다이어그램
    ├── codebook/                ← 코딩북 (변수 설명)
    └── protocol/                ← 추출 프로토콜
```

---

## 문의

GitHub 또는 OSF 연동에 문제가 있으면 Claude Code에 다시 질문하세요!
