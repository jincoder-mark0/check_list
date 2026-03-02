"""
CDC_Unsafe.rpt 리포트 파서

이 모듈은 CDC_Unsafe.rpt 파일을 읽어서 Q39, Q40 분석에 쓰이는
안전하지 않은(Unsafe) 클럭 도메인 교차 경로 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 동기화 회로가 결여되었거나 부적절하여 메타스테이빌리티 위험이 큰 경로 식별

## WHAT
* Unsafe 판정을 받은 CDC 경로의 소스/데스티네이션 및 위반 유형 추출

## HOW
* BaseParser를 상속받아 Unsafe 섹션 및 상세 경로 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class CDCUnsafeParser(BaseParser):
    """ CDC_Unsafe.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        CDC_Unsafe.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: CDC_Unsafe.rpt 절대경로

        Returns:
            Dict[str, Any]: Unsafe CDC 경로 통계 및 리스트
        """
        result: Dict[str, Any] = {'unsafe_paths': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_unsafe_row = self.get_pattern('cdc_unsafe_row', r'\|\s*(Unsafe)\s*\|\s*(CDC-\d+)\s*\|\s*(\d+)\s*\|')

        for line in lines:
            match = pat_unsafe_row.search(line)
            if match:
                result['unsafe_paths'].append({
                    'id': match.group(2),
                    'severity': match.group(1),
                    'count': int(match.group(3))
                })

        return result
