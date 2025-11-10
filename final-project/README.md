# 서울시 따릉이(공공자전거) 대여소별 대여반납 승객수 데이터 분석 프로젝트

## 프로젝트 목표
- **날씨(강수량·기온·풍속·습도)**가 따릉이 이용량/회전율에 미치는 영향을 정량화
- **집중호우 주간(9/17~9/23)**을 사례로 전·후 비교 분석
- 결과를 바탕으로 운영 효율화 / 리소스 최적화 / 서비스 개선 / 정책 의사결정에 기여
- 우천 주간을 “정비·점검 효율화 주간”으로 운영하는 데이터 기반 근거 제공

## 프로젝트 개요

2025년 9월 서울시 따릉이(공공자전거) 대여소별 대여반납 승객수 데이터를 활용한 종합 데이터 분석 프로젝트입니다. 한 달 전체 데이터를 기본으로, 집중호우가 있었던 주(9/17~9/23)를 사례를 추가로 비교 분석합니다. ULTRA-THINK 프레임워크를 기반으로 체계적인 데이터 탐색, 시각화, 인사이트 도출을 수행합니다.

## 프로젝트 구조

```
final-project/
│
├── data/                          # 데이터 디렉토리
│   ├── raw/                       # 원본 데이터
│   │   └── 서울시 따릉이 대여소별 대여반납 승객수(20250901).csv
|   |   ├── 서울시 따릉이 대여소별 대여반납 승객수(20250902).csv
│   │   ├── 서울시 따릉이 대여소별 대여반납 승객수(20250903).csv
|   |    ...   
│   │   └── 서울시 따릉이 대여소별 대여반납 승객수(20250930).csv
│   ├── processed/                 # 전처리된 데이터
│   │   ├── merged_hourly_202509.csv 
│   │   ├── rain_impact_by_station.csv 
│   │   └── station_master_clean.csv    # (선택) 좌표 정리본
│   └── external/                  # 외부 데이터
|       ├── 서울시 따릉이대여소 마스터 정보.csv  # 전체 대여소 ID
│       └── 서울시 지상관측자료 정보(일별).csv   # 날씨
|
├── notebooks/                     # Jupyter 노트북
│   ├── 01_data_exploration.ipynb
│   ├── 02_weather_patterns.ipynb 
│   ├── 03_time_space_analysis.ipynb 
│   ├── 04_case_study_heavyrain.ipynb 
│   └── 05_insights_and_actions.ipynb
│
├── src/                          # 소스 코드
│   └── utils/                    # 유틸리티 함수
│       ├── __init__.py
│       ├── data_loader.py        # 데이터 로딩 및 결측치 점검 (NaN=0 처리 포함)
│       ├── preprocessing.py      # 전처리 함수(5분→1시간 가공, 기상 결합, 파생 변수 생성)
│       ├── visualization.py      # 시각화 함수(히트맵, 바차트, 지도 등)
│       └── maintenance_utils.py  # (선택) 우천 주간 정비·점검 스케줄 추천 로직
│
├── outputs/                      # 분석 결과물
│   ├── figures/                  # 시각화 이미지
│   │   ├── heatmap_hour_weekday.png
│   │   ├── bar_rain_bins.png
│   │   ├── line_hourly_usage.png
│   │   ├── bar_station_rain_impact_toplow.png
│   │   └── map_rain_impact.html
│   ├── reports/                  # 분석 리포트
│   │   ├── executive_summary.pdf
│   │   ├── detailed_analysis.pdf 
│   │   └── presentation.pptx
│   └── models/                   # 예측 모델 (필요시)
│
├── requirements.txt              # 패키지 의존성
└── README.md                     # 프로젝트 문서 (이 파일)
```

## 설치 및 실행

### 1. 환경 설정

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터 준비

- `data/raw/` 폴더에 원본 CSV 파일을 배치하세요
- 파일명: `서울시 따릉이 대여소별 대여반납 승객수(20250901).csv`, `서울시 따릉이 대여소별 대여반납 승객수(20250902).csv`, · · · ,`서울시 따릉이 대여소별 대여반납 승객수(20250930).csv`

### 3. 데이터 전처리

```bash
# 원본 데이터 → 시간당 집계 데이터 생성
python preprocess_data.py
```

