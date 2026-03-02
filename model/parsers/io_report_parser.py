"""
IO_Report.rpt 리포트 파서

이 모듈은 IO_Report.rpt 파일을 읽어서 Q11, Q19 분석에 쓰이는
I/O 핀 사용량 및 개별 핀 전압/표준(Standard) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 물리적 I/O 핀 자원의 할당 현황 및 인터페이스 규격 준수 여부 확인

## WHAT
* Total User IO 수 및 개별 핀의 I/O Standard, Bank 정보 추출

## HOW
* BaseParser를 통해 요약 섹션 및 핀 매핑 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class IOReportParser(BaseParser):
    """ IO_Report.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        IO_Report.rpt 파일 파싱 후 IO 자원 데이터 반환

        Logic:
            - Summary 섹션에서 총 사용량 추출
            - 테이블에서 신호명 기반 상세 정보 수집

        Args:
            file_path: IO_Report.rpt 절대경로

        Returns:
            Dict[str, Any]: IO 통계 및 상세 핀 맵
        """
        result: Dict[str, Any] = {'pin_details': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_io_total = self.get_pattern('io_total', r'\|\s*(\d+)\s*\|') # Summary 섹션의 수치
        pat_io_row = self.get_pattern('io_row', r'\|\s*(\S+)\s*\|.*?\|\s*(\w+)\s*\|\s*([\w]+)\s*\|.*?\|\s*(\d+)\s*\|')

        for line in lines:
            # 총 IO 수 추출 (첫 번째 일치하는 요약 수치)
            if 'total_user_io' not in result:
                if val := self.extract_value_by_regex(line, pat_io_total):
                    result['total_user_io'] = int(val)

            # 핀별 상세 정보 추출
            match = pat_io_row.search(line)
            if match:
                result['pin_details'].append({
                    'signal_name': match.group(1),
                    'direction': match.group(2),
                    'io_standard': match.group(3),
                    'bank': match.group(4)
                })

        return result
