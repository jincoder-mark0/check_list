"""
CDC_Critical.rpt 리포트 파서

이 모듈은 CDC_Critical.rpt 파일을 읽어서 Q39 분석에 쓰이는
심각한(Critical) 클럭 도메인 교차 위반 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계에서 즉각적인 수정이 필요한 고위험 CDC 결함 집중 파악

## WHAT
* Critical 등급의 CDC 위반 항목 및 건수 추출

## HOW
* BaseParser를 상속받아 위반 상세 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class CDCCriticalParser(BaseParser):
    """ CDC_Critical.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        CDC_Critical.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: CDC_Critical.rpt 절대경로

        Returns:
            Dict[str, Any]: 심각 위반 항목 리스트
        """
        result: Dict[str, List[Dict[str, Any]]] = {'critical_violations': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_crit = self.get_pattern('cdc_crit_row', r'\|\s*(Critical|Warning)\s*\|\s*(CDC-\d+)\s*\|\s*(\d+)\s*\|')

        for line in lines:
            match = pat_crit.search(line)
            if match:
                result['critical_violations'].append({
                    'id': match.group(2),
                    'severity': match.group(1),
                    'count': int(match.group(3))
                })

        return result
