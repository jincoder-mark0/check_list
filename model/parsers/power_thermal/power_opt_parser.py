"""
Power_Opt.rpt 리포트 파서

이 모듈은 Power_Opt.rpt 파일을 읽어서 Q13 분석에 쓰이는
전력 최적화(Power Optimization) 적용 여부 및 조치 결과를 추출합니다.

Attributes:
    없음

## WHY
* Vivado의 전력 최적화 기능이 활성화되어 실제 소비전력을 낮추었는지 확인

## WHAT
* Power Optimization 수행 결과 및 적용 리포트 추출

## HOW
* BaseParser를 통해 최적화 요약 테이블 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PowerOptParser(BaseParser):
    """ Power_Opt.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Power_Opt.rpt 파일 파싱 후 최적화 정보 반환

        Args:
            file_path: Power_Opt.rpt 절대경로

        Returns:
            Dict[str, Any]: 최적화 수행 여부 및 메시지
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_power_opt = self.get_pattern('pwr_opt', r'Power Optimization\s*\|\s*(.*)')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_power_opt):
                result['optimization_status'] = val.strip()
                break

        return result
