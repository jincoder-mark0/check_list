"""
Check_Timing.rpt 리포트 파서

이 모듈은 Check_Timing.rpt 파일을 읽어서 Q12, Q32, Q34, Q35 분석에 쓰이는
타이밍 제약 누락(no_clock, no_input_delay 등) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 타이밍 분석에서 누락된 제약 조건이 있는지 확인하여 분석의 완전성 보장

## WHAT
* no_clock, constant_clock, multiple_clocks, no_input/output_delay 등 위반 건수 수집

## HOW
* BaseParser를 상속받아 요약 메시지 행 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class CheckTimingParser(BaseParser):
    """ Check_Timing.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Check_Timing.rpt 파일 파싱 후 타이밍 제약 누락 데이터 반환

        Args:
            file_path: Check_Timing.rpt 절대경로

        Returns:
            Dict[str, Any]: 각 제약 체크 항목별 위반 건수
        """
        result: Dict[str, Any] = {
            'no_clock': 0,
            'constant_clock': 0,
            'multiple_clocks': 0,
            'no_input_delay': 0,
            'no_output_delay': 0,
            'latch_loops': 0
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        patterns = {
            'no_clock': self.get_pattern('ct_no_clk', r'There are (\d+) register/latch pins with no clock'),
            'constant_clock': self.get_pattern('ct_const_clk', r'There are (\d+) register/latch pins with constant_clock'),
            'multiple_clocks': self.get_pattern('ct_multi_clk', r'There are (\d+) register/latch pins with multiple clocks'),
            'no_input_delay': self.get_pattern('ct_no_in', r'There are (\d+) input ports with no input delay'),
            'no_output_delay': self.get_pattern('ct_no_out', r'There are (\d+) output ports with no output delay'),
            'latch_loops': self.get_pattern('ct_latch', r'There are (\d+) combinational latch loops')
        }

        for line in lines:
            for key, pat in patterns.items():
                if val := self.extract_value_by_regex(line, pat):
                    result[key] = int(val)

        return result
