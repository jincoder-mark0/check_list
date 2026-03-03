"""
Clock_Networks.rpt 리포트 파서

이 모듈은 Clock_Networks.rpt 파일을 읽어서 Q32, Q34 분석에 쓰이는
클럭 포트 목록, 주파수 및 엔드포인트 통계 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 클럭 공급 인프라의 루트 구조 및 각 클럭이 제어하는 엔드포인트 수 파악

## WHAT
* 클럭 포트명, 주파수(MHz), Clock/Nonclock 엔드포인트 수 추출

## HOW
* BaseParser를 상속받아 클럭 선언 및 요약 행 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class ClockNetworksParser(BaseParser):
    """ Clock_Networks.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Clock_Networks.rpt 파일 파싱 후 클럭 네트워크 데이터 반환

        Logic:
            - Clock 포트 선언 행에서 이름, 주파수, 엔드포인트 수 추출

        Args:
            file_path: Clock_Networks.rpt 절대경로

        Returns:
            Dict[str, Any]: 클럭 포트별 상세 통계
        """
        result: Dict[str, List[Dict[str, Any]]] = {'clocks': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 패턴: Clock <name> (<freq>MHz)(endpoints: <clk_ep> clock, <nclk_ep> nonclock)
        pat_clk = self.get_pattern('clk_net', r'Clock\s+(\S+)\s+\(([\d.]+)MHz\)\(endpoints:\s+(\d+)\s+clock,\s+(\d+)\s+nonclock\)')

        for line in lines:
            match = pat_clk.search(line)
            if match:
                result['clocks'].append({
                    'name': match.group(1),
                    'frequency_mhz': float(match.group(2)),
                    'clock_endpoints': int(match.group(3)),
                    'nonclock_endpoints': int(match.group(4))
                })

        return result
