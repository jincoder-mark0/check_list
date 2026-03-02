"""
Clock_Utilization.rpt 리포트 파서

이 모듈은 Clock_Utilization.rpt 파일을 읽어서 Q11 분석에 쓰이는
클럭 자원(BUFG, MMCM, PLL 등) 사용량 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 클럭 공급 인프라 자원의 잔여 용량을 확인하여 설계 확장성 평가

## WHAT
* Clock Primitive 별 사용량(Used) 및 가용량(Available) 데이터 추출

## HOW
* BaseParser를 상속받아 Primitive 테이블 행 매칭 수행
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class ClockUtilizationParser(BaseParser):
    """ Clock_Utilization.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Clock_Utilization.rpt 파일 파싱 후 클럭 자원 데이터 반환

        Logic:
            - Clock Primitive Utilization 섹션의 모든 테이블 행 데이터 추출

        Args:
            file_path: Clock_Utilization.rpt 절대경로

        Returns:
            Dict[str, Any]: 클럭 리소스별 상세 통계
        """
        result: Dict[str, List[Dict[str, Any]]] = {'primitives': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 패턴: | Type | Used | Available | Util% |
        pat_clk_prim = self.get_pattern('clk_prim', r'\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|')

        for line in lines:
            match = pat_clk_prim.search(line)
            if match:
                prim_type = match.group(1).upper()
                # 헤더(Type) 제외하고 유의미한 프리미티브 수집
                if prim_type != 'TYPE':
                    result['primitives'].append({
                        'type': prim_type,
                        'used': int(match.group(2)),
                        'available': int(match.group(3))
                    })

        return result
