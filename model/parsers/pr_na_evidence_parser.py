"""
PR_NA_Evidence.txt 리포트 파서

이 모듈은 PR_NA_Evidence.txt 파일을 읽어서 PR 관련 데이터가
누락된 이유(N/A)를 추출합니다.

Attributes:
    없음

## WHY
* PR 분석 시 데이터가 없는 경우 그 근거를 리포트에 기재하기 위함

## WHAT
* N/A 사유 텍스트 추출

## HOW
* 파일 전체를 읽어 strip된 문자열 반환
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PRNAEvidenceParser(BaseParser):
    """ PR_NA_Evidence.txt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        PR_NA_Evidence.txt 파일 파싱 후 근거 텍스트 반환

        Args:
            file_path: PR_NA_Evidence.txt 절대경로

        Returns:
            Dict[str, Any]: N/A 근거 (evidence)
        """
        result = {'evidence': ''}
        content = self.read_file_content(file_path)
        if content:
            result['evidence'] = content.strip()

        return result
