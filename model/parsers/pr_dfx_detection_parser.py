"""
PR_DFX_Detection.txt 리포트 파서

이 모듈은 PR_DFX_Detection.txt 파일을 읽어서 DFX(Dynamic Function eXchange)
활성화 여부를 판정합니다.

Attributes:
    없음

## WHY
* 설계에서 PR/DFX 기능이 사용되었는지 자동 확인하기 위함

## WHAT
* 'PR/DFX is NOT used' 또는 'PR/DFX is used' 문자열 감지

## HOW
* 파일 전체 텍스트에서 간단한 문자열 매칭 수행
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PRDFXDetectionParser(BaseParser):
    """ PR_DFX_Detection.txt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        PR_DFX_Detection.txt 파일 파싱 후 DFX 사용 여부 반환

        Args:
            file_path: PR_DFX_Detection.txt 절대경로

        Returns:
            Dict[str, Any]: DFX 사용 여부 (is_used)
        """
        result = {'is_used': False, 'raw_text': ''}
        content = self.read_file_content(file_path)
        if not content:
            return result

        result['raw_text'] = content.strip()
        if "PR/DFX is used" in content:
            result['is_used'] = True
        elif "PR/DFX is NOT used" in content:
            result['is_used'] = False

        return result
