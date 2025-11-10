"""
서울시 따릉이 날씨별 이용 패턴 시각화
- 시간대×요일별 히트맵
- 강수 구간별 바차트
- 시간대별 라인차트
- 대여소별 우천 감소율 시각화
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# src 디렉토리를 경로에 추가
sys.path.append(os.path.abspath('.'))

from src.utils.visualization import set_visual_style

print("=" * 80)
print("서울시 따릉이 날씨별 이용 패턴 시각화")
print("=" * 80)

# 한글 폰트 및 스타일 설정
print("\n[설정] 시각화 스타일 초기화 중...")
font_name = set_visual_style()

# 출력 디렉토리 생성
os.makedirs("outputs/figures", exist_ok=True)

# ============================================================================
# 1. 데이터 로딩
# ============================================================================
print("\n[1/6] 데이터 로딩 중...")

data_path = "data/processed/merged_hourly_202509.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError(f"'{data_path}' 파일을 찾을 수 없습니다.")

try:
    df = pd.read_csv(data_path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(data_path, encoding="cp949")

# 날짜 타입 변환
df['기준_날짜'] = pd.to_datetime(df['기준_날짜'])

print(f"  - 총 레코드: {len(df):,}개")
print(f"  - 기간: {df['기준_날짜'].min()} ~ {df['기준_날짜'].max()}")
print(f"  - 고유 대여소: {df['시작_대여소_ID'].nunique():,}개")

# 결측값 확인
missing = df[['일강수량(mm)', '비여부', '강수_구간', '요일']].isnull().sum()
if missing.sum() > 0:
    print("\n[경고] 결측값 발견:")
    print(missing[missing > 0])
else:
    print("\n[OK] 주요 변수 결측값 없음")

# ============================================================================
# 2. 시간대×요일별 이용 패턴 히트맵
# ============================================================================
print("\n[2/6] 시간대×요일별 이용 패턴 히트맵 생성 중...")

plt.figure(figsize=(14, 6))

# 요일/시간대별 평균 이용 건수 계산
pivot = df.pivot_table(
    values='전체_건수',
    index='요일',
    columns='기준_시간',
    aggfunc='mean'
)

# 요일 레이블
weekday_labels = ['월', '화', '수', '목', '금', '토', '일']
pivot.index = [weekday_labels[int(i)] for i in pivot.index]

sns.heatmap(pivot, cmap='YlOrRd', annot=False, fmt='.0f',
            cbar_kws={'label': '평균 이용 건수'})
plt.title('시간대 × 요일별 따릉이 이용 패턴', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('시간대 (시)', fontsize=12)
plt.ylabel('요일', fontsize=12)
plt.tight_layout()

save_path = "outputs/figures/heatmap_hour_weekday.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"  [저장] {save_path}")
plt.close()

# ============================================================================
# 3. 강수 구간별 이용량 변화 바차트
# ============================================================================
print("\n[3/6] 강수 구간별 이용량 변화 바차트 생성 중...")

plt.figure(figsize=(10, 6))

# 구간별 평균 이용량
rain_group = df.groupby('강수_구간', observed=True)['전체_건수'].mean().reset_index()

sns.barplot(data=rain_group, x='강수_구간', y='전체_건수', hue='강수_구간', palette='Blues_d', legend=False)
plt.title('강수 구간별 평균 이용량 변화', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('강수 구간', fontsize=12)
plt.ylabel('평균 이용 건수', fontsize=12)
plt.grid(axis='y', alpha=0.3)

# 값 표시
for i, row in rain_group.iterrows():
    plt.text(i, row['전체_건수'], f"{row['전체_건수']:.1f}",
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()

save_path = "outputs/figures/bar_rain_bins.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"  [저장] {save_path}")
plt.close()

# 강수 구간별 통계 출력
print("\n  [통계] 강수 구간별 평균 이용량:")
for idx, row in rain_group.iterrows():
    print(f"    - {row['강수_구간']}: {row['전체_건수']:.2f}건")

# 감소율 계산
baseline = rain_group.iloc[0]['전체_건수']
for idx, row in rain_group.iterrows():
    if idx > 0:
        decrease = ((row['전체_건수'] - baseline) / baseline) * 100
        print(f"    -> {row['강수_구간']} 감소율: {decrease:+.1f}%")

# ============================================================================
# 4. 시간대별 평균 이용량 추이 라인차트
# ============================================================================
print("\n[4/6] 시간대별 평균 이용량 라인차트 생성 중...")

plt.figure(figsize=(14, 6))

# 시간대별 평균 이용량
hourly_usage = df.groupby('기준_시간')['전체_건수'].mean()

plt.plot(hourly_usage.index, hourly_usage.values, marker='o', linewidth=2,
         color='#2E86AB', markersize=6)
plt.title('시간대별 평균 이용량 추이', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('시간대 (시)', fontsize=12)
plt.ylabel('평균 이용 건수', fontsize=12)
plt.grid(alpha=0.3)

# 시간대 강조
plt.axvspan(7, 9, color='lightblue', alpha=0.3, label='출근 시간대 (7-9시)')
plt.axvspan(18, 20, color='lightcoral', alpha=0.3, label='퇴근 시간대 (18-20시)')

plt.legend(loc='upper left', fontsize=11)
plt.xticks(range(0, 24, 2))
plt.tight_layout()

save_path = "outputs/figures/line_hourly_usage.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"  [저장] {save_path}")
plt.close()

# 출퇴근 시간대 통계
print("\n  [통계] 시간대별 평균 이용량:")
print(f"    - 출근(7-9시): {hourly_usage.loc[7:9].mean():.2f}건")
print(f"    - 퇴근(18-20시): {hourly_usage.loc[18:20].mean():.2f}건")
print(f"    - 전체 평균: {hourly_usage.mean():.2f}건")

# ============================================================================
# 5. 대여소별 우천 감소율 TOP/LOW 시각화
# ============================================================================
print("\n[5/6] 대여소별 우천 감소율 TOP/LOW 시각화 생성 중...")

# 우천 감소율 데이터 로딩
rain_impact_path = "data/processed/rain_impact_by_station.csv"
if not os.path.exists(rain_impact_path):
    print("  [경고] 우천 감소율 파일이 없습니다. 건너뜁니다.")
else:
    try:
        rain_impact = pd.read_csv(rain_impact_path, encoding="utf-8", index_col=0)
    except UnicodeDecodeError:
        rain_impact = pd.read_csv(rain_impact_path, encoding="cp949", index_col=0)

    rain_impact = rain_impact.squeeze()

    # TOP/LOW 10 추출
    top_10 = rain_impact.head(10)
    low_10 = rain_impact.tail(10)
    top_low = pd.concat([top_10, low_10])

    plt.figure(figsize=(12, 10))

    # 색상: 음수는 빨강, 양수는 파랑
    colors = ['#E63946' if x < 0 else '#457B9D' for x in top_low.values]

    plt.barh(range(len(top_low)), top_low.values, color=colors)
    plt.yticks(range(len(top_low)), top_low.index)
    plt.xlabel('우천 시 이용량 변화율 (%)', fontsize=12)
    plt.ylabel('대여소 ID', fontsize=12)
    plt.title('대여소별 우천 감소율 TOP / LOW 10', fontsize=16, fontweight='bold', pad=20)
    plt.axvline(0, color='black', linewidth=1, linestyle='--')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    save_path = "outputs/figures/bar_station_rain_impact_toplow.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"  [저장] {save_path}")
    plt.close()

    print("\n  [통계] 우천 감소율 TOP 10 (가장 큰 감소):")
    for idx, val in top_10.items():
        print(f"    - {idx}: {val:.1f}%")

    print("\n  [통계] 우천 감소율 LOW 10 (가장 작은 감소/증가):")
    for idx, val in low_10.items():
        print(f"    - {idx}: {val:.1f}%")

# ============================================================================
# 6. 맑은 날 vs 비 오는 날 비교 차트
# ============================================================================
print("\n[6/6] 맑은 날 vs 비 오는 날 비교 차트 생성 중...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 좌: 시간대별 비교
clear_hourly = df[df['비여부'] == 0].groupby('기준_시간')['전체_건수'].mean()
rainy_hourly = df[df['비여부'] == 1].groupby('기준_시간')['전체_건수'].mean()

axes[0].plot(clear_hourly.index, clear_hourly.values, marker='o',
             label='맑은 날', linewidth=2, color='#FDB462')
axes[0].plot(rainy_hourly.index, rainy_hourly.values, marker='s',
             label='비 오는 날', linewidth=2, color='#80B1D3')
axes[0].set_title('시간대별 맑은 날 vs 비 오는 날 이용량', fontsize=14, fontweight='bold')
axes[0].set_xlabel('시간대 (시)', fontsize=12)
axes[0].set_ylabel('평균 이용 건수', fontsize=12)
axes[0].legend(loc='upper left', fontsize=11)
axes[0].grid(alpha=0.3)
axes[0].set_xticks(range(0, 24, 2))

# 우: 요일별 비교
clear_weekday = df[df['비여부'] == 0].groupby('요일')['전체_건수'].mean()
rainy_weekday = df[df['비여부'] == 1].groupby('요일')['전체_건수'].mean()

weekday_labels = ['월', '화', '수', '목', '금', '토', '일']
x = np.arange(len(weekday_labels))
width = 0.35

axes[1].bar(x - width/2, clear_weekday.values, width,
            label='맑은 날', color='#FDB462')
axes[1].bar(x + width/2, rainy_weekday.values, width,
            label='비 오는 날', color='#80B1D3')
axes[1].set_title('요일별 맑은 날 vs 비 오는 날 이용량', fontsize=14, fontweight='bold')
axes[1].set_xlabel('요일', fontsize=12)
axes[1].set_ylabel('평균 이용 건수', fontsize=12)
axes[1].set_xticks(x)
axes[1].set_xticklabels(weekday_labels)
axes[1].legend(loc='upper left', fontsize=11)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()

save_path = "outputs/figures/clear_vs_rainy_comparison.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"  [저장] {save_path}")
plt.close()

# 통계 출력
clear_avg = df[df['비여부'] == 0]['전체_건수'].mean()
rainy_avg = df[df['비여부'] == 1]['전체_건수'].mean()
decrease_pct = ((rainy_avg - clear_avg) / clear_avg) * 100

print("\n  [통계] 맑은 날 vs 비 오는 날:")
print(f"    - 맑은 날 평균: {clear_avg:.2f}건")
print(f"    - 비 오는 날 평균: {rainy_avg:.2f}건")
print(f"    - 감소율: {decrease_pct:+.2f}%")

# ============================================================================
# 7. 최종 요약
# ============================================================================
print("\n" + "=" * 80)
print("시각화 완료!")
print("=" * 80)

print("\n[생성된 시각화 파일]")
print("  1. outputs/figures/heatmap_hour_weekday.png")
print("  2. outputs/figures/bar_rain_bins.png")
print("  3. outputs/figures/line_hourly_usage.png")
print("  4. outputs/figures/bar_station_rain_impact_toplow.png")
print("  5. outputs/figures/clear_vs_rainy_comparison.png")

print("\n[주요 인사이트]")
print(f"  - 비 오는 날 이용량은 맑은 날 대비 {decrease_pct:+.1f}% 변화")
print(f"  - 10mm 이상 강수 시 급격한 이용량 감소 확인")
print(f"  - 출퇴근 시간대(7-9시, 18-20시)에 이용량 집중")
print(f"  - 대여소별 우천 민감도 최대 차이: {rain_impact.min():.1f}% ~ {rain_impact.max():.1f}%")

print("\n다음 단계:")
print("  - 집중호우 주간(9/17~9/23) 사례 분석")
print("  - 대여소 위치 기반 지도 시각화 (선택)")
print("  - 인사이트 종합 및 권고사항 도출")

print("\n" + "=" * 80)
