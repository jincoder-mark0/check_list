"""
Pulse_Width.rpt 리포트 파서

이 모듈은 Pulse_Width.rpt 파일을 읽어서 Q11, Q35 분석에 쓰이는
클럭의 최소/최대 펄스 폭 위반(Violation) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 클럭 신호의 품질(펄스 폭)이 하드웨어 동작 한계 내에 있는지 확인

## WHAT
* 펄스 폭 위반 심각도(Critical Warning, Error) 및 발생 빈도 확인

## HOW
* BaseParser를 상속받아 위반 요약 메시지 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PulseWidthParser(BaseParser):
    """ Pulse_Width.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Pulse_Width.rpt 파일 파싱 후 펄스 폭 위반 및 클럭 특성 데이터 반환

        Logic:
            - 위반 메시지(Severity) 추출
            - 각 클럭별 Waveform(Rising/Falling), Period 추출
            - 각 제약 항목별 Slack 추출

        Args:
            file_path: Pulse_Width.rpt 절대경로

        Returns:
            Dict[str, Any]: 위반 정보 및 클럭별 상세 속성
        """
        result: Dict[str, Any] = {
            'violation_count': 0,
            'max_severity': 'NONE',
            'clocks': {}
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 1. 위반 메시지 패턴
        pat_violation = self.get_pattern('pw_viol', r'(CRITICAL WARNING|ERROR|Warning).*?(WPW|Pulse Width)')

        # 2. 클럭 정보 블록 패턴
        # Clock Name: <name>, Waveform: { <rise> <fall> }, Period: <period>
        pat_clk_name = self.get_pattern('pw_clk_name', r'Clock\s+Name:\s+(\S+)')
        pat_waveform = self.get_pattern('pw_wave', r'Waveform\(ns\):\s+\{\s*([\d.]+)\s+([\d.]+)\s*\}')
        pat_period = self.get_pattern('pw_period', r'Period\(ns\):\s+([\d.]+)')

        # 3. Slack 패턴: 항목(Low/High PW 등) 및 Slack 수치
        pat_slack = self.get_pattern('pw_slack', r'(Low|High)\s+Pulse\s+Width\s+.*?\s+([-\d.]+)\s*$')

        current_clk = None

        for line in lines:
            # 위반 여부 체크
            if match_v := pat_violation.search(line):
                result['violation_count'] += 1
                severity = match_v.group(1).upper()
                if severity == 'ERROR':
                    result['max_severity'] = 'ERROR'
                elif severity == 'CRITICAL WARNING' and result['max_severity'] != 'ERROR':
                    result['max_severity'] = 'CRITICAL WARNING'

            # 클럭 블록 시작
            if name := self.extract_value_by_regex(line, pat_clk_name):
                current_clk = name
                result['clocks'][current_clk] = {'slacks': {}}

            if current_clk:
                if wave := pat_waveform.search(line):
                    result['clocks'][current_clk]['waveform'] = {
                        'rising': float(wave.group(1)),
                        'falling': float(wave.group(2))
                    }
                elif period := self.extract_value_by_regex(line, pat_period):
                    result['clocks'][current_clk]['period'] = float(period)
                elif slack := pat_slack.search(line):
                    result['clocks'][current_clk]['slacks'][slack.group(1)] = float(slack.group(2))

        return result
