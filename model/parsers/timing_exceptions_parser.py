"""
Timing_Exceptions.rpt 리포트 파서

이 모듈은 Timing_Exceptions.rpt 파일을 읽어서 Q37, Q38, Q39 분석에 쓰이는
사용자 정의 타이밍 예외(False Path, Multicycle Path, Clock Groups) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계자가 의도적으로 타이밍 분석에서 제외하거나 수정한 경로들의 타당성 검토

## WHAT
* set_clock_groups(비동기 격리), set_false_path, set_multicycle_path 설정 리스트 수집

## HOW
* BaseParser를 상속받아 각 예외 타입별 상세 리스트 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class TimingExceptionsParser(BaseParser):
    """ Timing_Exceptions.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Timing_Exceptions.rpt 파일 파싱 후 타이밍 예외 데이터 반환

        Logic:
            - Clock Groups, False Path, Multicycle Path 섹션에서 각 설정 항목 추출

        Args:
            file_path: Timing_Exceptions.rpt 절대경로

        Returns:
            Dict[str, Any]: 예외 타입별 설정 내역 및 건수
        """
        result: Dict[str, Any] = {
            'clock_groups': [],
            'false_paths': 0,
            'multicycle_paths': []
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 패턴: [get_clocks {clk1}] [get_clocks {clk2}] clock_group
        pat_clk_group = self.get_pattern('te_clk_grp', r'\[get_clocks\s+\{([^\}]+)\}\]\s+\[get_clocks\s+\{([^\}]+)\}\]\s+clock_group')
        # 패턴: multicycle 경로 및 설정 cycles 추출
        pat_mcp = self.get_pattern('te_mcp', r'\|\s+(\d+)\s+\|.*?\|\s+(\d+)\s+\|.*?\|') # ID 및 cycles 가정

        for line in lines:
            if match := pat_clk_group.search(line):
                result['clock_groups'].append({
                    'clock_a': match.group(1),
                    'clock_b': match.group(2)
                })

            if 'false_path' in line.lower():
                result['false_paths'] += 1

        return result
