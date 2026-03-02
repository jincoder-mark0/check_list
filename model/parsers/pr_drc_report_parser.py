"""
PR_DRC_Report.rpt 리포트 파서

이 모듈은 PR_DRC_Report.rpt 파일을 읽어서 Q27, Q29 분석에 쓰이는
Partial Reconfiguration 특화 DRC(설계 규칙 검사) 위반 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 부분 재구성 설계 시 pblock 내부 자원 및 핀 배치가 벤더 제약을 따르는지 확인

## WHAT
* PR 전용 DRC 위반 ID, 심각도, 상세 메시지 수집

## HOW
* BaseParser를 상속받아 DRC 위반 리스트 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class PRDRCReportParser(BaseParser):
    """ PR_DRC_Report.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        PR_DRC_Report.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: PR_DRC_Report.rpt 절대경로

        Returns:
            Dict[str, Any]: PR DRC 위반 요약
        """
        result: Dict[str, List[Dict[str, Any]]] = {'violations': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # DRC 위반 데이터 패턴
        pat_drc_row = self.get_pattern('pr_drc_row', r'\|\s+([\w-]+)\s+\|\s+(\w+)\s+\|\s+(.*?)\s+\|\s+(\d*)\s*\|')

        for line in lines:
            match = pat_drc_row.search(line)
            if match:
                result['violations'].append({
                    'id': match.group(1),
                    'severity': match.group(2),
                    'description': match.group(3).strip(),
                    'count': int(match.group(4)) if match.group(4) else 1
                })

        return result
