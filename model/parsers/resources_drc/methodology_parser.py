"""
Methodology.rpt 리포트 파서

이 모듈은 Methodology.rpt 파일을 읽어서 Q22(RAM 충돌), Q29(설계 이상) 분석에 쓰이는
설계 방법론 위반 사항(Critical Warning, Warning) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계 규칙(DRC/Methodology) 위반 여부를 확인하여 잠재적 오작동 위험 식별

## WHAT
* Methodology 관련 위반 ID, 심각도, 발생 횟수 정보 추출

## HOW
* BaseParser를 상속받아 요약 및 상세 위반 리스트 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class MethodologyParser(BaseParser):
    """ Methodology.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Methodology.rpt 파일 파싱 후 데이터 반환

        Logic:
            - 위반 요약 테이블에서 ID별 Criticality 및 Count 추출

        Args:
            file_path: Methodology.rpt 절대경로

        Returns:
            Dict[str, Any]: 방법론 위반 통계
        """
        result: Dict[str, List[Dict[str, Any]]] = {'violations': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 위반 행 패턴: | Rule | Severity | Description | Count |
        pat_method_row = self.get_pattern('method_row', r'\|\s+([\w-]+)\s+\|\s+(\w+)\s+\|\s+(.*?)\s+\|\s+(\d+)\s+\|')

        for line in lines:
            match = pat_method_row.search(line)
            if match:
                result['violations'].append({
                    'id': match.group(1),
                    'severity': match.group(2),
                    'description': match.group(3).strip(),
                    'count': int(match.group(4))
                })

        return result
