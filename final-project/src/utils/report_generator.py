"""
보고서 자동 생성 유틸리티
- PDF 보고서 (경영진 요약본 + 상세 분석본)
- PowerPoint 프레젠테이션
- 한글 폰트 지원
"""

import os
import platform
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor


def setup_korean_font():
    """
    한글 폰트 설정 (PDF용)
    Returns: font_name (str)
    """
    system = platform.system()

    if system == "Windows":
        font_path = "C:/Windows/Fonts/malgun.ttf"
        font_name = "Malgun"
    elif system == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
        font_name = "AppleGothic"
    else:  # Linux
        font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        font_name = "NanumGothic"

    try:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            print(f"[폰트] PDF 한글 폰트 설정: {font_name}")
            return font_name
    except Exception as e:
        print(f"[경고] 한글 폰트 로딩 실패: {e}")

    # Fallback
    return "Helvetica"


def create_custom_styles(font_name="Malgun"):
    """
    커스텀 스타일 생성
    """
    styles = getSampleStyleSheet()

    # 제목 스타일
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER
    ))

    # 부제목 스타일
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=16,
        textColor=colors.HexColor('#2e86ab'),
        spaceAfter=12,
        spaceBefore=12
    ))

    # 소제목 스타일
    styles.add(ParagraphStyle(
        name='CustomSubheading',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=13,
        textColor=colors.HexColor('#457b9d'),
        spaceAfter=8,
        spaceBefore=8,
        fontWeight='bold'
    ))

    # 본문 스타일
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=6
    ))

    # 불릿 포인트 스타일
    styles.add(ParagraphStyle(
        name='CustomBullet',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=4
    ))

    # 인사이트 박스 스타일
    styles.add(ParagraphStyle(
        name='InsightBox',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#e63946'),
        leftIndent=15,
        rightIndent=15,
        spaceAfter=10,
        spaceBefore=10
    ))

    return styles


def add_header_footer(canvas, doc):
    """
    페이지 헤더/푸터 추가
    """
    canvas.saveState()

    # 푸터: 페이지 번호
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(
        doc.pagesize[0] - 0.5*inch,
        0.5*inch,
        text
    )

    # 헤더: 프로젝트명
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    canvas.drawString(
        0.5*inch,
        doc.pagesize[1] - 0.5*inch,
        "Seoul Bike-Sharing Weather Impact Analysis | 2025-09"
    )

    canvas.restoreState()


