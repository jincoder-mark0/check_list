"""
Debug_Core.rpt 리포트 파서

이 모듈은 Debug_Core.rpt 파일을 읽어서 Q18 분석에 쓰이는
프로젝트 내 삽입된 디버그 코어(ILA, VIO 등)의 유무 및 상세 리스트를 추출합니다.

Attributes:
    없음

## WHY
* 최종 릴리스 빌드에 의도치 않은 디버그 코어 포함 여부 및 보안성 확인

## WHAT
* 디버그 코어 발견 여부, 코어 타입(ILA/VIO), 프로브 개수 추출

## HOW
* BaseParser를 통해 디버그 코어 요약 문구 및 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class DebugCoreParser(BaseParser):
    """ Debug_Core.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Debug_Core.rpt 파일 파싱 후 디버그 코어 데이터 반환

        Args:
            file_path: Debug_Core.rpt 절대경로

        Returns:
            Dict[str, Any]: 발견된 디버그 코어 정보
        """
        result: Dict[str, Any] = {'debug_cores': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_no_debug = self.get_pattern('dbg_none', r'No debug cores were found in this design')
        pat_dbg_row = self.get_pattern('dbg_row', r'\|\s+(\S+)\s+\|\s+(\S+)\s+\|\s+(\d+)\s+\|')

        for line in lines:
            if pat_no_debug.search(line):
                result['found'] = False
                return result

            match = pat_dbg_row.search(line)
            if match:
                result['found'] = True
                result['debug_cores'].append({
                    'name': match.group(1),
                    'type': match.group(2),
                    'probe_count': int(match.group(3))
                })

        return result
