"""
DRC_Report.rpt 리포트 파서

이 모듈은 DRC_Report.rpt 파일을 읽어서 Q29 분석에 쓰이는
디자인 규칙 검사(DRC) 위반 심각도별 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 하드웨어 구현 전 물리적/논리적 설계 결함을 사전에 식별

## WHAT
* Errors, Critical Warnings, Warnings 건수 수집

## HOW
* BaseParser를 통해 요약(Summary) 섹션 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class DRCReportParser(BaseParser):
    """ DRC_Report.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        DRC_Report.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: DRC_Report.rpt 절대경로

        Returns:
            Dict[str, Any]: DRC 위반 통계
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_errors = self.get_pattern('drc_errors', r'Errors\s*:\s*(\d+)')
        pat_crit_warns = self.get_pattern('drc_crit', r'Critical Warnings\s*:\s*(\d+)')
        pat_warns = self.get_pattern('drc_warns', r'Warnings\s*:\s*(\d+)')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_errors):
                result['error_count'] = int(val)
            elif val := self.extract_value_by_regex(line, pat_crit_warns):
                result['critical_warning_count'] = int(val)
            elif val := self.extract_value_by_regex(line, pat_warns):
                result['warning_count'] = int(val)

        return result
