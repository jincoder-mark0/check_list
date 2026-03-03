"""
Power_Data.xpe 리포트 파서

이 모듈은 Power_Data.xpe 파일을 읽어서 Q13, Q14, Q20 분석에 쓰이는
총 소비전력, 접합 온도, 전압 레일별 소비전류 성분을 추출합니다.

Attributes:
    없음

## WHY
* 설계의 전력 소비량이 전원 장치 및 방열 설계 사양 내에 있는지 검증

## WHAT
* Total Power, Dynamic/Static Power, Junction Temp, Supply Current 테이블 데이터 추출

## HOW
* BaseParser를 통해 요약 섹션 및 Power Supply Summary 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class PowerDataParser(BaseParser):
    """ Power_Data.xpe 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Power_Data.xpe 파일 파싱 후 전력 및 온도 데이터 반환

        Logic:
            - 요약 섹션에서 전체 전력, 온도, 신뢰도 추출
            - Power Supply Summary 테이블에서 레일별 전류 추출

        Args:
            file_path: Power_Data.xpe 절대경로

        Returns:
            Dict[str, Any]: 전력 및 레일별 세부 수치 정보
        """
        result: Dict[str, Any] = {'supplies': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_total = self.get_pattern('pwr_total', r'Total On-Chip Power \(W\)\s*\|\s*([\d.]+)')
        pat_dynamic = self.get_pattern('pwr_dyn', r'Dynamic \(W\)\s*\|\s*([\d.]+)')
        pat_static = self.get_pattern('pwr_stat', r'Device Static \(W\)\s*\|\s*([\d.]+)')
        pat_junction = self.get_pattern('pwr_temp', r'Junction Temperature \(C\)\s*\|\s*([\d.]+)')
        pat_confidence = self.get_pattern('pwr_conf', r'Confidence Level\s*\|\s*(\w+)')

        # Power Supply Summary 패턴: source, voltage_v, total_a, dynamic_a, static_a
        pat_supply = self.get_pattern('pwr_supply', r'\|\s+(\w+)\s+\|\s+([\d.]+)\s+\|\s+([\d.*]+)\s+\|\s+([\d.]+)\s+\|\s+([\d.]+)\s+\|')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_total):
                result['total_power'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_dynamic):
                result['dynamic_power'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_static):
                result['static_power'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_junction):
                result['junction_temp'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_confidence):
                result['confidence'] = val

            match_sup = pat_supply.search(line)
            if match_sup:
                result['supplies'].append({
                    'source': match_sup.group(1),
                    'voltage': float(match_sup.group(2)),
                    'total_current': float(match_sup.group(3).replace('*', '')), # * 표시 제거
                    'dynamic_current': float(match_sup.group(4)),
                    'static_current': float(match_sup.group(5))
                })

        return result
