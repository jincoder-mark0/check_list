"""
Switching_Activity.rpt 리포트 파서

이 모듈은 Switching_Activity.rpt 파일을 읽어서 Q14 분석에 쓰이는
동적 전력 계산의 신뢰도 근거가 되는 기본 스위칭 확률 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 동적 전력 분석 시 가정한 노드별 스위칭 확률(Toggle Rate)의 현실성 점검

## WHAT
* Default Toggle Rate, Default Static Probability 정보 추출

## HOW
* BaseParser를 통해 요약 섹션의 확률 수치 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class SwitchingActivityParser(BaseParser):
    """ Switching_Activity.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Switching_Activity.rpt 파일 파싱 후 확률 데이터 반환

        Args:
            file_path: Switching_Activity.rpt 절대경로

        Returns:
            Dict[str, Any]: 기본 토글률 및 정적 확률
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_toggle = self.get_pattern('sa_toggle', r'Default Toggle Rate\s*:\s*([\d.]+)%')
        pat_static = self.get_pattern('sa_static', r'Default Static Probability\s*:\s*([\d.]+)')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_toggle):
                result['default_toggle_rate_pct'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_static):
                result['default_static_probability'] = float(val)

        return result
