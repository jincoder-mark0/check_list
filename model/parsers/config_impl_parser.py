"""
Config_Impl.rpt 리포트 파서

이 모듈은 Config_Impl.rpt 파일을 읽어서 Q08(구현 설정) 분석에 쓰이는
Strategy, Place Directive, Route Directive 등의 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 구현 과정에서 적용된 컴파일 전략 및 배선 지침을 확인하기 위함

## WHAT
* Implementation Strategy 및 주요 레이아웃 옵션 설정값 추출

## HOW
* BaseParser의 특정 키워드 행 매칭 기능 활용
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class ConfigImplParser(BaseParser):
    """ Config_Impl.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Config_Impl.rpt 파일 파싱 후 구현 설정 데이터 반환

        Args:
            file_path: Config_Impl.rpt 절대경로

        Returns:
            Dict[str, Any]: 구현 전략 및 설정 정보
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_strategy = self.get_pattern('cfg_strategy', r'Strategy\s*:\s*(.*)')
        pat_place = self.get_pattern('cfg_place', r'Place Directive\s*:\s*(.*)')
        pat_route = self.get_pattern('cfg_route', r'Route Directive\s*:\s*(.*)')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_strategy):
                result['strategy'] = val
            elif val := self.extract_value_by_regex(line, pat_place):
                result['place_directive'] = val
            elif val := self.extract_value_by_regex(line, pat_route):
                result['route_directive'] = val

        return result