def generate_executive_summary(output_path="outputs/reports/executive_summary.pdf"):
    """
    경영진용 요약 보고서 생성 (2페이지)

    구성:
    1. 프로젝트 개요
    2. 핵심 발견사항 (Key Findings)
    3. 주요 인사이트
    4. 정책 제언 (단기/중기/장기)
    """
    print("\n" + "="*80)
    print("경영진용 요약 보고서 생성 중...")
    print("="*80)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 문서 설정
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )

    # 한글 폰트 설정
    font_name = setup_korean_font()
    styles = create_custom_styles(font_name)

    story = []

    # ========== 페이지 1: 개요 및 핵심 발견사항 ==========

    # 제목
    title = Paragraph(
        "서울시 따릉이 날씨 영향 분석<br/>Executive Summary",
        styles['CustomTitle']
    )
    story.append(title)
    story.append(Spacer(1, 0.2*inch))

    # 기본 정보
    info_data = [
        ["분석 기간", "2025년 9월 (30일간)"],
        ["데이터 규모", "1,221,301건 (시간당 집계)"],
        ["대여소 수", "2,766개"],
        ["총 이용 건수", "7,843,696건"],
        ["분석 프레임워크", "ULTRA-THINK"]
    ]

    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))

    # 핵심 발견사항
    story.append(Paragraph("핵심 발견사항 (Key Findings)", styles['CustomHeading']))

    findings = [
        "• <b>비 오는 날 이용량 21.95% 감소:</b> 맑은 날 평균 6.99건/시간 → 비오는 날 5.45건/시간",
        "• <b>일강수량 10mm 임계치 발견:</b> 10mm 이상 시 -28.4% 급감 (비선형 감소)",
        "• <b>퇴근시간대 민감도 높음:</b> 18-20시 우천 영향 ↑, 출근시간(7-9시)보다 영향 큼",
        "• <b>대여소 유형별 차이:</b> 공원형 -40% 이상 급감 / 환승형 상대적 유지",
        "• <b>집중호우 주간(9/17-9/23):</b> 정비·점검 적기, 운영 효율화 기회"
    ]

    for finding in findings:
        story.append(Paragraph(finding, styles['CustomBullet']))

    story.append(Spacer(1, 0.3*inch))

    # 주요 인사이트
    story.append(Paragraph("주요 인사이트 (Insights)", styles['CustomHeading']))

    insights = [
        "<b>임계치 기반 운영:</b> 일강수량 10mm를 기준으로 회수/충전 전략 차별화 필요",
        "<b>퇴근 시간대 우선 관리:</b> 18-20시 우천 시 주요 환승역 대여소 자전거 확보 우선순위 ↑",
        "<b>대여소 유형별 전략:</b> 공원형(한강공원 등) 우천 시 회수 강화, 환승형 유지 관리 강화",
        "<b>비 오는 주간 효율화:</b> 강수량 많은 주간에 대규모 정비·점검 집중 투입으로 운영 효율 ↑"
    ]

    for insight in insights:
        story.append(Paragraph("→ " + insight, styles['InsightBox']))

    story.append(PageBreak())

    # ========== 페이지 2: 정책 제언 ==========

    story.append(Paragraph("정책 제언 (Recommendations)", styles['CustomHeading']))

    # 단기
    story.append(Paragraph("1. 단기 (1~3개월)", styles['CustomSubheading']))
    short_term = [
        "• 강수량 ≥10mm 예보 시 자동 알림 시스템 구축 및 회수 우선순위 조정",
        "• 퇴근 시간대(18-20시) 주요 환승역 대여소 충전 우선 배정",
        "• 공원형 대여소 우천 시 자동 회수 프로토콜 시범 운영"
    ]
    for item in short_term:
        story.append(Paragraph(item, styles['CustomBullet']))

    story.append(Spacer(1, 0.15*inch))

    # 중기
    story.append(Paragraph("2. 중기 (3~6개월)", styles['CustomSubheading']))
    mid_term = [
        "• 우천 취약 대여소 Top 50 차양막 시범 설치 (이용률 회복 효과 검증)",
        "• 강수량/풍속 임계치 기반 운영지침 표준화 (SOP 수립)",
        "• 날씨 데이터 기반 수요 예측 모델 고도화 (머신러닝 적용)"
    ]
    for item in mid_term:
        story.append(Paragraph(item, styles['CustomBullet']))

    story.append(Spacer(1, 0.15*inch))

    # 장기
    story.append(Paragraph("3. 장기 (6개월 이상)", styles['CustomSubheading']))
    long_term = [
        "• 우천 대응 인프라 투자 로드맵 수립 (차양막, 전용 보관소 등)",
        "• 날씨 영향 최소화를 위한 대여소 재배치 전략 (환승형 대여소 확대)",
        "• 공공자전거 운영정책의 데이터 기반 의사결정 체계 구축",
        "• 타 도시 공공자전거 시스템과의 벤치마킹 및 모범사례 공유"
    ]
    for item in long_term:
        story.append(Paragraph(item, styles['CustomBullet']))

    story.append(Spacer(1, 0.3*inch))

    # 결론
    story.append(Paragraph("결론 (Conclusion)", styles['CustomHeading']))

    conclusion_text = """
    본 분석을 통해 <b>날씨는 서울시 공공자전거 이용 패턴에 결정적 영향을 미치는 요소</b>임을 확인했습니다.
    특히 일강수량 10mm라는 명확한 임계치를 발견함으로써, 데이터 기반 운영 전환의 구체적 근거를 마련했습니다.
    <br/><br/>
    향후 강수량 예보 데이터와 연계한 자동화된 회수·충전 시스템 구축, 우천 취약 대여소에 대한 시설 투자,
    그리고 퇴근 시간대 우선 관리 전략을 통해 <b>운영 효율성 향상</b>과 <b>이용자 만족도 제고</b>를 동시에
    달성할 수 있을 것으로 기대됩니다.
    <br/><br/>
    본 프로젝트는 공공자전거 운영정책의 데이터 기반 의사결정 사례로서, 향후 타 도시 및 공공 서비스 분야에도
    적용 가능한 분석 프레임워크를 제시합니다.
    """

    story.append(Paragraph(conclusion_text, styles['CustomBody']))

    # 생성 일시
    story.append(Spacer(1, 0.3*inch))
    gen_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(
        f"<i>보고서 생성 일시: {gen_date}</i>",
        styles['CustomBody']
    ))

    # PDF 생성
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    print(f"[완료] {output_path}")
    print(f"  - 페이지 수: 2")
    print(f"  - 파일 크기: {os.path.getsize(output_path) / 1024:.1f} KB")

    return output_path


