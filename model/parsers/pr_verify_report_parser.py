"""
PR_Verify_Report.rpt 리포트 파서

이 모듈은 PR_Verify_Report.rpt 파일을 읽어서 Q26 분석에 쓰이는
Partial Reconfiguration 구성 간 무결성 검증 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 정적 비트스트림과 부분 비트스트림 간의 인터페이스 정합성 확인

## WHAT
* PR Verify 성공 여부 및 요약 메시지 수집

## HOW
* BaseParser를 통해 검증 결과 요약 섹션 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PRVerifyReportParser(BaseParser):
    """ PR_Verify_Report.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        PR_Verify_Report.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: PR_Verify_Report.rpt 절대경로

        Returns:
            Dict[str, Any]: PR 검증 수행 결과
        """
        result: Dict[str, Any] = {'status': 'Unknown'}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_success = self.get_pattern('pr_v_succ', r'(?i)Verification\s+PASSED')
        pat_fail = self.get_pattern('pr_v_fail', r'(?i)Verification\s+FAILED')

        for line in lines:
            if pat_success.search(line):
                result['status'] = 'PASSED'
                break
            elif pat_fail.search(line):
                result['status'] = 'FAILED'
                break

        return result
