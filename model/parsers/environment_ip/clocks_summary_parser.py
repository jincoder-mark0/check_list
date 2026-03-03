"""
Clocks_Summary.rpt 리포트 파서

이 모듈은 Clocks_Summary.rpt 파일을 읽어서 클럭 트리 요약 정보를 추출합니다.
(report_clocks 명령 결과 분석)

Attributes:
    없음

## WHY
* 설계에 정의된 클럭 목록 및 주기를 파악하기 위함

## WHAT
* Clock, Period, Waveform, Attributes, Sources, Jitter 추출

## HOW
* 테이블 형식 데이터 및 하단 Jitter 섹션 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class ClocksSummaryParser(BaseParser):
    """ Clocks_Summary.rpt 파일 파싱 클래스 (report_clocks 결과) """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Clocks_Summary.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: Clocks_Summary.rpt 절대경로

        Returns:
            Dict[str, Any]: 클럭 리스트 및 지터 정보
        """
        result: Dict[str, Any] = {'clocks': [], 'jitter': {}}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 테이블 데이터 패턴: pin_i_clk_100m 10.000 {0.000 5.000} P {pin_i_clk_100m}
        pat_clk = self.get_pattern('clk_row', r'^(\S+)\s+([\d.]+)\s+\{([\d.\s]+)\}\s+(\S+)\s+(\S+)')
        # 지터 패턴: pin_i_clk_100m 0.100
        pat_jitter = self.get_pattern('clk_jitter', r'^(\S+)\s+([\d.]+)\s*$')

        in_jitter_section = False

        for line in lines:
            line = line.strip()
            if not line: continue

            if "User Jitter" in line:
                in_jitter_section = True
                continue

            if not in_jitter_section:
                match = pat_clk.search(line)
                if match:
                    result['clocks'].append({
                        'name': match.group(1),
                        'period': float(match.group(2)),
                        'waveform': match.group(3),
                        'attributes': match.group(4),
                        'sources': match.group(5)
                    })
            else:
                # Jitter 섹션 헤더 스킵
                if line.startswith('Clock') or line.startswith('-'):
                    continue
                match = pat_jitter.search(line)
                if match:
                    result['jitter'][match.group(1)] = float(match.group(2))

        return result
