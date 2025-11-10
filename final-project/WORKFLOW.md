# 서울시 따릉이 날씨 영향 분석 - 전체 워크플로우

본 문서는 프로젝트의 전체 실행 흐름을 단계별로 설명합니다.

## 📋 전체 워크플로우

```
1. 데이터 준비
   ↓
2. 전처리 (preprocess_data.py)
   ↓
3. 시각화 생성 (visualize_weather_patterns.py)
   ↓
4. 보고서 자동 생성 (generate_reports.py)
   ↓
5. 분석 완료!
```

---

## 1️⃣ 데이터 준비

### 필수 파일 배치

**위치:** `data/raw/`

```
data/raw/
├── 서울시 따릉이 대여소별 대여반납 승객수(20250901).csv
├── 서울시 따릉이 대여소별 대여반납 승객수(20250902).csv
├── ...
└── 서울시 따릉이 대여소별 대여반납 승객수(20250930).csv  (30개 파일)
```

**위치:** `data/external/`

```
data/external/
├── 서울시 따릉이대여소 마스터 정보.csv
└── 서울시 지상관측자료 정보(일별).csv
```

### 환경 설정

```bash
# 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

---

## 2️⃣ 데이터 전처리

### 실행 명령

```bash
python preprocess_data.py
```

### 처리 과정

1. **원본 데이터 로딩** (30개 CSV, ~7.4M 레코드)
2. **시간 리샘플링** (5분 → 1시간 집계)
3. **날씨 데이터 병합** (강수량, 기온, 풍속, 습도)
4. **대여소 정보 병합** (위도, 경도, 주소)
5. **파생 변수 생성** (비여부, 강수구간, 요일, 시간대)
6. **우천 영향 분석** (대여소별 감소율 계산)

### 출력 파일

| 파일 | 설명 | 크기 |
|------|------|------|
| `data/processed/merged_hourly_202509.csv` | 1시간 단위 집계 데이터 | 1,221,301건 |
| `data/processed/rain_impact_by_station.csv` | 대여소별 우천 감소율 | 2,761개소 |

### 실행 시간

약 **2-3분** (시스템 성능에 따라 다름)

---

## 3️⃣ 시각화 생성

### 실행 명령

```bash
python visualize_weather_patterns.py
```

### 생성 차트

| 번호 | 파일명 | 설명 | 인사이트 |
|------|--------|------|----------|
| 1 | `heatmap_hour_weekday.png` | 시간대×요일 히트맵 | 평일 출퇴근 시간대 집중 |
| 2 | `bar_rain_bins.png` | 강수 구간별 이용량 | **10mm 임계치 발견** (-28.4%) |
| 3 | `line_hourly_usage.png` | 시간대별 추이 | 퇴근(18시) > 출근(7시) |
| 4 | `bar_station_rain_impact_toplow.png` | 대여소별 우천 영향 | 공원형 -40%, 환승형 유지 |
| 5 | `clear_vs_rainy_comparison.png` | 맑은날 vs 비오는날 | 전체 -21.95% 감소 |

### 출력 위치

`outputs/figures/` (총 5개 PNG 파일, ~800KB)

### 실행 시간

약 **30초**

### 주요 기능

- ✅ **크로스 플랫폼 한글 폰트 자동 감지** (Windows/Mac/Linux)
- ✅ **고해상도 출력** (DPI=300)
- ✅ **통일된 디자인** (색상, 폰트, 레이아웃)

---

## 4️⃣ 보고서 자동 생성

### 실행 명령

```bash
python generate_reports.py
```

### 생성 보고서

#### 📄 1. 경영진용 요약 보고서 (`executive_summary.pdf`)

- **페이지 수:** 2페이지
- **구성:**
  - 프로젝트 개요
  - 핵심 발견사항 (5가지)
  - 주요 인사이트 (4가지)
  - 정책 제언 (단기/중기/장기)
  - 결론
- **대상:** 경영진, 의사결정권자
- **파일 크기:** ~70KB

#### 📄 2. 상세 분석 보고서 (`detailed_analysis.pdf`)

- **페이지 수:** 8-10페이지
- **구성:**
  - 프로젝트 개요
  - 데이터 및 전처리
  - 분석 결과 (시각화 5종 포함)
  - 종합 인사이트
  - 정책 제언 (상세)
  - 결론
- **대상:** 분석가, 운영팀
- **파일 크기:** ~1.3MB

#### 📊 3. PowerPoint 프레젠테이션 (`presentation.pptx`)

- **슬라이드 수:** 11장
- **구성:**
  1. 표지
  2. 프로젝트 개요
  3. 핵심 발견사항
  4-8. 시각화 5종 (각 1슬라이드)
  9. 종합 인사이트
  10. 정책 제언
  11. 결론
- **대상:** 발표, 회의
- **파일 크기:** ~630KB

### 출력 위치

`outputs/reports/` (총 3개 파일, ~2MB)

### 실행 시간

약 **10-15초**

### 주요 기능

- ✅ **한글 폰트 자동 설정** (PDF: Malgun Gothic)
- ✅ **고품질 시각화 임베드** (이미지 자동 삽입)
- ✅ **전문적 디자인** (색상, 레이아웃, 타이포그래피)

---

## 5️⃣ 결과 확인

### 생성 파일 트리

```
outputs/
├── figures/                          (시각화 이미지)
│   ├── heatmap_hour_weekday.png      87 KB
│   ├── bar_rain_bins.png             76 KB
│   ├── line_hourly_usage.png         189 KB
│   ├── bar_station_rain_impact_toplow.png  181 KB
│   └── clear_vs_rainy_comparison.png 222 KB
│
└── reports/                          (보고서)
    ├── executive_summary.pdf         70 KB
    ├── detailed_analysis.pdf         1.3 MB
    └── presentation.pptx              632 KB
