"""
PR_PBLOCK_Utilization.rpt 리포트 파서

이 모듈은 PR_PBLOCK_Utilization.rpt 파일을 읽어서 Q11, Q15 분석에 쓰이는
Pblock 별 자원 사용률 데이터를 추출합니다.

Attributes:
    없음

## WHY
* Partial Reconfiguration 환경에서 각 Pblock의 자원 포화도 점검

## WHAT
* Pblock 이름별 자원 사용량 및 퍼센트 수집

## HOW
* BaseParser를 상속받아 테이블 행 데이터 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class PRPBlockUtilizationParser(BaseParser):
    """ PR_PBLOCK_Utilization.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        PR_PBLOCK_Utilization.rpt 파일 파싱 후 Pblock 데이터 반환

        Args:
            file_path: PR_PBLOCK_Utilization.rpt 절대경로

        Returns:
            Dict[str, Any]: Pblock별 사용률 리스트
        """
        result: Dict[str, List[Dict[str, Any]]] = {'pblocks': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_pblock_util = self.get_pattern('pblock_util', r'\|\s*(pblock_\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|')

        for line in lines:
            match = pat_pblock_util.search(line)
            if match:
                result['pblocks'].append({
                    'name': match.group(1),
                    'used': int(match.group(2)),
                    'available': int(match.group(3)),
                    'util_pct': float(match.group(4))
                })

        return result
