"""
Bus_Skew.rpt 리포트 파서

이 모듈은 Bus_Skew.rpt 파일을 읽어서 Q38 분석에 쓰이는
버스 스큐(Bus Skew) 제약 충족 여부 및 최악 스큐(WBS) 수치를 추출합니다.

Attributes:
    없음

## WHY
* 소스 동기 방식이나 비동기 버스 인터페이스의 비트 간 지연 차이(Skew) 보증 확인

## WHAT
* Worst Bus Skew (WBS) 수치 및 Slack(여유도) 정보 추출

## HOW
* BaseParser를 상속받아 요약 섹션 및 최악 경로 수치 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class BusSkewParser(BaseParser):
    """ Bus_Skew.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Bus_Skew.rpt 파일 파싱 후 버스 스큐 데이터 반환

        Logic:
            - 최악 버스 스큐(WBS)와 그에 따른 Slack 수치 추출

        Args:
            file_path: Bus_Skew.rpt 절대경로

        Returns:
            Dict[str, Any]: WBS 및 Slack 정보
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_wbs = self.get_pattern('bs_wbs', r'WBS\s*\(ns\)\s*\|\s*([-\d.]+)\s*\|')
        pat_slack = self.get_pattern('bs_slack', r'Slack\s*\(ns\)\s*\|\s*([-\d.]+)\s*\|')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_wbs):
                result['worst_bus_skew'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_slack):
                result['bus_skew_slack'] = float(val)

        return result
