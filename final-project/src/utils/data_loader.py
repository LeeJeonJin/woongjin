"""
데이터 로딩 및 결측치 처리 유틸리티
"""

import os
import glob
import pandas as pd
import numpy as np


def load_bike_data(data_dir="data/raw", pattern="서울시 따릉이 대여소별 대여반납 승객수(202509??).csv"):
    """
    따릉이 원본 데이터를 로딩하고 병합합니다.

    Parameters:
    -----------
    data_dir : str
        원본 데이터 디렉토리 경로
    pattern : str
        파일 패턴

    Returns:
    --------
    pd.DataFrame
        병합된 따릉이 데이터
    """
    paths = sorted(glob.glob(os.path.join(data_dir, pattern)))

    if not paths:
        raise FileNotFoundError(f"'{data_dir}' 디렉토리에서 패턴 '{pattern}'과 일치하는 파일을 찾을 수 없습니다.")

    print(f"📂 {len(paths)}개의 파일을 로딩합니다...")

    bike_list = []
    for p in paths:
        try:
            df = pd.read_csv(p, encoding="utf-8")
            bike_list.append(df)
            print(f"  ✓ {os.path.basename(p)}")
        except Exception as e:
            print(f"  ✗ {os.path.basename(p)} 로딩 실패: {e}")

    bike = pd.concat(bike_list, ignore_index=True)

    # 기본 전처리
    bike["기준_날짜"] = pd.to_datetime(bike["기준_날짜"], format="%Y%m%d", errors="coerce")
    bike["기준_시간"] = (bike["기준_시간대"] // 100).astype(int)

    # 이용 데이터 NaN = 0 처리
    if "전체_이용_분" in bike.columns:
        bike["전체_이용_분"] = bike["전체_이용_분"].fillna(0)
    if "전체_이용_거리" in bike.columns:
        bike["전체_이용_거리"] = bike["전체_이용_거리"].fillna(0)

    print(f"✅ 총 {len(bike):,}개 레코드 로딩 완료")
    print(f"📅 기간: {bike['기준_날짜'].min()} ~ {bike['기준_날짜'].max()}")

    return bike


def load_station_master(file_path="data/external/서울시 따릉이대여소 마스터 정보.csv"):
    """
    대여소 마스터 정보를 로딩합니다.

    Parameters:
    -----------
    file_path : str
        마스터 파일 경로

    Returns:
    --------
    pd.DataFrame
        대여소 마스터 데이터
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"'{file_path}' 파일을 찾을 수 없습니다.")

    station = pd.read_csv(file_path, encoding="utf-8")

    print(f"🚲 대여소 마스터 로딩 완료: {len(station):,}개 대여소")

    return station


def load_weather_data(file_path="data/external/서울시 지상관측자료 정보(일별).csv"):
    """
    기상 데이터를 로딩하고 결측치를 처리합니다.

    Parameters:
    -----------
    file_path : str
        기상 데이터 파일 경로

    Returns:
    --------
    pd.DataFrame
        기상 데이터
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"'{file_path}' 파일을 찾을 수 없습니다.")

    wx = pd.read_csv(file_path, encoding="utf-8")

    # 날짜 변환
    wx["일시"] = pd.to_datetime(wx["일시"], errors="coerce")

    # 🚨 중요: 강수 NaN = 비가 안 온 날 → 0mm 처리
    if "일강수량(mm)" in wx.columns:
        wx["일강수량(mm)"] = wx["일강수량(mm)"].fillna(0)
        print(f"⚠️  일강수량 결측값을 0mm로 처리했습니다.")

    print(f"🌦️  기상 데이터 로딩 완료: {len(wx)}일")
    print(f"📅 기간: {wx['일시'].min()} ~ {wx['일시'].max()}")

    return wx


def check_missing_values(df, name="DataFrame"):
    """
    결측값을 확인하고 리포트합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        확인할 데이터프레임
    name : str
        데이터프레임 이름
    """
    print(f"\n📊 [{name}] 결측값 확인")
    print("=" * 50)

    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100

    missing_df = pd.DataFrame({
        '결측 수': missing,
        '결측 비율(%)': missing_pct
    })

    missing_df = missing_df[missing_df['결측 수'] > 0].sort_values('결측 수', ascending=False)

    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("✅ 결측값이 없습니다.")

    print("=" * 50)