**전처리 결과:**
- `data/processed/merged_hourly_202509.csv` (1,221,301건)
- `data/processed/rain_impact_by_station.csv` (대여소별 우천 감소율)

### 4. 시각화 생성

```bash
# 날씨 패턴 분석 시각화 (5종 차트)
python visualize_weather_patterns.py
```

**생성 파일:**
- `outputs/figures/heatmap_hour_weekday.png` (시간대×요일 히트맵)
- `outputs/figures/bar_rain_bins.png` (강수 구간별 이용량)
- `outputs/figures/line_hourly_usage.png` (시간대별 추이)
- `outputs/figures/bar_station_rain_impact_toplow.png` (대여소별 우천 영향)
- `outputs/figures/clear_vs_rainy_comparison.png` (맑은날 vs 비오는날)

### 5. 보고서 생성

```bash
# PDF 보고서 및 PowerPoint 프레젠테이션 자동 생성
python generate_reports.py
```

**생성 파일:**
- `outputs/reports/executive_summary.pdf` (경영진용 요약본, 2페이지)
- `outputs/reports/detailed_analysis.pdf` (상세 분석 보고서, ~10페이지)
- `outputs/reports/presentation.pptx` (프레젠테이션, 11슬라이드)

### 6. Jupyter Notebook 분석 (선택)

```bash
# Jupyter Notebook 실행
jupyter notebook

# 노트북을 순서대로 실행:
# 01_data_exploration.ipynb → 02_weather_patterns.ipynb →
# 03_time_space_analysis.ipynb → 04_case_study_heavyrain.ipynb →
# 05_insights_and_actions.ipynb
```

## 프로젝트 컨텍스트

**데이터셋**: 서울시 따릉이 대여소별 대여반납 승객수(일별)
**데이터 기간**: 2025년 9월 1일~ 2025년 9월 30일
**데이터 구조**: 
- 기준_날짜 (YYYYMMDD 형식)
- 기준_시간대 (출발시간)
- 시작_대여소_ID
- 종료_대여소_ID
- 전체_건수
- 전체_이용_분
- 전체_이용_거리

