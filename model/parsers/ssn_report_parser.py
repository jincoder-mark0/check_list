"""
SSN_Report.rpt 리포트 파서

이 모듈은 SSN_Report.rpt 파일을 읽어서 Q52, Q53, Q59, Q60 분석에 쓰이는
핀별 동시 스위칭 노이즈(SSN) 마진 및 판정 데이터를 추출합니다.

Attributes:
    없음

## WHY
* IO 핀들의 동시 스위칭으로 인한 노이즈가 허용치 이내인지 검증하여 신호 무결성 보장

## WHAT
* 핀 이름, IO 표준, 종단 설정(OFFCHIP_TERM), SSN 판정 결과(PASS/FAIL) 및 마진(%) 추출

## HOW
* BaseParser를 상속받아 SSN 상세 테이블 행 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class SSNReportParser(BaseParser):
    """ SSN_Report.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        SSN_Report.rpt 파일 파싱 후 데이터 반환

        Logic:
            - SSN 상세 테이블에서 각 핀의 판정 결과 및 마진 추출

        Args:
            file_path: SSN_Report.rpt 절대경로

        Returns:
            Dict[str, Any]: 핀별 SSN 분석 통계 및 상세 리스트
        """
        result: Dict[str, Any] = {
            'summary': {
                'total_pins': 0,
                'pass_count': 0,
                'fail_count': 0,
                'min_margin': 100.0
            },
            'pins': []
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 패턴: | IO Bank | VCCO | Signal Name | Pin Number | IO Standard | ... | OFFCHIP_TERM | Remaining Margin(%) | Result |
        pat_ssn_row = self.get_pattern('ssn_row', r'\|\s*(\d*)\s*\|\s*[\d.]*\s*\|\s*(\S+)\s*\|\s*\S+\s*\|\s*([^\|]+?)\s*\|.*?\|\s*(\S+)\s*\|\s*([-\d.]+)\s*\|\s*(\w+)\s*\|')

        for line in lines:
            match = pat_ssn_row.search(line)
            if match:
                # 헤더 제외 (IO Bank가 숫자인 경우만 데이터로 간주)
                if match.group(1).isdigit():
                    sig_name = match.group(2)
                    io_std = match.group(3).strip()
                    term = match.group(4).strip()
                    margin = float(match.group(5))
                    status = match.group(6).strip().upper()

                    result['summary']['total_pins'] += 1
                    if status == 'PASS':
                        result['summary']['pass_count'] += 1
                    else:
                        result['summary']['fail_count'] += 1

                    if margin < result['summary']['min_margin']:
                        result['summary']['min_margin'] = margin

                    result['pins'].append({
                        'signal_name': sig_name,
                        'io_standard': io_std,
                        'offchip_term': term,
                        'margin': margin,
                        'result': status
                    })

        return result
