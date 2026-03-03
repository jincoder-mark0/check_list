"""
Control_Sets.rpt 리포트 파서

이 모듈은 Control_Sets.rpt 파일을 읽어서 Q11 분석에 쓰이는
Control Sets 자원 사용 현황 및 라우팅 효율 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 과도한 Control Set 사용에 따른 라우팅 혼잡 및 자원 낭비 여부 판단

## WHAT
* Total Control Sets 수 수집

## HOW
* BaseParser를 이용해 요약 문구의 수치 추출
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class ControlSetsParser(BaseParser):
    """ Control_Sets.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Control_Sets.rpt 파일 파싱 후 요약 데이터 반환

        Args:
            file_path: Control_Sets.rpt 절대경로

        Returns:
            Dict[str, Any]: 컨트롤 셋 통계 수치
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_ctrl_set = self.get_pattern('ctrl_set', r'\|\s*Total control sets\s*\|\s*(\d+)\s*\|')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_ctrl_set):
                result['total_control_sets'] = int(val)
                break

        return result