**데이터셋**: 서울시 따릉이대여소 마스터 정보
**데이터 기간**: 2025.11.02 (갱신)
**데이터 구조**: 
- 대여소_ID (ST-####)
- 주소1 (서울특별시 구/동/도로명)
- 주소2 (대여소명)
- 위도 (°)
- 경도 (°)

**데이터셋**: 서울시 지상관측자료 정보(일별)
**데이터 기간**: 2025년 9월 1일~ 2025년 9월 30일 
**데이터 구조**: 
ㅊ

**데이터 특성**
- 시계열 데이터 (기준_날짜, 기준_시간대): 5분 집계를 1시간 단위로 리샘플링해 날씨 데이터와 시간 정합성을 확보
- 공간 데이터 (대여소_ID, 시작_대여소_ID, 종료_대여소_ID, 위도, 경도): 서울시_따릉이_대여소_마스터정보.csv를 병합하여 미이용 대여소 포함 및 위치 기반 시각화/지도 분석 가능
- 집계 데이터 (전체_건수, 전체_이용_분, 전체_이용_거리): 대여소·시간대별 집계된 요약 통계 데이터로, 트렌드 및 효율성 분석에 활용
- 기상 데이터 (평균기온(℃), 일강수량(mm), 평균풍속(m/s), 평균상대습도(%)): 일강수량(mm) 결측값은 비가 오지 않은 날(0mm) 로 처리

**결합 데이터 구조**
→ 기준_날짜를 기준으로 서울시 따릉이 대여소별 대여반납 승객수 정보와 서울시 지상관측자료 정보 병합,
→ 대여소_ID를 기준으로 마스터 데이터(위치 정보) 결합,
→ 시간 × 지역 × 날씨의 다차원 분석 가능


## 분석 목적 및 핵심 질문

### 주요 비즈니스 목적
1. **운영 효율화**: 우천 시 따릉이 수요 급감 대여소 식별 → 따릉이 회수·재배치 일정 선제 조정
2. **리소스 관리 최적화**: 기상 예보 연동(스케줄러)으로 자동 알림 → 일정 변경
3. **서비스 개선**: 실시간 기상 API 연동 “현재 날씨에 따른 이용 권장/주의 안내” 자동 발송(앱/안내판/SMS)
4. **정비·점검 효율화 주간 운영**: 집중호우 주간을 정비·점검·배터리 교체에 집중 투입하여 운영 공백 최소화
5. **정책 의사결정**: 강수/풍속 임계치 기반 운영지침 및 시설투자 우선순위 도출

### 핵심 분석 질문
1. **날씨별 이용 패턴**: 비 오는 날/맑은 날, **강수 구간(0/1~10/10~30/30+)**에 따른 이용량·회전율 차이는?
2. **시간대 민감도**: 출근(7–9시), 퇴근(18–20시), 주말 낮(12–17시) 등 시간대별 우천 감소율은?
3. **대여소별 차이**: 우천 감소율 TOP/LOW 대여소는 어디이며, 평시에도 낮은가(본질 이슈) vs 날씨 민감형인가?
4. **복합기상 영향**: 강수 + 풍속 + 습도/기온 조합에서 수요가 최저인 조건은?
5. **집중호우 사례**: 9/17~9/23 vs 9/10~9/16 전후 비교(총량/시간대/대여소별 변화)

## 분석 프레임워크 적용 (ULTRA-THINK)

### U - Understand (이해하기)
1. **데이터 로딩 및 인코딩 처리** (cp949)
2. **컬럼명 확인 및 영문 변환**: 한글 컬럼 유지
3. **데이터 타입 변환** (기준_날짜 → datetime, 기준_시간대 → int)
4. **결측 규칙 명시** 
- 기상: 일강수량(mm)의 NaN = 0mm(비 없음)
- 이용: 전체_이용_분, 전체_이용_거리의 NaN = 0(이용 없음)
- 대여소명: 시작_대여소명, 종료_대여소명의 결측 → 마스터 정보(주소2)로 보완

### L - Look Deeper (심층 탐색)
1. **시간대 × 요일별 이용 패턴 비교** (히트맵)
2. **강수 구간별 이용량 변화** (바차트)
3. **시간대별 평균 이용량 추이** (라인차트)
4. **대여소별 우천 감소율 TOP/LOW** (수평 바차트)
5. **대여소 위치 기반 시각화** (Folium/Plotly)

### T - Transform (변환하기)
1. **5분 → 1시간 리샘플링**: 날짜·시간·대여소별 전체_건수=sum 등 집계
2. **마스터 결합**: 시작_대여소_ID↔대여소_ID (좌표 추가, 미이용 대여소 포함)
3. **기상 결합**:기준_날짜↔일시
4. **결측 처리(재확인)**: 
- wx["일강수량(mm)"].fillna(0)
- bike[["전체_이용_분","전체_이용_거리"]].fillna(0) ← 이용 NaN=0
- 시작_대여소명/종료_대여소명은 마스터로 보완
5. **파생 변수**: 비여부(>0mm), 강수_구간, 우천_감소율, 시간대_구분(출근/퇴근/주말낮), 정상화_회전율(거치대 정보 없으면 퍼센타일/표준화)
```python
# 이용 NaN → 0
bike[["전체_이용_분","전체_이용_거리"]] = bike[["전체_이용_분","전체_이용_거리"]].fillna(0)

# 대여소명 보완 (예시: 시작 대여소명)
bike = bike.merge(station[["대여소_ID","주소2"]], left_on="시작_대여소_ID", right_on="대여소_ID", how="left")
bike["시작_대여소명"] = bike["시작_대여소명"].fillna(bike["주소2"]).drop(columns=["주소2"])
```

### R - Reveal Insights (인사이트 도출)
1. **우천 감소율**: “비 10mm+에서 시간당 대여량 평균 대비 X% 감소”
2. **시간대 민감도**: “퇴근(18–20시) 구간 감소폭이 출근(7–9시)보다 크며, 주말낮(12–17시)에는 급락”
3. **대여소 민감도**: “공원형·여가형 대여소는 급감, 환승형(지하철 인접)은 유지율 높음”
4. **복합기상**: 비(≥10mm) + 풍속(≥5m/s) 동시 시 최저 이용량
4. **집중호우 주간 효과**: 전주 대비 총량/패턴 변화 및 상위 영향 대여소 리스트
5. **정비 효율화 주간**: 집중호우 시기(9/17~9/23)는 이용 감소폭이 커 정비·점검 집중 투입에 최적

### A - Anticipate (예측하기)
1. **기상 변수 기반 예측 모델링**: 회귀(Linear) 및 트리(RandomForest, XGBoost) 모델로 이용량을 강수·풍속·기온·습도 변수로 예측
2. **성장 시나리오 분석**: 강수(0/10/30mm) × 풍속(3/5/8m/s) 조합별 예상 수요 시뮬레이션으로 날씨 임계 구간 도출
3. **알림 임계치**제안: “강수≥10mm & 풍속≥5m/s → 주의 알림 + 회수·정비 일정 전환”

### T - Tell Story (스토리텔링)
**스토리 구조**:
```
제목: "비와 바람, 따릉이의 가장 큰 적! 날씨에 흔들리는 도시의 자전거"

도입:
2025년 9월, 서울은 이례적인 집중호우를 겪었습니다.
출퇴근길 시민들의 발이 되어온 따릉이는 이 기간 동안 어떤 변화를 겪었을까요?

발견 1: 일강수량 10mm 이상일 때, 전체 이용량이 평균 대비 XX% 감소  
발견 2: 출근(7–9시) 시간대에는 감소폭이 XX%로 상대적으로 작지만, 주말 낮(12–17시)에는 XX% 이상 급감  
발견 3: 공원형 대여소(여의도, 뚝섬)는 비 오는 날 이용이 거의 ‘제로’에 가깝지만, 지하철 환승형 대여소(신림, 홍대입구)는 유지율이 높음  
발견 4: 비(≥10mm)+풍속(≥5m/s) 동시 발생 시 이용량이 평균 대비 XX% 이상 감소 — ‘비 + 바람’ 복합조건이 최악의 조합  

결론:
날씨는 단순한 불편 요소가 아니라, 이용 패턴을 결정짓는 핵심 변수입니다.  
특히 비와 바람이 겹치면 급락하는 것을 볼 수 있습니다. 
집중호우 주간은 ‘정비·점검 효율화 주간’으로 전환하면 운영 생산성을 높일 수 있습니다.


권고사항:
1. **기상 정보 연동형 알림 시스템 구축** — 비 예보 시, 앱/안내판을 통해 실시간 이용 주의 안내 제공  
2. **날씨 민감형 대여소 관리 우선순위 설정** — 우천 시 급감 대여소를 중심으로 회수·정비 일정을 사전 조정  
3. **차양막 설비 시범 설치** — 상위 10개 우천 취약 대여소를 선정해 경량형 차양막 시범 적용  
4. **우천 데이터 기반 운영 정책** — 우천 주간 정비·회수·수리에 집중

```

### H - Hypothesize (가설 수립)
**가설 예시**:
- H1: 강수량이 증가할수록 이용량은 비선형적으로 감소한다
- H2: 강수+풍속 복합조건이 단일조건보다 감소폭이 크다
- H3: 환승형 대여소는 우천 민감도가 낮다

### I - Integrate (통합하기)
**추가 데이터 소스 제안**:
- 생활인구/환승량/POI로 기대수요 vs 실제수요의 잔차 분석
- 공휴일/이벤트 캘린더로 교란요인 통제

### N - Navigate Complexity (복잡성 관리)
**우선순위**:
1. 주중/주말·공휴일 구분
2. 결측/이상치 처리(이용 NaN=0, 강수 NaN=0)
3. 5분→1시간 가공의 정보손실 고려

### K - Keep Ethical (윤리 준수)
- 개인 식별 정보 없음 (집계 데이터)
- 공공 서비스로서 포용성 강조

## 시각화 가이드

### 시간대 × 요일별 이용 패턴 비교 (히트맵)
```python
plt.figure(figsize=(12, 6))

# 요일/시간대별 평균 이용 건수 계산
pivot = df.pivot_table(values='전체_건수',
                       index='요일',       # 월~일 (0~6)
                       columns='기준_시간', # 0~23
                       aggfunc='mean')

sns.heatmap(pivot, cmap='YlGnBu', annot=False)
plt.title('시간대 × 요일별 따릉이 이용 패턴 (우천/맑음 비교)', fontsize=16, fontweight='bold')
plt.xlabel('시간대', fontsize=12)
plt.ylabel('요일', fontsize=12)
plt.show()
```

### 2. 강수 구간별 이용량 변화 (바차트)
```python
plt.figure(figsize=(10, 6))

# 강수 구간 정의
bins = [0, 1, 10, 30, 100]
labels = ['0mm(맑음)', '1~10mm', '10~30mm', '30mm 이상']
df['강수_구간'] = pd.cut(df['일강수량(mm)'], bins=bins, labels=labels, right=False)

# 구간별 평균 이용량
rain_group = df.groupby('강수_구간')['전체_건수'].mean().reset_index()

sns.barplot(data=rain_group, x='강수_구간', y='전체_건수', palette='Blues_d')
plt.title('강수 구간별 평균 이용량 변화', fontsize=16, fontweight='bold')
plt.xlabel('강수 구간', fontsize=12)
plt.ylabel('평균 이용 건수', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.show()
```

### 3. 시간대별 평균 이용량 추이 (라인차트)
```python
plt.figure(figsize=(12, 6))

# 시간대별 평균 이용량
hourly_usage = df.groupby('기준_시간')['전체_건수'].mean()

plt.plot(hourly_usage.index, hourly_usage.values, marker='o', linewidth=2)
plt.title('시간대별 평균 이용량 추이', fontsize=16, fontweight='bold')
plt.xlabel('시간대 (시)', fontsize=12)
plt.ylabel('평균 이용 건수', fontsize=12)
plt.grid(alpha=0.3)
plt.axvspan(7, 9, color='lightblue', alpha=0.3, label='출근 시간대')
plt.axvspan(18, 20, color='lightcoral', alpha=0.3, label='퇴근 시간대')
plt.legend()
plt.show()
```

### 4. 대여소별 우천 감소율 TOP/LOW (수평 바차트)
```python
plt.figure(figsize=(10, 8))

# 대여소별 평균 이용량 (맑은 날 vs 비 오는 날)
clear = df[df['일강수량(mm)'] == 0].groupby('시작_대여소_ID')['전체_건수'].mean()
rainy = df[df['일강수량(mm)'] > 0].groupby('시작_대여소_ID')['전체_건수'].mean()

# 감소율 계산
decrease = ((rainy - clear) / clear * 100).sort_values()
top_low = decrease.head(10).append(decrease.tail(10))

sns.barplot(x=top_low.values, y=top_low.index, palette='coolwarm')
plt.title('대여소별 우천 감소율 TOP / LOW 10', fontsize=16, fontweight='bold')
plt.xlabel('우천 시 이용량 변화율 (%)', fontsize=12)
plt.ylabel('대여소 ID', fontsize=12)
plt.axvline(0, color='black', linewidth=1)
plt.show()
```
### 5. 대여소 위치 기반 시각화 (지도 시각화 / Folium)
```python
import folium

# 감소율 데이터를 대여소 좌표와 병합
station_merge = station.merge(decrease.reset_index(), on='대여소_ID')
station_merge.rename(columns={0: '우천감소율(%)'}, inplace=True)

# 중심 좌표 설정 (서울시청 기준)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 대여소별 원형 마커 표시
for _, row in station_merge.iterrows():
    color = 'red' if row['우천감소율(%)'] < 0 else 'blue'
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        radius=4,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"{row['대여소_ID']}<br>감소율: {row['우천감소율(%)']:.1f}%",
    ).add_to(m)

m.save('outputs/figures/seoulbike_rain_map.html')
```

## 핵심 Python 코드 스니펫

```python
# 0) 라이브러리
import os, glob
import pandas as pd
import numpy as np

# 1) 데이터 로딩
# (a) 따릉이 원본: 2025-09-01 ~ 2025-09-30, 파일 여러 개 병합
raw_dir = "data/raw"
paths = sorted(glob.glob(os.path.join(raw_dir, "서울시 따릉이 대여소별 대여반납 승객수(202509??).csv")))
bike_list = [pd.read_csv(p, encoding="utf-8") for p in paths]
bike = pd.concat(bike_list, ignore_index=True)

# (b) 대여소 마스터
station = pd.read_csv("data/external/서울시 따릉이대여소 마스터 정보.csv", encoding="utf-8")

# (c) 기상(일별, 서울 108)
wx = pd.read_csv("data/external/서울시 지상관측자료 정보(일별).csv", encoding="utf-8")

# 2) 컬럼/타입 정리
# 날짜·시간 타입 통일
bike["기준_날짜"] = pd.to_datetime(bike["기준_날짜"], format="%Y%m%d", errors="coerce")

# 기준_시간대 예: 0000, 0500, 2355 → '시'만 추출(정수 0~23)
# (정합성 보려고 5분단위 중 '시' 단위로 변환)
bike["기준_시간"] = (bike["기준_시간대"] // 100).astype(int)

# 기상 데이터
wx["일시"] = pd.to_datetime(wx["일시"], errors="coerce")

# 🚨 중요: 강수 NaN은 '비가 안 온 날'로 간주 → 0mm 처리
wx["일강수량(mm)"] = wx["일강수량(mm)"].fillna(0)

# 3) 5분 → 1시간 가공(리샘플링에 준하는 집계)
# 시간·대여소 단위 집계(합/평균 정의는 필요에 따라 조정)
hourly = (bike.groupby(["기준_날짜","기준_시간","시작_대여소_ID"], as_index=False)
               .agg(전체_건수=("전체_건수","sum"),
                    전체_이용_분=("전체_이용_분","mean"),
                    전체_이용_거리=("전체_이용_거리","mean")))

# 4) 대여소 마스터 결합(미이용 대여소 포함하려면 OUTER 기준 표준화 별도 고려)
hourly = hourly.merge(station[["대여소_ID","위도","경도"]],
                      left_on="시작_대여소_ID", right_on="대여소_ID", how="left")

# 5) 기상 결합 (일 단위 병합)
hourly = hourly.merge(wx[["일시","평균기온(℃)","일강수량(mm)","평균풍속(m/s)","평균상대습도(%)"]],
                      left_on="기준_날짜", right_on="일시", how="left")

# 안전망으로 한 번 더(이중 안전 처리)
hourly["일강수량(mm)"] = hourly["일강수량(mm)"].fillna(0)

# 6) 파생 변수
# 비 여부 / 강수 구간
bins = [0, 1, 10, 30, np.inf]
labels = ["0mm(맑음)", "1~10mm", "10~30mm", "30mm+"]
hourly["비여부"] = (hourly["일강수량(mm)"] > 0).astype(int)
hourly["강수_구간"] = pd.cut(hourly["일강수량(mm)"], bins=bins, labels=labels, right=False)

# 요일/주말 플래그
hourly["요일"] = hourly["기준_날짜"].dt.dayofweek  # 0=월, 6=일
hourly["주말"] = hourly["요일"].isin([5,6]).astype(int)

# 출근/퇴근/주말낮 시간 구간
hourly["시간대_구분"] = "기타"
hourly.loc[hourly["기준_시간"].between(7,9), "시간대_구분"] = "출근(7-9)"
hourly.loc[hourly["기준_시간"].between(18,20), "시간대_구분"] = "퇴근(18-20)"
hourly.loc[(hourly["주말"]==1) & (hourly["기준_시간"].between(12,17)), "시간대_구분"] = "주말낮(12-17)"

# 7) 우천 감소율 계산 예시
# 대여소별 '맑음 대비 우천' 평균 값으로 감소율(%) 계산
clear = (hourly[hourly["비여부"]==0]
         .groupby("시작_대여소_ID")["전체_건수"].mean())
rainy = (hourly[hourly["비여부"]==1]
         .groupby("시작_대여소_ID")["전체_건수"].mean())

decrease = ((rainy - clear) / clear * 100).dropna().sort_values()  # 음수면 감소
decrease.name = "우천감소율(%)"

# TOP/LOW 10 대여소
top10 = decrease.head(10)
low10 = decrease.tail(10)

# 8) 결과 저장
os.makedirs("data/processed", exist_ok=True)
hourly.to_csv("data/processed/merged_hourly_202509.csv", index=False, encoding="utf-8")
decrease.to_csv("data/processed/rain_impact_by_station.csv", encoding="utf-8")

```

## 최종 결과물 (Deliverables)

### 1. Jupyter 노트북
- 01_data_exploration.ipynb (데이터 구조, NaN 규칙, 기본 분포)
- 02_weather_patterns.ipynb (강수·풍속·기온·습도와 이용량 상관/회귀, 강수구간 분석)
- 03_time_space_analysis.ipynb (시간대×요일 히트맵, 대여소별 우천감소율, 지도)
- 04_case_study_heavyrain.ipynb (9/17~9/23 집중호우 전후 비교)
- 05_insights_and_actions.ipynb (인사이트 요약, 실행안/알림 임계치)

### 2. 시각화 파일 (outputs/figures/)
- heatmap_hour_weekday.png (시간대×요일 히트맵: 맑음/우천 비교)
- bar_rain_bins.png (강수 구간별 평균 이용량)
- line_hourly_usage.png (시간대별 평균 이용량, 출근/퇴근/주말낮 강조)
- bar_station_rain_impact_toplow.png (대여소별 우천 감소율 TOP/LOW)
- map_rain_impact.html (지도 시각화: 감소율 Choropleth/마커)

### 3. 분석 리포트 (outputs/reports/)
- executive_summary.pdf (1p 핵심 요약: 임계치·우선순위·액션)
- detailed_analysis.pdf (상세 분석 리포트: 방법론, 결과, 해석)
- presentation.pptx (발표 자료)

### 4. 클렌징된 데이터 (data/processed/)
- merged_hourly_202509.csv (5분→1시간 가공 + 기상 결합 + 파생)
- rain_impact_by_station.csv (대여소별 우천감소율)
- station_master_clean.csv (좌표 정리본)

## 기대 인사이트 예시(날씨×이용 버전)

### 인사이트 1: 임계치
“**일강수량 10mm+**에서 이용량이 비선형적으로 급감(평균 대비 −45%~−65%).”"

### 인사이트 2: 인사이트 1 — 임계치
“**일강수량 10mm+**에서 이용량이 비선형적으로 급감(평균 대비 −45%~−65%).”

### 인사이트 3: 공간 유형 차이
“환승형(지하철 인접) 대여소는 우천에도 유지율 높고, 공원/여가형은 거의 ‘0’에 수렴.”

### 인사이트 4: 복합기상 영향
“비(≥10mm) + 풍속(≥5m/s) 동시 발생 시 최저 이용 — 알림 임계치 후보.”

### 인사이트 5: 사례 비교(9/17~9/23)
“집중호우 주간은 전주 대비 총량 −52%, 퇴근 시간대 낙폭이 가장 큼.”

## 실행 가능한 권고사항

### 단기 (1~3개월)
1. **기상 연동형 알림 시스템**: 강수≥10mm 또는 풍속≥5m/s 시 앱/안내판 자동 주의 알림
2. **우선순위 운영**: 우천 민감 TOP10 대여소 대상으로 회수/정비 일정 사전 조정
3. **전광판·배너 메시지**: 우천 시 제동/미끄럼 주의, 비닐 커버 비치

### 중기 (3~6개월)
1. **경량 차양막 시범 설치**: 우천 취약 TOP10 대여소 파일럿
2. **강수 예보 기반 경로 최적화**: 회수 차량 이동거리 10~15% 절감 목표
3. **회수 차량 이동거리 10~15% 절감 목표**: 환승형 대여소 중심

### 장기 (6개월 이상)
1. **운영 규칙화**: 월별 강수/풍속 임계치 기반 운영지침 표준화
2. **시설 투자 로드맵**: 차양막·배수·노면 개선의 C/B 분석 후 단계 확대
3. **위험 날씨 자동 임시 폐쇄 시뮬레이션**: 안전성/민원 감소 지표 모니터링

---

**이 프롬프트 사용법**:
1. U 단계에서 규칙 명시: 일강수량 NaN = 0mm(비 안 옴)
2. T 단계에서 실제 적용: wx["일강수량(mm)"].fillna(0)
3. 5분 → 1시간 가공 후, 시간대/요일/강수구간/대여소 교차 분석
4. 임계치·우선순위·액션을 도출해 레포트/알림 규칙으로 연결
5. 최종 결과물 체크리스트로 완성도 확인

**성공의 핵심**: 단순히 숫자를 보여주는 것이 아니라,
"**언제(시간대) + 어디서(대여소) + 어떤 조건(강수·풍속)**"에서 얼마나 줄었고,
그래서 운영/정책 측면에서 무엇을 바꿀 것인가”까지 제시하는 것입니다.