```

### 빠른 확인

```bash
# 파일 목록 확인
ls -lh outputs/figures/
ls -lh outputs/reports/

# PDF 열기 (Windows)
start outputs/reports/executive_summary.pdf

# PowerPoint 열기 (Windows)
start outputs/reports/presentation.pptx
```

---

## 📊 핵심 인사이트 요약

### 1. 비 오는 날 이용량 **-21.95%** 감소
- 맑은 날: 6.99건/시간
- 비오는 날: 5.45건/시간

### 2. 일강수량 **10mm 임계치** 발견
- 10mm 미만: 정상 운영
- 10mm 이상: -28.4% 급감 → **회수 우선**

### 3. 퇴근 시간대(18-20시) 민감도 ↑
- 출근(7-9시) 평균 8.04건
- 퇴근(18-20시) 평균 9.38건 (+16.7%)

### 4. 대여소 유형별 차이
- 공원형 (한강공원 등): **-40% 이상 급감**
- 환승형 (지하철역): **상대적 유지**

### 5. 집중호우 주간 효율화
- 9/17-9/23: 정비·점검 **적기**

---

## 🚀 정책 제언

### 단기 (1-3개월)
- ✅ 강수≥10mm 자동 알림 시스템
- ✅ 퇴근 시간대 환승역 충전 강화
- ✅ 공원형 대여소 우천 회수 프로토콜

### 중기 (3-6개월)
- ✅ 우천 취약 대여소 차양막 시범 설치 (Top 50)
- ✅ 날씨 기반 운영지침 표준화 (SOP)
- ✅ 수요 예측 모델 고도화 (ML)

### 장기 (6개월+)
- ✅ 인프라 투자 로드맵 (800개소 차양막)
- ✅ 대여소 재배치 전략 (환승형 확대)
- ✅ 데이터 기반 의사결정 체계 구축

---

## 🛠️ 트러블슈팅

### Q1. 한글이 깨져서 나와요!

**A:** 시스템에 한글 폰트가 설치되어 있는지 확인하세요.

- **Windows:** Malgun Gothic (C:/Windows/Fonts/malgun.ttf)
- **Mac:** AppleGothic
- **Linux:** NanumGothic

폰트가 없으면 자동으로 기본 폰트를 사용하지만, 일부 한글이 깨질 수 있습니다.

### Q2. 파일을 찾을 수 없다는 오류가 나요!

**A:** 데이터 파일이 올바른 위치에 있는지 확인하세요.

```bash
# 필수 파일 확인
ls data/raw/
ls data/external/
```

### Q3. 메모리 부족 오류가 나요!

**A:** 대용량 데이터 처리 시 메모리가 부족할 수 있습니다. 청크 단위로 읽어들이도록 코드를 수정하거나, 더 많은 메모리를 가진 시스템에서 실행하세요.

### Q4. 시각화가 생성되지 않아요!

**A:** matplotlib 백엔드 문제일 수 있습니다. 환경 변수를 설정하거나 다른 백엔드를 사용해보세요.

```bash
export MPLBACKEND=Agg  # Linux/Mac
set MPLBACKEND=Agg     # Windows
```

---

## 📝 참고 문서

- [README.md](README.md) - 프로젝트 전체 개요
- [requirements.txt](requirements.txt) - 패키지 의존성
- [weather_patterns_insights.md](outputs/reports/weather_patterns_insights.md) - 인사이트 상세 문서

---

## 📧 문의

프로젝트 관련 문의사항은 이슈를 등록해주세요.

**프로젝트 완료일:** 2025-11-09
