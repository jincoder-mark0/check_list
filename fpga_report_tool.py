"""
FPGA 리포트 분석 도구 메인 진입점

이 스크립트는 지정된 리포트 디렉토리를 탐색하고, 파싱하여
체크리스트 답변을 생성하거나 민감정보를 제거하는 기능을 수행합니다.

## 사용법
python fpga_report_tool.py checklist --report-dir <경로> --output <출력파일>
python fpga_report_tool.py redact --report-dir <경로> --output-dir <경로>
python fpga_report_tool.py all --report-dir <경로>
"""

import argparse
import os
import sys
from typing import Dict, List, Any

from core.report_finder import find_reports
from config.config_loader import load_criteria
from checklist.answer_generator import AnswerGenerator
from model.report_models import ReportSummary, ParseResult

def parse_checklist_titles() -> Dict[str, str]:
    """ checklist.md 파일에서 질문 번호별 개요(타이틀) 추출 """
    titles = {}
    checklist_path = os.path.join(os.path.dirname(__file__), "resources/checklist.md")
    if not os.path.exists(checklist_path):
        return titles

    try:
        with open(checklist_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split('|')
                if len(parts) > 6:
                    q_no_str = parts[1].strip()
                    if q_no_str.isdigit():
                        q_id = f"Q{int(q_no_str):02d}"
                        # 6번째 열(index 6) 대신 5번째 열(index 5, 한국어 질문) 사용
                        titles[q_id] = parts[5].strip()
    except Exception as e:
        print(f"Warning: Failed to parse checklist titles: {e}")

    return titles

def save_as_markdown(summary: ReportSummary, output_path: str, titles: Dict[str, str]):
    """ 분석 결과를 마크다운 테이블 형식으로 저장 """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# FPGA 체크리스트 자동 판정 결과\n\n")
        f.write(f"- **대상 프로젝트**: {summary.project_name}\n")
        f.write(f"- **총 점검 문항**: {summary.total_questions}\n\n")

        f.write("| No | 질문 개요 | 판정 | 답변 요약 | 근거 리포트 |\n")
        f.write("|:--:|:----------|:----:|:----------|:------------|\n")

        for res in summary.results:
            q_id = res.question_id
            title = titles.get(q_id, "Unknown Question")
            status = res.status
            reason = res.reason or ""
            # 근거 파일 리스트를 파일명만 추출하여 쉼표로 연결
            evidences = ", ".join([os.path.basename(f) for f in res.evidence_files if f])

            f.write(f"| {q_id} | {title} | **{status}** | {reason} | {evidences} |\n")

    print(f"Successfully saved checklist answers to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="FPGA Report Analysis Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Checklist 명령
    chk_parser = subparsers.add_parser("checklist", help="Generate checklist answers")
    chk_parser.add_argument("--report-dir", required=True, help="Directory containing report files")
    chk_parser.add_argument("--output", default="checklist_results.md", help="Output markdown file path")
    chk_parser.add_argument("--criteria", help="Custom criteria.json path")

    # Redact 명령 (Placeholder)
    red_parser = subparsers.add_parser("redact", help="Redact sensitive info from reports")
    red_parser.add_argument("--report-dir", required=True, help="Directory containing report files")
    red_parser.add_argument("--output-dir", default="_redacted", help="Output directory for redacted files")

    # All 명령 (Checklist + Redact)
    all_parser = subparsers.add_parser("all", help="Perform both checklist generation and redaction")
    all_parser.add_argument("--report-dir", required=True, help="Directory containing report files")
    all_parser.add_argument("--output", default="checklist_results.md", help="Output markdown file path")
    all_parser.add_argument("--output-dir", default="_redacted", help="Output directory for redacted files")

    args = parser.parse_args()

    # 공통 로직: 리포트 탐색
    if args.command in ["checklist", "redact", "all"]:
        print(f"[*] Searching reports in: {args.report_dir}")
        found_reports = find_reports(args.report_dir)
        if not found_reports:
            print("Error: No report files found in the specified directory.")
            sys.exit(1)
        print(f"[*] Found {len(found_reports)} reports.")

    else:
        parser.print_help()
        return
        
    if args.command == "checklist" or args.command == "all":
        # 1. 환경 및 설정 로드
        print(f"[*] Loading criteria...")
        criteria = load_criteria()

        # 2. 분석 수행
        print(f"[*] Starting checklist analysis...")
        generator = AnswerGenerator(criteria, found_reports)
        summary = generator.generate_summary()

        # 3. 결과 저장
        titles = parse_checklist_titles()
        save_as_markdown(summary, args.output, titles)
        print("[*] Analysed reports saved to: {args.output_dir}")

    if args.command == "redact" or args.command == "all":
        from redactor import ReportRedactor
        print(f"[*] Starting redaction...")

        redactor = ReportRedactor(args.output_dir)
        redactor.batch_redact(found_reports)
        print(f"[*] Redacted reports saved to: {args.output_dir}")

if __name__ == "__main__":
    main()
