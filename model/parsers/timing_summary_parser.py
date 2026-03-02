"""
Timing_Summary.rpt 리포트 파서

이 모듈은 Timing_Summary.rpt 파일을 읽어서 Q12 분석에 쓰이는
WNS, TNS, WHS, THS 및 타이밍 제약 경고 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계의 클럭 성능이 목표 사양을 충족하는지 확인하기 위함

## WHAT
* 스피드 그레이드 정보, 타이밍 요약 수치(WNS/WHS 등), 제약 누락 경고 추출

## HOW
* BaseParser를 통해 헤더 정보 및 타이밍 요약 테이블 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class TimingSummaryParser(BaseParser):
    """ Timing_Summary.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Timing_Summary.rpt 파일 파싱 후 타이밍 데이터 반환

        Logic:
            - 헤더에서 스피드 그레이드 추출
            - Timer Settings에서 Multi Corner, Pessimism Removal 확인
            - Design Timing Summary에서 WNS, TNS, WHS, THS, WPWS, TPWS 수치 및 Failing 카운트 추출
            - Clock Summary에서 모든 정의된 클럭의 속성 추출
            - Inter Clock Table 및 User Ignored Path Table 추출
            - Jitter 관련 정보 추출
            - check_timing 정보 추출

        Args:
            file_path: Timing_Summary.rpt 절대경로

        Returns:
            Dict[str, Any]: 상세 타이밍 분석 정보
        """
        result: Dict[str, Any] = {
            'summary': {},
            'timer_settings': {},
            'clocks': [],
            'inter_clock': [],
            'ignored_paths': [],
            'path_groups': {},
            'jitter': {}
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 1. 헤더 및 설정 패턴
        pat_speed = self.get_pattern('ts_speed', r'Speed File\s*:\s*(-\d+)\s+(\w+)\s+([\d.]+)')
        pat_mc = self.get_pattern('ts_mc', r'Enable Multi Corner Analysis\s+:\s+(\w+)')
        pat_pr = self.get_pattern('ts_pr', r'Enable Pessimism Removal\s+:\s+(\w+)')

        # 2. Design Timing Summary 패턴
        # WNS(ns) TNS(ns) TNS Failing Endpoints TNS Total Endpoints ...
        pat_dts_header = self.get_pattern('ts_dts_h', r'WNS\(ns\)\s+TNS\(ns\)')
        pat_dts_values = self.get_pattern('ts_dts_v', r'^\s*([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)')

        # 3. Clock Summary 패턴 (Clock | Period | Waveform | Attributes | Sources)
        pat_clk = self.get_pattern('ts_clk', r'^(\S+)\s+([\d.]+)\s+\{([\d.\s]+)\}')

        # 4. Jitter 패턴
        pat_tsj = self.get_pattern('tsj', r'Total System Jitter\s+\(TSJ\)\s*:\s*([\d.]+)ns')
        pat_dj = self.get_pattern('dj', r'Discrete Jitter\s+\(DJ\)\s*:\s*([\d.]+)ns')

        # 5. Check Timing 패턴
        pat_ct_no_clk = self.get_pattern('ct_no_clk', r'There are (\d+) register/latch pins with no clock')
        pat_ct_no_in = self.get_pattern('ct_no_in', r'There are (\d+) input ports with no input delay')
        pat_ct_no_out = self.get_pattern('ct_no_out', r'There are (\d+) output ports with no output delay')

        # 6. Other Path Groups 패턴
        pat_path_group = self.get_pattern('ts_pg', r'^\s*(\S+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)')

        current_section = ""

        for line in lines:
            # 섹션 감지
            if 'Timer Settings' in line: current_section = "TIMER"
            elif 'Design Timing Summary' in line: current_section = "DTS"
            elif 'Clock Summary' in line: current_section = "CLOCK"
            elif 'Inter Clock Table' in line: current_section = "INTER"
            elif 'User Ignored Path Table' in line: current_section = "IGNORED"
            elif 'Other Path Groups Table' in line: current_section = "PATH_GROUPS"
            elif 'check_timing' in line: current_section = "CHECK"

            # 데이터 추출
            if val := self.extract_value_by_regex(line, pat_speed):
                result['speed_grade'] = val
            elif val := self.extract_value_by_regex(line, pat_mc):
                result['timer_settings']['multi_corner'] = val
            elif val := self.extract_value_by_regex(line, pat_pr):
                result['timer_settings']['pessimism_removal'] = val
            elif val := self.extract_value_by_regex(line, pat_tsj):
                result['jitter']['tsj'] = float(val)
            elif val := self.extract_value_by_regex(line, pat_dj):
                result['jitter']['dj'] = float(val)

            if current_section == "DTS":
                if match := pat_dts_values.search(line):
                    result['summary'] = {
                        'WNS': float(match.group(1)), 'TNS': float(match.group(2)),
                        'TNS_FAIL': int(match.group(3)), 'TNS_TOTAL': int(match.group(4)),
                        'WHS': float(match.group(5)), 'THS': float(match.group(6)),
                        'THS_FAIL': int(match.group(7)), 'THS_TOTAL': int(match.group(8)),
                        'WPWS': float(match.group(9)), 'TPWS': float(match.group(10)),
                        'TPWS_FAIL': int(match.group(11)), 'TPWS_TOTAL': int(match.group(12))
                    }
            elif current_section == "CLOCK":
                if match := pat_clk.search(line):
                    result['clocks'].append({
                        'name': match.group(1),
                        'waveform': match.group(2),
                        'period': float(match.group(3)),
                        'frequency': float(match.group(4))
                    })
            elif current_section == "PATH_GROUPS":
                if match := pat_path_group.search(line):
                    result['path_groups'][match.group(1)] = {
                        'WNS': float(match.group(2)), 'TNS': float(match.group(3)),
                        'FAIL': int(match.group(4)), 'TOTAL': int(match.group(5)),
                        'WHS': float(match.group(6)), 'THS': float(match.group(7))
                    }
            elif current_section == "CHECK":
                if val := self.extract_value_by_regex(line, pat_ct_no_clk):
                    result['no_clock'] = int(val)
                elif val := self.extract_value_by_regex(line, pat_ct_no_in):
                    result['no_input_delay'] = int(val)
                elif val := self.extract_value_by_regex(line, pat_ct_no_out):
                    result['no_output_delay'] = int(val)

        return result
