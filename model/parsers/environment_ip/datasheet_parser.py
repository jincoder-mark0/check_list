"""
Datasheet.rpt 리포트 파서

이 모듈은 Datasheet.rpt 파일을 읽어서 Q12(클럭 도메인), Q19(메모리 타이밍) 분석에 쓰이는
클럭 도메인 간 타이밍 마진 및 입출력 포트 성능 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 보드 레벨 인터페이스(DDR3, I/O) 타이밍 전파 지연 및 마진의 수치적 확인

## WHAT
* Setup between Clocks, I/O Port Setup/Hold 마진 정보 추출

## HOW
* BaseParser를 상속받아 클럭 간 관계 테이블 및 포트별 수치 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class DatasheetParser(BaseParser):
    """ Datasheet.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Datasheet.rpt 파일 파싱 후 데이터 반환

        Logic:
            - Setup between Clocks 섹션에서 도메인 간 마진 수집
            - 포트별 Setup/Hold 테이블 파싱

        Args:
            file_path: Datasheet.rpt 절대경로

        Returns:
            Dict[str, Any]: 클럭 도메인 및 포트 타이밍 정보
        """
        result: Dict[str, Any] = {'inter_clock_margins': [], 'port_timing': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 포트별 타이밍 패턴 (예: signal, setup_ns, edge, hold_ns, edge)
        # pin_i_clk_100m  |  ddr3_dq[0]  | ... | 0.5 | (R) | 0.1 | (F) |
        pat_port = self.get_pattern('ds_port', r'\|\s*(\S+)\s*\|\s*([-\d.]+)\s*\((\w)\)\s*\|\s*([-\d.]+)\s*\((\w)\)\s*\|')

        for line in lines:
            match = pat_port.search(line)
            if match:
                result['port_timing'].append({
                    'signal': match.group(1),
                    'setup': float(match.group(2)),
                    'setup_edge': match.group(3),
                    'hold': float(match.group(4)),
                    'hold_edge': match.group(5)
                })

        return result
