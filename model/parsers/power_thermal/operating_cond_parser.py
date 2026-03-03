"""
Operating_Cond.rpt 리포트 파서

이 모듈은 Operating_Cond.rpt 파일을 읽어서 Q13 분석에 쓰이는
설정된 주변 온도(Ambient Temp) 및 전원 전압 동작 환경 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 전력 분석 시 사용자가 설정한 시스템 동작 환경(온도, 전압)의 정합성 확인

## WHAT
* Ambient Temperature, Voltage 설정값 추출

## HOW
* BaseParser를 상속받아 요약 테이블의 설정값 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class OperatingCondParser(BaseParser):
    """ Operating_Cond.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Operating_Cond.rpt 파일 파싱 후 환경 설정 정보 반환

        Args:
            file_path: Operating_Cond.rpt 절대경로

        Returns:
            Dict[str, Any]: 설정된 온도/전압 환경 데이터
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_ambient = self.get_pattern('op_ambient', r'Ambient Temp \(C\)\s*\|\s*([\d.]+)')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_ambient):
                result['ambient_temp'] = float(val)
                break

        return result
