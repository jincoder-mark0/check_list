"""
CDC_Interaction.rpt 리포트 파서

이 모듈은 CDC_Interaction.rpt 파일을 읽어서 Q39, Q40 분석에 쓰이는
클럭 도메인 간 상호작용(Interaction) 및 결합 매트릭스 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계 내 모든 클럭 도메인 쌍 간의 결합 관계 및 타이밍 제약 적용 상태 파악

## WHAT
* 클럭 도메인 쌍, 경로 존재 여부, 적용된 제약(Timed/Ignored) 추출

## HOW
* BaseParser를 통해 도메인 매트릭스 또는 요약 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class CDCInteractionParser(BaseParser):
    """ CDC_Interaction.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        CDC_Interaction.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: CDC_Interaction.rpt 절대경로

        Returns:
            Dict[str, Any]: 클럭 도메인 간 결합 정보 요약
        """
        result: Dict[str, List[Dict[str, Any]]] = {'interactions': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 도메인 간 상호작용 패턴: | Source Clock | Destination Clock | Status | Paths |
        pat_inter = self.get_pattern('cdc_inter', r'\|\s+(\S+)\s+\|\s+(\S+)\s+\|\s+(\w+)\s+\|\s+(\d+)\s+\|')

        for line in lines:
            match = pat_inter.search(line)
            if match:
                result['interactions'].append({
                    'src_clk': match.group(1),
                    'dst_clk': match.group(2),
                    'status': match.group(3),
                    'path_count': int(match.group(4))
                })

        return result
