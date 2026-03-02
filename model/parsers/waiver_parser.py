"""
Waiver.rpt 리포트 파서

이 모듈은 Waiver.rpt 파일을 읽어서 Q29 분석에 쓰이는
설계 위반 예외 처리(Waived) 내역을 추출합니다.

Attributes:
    없음

## WHY
* 강제로 무시된 CDC/DRC 경고 리스트를 파악하여 설계 리스크 상기

## WHAT
* Waiver 카테고리(CDC, DRC 등)별 적용 건수 수집

## HOW
* BaseParser를 통해 요약(Summary) 테이블 행 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class WaiverParser(BaseParser):
    """ Waiver.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Waiver.rpt 파일 파싱 후 데이터 반환

        Logic:
            - 요약 테이블에서 카테고리별 건수 추출
            - create_waiver 명령 구문에서 상세 정보(ID, 사용자, 사유) 추출

        Args:
            file_path: Waiver.rpt 절대경로

        Returns:
            Dict[str, Any]: Waiver 카테고리별 통계 및 상세 리스트
        """
        result: Dict[str, Any] = {
            'counts': {},
            'details': []
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 1. 요약 패턴: | Category | Waived |
        pat_waiver_row = self.get_pattern('waiver_row', r'\|\s*(\w+)\s*\|\s*(\d+)\s*\|')

        # 2. 상세 명령 패턴: create_waiver -type <type> -id <id> -user <user> -description "<desc>"
        pat_details = self.get_pattern('waiver_detail', r'create_waiver\s+-type\s+(\w+)\s+-id\s+([\w-]+)\s+-user\s+(\w+).*?-description\s+"([^"]+)"')

        for line in lines:
            if match := pat_waiver_row.search(line):
                result['counts'][match.group(1)] = int(match.group(2))

            if match_d := pat_details.search(line):
                result['details'].append({
                    'type': match_d.group(1),
                    'id': match_d.group(2),
                    'user': match_d.group(3),
                    'description': match_d.group(4)
                })

        return result
