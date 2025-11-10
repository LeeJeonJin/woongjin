"""
서울시 따릉이 데이터 전처리 스크립트
- 5분 단위  1시간 단위 리샘플링
- 기상 데이터 병합
- 대여소 마스터 정보 병합
- 파생 변수 생성
"""

import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("서울시 따릉이 데이터 전처리 시작")
print("=" * 80)

# ============================================================================
# 1. 따릉이 원본 데이터 로딩
# ============================================================================
print("\n[1/8] 따릉이 원본 데이터 로딩 중...")

raw_dir = "data/raw"
# 모든 CSV 파일 찾기 (202509로 시작하는 파일만)
all_files = glob.glob(os.path.join(raw_dir, "*.csv"))
paths = sorted([f for f in all_files if "202509" in f])

if not paths:
    raise FileNotFoundError(f"'{raw_dir}' 디렉토리에서 202509 파일을 찾을 수 없습니다.")

print(f">> {len(paths)}개의 파일을 로딩합니다...")

bike_list = []
for p in paths:
    try:
        # UTF-8 시도, 실패 시 CP949(EUC-KR) 사용
        try:
            df = pd.read_csv(p, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(p, encoding="cp949")
        bike_list.append(df)
        print(f"  [OK] {os.path.basename(p)} - {len(df):,}개 레코드")
    except Exception as e:
        print(f"  [ERROR] {os.path.basename(p)} 로딩 실패: {e}")

bike = pd.concat(bike_list, ignore_index=True)
print(f"[완료] 총 {len(bike):,}개 레코드 로딩 완료")

# ============================================================================
# 2. 컬럼 및 타입 변환
# ============================================================================
print("\n[2/8] 컬럼 및 타입 변환 중...")

# 기준_날짜  datetime
bike["기준_날짜"] = pd.to_datetime(bike["기준_날짜"], format="%Y%m%d", errors="coerce")
print(f"   기준_날짜  datetime 변환")

# 기준_시간대  정수 (시 단위만 추출)
bike["기준_시간"] = (bike["기준_시간대"] // 100).astype(int)
print(f"   기준_시간대  기준_시간 (정수) 추출")

# 이용 데이터 NaN = 0 처리
if "전체_이용_분" in bike.columns:
    bike["전체_이용_분"] = bike["전체_이용_분"].fillna(0)
    print(f"   전체_이용_분 NaN  0 처리")

if "전체_이용_거리" in bike.columns:
    bike["전체_이용_거리"] = bike["전체_이용_거리"].fillna(0)
    print(f"   전체_이용_거리 NaN  0 처리")

print(f" 컬럼 변환 완료")
print(f"   - 기간: {bike['기준_날짜'].min()} ~ {bike['기준_날짜'].max()}")
print(f"   - 고유 대여소 수: {bike['시작_대여소_ID'].nunique():,}개")

# ============================================================================
# 3. 외부 데이터 로딩 (마스터 + 기상)
# ============================================================================
print("\n[3/8] 외부 데이터 로딩 중...")

# 대여소 마스터
station_path = "data/external/서울시 따릉이대여소 마스터 정보.csv"
if not os.path.exists(station_path):
    raise FileNotFoundError(f"'{station_path}' 파일을 찾을 수 없습니다.")

try:
    station = pd.read_csv(station_path, encoding="utf-8")
except UnicodeDecodeError:
    station = pd.read_csv(station_path, encoding="cp949")
print(f"   대여소 마스터 로딩 완료: {len(station):,}개 대여소")

# 기상 데이터
weather_path = "data/external/지상관측자료 정보(일별).csv"
if not os.path.exists(weather_path):
    raise FileNotFoundError(f"'{weather_path}' 파일을 찾을 수 없습니다.")

try:
    weather = pd.read_csv(weather_path, encoding="utf-8")
except UnicodeDecodeError:
    weather = pd.read_csv(weather_path, encoding="cp949")
print(f"   기상 데이터 로딩 완료: {len(weather)}일")

# 기상 데이터 전처리
weather["일시"] = pd.to_datetime(weather["일시"], errors="coerce")
print(f"   일시  datetime 변환")

#  중요: 강수 NaN = 비가 안 온 날  0mm 처리
if "일강수량(mm)" in weather.columns:
    before_fillna = weather["일강수량(mm)"].isna().sum()
    weather["일강수량(mm)"] = weather["일강수량(mm)"].fillna(0)
    print(f"    일강수량 결측값 {before_fillna}개를 0mm로 처리했습니다.")
else:
    print(f"    '일강수량(mm)' 컬럼을 찾을 수 없습니다.")

print(f" 외부 데이터 로딩 완료")

# ============================================================================
# 4. 5분  1시간 단위 리샘플링
# ============================================================================
print("\n[4/8] 5분  1시간 단위 리샘플링 중...")

hourly = (bike.groupby(["기준_날짜", "기준_시간", "시작_대여소_ID"], as_index=False)
          .agg(
              전체_건수=("전체_건수", "sum"),
              전체_이용_분=("전체_이용_분", "mean"),
              전체_이용_거리=("전체_이용_거리", "mean")
          ))

print(f" 리샘플링 완료: {len(bike):,}개  {len(hourly):,}개 레코드")
print(f"   - 압축률: {(1 - len(hourly)/len(bike))*100:.1f}%")

# ============================================================================
# 5. 데이터 병합 (기상 + 마스터)
# ============================================================================
print("\n[5/8] 데이터 병합 중...")

# 기상 데이터 병합 (일 단위)
print("    기상 데이터 병합 중...")

# 기상 데이터 컬럼 확인 및 선택
weather_cols = ["일시"]
if "평균기온(°C)" in weather.columns:
    weather_cols.append("평균기온(°C)")
elif "평균기온()" in weather.columns:
    weather_cols.append("평균기온()")

weather_cols.append("일강수량(mm)")

if "평균 풍속(m/s)" in weather.columns:
    weather_cols.append("평균 풍속(m/s)")
elif "평균풍속(m/s)" in weather.columns:
    weather_cols.append("평균풍속(m/s)")

if "평균 상대습도(%)" in weather.columns:
    weather_cols.append("평균 상대습도(%)")
elif "평균상대습도(%)" in weather.columns:
    weather_cols.append("평균상대습도(%)")

hourly = hourly.merge(
    weather[weather_cols],
    left_on="기준_날짜",
    right_on="일시",
    how="left"
)
print(f"   기상 데이터 병합 완료")

# 안전망: 강수량 결측값 재처리
hourly["일강수량(mm)"] = hourly["일강수량(mm)"].fillna(0)

# 대여소 마스터 병합 (위치 정보)
print("   대여소 마스터 정보 병합 중...")
hourly = hourly.merge(
    station[["대여소_ID", "주소1", "주소2", "위도", "경도"]],
    left_on="시작_대여소_ID",
    right_on="대여소_ID",
    how="left"
)
print(f"   대여소 마스터 병합 완료")

# 대여소명 보완 (주소2로)
if "시작_대여소명" not in hourly.columns:
    hourly["시작_대여소명"] = hourly["주소2"]
else:
    hourly["시작_대여소명"] = hourly["시작_대여소명"].fillna(hourly["주소2"])

print(f" 데이터 병합 완료: {len(hourly):,}개 레코드")

# ============================================================================
# 6. 파생 변수 생성
# ============================================================================
print("\n[6/8] 파생 변수 생성 중...")

# 1. 비 여부
hourly["비여부"] = (hourly["일강수량(mm)"] > 0).astype(int)
print(f"   비여부 생성 (>0mm)")

# 2. 강수 구간
bins = [0, 1, 10, 30, np.inf]
labels = ["0mm(맑음)", "1~10mm", "10~30mm", "30mm+"]
hourly["강수_구간"] = pd.cut(hourly["일강수량(mm)"], bins=bins, labels=labels, right=False)
print(f"   강수_구간 생성 (0 / 1~10 / 10~30 / 30mm+)")

# 3. 요일 및 주말
hourly["요일"] = hourly["기준_날짜"].dt.dayofweek  # 0=월, 6=일
hourly["주말"] = hourly["요일"].isin([5, 6]).astype(int)
print(f"   요일, 주말 생성")

# 4. 시간대 구분
hourly["시간대_구분"] = "기타"
hourly.loc[hourly["기준_시간"].between(7, 9), "시간대_구분"] = "출근(7-9)"
hourly.loc[hourly["기준_시간"].between(18, 20), "시간대_구분"] = "퇴근(18-20)"
hourly.loc[(hourly["주말"] == 1) & (hourly["기준_시간"].between(12, 17)), "시간대_구분"] = "주말낮(12-17)"
print(f"   시간대_구분 생성 (출근/퇴근/주말낮)")

# 5. 날짜 관련
hourly["일"] = hourly["기준_날짜"].dt.day
hourly["주차"] = hourly["기준_날짜"].dt.isocalendar().week
print(f"   일, 주차 생성")

print(f" 파생 변수 생성 완료")

# ============================================================================
# 7. 결측치 최종 검증
# ============================================================================
print("\n[7/8] 결측치 최종 검증 중...")

missing = hourly.isnull().sum()
missing_pct = (missing / len(hourly)) * 100

missing_df = pd.DataFrame({
    '결측 수': missing,
    '결측 비율(%)': missing_pct
})

missing_df = missing_df[missing_df['결측 수'] > 0].sort_values('결측 수', ascending=False)

if len(missing_df) > 0:
    print("  결측값이 남아있습니다:")
    print(missing_df.head(10))
else:
    print(" 결측값이 없습니다.")

# ============================================================================
# 8. 결과 저장
# ============================================================================
print("\n[8/8] 결과 저장 중...")

os.makedirs("data/processed", exist_ok=True)

# 1. 전처리된 데이터 저장
output_path = "data/processed/merged_hourly_202509.csv"
hourly.to_csv(output_path, index=False, encoding="utf-8")
print(f"   {output_path} 저장 완료 ({len(hourly):,}개 레코드)")

# 2. 우천 감소율 계산 및 저장 (선택)
print("\n   우천 감소율 계산 중...")
clear = (hourly[hourly["비여부"] == 0]
         .groupby("시작_대여소_ID")["전체_건수"]
         .mean())

rainy = (hourly[hourly["비여부"] == 1]
         .groupby("시작_대여소_ID")["전체_건수"]
         .mean())

decrease = ((rainy - clear) / clear * 100).dropna().sort_values()
decrease.name = "우천감소율(%)"

rain_impact_path = "data/processed/rain_impact_by_station.csv"
decrease.to_csv(rain_impact_path, encoding="utf-8")
print(f"   {rain_impact_path} 저장 완료 ({len(decrease)}개 대여소)")

# ============================================================================
# 최종 요약
# ============================================================================
print("\n" + "=" * 80)
print(" 전처리 완료!")
print("=" * 80)
print(f"\n 전처리 결과 요약:")
print(f"   - 전체 레코드: {len(hourly):,}개")
print(f"   - 기간: {hourly['기준_날짜'].min()} ~ {hourly['기준_날짜'].max()}")
print(f"   - 고유 대여소: {hourly['시작_대여소_ID'].nunique():,}개")
print(f"   - 총 이용 건수: {hourly['전체_건수'].sum():,.0f}건")
print(f"   - 비 오는 날: {hourly[hourly['비여부']==1]['기준_날짜'].nunique()}일")
print(f"   - 맑은 날: {hourly[hourly['비여부']==0]['기준_날짜'].nunique()}일")

print(f"\n 출력 파일:")
print(f"   1. {output_path}")
print(f"   2. {rain_impact_path}")

print(f"\n 주요 컬럼:")
print(f"   - 시간: 기준_날짜, 기준_시간")
print(f"   - 대여소: 시작_대여소_ID, 시작_대여소명, 위도, 경도")
print(f"   - 이용: 전체_건수, 전체_이용_분, 전체_이용_거리")
print(f"   - 기상: 일강수량(mm) 및 기상 관측 데이터")
print(f"   - 파생: 비여부, 강수_구간, 요일, 주말, 시간대_구분")

print("\n 다음 단계:")
print("   - notebooks/02_weather_patterns.ipynb 실행")
print("   - 시각화 및 인사이트 도출")

print("\n" + "=" * 80)
