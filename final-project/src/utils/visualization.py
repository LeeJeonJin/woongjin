"""
시각화 유틸리티 함수
- 크로스 플랫폼 한글 폰트 처리
- 통일된 디자인 적용
- 재사용 가능한 차트 함수들
"""

import os
import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import folium
from matplotlib import font_manager, rc


def set_visual_style():
    """
    통합 시각화 스타일 설정
    - 크로스 플랫폼 한글 폰트 자동 감지
    - 마이너스 폰트 깨짐 방지
    - 공통 DPI, 스타일 적용
    """
    system = platform.system()
    font_name = None

    # OS별 한글 폰트 우선순위
    if system == "Windows":
        font_candidates = ["Malgun Gothic", "맑은 고딕", "gulim", "굴림"]
        font_paths = [
            "C:/Windows/Fonts/malgun.ttf",
            "C:/Windows/Fonts/malgunbd.ttf",
            "C:/Windows/Fonts/gulim.ttc"
        ]
    elif system == "Darwin":  # macOS
        font_candidates = ["AppleGothic", "Apple SD Gothic Neo"]
        font_paths = [
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
            "/Library/Fonts/AppleGothic.ttf"
        ]
    else:  # Linux
        font_candidates = ["NanumGothic", "NanumBarunGothic", "DejaVu Sans"]
        font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"
        ]

    # 1단계: 시스템 폰트 목록에서 검색
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for candidate in font_candidates:
        if candidate in available_fonts:
            font_name = candidate
            print(f"[폰트] {font_name} 설정 완료 (시스템 폰트)")
            break

    # 2단계: 직접 경로로 폰트 로딩
    if font_name is None:
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font_prop = fm.FontProperties(fname=path)
                    font_name = font_prop.get_name()
                    fm.fontManager.addfont(path)
                    print(f"[폰트] {font_name} 설정 완료 (경로: {path})")
                    break
                except Exception as e:
                    print(f"[경고] {path} 폰트 로딩 실패: {e}")
                    continue

    # 3단계: 폰트 적용
    if font_name:
        plt.rcParams['font.family'] = font_name
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 폰트 깨짐 방지
        # matplotlib 폰트 캐시 갱신
        fm._load_fontmanager(try_read_cache=False)
    else:
        print("[경고] 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        plt.rcParams['axes.unicode_minus'] = False

    # 공통 스타일 설정
    sns.set_style("whitegrid")
    plt.rcParams['figure.dpi'] = 100  # 화면 출력용
    plt.rcParams['savefig.dpi'] = 300  # 저장용 고해상도

    # seaborn이 폰트를 무시하지 않도록 강제 설정
    sns.set(font=font_name if font_name else "sans-serif", rc={"axes.unicode_minus": False})

    return font_name


def plot_heatmap_hour_weekday(df, save_path="outputs/figures/heatmap_hour_weekday.png"):
    """
    시간대 × 요일별 이용 패턴 히트맵을 생성합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        전처리된 데이터프레임
    save_path : str
        저장 경로
    """
    print("📊 시간대 × 요일 히트맵 생성 중...")

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
    pivot.index = [weekday_labels[i] for i in pivot.index]

    sns.heatmap(pivot, cmap='YlOrRd', annot=False, fmt='.0f', cbar_kws={'label': '평균 이용 건수'})
    plt.title('시간대 × 요일별 따릉이 이용 패턴', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('시간대 (시)', fontsize=12)
    plt.ylabel('요일', fontsize=12)
    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ 저장 완료: {save_path}")
    plt.close()


def plot_rain_bins(df, save_path="outputs/figures/bar_rain_bins.png"):
    """
    강수 구간별 이용량 변화 막대 차트를 생성합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        전처리된 데이터프레임
    save_path : str
        저장 경로
    """
    print("📊 강수 구간별 이용량 차트 생성 중...")

    plt.figure(figsize=(10, 6))

    # 구간별 평균 이용량
    rain_group = df.groupby('강수_구간', observed=True)['전체_건수'].mean().reset_index()

    sns.barplot(data=rain_group, x='강수_구간', y='전체_건수', palette='Blues_d')
    plt.title('강수 구간별 평균 이용량 변화', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('강수 구간', fontsize=12)
    plt.ylabel('평균 이용 건수', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ 저장 완료: {save_path}")
    plt.close()


def plot_hourly_usage(df, save_path="outputs/figures/line_hourly_usage.png"):
    """
    시간대별 평균 이용량 추이 라인 차트를 생성합니다.

    Parameters:
    -----------
    df : pd.DataFrame
        전처리된 데이터프레임
    save_path : str
        저장 경로
    """
    print("📊 시간대별 이용량 추이 차트 생성 중...")

    plt.figure(figsize=(14, 6))

    # 시간대별 평균 이용량
    hourly_usage = df.groupby('기준_시간')['전체_건수'].mean()

    plt.plot(hourly_usage.index, hourly_usage.values, marker='o', linewidth=2, color='#2E86AB')
    plt.title('시간대별 평균 이용량 추이', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('시간대 (시)', fontsize=12)
    plt.ylabel('평균 이용 건수', fontsize=12)
    plt.grid(alpha=0.3)

    # 시간대 강조
    plt.axvspan(7, 9, color='lightblue', alpha=0.3, label='출근 시간대 (7-9시)')
    plt.axvspan(18, 20, color='lightcoral', alpha=0.3, label='퇴근 시간대 (18-20시)')

    plt.legend(loc='upper left')
    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ 저장 완료: {save_path}")
    plt.close()


def plot_station_rain_impact(rain_impact_series, top_n=10, save_path="outputs/figures/bar_station_rain_impact_toplow.png"):
    """
    대여소별 우천 감소율 TOP/LOW 수평 막대 차트를 생성합니다.

    Parameters:
    -----------
    rain_impact_series : pd.Series
        대여소별 우천 감소율
    top_n : int
        상/하위 표시 개수
    save_path : str
        저장 경로
    """
    print(f"📊 대여소별 우천 감소율 TOP/LOW {top_n} 차트 생성 중...")

    plt.figure(figsize=(12, 10))

    # TOP/LOW 추출
    top_low = pd.concat([
        rain_impact_series.head(top_n),
        rain_impact_series.tail(top_n)
    ])

    # 색상: 음수는 빨강, 양수는 파랑
    colors = ['#E63946' if x < 0 else '#457B9D' for x in top_low.values]

    plt.barh(range(len(top_low)), top_low.values, color=colors)
    plt.yticks(range(len(top_low)), top_low.index)
    plt.xlabel('우천 시 이용량 변화율 (%)', fontsize=12)
    plt.ylabel('대여소 ID', fontsize=12)
    plt.title(f'대여소별 우천 감소율 TOP / LOW {top_n}', fontsize=16, fontweight='bold', pad=20)
    plt.axvline(0, color='black', linewidth=1, linestyle='--')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ 저장 완료: {save_path}")
    plt.close()


def create_rain_impact_map(station_df, rain_impact_series, save_path="outputs/figures/map_rain_impact.html"):
    """
    대여소 위치 기반 우천 감소율 지도를 생성합니다.

    Parameters:
    -----------
    station_df : pd.DataFrame
        대여소 마스터 데이터
    rain_impact_series : pd.Series
        대여소별 우천 감소율
    save_path : str
        저장 경로
    """
    print("🗺️  우천 감소율 지도 생성 중...")

    # 감소율 데이터와 좌표 병합
    station_merge = station_df.merge(
        rain_impact_series.reset_index(),
        left_on='대여소_ID',
        right_on='시작_대여소_ID',
        how='inner'
    )

    if '우천감소율(%)' not in station_merge.columns:
        station_merge.rename(columns={station_merge.columns[-1]: '우천감소율(%)'}, inplace=True)

    # 중심 좌표 설정 (서울시청)
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 대여소별 원형 마커 표시
    for _, row in station_merge.iterrows():
        # 감소율에 따라 색상 결정
        if pd.isna(row['우천감소율(%)']):
            continue

        impact = row['우천감소율(%)']
        if impact < -50:
            color = 'darkred'
        elif impact < -20:
            color = 'red'
        elif impact < 0:
            color = 'orange'
        else:
            color = 'blue'

        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"<b>{row['대여소_ID']}</b><br>"
                  f"{row.get('주소2', 'N/A')}<br>"
                  f"감소율: {impact:.1f}%",
            tooltip=f"{row['대여소_ID']}: {impact:.1f}%"
        ).add_to(m)

    # 범례 추가
    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 200px; height: 140px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px">
    <p style="margin:0"><b>우천 감소율</b></p>
    <p style="margin:5px 0"><i class="fa fa-circle" style="color:darkred"></i> -50% 이하 (급감)</p>
    <p style="margin:5px 0"><i class="fa fa-circle" style="color:red"></i> -50% ~ -20%</p>
    <p style="margin:5px 0"><i class="fa fa-circle" style="color:orange"></i> -20% ~ 0%</p>
    <p style="margin:5px 0"><i class="fa fa-circle" style="color:blue"></i> 증가</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save(save_path)
    print(f"✅ 저장 완료: {save_path}")


def plot_comparison_before_after(before_df, after_df, save_path="outputs/figures/comparison_heavy_rain.png"):
    """
    집중호우 전후 비교 차트를 생성합니다.

    Parameters:
    -----------
    before_df : pd.DataFrame
        집중호우 이전 데이터
    after_df : pd.DataFrame
        집중호우 기간 데이터
    save_path : str
        저장 경로
    """
    print("📊 집중호우 전후 비교 차트 생성 중...")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 시간대별 비교
    before_hourly = before_df.groupby('기준_시간')['전체_건수'].mean()
    after_hourly = after_df.groupby('기준_시간')['전체_건수'].mean()

    axes[0].plot(before_hourly.index, before_hourly.values, marker='o', label='이전 주 (9/10-9/16)', linewidth=2)
    axes[0].plot(after_hourly.index, after_hourly.values, marker='s', label='집중호우 주 (9/17-9/23)', linewidth=2)
    axes[0].set_title('시간대별 이용량 비교', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('시간대 (시)', fontsize=12)
    axes[0].set_ylabel('평균 이용 건수', fontsize=12)
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # 요일별 비교
    before_weekday = before_df.groupby('요일')['전체_건수'].mean()
    after_weekday = after_df.groupby('요일')['전체_건수'].mean()

    weekday_labels = ['월', '화', '수', '목', '금', '토', '일']
    x = np.arange(len(weekday_labels))
    width = 0.35

    axes[1].bar(x - width/2, before_weekday.values, width, label='이전 주 (9/10-9/16)')
    axes[1].bar(x + width/2, after_weekday.values, width, label='집중호우 주 (9/17-9/23)')
    axes[1].set_title('요일별 이용량 비교', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('요일', fontsize=12)
    axes[1].set_ylabel('평균 이용 건수', fontsize=12)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(weekday_labels)
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ 저장 완료: {save_path}")
    plt.close()