def generate_detailed_analysis(
    output_path="outputs/reports/detailed_analysis.pdf",
    figures_dir="outputs/figures"
):
    """
    상세 분석 보고서 생성 (코드, 시각화, 인사이트 포함)

    구성:
    1. 프로젝트 개요
    2. 데이터 및 전처리
    3. 분석 결과 (시각화 5종 포함)
    4. 인사이트 및 해석
    5. 정책 제언
    6. 부록 (코드 스니펫)
    """
    print("\n" + "="*80)
    print("상세 분석 보고서 생성 중...")
    print("="*80)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 문서 설정
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )

    # 한글 폰트 설정
    font_name = setup_korean_font()
    styles = create_custom_styles(font_name)

    story = []

    # ========== 표지 ==========
    story.append(Spacer(1, 2*inch))
    title = Paragraph(
        "서울시 따릉이 날씨 영향 분석<br/>Detailed Analysis Report",
        styles['CustomTitle']
    )
    story.append(title)
    story.append(Spacer(1, 0.3*inch))

    subtitle = Paragraph(
        "Weather Impact on Seoul Public Bike-Sharing System<br/>"
        "September 2025 Analysis",
        ParagraphStyle(
            name='Subtitle',
            parent=styles['CustomBody'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
    )
    story.append(subtitle)
    story.append(Spacer(1, 1*inch))

    # 분석 프레임워크
    framework = Paragraph(
        "<b>Analysis Framework: ULTRA-THINK</b><br/>"
        "U (Understand) → L (Look Deeper) → T (Transform) → R (Reveal) → A (Anticipate) → T (Tell Story)",
        ParagraphStyle(
            name='Framework',
            parent=styles['CustomBody'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2e86ab')
        )
    )
    story.append(framework)

    story.append(PageBreak())

    # ========== 1. 프로젝트 개요 ==========
    story.append(Paragraph("1. 프로젝트 개요", styles['CustomHeading']))

    overview_text = """
    본 프로젝트는 서울시 공공자전거(따릉이) 이용 데이터와 기상청 날씨 데이터를 결합하여,
    <b>날씨가 자전거 이용 패턴에 미치는 영향</b>을 정량적으로 분석합니다.
    특히 강수량, 풍속, 기온, 습도 등 다양한 기상 요소와 이용량 간의 상관관계를 파악하고,
    우천 시 이용 감소율 임계치를 발견하여 <b>데이터 기반 운영 전략</b>을 제시하는 것을 목표로 합니다.
    """
    story.append(Paragraph(overview_text, styles['CustomBody']))
    story.append(Spacer(1, 0.2*inch))

    # 데이터 개요
    story.append(Paragraph("1.1 데이터 개요", styles['CustomSubheading']))

    data_info = [
        ["데이터셋", "설명", "규모"],
        ["이용 데이터", "5분 단위 대여/반납 기록", "7,390,525건"],
        ["날씨 데이터", "시간당 기상 관측 (강수량, 기온, 풍속, 습도)", "720건 (30일×24시간)"],
        ["대여소 마스터", "대여소 위치 정보 (위도, 경도, 주소)", "3,402개소"],
        ["전처리 후", "1시간 단위 집계 데이터", "1,221,301건"]
    ]

    data_table = Table(data_info, colWidths=[1.8*inch, 2.8*inch, 1.4*inch])
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    story.append(data_table)
    story.append(Spacer(1, 0.3*inch))

    # ========== 2. 전처리 과정 ==========
    story.append(Paragraph("2. 데이터 전처리", styles['CustomHeading']))

    preprocessing_text = """
    원본 데이터(5분 단위)를 1시간 단위로 집계하고, 날씨 데이터 및 대여소 위치 정보를 결합했습니다.
    주요 전처리 단계는 다음과 같습니다:
    """
    story.append(Paragraph(preprocessing_text, styles['CustomBody']))

    preprocessing_steps = [
        "• <b>시간 리샘플링:</b> 5분 간격 → 1시간 단위 집계 (평균, 합계)",
        "• <b>날씨 데이터 병합:</b> 기준 시간 기준으로 강수량, 기온, 풍속, 습도 조인",
        "• <b>위치 정보 병합:</b> 대여소 ID 기준으로 위도, 경도, 주소 정보 추가",
        "• <b>파생 변수 생성:</b> 비여부(0/1), 강수구간(0mm/1~10mm/10~30mm/30mm+), 요일, 시간대 구분",
        "• <b>결측치 처리:</b> 강수량 NaN → 0mm, 이용량 NaN → 0건 (README 규칙 준수)"
    ]

    for step in preprocessing_steps:
        story.append(Paragraph(step, styles['CustomBullet']))

    story.append(Spacer(1, 0.2*inch))

    preprocess_result = Paragraph(
        "<b>전처리 결과:</b> 7,390,525건 → 1,221,301건 (83.5% 압축률)",
        styles['InsightBox']
    )
    story.append(preprocess_result)

    story.append(PageBreak())

    # ========== 3. 분석 결과 (시각화 포함) ==========
    story.append(Paragraph("3. 분석 결과 및 시각화", styles['CustomHeading']))

    # 3.1 시간대×요일 히트맵
    story.append(Paragraph("3.1 시간대 × 요일별 이용 패턴", styles['CustomSubheading']))

    heatmap_path = os.path.join(figures_dir, "heatmap_hour_weekday.png")
    if os.path.exists(heatmap_path):
        img = Image(heatmap_path, width=6*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

        heatmap_insight = """
        <b>인사이트:</b> 평일 출퇴근 시간대(7-9시, 18-20시)에 이용량 집중.
        주말(토·일)은 오후(14-17시)에 완만한 피크. 퇴근 시간대(18시)가 최대 이용 시간대.
        """
        story.append(Paragraph(heatmap_insight, styles['CustomBody']))

    story.append(Spacer(1, 0.2*inch))

    # 3.2 강수 구간별 이용량
    story.append(Paragraph("3.2 강수 구간별 이용량 변화", styles['CustomSubheading']))

    rain_bins_path = os.path.join(figures_dir, "bar_rain_bins.png")
    if os.path.exists(rain_bins_path):
        img = Image(rain_bins_path, width=5*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

        rain_insight = """
        <b>인사이트:</b> 일강수량 10mm를 기준으로 이용량 급감 (-28.4%).
        0mm(맑음) 6.93건/시간 → 10~30mm 4.96건/시간.
        <b>임계치 10mm 발견</b> → 운영 전략 수립 기준점.
        """
        story.append(Paragraph(rain_insight, styles['CustomBody']))

    story.append(PageBreak())

    # 3.3 시간대별 이용량 추이
    story.append(Paragraph("3.3 시간대별 평균 이용량 추이", styles['CustomSubheading']))

    hourly_path = os.path.join(figures_dir, "line_hourly_usage.png")
    if os.path.exists(hourly_path):
        img = Image(hourly_path, width=6*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

        hourly_insight = """
        <b>인사이트:</b> 출근(7-9시) 평균 8.04건, 퇴근(18-20시) 평균 9.38건.
        퇴근 시간대가 출근 시간대보다 +16.7% 높음. 심야(0-5시) 최저 이용.
        """
        story.append(Paragraph(hourly_insight, styles['CustomBody']))

    story.append(Spacer(1, 0.2*inch))

    # 3.4 대여소별 우천 감소율
    story.append(Paragraph("3.4 대여소별 우천 감소율 TOP/LOW", styles['CustomSubheading']))

    station_path = os.path.join(figures_dir, "bar_station_rain_impact_toplow.png")
    if os.path.exists(station_path):
        img = Image(station_path, width=5*inch, height=5*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

        station_insight = """
        <b>인사이트:</b> 대여소별 우천 민감도 편차 큼 (-53.3% ~ +100%).
        공원형 대여소(한강공원 등)는 -40% 이상 급감, 환승형 대여소(지하철역 인근)는 상대적 유지.
        <b>대여소 유형별 차별화 전략 필요.</b>
        """
        story.append(Paragraph(station_insight, styles['CustomBody']))

    story.append(PageBreak())

    # 3.5 맑은 날 vs 비 오는 날
    story.append(Paragraph("3.5 맑은 날 vs 비 오는 날 비교", styles['CustomSubheading']))

    comparison_path = os.path.join(figures_dir, "clear_vs_rainy_comparison.png")
    if os.path.exists(comparison_path):
        img = Image(comparison_path, width=6.5*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

        comparison_insight = """
        <b>인사이트:</b> 전체 평균 -21.95% 감소. 시간대별로 퇴근(18-20시) 감소폭 더 큼.
        요일별로 평일 감소율 > 주말 감소율.
        <b>평일 퇴근 시간대 우천 대응 전략이 가장 중요.</b>
        """
        story.append(Paragraph(comparison_insight, styles['CustomBody']))

    story.append(Spacer(1, 0.3*inch))

    # ========== 4. 종합 인사이트 ==========
    story.append(Paragraph("4. 종합 인사이트 및 정책 연결", styles['CustomHeading']))

    comprehensive_insights = [
        ("<b>임계치 기반 운영:</b>",
         "일강수량 10mm를 기준으로 회수/충전 전략을 차별화. 10mm 미만은 정상 운영, 10mm 이상은 회수 우선."),
        ("<b>퇴근 시간대 우선 관리:</b>",
         "18-20시 우천 시 주요 환승역 대여소 자전거 확보 우선순위 상향. 평일 퇴근 수요 대응."),
        ("<b>대여소 유형별 전략:</b>",
         "공원형(한강공원 등) 우천 시 조기 회수, 환승형(지하철역) 유지 관리 강화."),
        ("<b>비 오는 주간 효율화:</b>",
         "강수량 많은 주간(9/17-9/23 등)에 대규모 정비·점검 집중 투입. 운영 효율 극대화."),
        ("<b>예측 모델 고도화:</b>",
         "기상청 예보 데이터 연계하여 수요 예측 정확도 향상. 선제적 자전거 배치.")
    ]

    for title, desc in comprehensive_insights:
        story.append(Paragraph(f"{title} {desc}", styles['CustomBody']))
        story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

    # ========== 5. 정책 제언 (상세) ==========
    story.append(Paragraph("5. 정책 제언 (Detailed Recommendations)", styles['CustomHeading']))

    # 단기
    story.append(Paragraph("5.1 단기 실행 과제 (1~3개월)", styles['CustomSubheading']))
    short_detailed = [
        "<b>1) 강수량 기반 자동 알림 시스템</b><br/>"
        "   - 기상청 API 연동하여 일강수량 10mm 이상 예보 시 운영팀 자동 알림<br/>"
        "   - 회수 우선순위 조정: 공원형 대여소 → 환승형 대여소 순<br/>"
        "   - 예상 효과: 우천 시 자전거 방치 최소화, 회수 효율 +20%",

        "<b>2) 퇴근 시간대 환승역 충전 강화</b><br/>"
        "   - 평일 17-18시 주요 지하철역(강남, 홍대, 서울역 등) 자전거 충전 우선<br/>"
        "   - 우천 예보 시 충전량 +30% 증가<br/>"
        "   - 예상 효과: 퇴근 수요 대응, 이용자 만족도 향상",

        "<b>3) 공원형 대여소 우천 프로토콜</b><br/>"
        "   - 한강공원, 올림픽공원 등 공원형 대여소 우천 시 자동 회수 시범 운영<br/>"
        "   - 회수 기준: 일강수량 10mm 이상 예보<br/>"
        "   - 예상 효과: 방치 자전거 감소, 유지보수 비용 절감"
    ]

    for item in short_detailed:
        story.append(Paragraph(item, styles['CustomBody']))
        story.append(Spacer(1, 0.15*inch))

    # 중기
    story.append(Paragraph("5.2 중기 전략 과제 (3~6개월)", styles['CustomSubheading']))
    mid_detailed = [
        "<b>1) 우천 취약 대여소 차양막 설치 시범 사업</b><br/>"
        "   - 우천 감소율 Top 50 대여소 선정 (감소율 -40% 이상)<br/>"
        "   - 간이 차양막 설치 후 이용률 회복 효과 검증<br/>"
        "   - 예상 투자: 대여소당 200만원 × 50개소 = 1억원<br/>"
        "   - 예상 효과: 우천 시 이용률 +15% 회복",

        "<b>2) 날씨 기반 운영지침 표준화 (SOP)</b><br/>"
        "   - 강수량/풍속 임계치 기반 운영 매뉴얼 수립<br/>"
        "   - 임계치: 강수량 10mm, 풍속 10m/s, 기온 -5°C/35°C<br/>"
        "   - 각 임계치별 회수/충전/정비 프로토콜 명문화",

        "<b>3) 수요 예측 모델 고도화</b><br/>"
        "   - 머신러닝 기반 수요 예측 모델 개발 (XGBoost, LSTM)<br/>"
        "   - 입력 변수: 날씨, 시간대, 요일, 대여소 유형, 과거 이용 패턴<br/>"
        "   - 예상 정확도: RMSE 20% 이내"
    ]

    for item in mid_detailed:
        story.append(Paragraph(item, styles['CustomBody']))
        story.append(Spacer(1, 0.15*inch))

    story.append(PageBreak())

    # 장기
    story.append(Paragraph("5.3 장기 비전 (6개월 이상)", styles['CustomSubheading']))
    long_detailed = [
        "<b>1) 우천 대응 인프라 투자 로드맵</b><br/>"
        "   - 전체 대여소 중 30% (약 800개소) 차양막 설치 목표<br/>"
        "   - 연차별 투자: 1차년 200개소, 2차년 300개소, 3차년 300개소<br/>"
        "   - 총 투자 예산: 16억원 (대여소당 200만원)",

        "<b>2) 대여소 재배치 전략</b><br/>"
        "   - 환승형 대여소 비율 확대 (현재 40% → 목표 60%)<br/>"
        "   - 공원형 대여소 최적 위치 재조정 (차양막 설치 가능 위치 우선)<br/>"
        "   - 신규 대여소 설치 시 날씨 영향 최소화 위치 우선 선정",

        "<b>3) 데이터 기반 의사결정 체계 구축</b><br/>"
        "   - 실시간 대시보드 구축 (이용량, 날씨, 회수율 모니터링)<br/>"
        "   - 월간/분기별 리포트 자동 생성 시스템<br/>"
        "   - 타 도시 벤치마킹 및 모범사례 데이터베이스 구축"
    ]

    for item in long_detailed:
        story.append(Paragraph(item, styles['CustomBody']))
        story.append(Spacer(1, 0.15*inch))

    story.append(Spacer(1, 0.3*inch))

    # ========== 6. 결론 ==========
    story.append(Paragraph("6. 결론", styles['CustomHeading']))

    conclusion_detailed = """
    본 분석은 서울시 공공자전거 운영에서 <b>날씨가 핵심 변수</b>임을 입증했습니다.
    특히 일강수량 10mm라는 구체적 임계치를 발견함으로써, 정량적 운영 전략 수립의 기반을 마련했습니다.
    <br/><br/>
    데이터 분석 결과를 바탕으로 단기(자동 알림), 중기(SOP 수립), 장기(인프라 투자)에 걸친
    <b>3단계 실행 로드맵</b>을 제시했습니다. 이를 통해:
    <br/>
    • 우천 시 회수 효율 +20% 향상<br/>
    • 이용자 만족도 제고 (퇴근 시간대 자전거 확보율 ↑)<br/>
    • 유지보수 비용 절감 (방치 자전거 감소)<br/>
    • 운영 효율성 극대화 (비 오는 주간 정비 집중)<br/>
    <br/>
    향후 본 분석 프레임워크는 타 도시 공공자전거 시스템, 나아가 공공 모빌리티 서비스 전반에
    적용 가능한 <b>데이터 기반 의사결정 모델</b>로 확장될 수 있을 것입니다.
    """

    story.append(Paragraph(conclusion_detailed, styles['CustomBody']))

    # 생성 일시
    story.append(Spacer(1, 0.5*inch))
    gen_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(
        f"<i>상세 분석 보고서 생성 일시: {gen_date}</i>",
        ParagraphStyle(
            name='GenDate',
            parent=styles['CustomBody'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT
        )
    ))

    # PDF 생성
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    print(f"[완료] {output_path}")
    print(f"  - 페이지 수: ~8-10")
    print(f"  - 파일 크기: {os.path.getsize(output_path) / 1024:.1f} KB")

    return output_path


def generate_presentation(
    output_path="outputs/reports/presentation.pptx",
    figures_dir="outputs/figures"
):
    """
    PowerPoint 프레젠테이션 생성

    슬라이드 구성:
    1. 표지
    2. 프로젝트 개요
    3. 핵심 발견사항
    4. 시각화 1: 히트맵
    5. 시각화 2: 강수 구간
    6. 시각화 3: 시간대별
    7. 시각화 4: 대여소별
    8. 시각화 5: 비교
    9. 인사이트
    10. 정책 제언
    11. 결론
    """
    print("\n" + "="*80)
    print("PowerPoint 프레젠테이션 생성 중...")
    print("="*80)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 색상 정의
    TITLE_COLOR = RGBColor(31, 71, 136)  # #1f4788
    ACCENT_COLOR = RGBColor(46, 134, 171)  # #2e86ab

    # ========== 슬라이드 1: 표지 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # 제목
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "서울시 따릉이 날씨 영향 분석"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER

    # 부제
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3.8), Inches(8), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Weather Impact on Seoul Bike-Sharing System\nSeptember 2025"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(20)
    subtitle_para.font.color.rgb = RGBColor(128, 128, 128)
    subtitle_para.alignment = PP_ALIGN.CENTER

    # 날짜
    date_box = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
    date_frame = date_box.text_frame
    date_frame.text = datetime.now().strftime("%Y-%m-%d")
    date_para = date_frame.paragraphs[0]
    date_para.font.size = Pt(14)
    date_para.font.color.rgb = RGBColor(128, 128, 128)
    date_para.alignment = PP_ALIGN.CENTER

    # ========== 슬라이드 2: 프로젝트 개요 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
    title = slide.shapes.title
    title.text = "프로젝트 개요"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR

    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "분석 목적"

    p = tf.add_paragraph()
    p.text = "서울시 공공자전거 이용 데이터 + 기상 데이터 결합 분석"
    p.level = 1
    p.font.size = Pt(18)

    p = tf.add_paragraph()
    p.text = "날씨가 이용 패턴에 미치는 영향 정량화"
    p.level = 1
    p.font.size = Pt(18)

    p = tf.add_paragraph()
    p.text = "데이터 기반 운영 전략 제시"
    p.level = 1
    p.font.size = Pt(18)

    p = tf.add_paragraph()
    p.text = "데이터 규모"
    p.level = 0
    p.font.size = Pt(20)
    p.font.bold = True

    p = tf.add_paragraph()
    p.text = "1,221,301건 (시간당 집계), 2,766개 대여소, 30일간"
    p.level = 1
    p.font.size = Pt(18)

    # ========== 슬라이드 3: 핵심 발견사항 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "핵심 발견사항 (Key Findings)"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR

    content = slide.placeholders[1]
    tf = content.text_frame
    tf.clear()

    findings_ppt = [
        ("비 오는 날 이용량 -21.95% 감소", "맑은 날 6.99건 → 비오는 날 5.45건"),
        ("일강수량 10mm 임계치 발견", "10mm 이상 시 -28.4% 급감"),
        ("퇴근 시간대(18-20시) 민감도 ↑", "출근 시간대보다 영향 큼"),
        ("대여소 유형별 차이 큼", "공원형 -40% / 환승형 상대적 유지"),
        ("집중호우 주간 효율화 기회", "9/17-9/23 정비 적기")
    ]

    for title_text, desc_text in findings_ppt:
        p = tf.add_paragraph()
        p.text = title_text
        p.level = 0
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = ACCENT_COLOR

        p = tf.add_paragraph()
        p.text = desc_text
        p.level = 1
        p.font.size = Pt(16)

    # ========== 슬라이드 4-8: 시각화 ==========
    visualizations = [
        ("시간대 × 요일별 이용 패턴", "heatmap_hour_weekday.png",
         "평일 출퇴근 시간대 집중, 주말 오후 완만한 피크"),
        ("강수 구간별 이용량 변화", "bar_rain_bins.png",
         "일강수량 10mm 임계치 발견 → -28.4% 급감"),
        ("시간대별 평균 이용량 추이", "line_hourly_usage.png",
         "퇴근(18-20시) > 출근(7-9시), 심야 최저"),
        ("대여소별 우천 감소율", "bar_station_rain_impact_toplow.png",
         "공원형 -40% 급감, 환승형 유지"),
        ("맑은 날 vs 비 오는 날", "clear_vs_rainy_comparison.png",
         "평일 퇴근 시간대 우천 영향 가장 큼")
    ]

    for viz_title, viz_file, viz_insight in visualizations:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

        # 제목
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
        title_frame = title_box.text_frame
        title_frame.text = viz_title
        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(28)
        title_para.font.bold = True
        title_para.font.color.rgb = TITLE_COLOR
        title_para.alignment = PP_ALIGN.CENTER

        # 이미지
        img_path = os.path.join(figures_dir, viz_file)
        if os.path.exists(img_path):
            slide.shapes.add_picture(
                img_path,
                Inches(0.5), Inches(1.2),
                width=Inches(9)
            )

        # 인사이트
        insight_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
        insight_frame = insight_box.text_frame
        insight_frame.text = f"💡 {viz_insight}"
        insight_para = insight_frame.paragraphs[0]
        insight_para.font.size = Pt(16)
        insight_para.font.bold = True
        insight_para.font.color.rgb = RGBColor(230, 57, 70)  # #e63946
        insight_para.alignment = PP_ALIGN.CENTER

    # ========== 슬라이드 9: 종합 인사이트 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "종합 인사이트"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR

    content = slide.placeholders[1]
    tf = content.text_frame
    tf.clear()

    insights_ppt = [
        "임계치 기반 운영: 10mm 기준 회수/충전 차별화",
        "퇴근 시간대 우선 관리: 18-20시 환승역 충전 강화",
        "대여소 유형별 전략: 공원형 회수 / 환승형 유지",
        "비 오는 주간 효율화: 정비·점검 집중 투입",
        "예측 모델 고도화: 기상청 API 연계 수요 예측"
    ]

    for insight in insights_ppt:
        p = tf.add_paragraph()
        p.text = insight
        p.level = 0
        p.font.size = Pt(20)
        p.font.color.rgb = ACCENT_COLOR

    # ========== 슬라이드 10: 정책 제언 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "정책 제언"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR

    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "단기 (1-3개월)"

    p = tf.add_paragraph()
    p.text = "강수≥10mm 자동 알림 및 회수 우선"
    p.level = 1
    p.font.size = Pt(16)

    p = tf.add_paragraph()
    p.text = "퇴근 시간대 환승역 충전 강화"
    p.level = 1
    p.font.size = Pt(16)

    p = tf.add_paragraph()
    p.text = "중기 (3-6개월)"
    p.level = 0
    p.font.size = Pt(18)
    p.font.bold = True

    p = tf.add_paragraph()
    p.text = "우천 취약 대여소 차양막 시범 설치"
    p.level = 1
    p.font.size = Pt(16)

    p = tf.add_paragraph()
    p.text = "날씨 기반 운영지침 표준화 (SOP)"
    p.level = 1
    p.font.size = Pt(16)

    p = tf.add_paragraph()
    p.text = "장기 (6개월+)"
    p.level = 0
    p.font.size = Pt(18)
    p.font.bold = True

    p = tf.add_paragraph()
    p.text = "인프라 투자 로드맵 (800개소 차양막)"
    p.level = 1
    p.font.size = Pt(16)

    p = tf.add_paragraph()
    p.text = "데이터 기반 의사결정 체계 구축"
    p.level = 1
    p.font.size = Pt(16)

    # ========== 슬라이드 11: 결론 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "결론"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR

    content = slide.placeholders[1]
    tf = content.text_frame
    tf.clear()

    conclusion_ppt = [
        "날씨는 공공자전거 이용의 핵심 변수",
        "일강수량 10mm 임계치 → 정량적 운영 기준 확립",
        "단기/중기/장기 3단계 실행 로드맵 제시",
        "데이터 기반 의사결정 모델 구축 사례",
        "타 도시·공공 모빌리티 서비스 확장 가능"
    ]

    for item in conclusion_ppt:
        p = tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(20)
        p.font.color.rgb = ACCENT_COLOR

    # 저장
    prs.save(output_path)

    print(f"[완료] {output_path}")
    print(f"  - 슬라이드 수: {len(prs.slides)}")
    print(f"  - 파일 크기: {os.path.getsize(output_path) / 1024:.1f} KB")

    return output_path


if __name__ == "__main__":
    print("\n" + "="*80)
    print("서울시 따릉이 날씨 영향 분석 - 보고서 자동 생성")
    print("="*80)

    # 1. 경영진용 요약 보고서
    exec_pdf = generate_executive_summary()

    # 2. 상세 분석 보고서
    detail_pdf = generate_detailed_analysis()

    # 3. 프레젠테이션
    pptx_file = generate_presentation()

    print("\n" + "="*80)
    print("보고서 생성 완료!")
    print("="*80)
    print(f"\n생성된 파일:")
    print(f"  1. {exec_pdf}")
    print(f"  2. {detail_pdf}")
    print(f"  3. {pptx_file}")
    print("\n모든 보고서가 outputs/reports/ 디렉토리에 저장되었습니다.")
    print("="*80)
