"""
데이터 전처리 및 파생 변수 생성 유틸리티
"""

import pandas as pd
import numpy as np


def resample_to_hourly(bike_df):
    """
    5분 단위 데이터를 1시간 단위로 리샘플링합니다.

    Parameters:
    -----------
    bike_df : pd.DataFrame
        원본 따릉이 데이터

    Returns:
    --------
    pd.DataFrame
        시간 단위로 집계된 데이터
    """
    print("⏰ 5분 → 1시간 단위 리샘플링 중...")

    hourly = (bike_df.groupby(["기준_날짜", "기준_시간", "시작_대여소_ID"], as_index=False)
              .agg(
                  전체_건수=("전체_건수", "sum"),
                  전체_이용_분=("전체_이용_분", "mean"),
                  전체_이용_거리=("전체_이용_거리", "mean")
              ))

    print(f"✅ 리샘플링 완료: {len(hourly):,}개 레코드")

    return hourly


def merge_weather_data(bike_df, weather_df):
    """
    따릉이 데이터에 기상 데이터를 병합합니다.

    Parameters:
    -----------
    bike_df : pd.DataFrame
        따릉이 데이터
    weather_df : pd.DataFrame
        기상 데이터

    Returns:
    --------
    pd.DataFrame
        병합된 데이터
    """
    print("🌦️  기상 데이터 병합 중...")

    # 기상 데이터 병합 (일 단위)
    merged = bike_df.merge(
        weather_df[["일시", "평균기온(℃)", "일강수량(mm)", "평균풍속(m/s)", "평균상대습도(%)"]],
        left_on="기준_날짜",
        right_on="일시",
        how="left"
    )

    # 안전망: 강수량 결측값 재처리
    merged["일강수량(mm)"] = merged["일강수량(mm)"].fillna(0)

    print(f"✅ 병합 완료: {len(merged):,}개 레코드")

    return merged


def merge_station_master(bike_df, station_df):
    """
    따릉이 데이터에 대여소 마스터 정보(좌표)를 병합합니다.

    Parameters:
    -----------
    bike_df : pd.DataFrame
        따릉이 데이터
    station_df : pd.DataFrame
        대여소 마스터 데이터

    Returns:
    --------
    pd.DataFrame
        병합된 데이터
    """
    print("📍 대여소 마스터 정보 병합 중...")

    merged = bike_df.merge(
        station_df[["대여소_ID", "주소1", "주소2", "위도", "경도"]],
        left_on="시작_대여소_ID",
        right_on="대여소_ID",
        how="left"
    )

    # 대여소명 보완
    if "시작_대여소명" not in merged.columns:
        merged["시작_대여소명"] = merged["주소2"]
    else:
        merged["시작_대여소명"] = merged["시작_대여소명"].fillna(merged["주소2"])

    print(f"✅ 병합 완료: {len(merged):,}개 레코드")

    return merged


def create_derived_features(df):
    """
    파생 변수를 생성합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        원본 데이터프레임

    Returns:
    --------
    pd.DataFrame
        파생 변수가 추가된 데이터프레임
    """
    print("🔧 파생 변수 생성 중...")

    df = df.copy()

    # 1. 비 여부
    df["비여부"] = (df["일강수량(mm)"] > 0).astype(int)

    # 2. 강수 구간
    bins = [0, 1, 10, 30, np.inf]
    labels = ["0mm(맑음)", "1~10mm", "10~30mm", "30mm+"]
    df["강수_구간"] = pd.cut(df["일강수량(mm)"], bins=bins, labels=labels, right=False)

    # 3. 요일 및 주말
    df["요일"] = df["기준_날짜"].dt.dayofweek  # 0=월, 6=일
    df["주말"] = df["요일"].isin([5, 6]).astype(int)

    # 4. 시간대 구분
    df["시간대_구분"] = "기타"
    df.loc[df["기준_시간"].between(7, 9), "시간대_구분"] = "출근(7-9)"
    df.loc[df["기준_시간"].between(18, 20), "시간대_구분"] = "퇴근(18-20)"
    df.loc[(df["주말"] == 1) & (df["기준_시간"].between(12, 17)), "시간대_구분"] = "주말낮(12-17)"

    # 5. 날짜 관련
    df["일"] = df["기준_날짜"].dt.day
    df["주차"] = df["기준_날짜"].dt.isocalendar().week

    print("✅ 파생 변수 생성 완료:")
    print("   - 비여부, 강수_구간")
    print("   - 요일, 주말")
    print("   - 시간대_구분 (출근/퇴근/주말낮)")
    print("   - 일, 주차")

    return df


def calculate_rain_impact(df):
    """
    대여소별 우천 감소율을 계산합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        전처리된 데이터프레임

    Returns:
    --------
    pd.Series
        대여소별 우천 감소율 (%)
    """
    print("📉 대여소별 우천 감소율 계산 중...")

    # 맑은 날 평균 이용량
    clear = (df[df["비여부"] == 0]
             .groupby("시작_대여소_ID")["전체_건수"]
             .mean())

    # 비 오는 날 평균 이용량
    rainy = (df[df["비여부"] == 1]
             .groupby("시작_대여소_ID")["전체_건수"]
             .mean())

    # 감소율 계산 (음수면 감소)
    decrease = ((rainy - clear) / clear * 100).dropna().sort_values()
    decrease.name = "우천감소율(%)"

    print(f"✅ 우천 감소율 계산 완료: {len(decrease)}개 대여소")
    print(f"   - 최대 감소: {decrease.min():.1f}%")
    print(f"   - 최소 감소: {decrease.max():.1f}%")

    return decrease


def filter_heavy_rain_period(df, start_date="2025-09-17", end_date="2025-09-23"):
    """
    집중호우 기간 데이터를 필터링합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        전체 데이터프레임
    start_date : str
        시작 날짜
    end_date : str
        종료 날짜

    Returns:
    --------
    pd.DataFrame
        필터링된 데이터프레임
    """
    mask = (df["기준_날짜"] >= start_date) & (df["기준_날짜"] <= end_date)
    filtered = df[mask].copy()

    print(f"🌧️  집중호우 기간 ({start_date} ~ {end_date}) 필터링:")
    print(f"   - {len(filtered):,}개 레코드")

    return filtered
