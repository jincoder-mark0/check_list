"""
CDC_Report.rpt 리포트 파서

이 모듈은 CDC_Report.rpt 파일을 읽어서 Q29 분석에 쓰이는
클럭 도메인 교차(CDC) 경로의 안전성 검증 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 비동기 클럭 간 데이터 전달 시 메타스테이빌리티 발생 가능성 확인

## WHAT
* Safe, Unsafe, Unknown CDC 엔드포인트 수집

## HOW
* BaseParser를 통해 CDC 요약 테이블 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class CDCReportParser(BaseParser):
    """ CDC_Report.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        CDC_Report.rpt 파일 파싱 후 데이터 반환

        Logic:
            - 요약 섹션에서 Safe/Unsafe/Unknown 전체 수 추출
            - 상세 요약 테이블에서 유형별(CDC-ID), 심각도별 건수 수집
            - Waived 섹션에서 면제된 항목 수집

        Args:
            file_path: CDC_Report.rpt 절대경로

        Returns:
            Dict[str, Any]: CDC 안전성 관련 상세 통계
        """
        result: Dict[str, Any] = {
            'summary': {},
            'violations': [],
            'waived': {}
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_unsafe = self.get_pattern('cdc_unsafe', r'Total\s+Unsafe\s*\|\s*(\d+)')
        pat_unknown = self.get_pattern('cdc_unknown', r'Total\s+Unknown\s*\|\s*(\d+)')
        pat_safe = self.get_pattern('cdc_safe', r'Total\s+Safe\s*\|\s*(\d+)')

        # 상세 요약 패턴: | Severity | ID | Count | Description |
        pat_cdc_row = self.get_pattern('cdc_row', r'\|\s*(Warning|Info)\s*\|\s*(CDC-\d+)\s*\|\s*(\d+)\s*\|')

        # Waived 섹션 패턴: | CDC-1 | 63 | ... |
        pat_waived_row = self.get_pattern('cdc_waived', r'\|\s*(CDC-\d+)\s*\|\s*(\d+)\s*\|')

        is_waived_section = False

        for line in lines:
            if 'Waived' in line:
                is_waived_section = True

            if val := self.extract_value_by_regex(line, pat_unsafe):
                result['summary']['unsafe_count'] = int(val)
            elif val := self.extract_value_by_regex(line, pat_unknown):
                result['summary']['unknown_count'] = int(val)
            elif val := self.extract_value_by_regex(line, pat_safe):
                result['summary']['safe_count'] = int(val)

            if is_waived_section:
                match_w = pat_waived_row.search(line)
                if match_w:
                    result['waived'][match_w.group(1)] = int(match_w.group(2))
            else:
                match_row = pat_cdc_row.search(line)
                if match_row:
                    result['violations'].append({
                        'severity': match_row.group(1),
                        'id': match_row.group(2),
                        'count': int(match_row.group(3))
                    })

        return result
