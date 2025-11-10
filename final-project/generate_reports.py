"""
서울시 따릉이 날씨 영향 분석 - 보고서 일괄 생성 스크립트

실행: python generate_reports.py

생성 파일:
- outputs/reports/executive_summary.pdf (경영진용 요약본, 2페이지)
- outputs/reports/detailed_analysis.pdf (상세 분석 보고서, ~10페이지)
- outputs/reports/presentation.pptx (프레젠테이션, 11슬라이드)
"""

import sys
import os

# src 디렉토리를 경로에 추가
sys.path.append(os.path.abspath('.'))

from src.utils.report_generator import (
    generate_executive_summary,
    generate_detailed_analysis,
    generate_presentation
)


def main():
    print("\n" + "="*80)
    print("서울시 따릉이 날씨 영향 분석 - 보고서 일괄 생성")
    print("="*80)
    print("\n생성 대상:")
    print("  1. 경영진용 요약 보고서 (executive_summary.pdf)")
    print("  2. 상세 분석 보고서 (detailed_analysis.pdf)")
    print("  3. PowerPoint 프레젠테이션 (presentation.pptx)")
    print("\n" + "="*80)

    try:
        # 1. 경영진용 요약 보고서
        print("\n[1/3] 경영진용 요약 보고서 생성 중...")
        exec_pdf = generate_executive_summary()

        # 2. 상세 분석 보고서
        print("\n[2/3] 상세 분석 보고서 생성 중...")
        detail_pdf = generate_detailed_analysis()

        # 3. 프레젠테이션
        print("\n[3/3] PowerPoint 프레젠테이션 생성 중...")
        pptx_file = generate_presentation()

        # 완료 메시지
        print("\n" + "="*80)
        print("보고서 생성 완료!")
        print("="*80)
        print(f"\n생성된 파일:")
        print(f"  1. {exec_pdf}")
        print(f"  2. {detail_pdf}")
        print(f"  3. {pptx_file}")
        print("\n모든 보고서가 outputs/reports/ 디렉토리에 저장되었습니다.")
        print("="*80 + "\n")

        # 파일 정보 요약
        print("파일 크기 요약:")
        for filepath in [exec_pdf, detail_pdf, pptx_file]:
            if os.path.exists(filepath):
                size_kb = os.path.getsize(filepath) / 1024
                filename = os.path.basename(filepath)
                print(f"  - {filename}: {size_kb:.1f} KB")

        return True

    except Exception as e:
        print(f"\n[오류] 보고서 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
