"""
IP_Status.rpt 리포트 파서

이 모듈은 IP_Status.rpt 파일을 읽어서 Q01, Q09, Q10 등에 쓰이는
IP 개수, 업데이트 상태, 라이선스 상태, 변경 로그 존재 여부 등을 추출합니다.

Attributes:
    없음

## WHY
* 프로젝트에서 사용 중인 IP의 버전 현황 및 관리 상태를 점검하기 위함

## WHAT
* IP 인스턴스별 상태(Up-to-date, Major Update Available 등) 집계 및 변경 로그 확인

## HOW
* BaseParser를 상속받아 요약 문구 및 테이블 행 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class IPStatusParser(BaseParser):
    """ IP_Status.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        IP_Status.rpt 파일 파싱 후 IP 상태 데이터 반환

        Logic:
            - 요약 문장에서 전체 IP 수 추출
            - 테이블 내 각 IP의 상태를 분주하여 집계

        Args:
            file_path: IP_Status.rpt 절대경로

        Returns:
            Dict[str, Any]: IP 상태 및 통계 정보
        """
        result: Dict[str, Any] = {
            'total_ip_count': 0,
            'status_up_to_date': 0,
            'status_update_available': 0,
            'status_deprecated': 0,
            'has_changelogs': False
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_total = self.get_pattern('ip_total', r'Your project uses (\d+) IP')
        pat_row = self.get_pattern('ip_row', r'\|\s*\S+\s*\|\s*([\w-]+)\s*\|\s*.*?\|')
        pat_changelog = self.get_pattern('ip_log', r'changelog\.txt')

        for line in lines:
            if total_val := self.extract_value_by_regex(line, pat_total):
                result['total_ip_count'] = int(total_val)
                continue

            match_row = pat_row.search(line)
            if match_row:
                status = match_row.group(1).lower()
                if status == 'up-to-date':
                    result['status_up_to_date'] += 1
                elif 'update' in status:
                    result['status_update_available'] += 1
                elif 'deprecated' in status:
                    result['status_deprecated'] += 1

            if pat_changelog.search(line):
                result['has_changelogs'] = True

        return result
