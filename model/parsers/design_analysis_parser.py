"""
Design_Analysis.rpt 리포트 파서

이 모듈은 Design_Analysis.rpt 파일을 읽어서 Q55, Q57 분석에 쓰이는
설계 복잡도(Complexity) 및 혼잡도(Congestion) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계의 복잡도 및 배치/라우팅 혼잡도를 분석하여 설계 변경 영향 및 구현 난도를 평가

## WHAT
* 계층별 복잡도(Rent 지수, 인스턴스 수) 및 혼잡도 레벨/위치 정보 추출

## HOW
* BaseParser를 상속받아 Complexity 테이블 및 Congestion 섹션 파싱
"""

from typing import Any, Dict, List
import re
from core.base_parser import BaseParser

class DesignAnalysisParser(BaseParser):
    """ Design_Analysis.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Design_Analysis.rpt 파일 파싱 후 데이터 반환

        Logic:
            - Complexity Characteristics 테이블에서 계층별 Rent 지수 및 인스턴스 수 추출
            - Congestion 섹션에서 혼잡도 레벨 확인

        Args:
            file_path: Design_Analysis.rpt 절대경로

        Returns:
            Dict[str, Any]: 설계 복잡도 및 혼잡도 정보
        """
        result: Dict[str, Any] = {
            'complexity': [],
            'congestion': {
                'placer': 'None',
                'router': 'None'
            }
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 1. Complexity 테이블 패턴: | Hierarchical Name | ... | Rent | ... | Instances |
        pat_complexity = self.get_pattern('da_complexity', r'\|\s*(\S+)\s*\|.*?\|\s*([\d.]+)\s*\|.*?\|\s*(\d+)\s*\|')

        # 2. Congestion 패턴: No congestion windows are found above level 5
        pat_no_congestion = self.get_pattern('da_no_cong', r'No congestion windows are found above level (\d+)')

        # 3. 실제 Congestion 레벨 패턴 (테이블 형태 등)
        pat_placer_cong = self.get_pattern('da_placer_cong', r'Placer Congestion\s*\|\s*Level\s*(\d+)')
        pat_router_cong = self.get_pattern('da_router_cong', r'Router Congestion\s*\|\s*Level\s*(\d+)')

        for line in lines:
            # Complexity 정보 추출
            if match_comp := pat_complexity.search(line):
                # 헤더 제외
                if match_comp.group(1).lower() != 'hierarchical':
                    result['complexity'].append({
                        'name': match_comp.group(1),
                        'rent': float(match_comp.group(2)),
                        'instances': int(match_comp.group(3))
                    })

            # Congestion 정보 추출
            if 'No congestion windows' in line:
                if match_no := pat_no_congestion.search(line):
                    # Level 5 이상 없다는 의미
                    pass

            if match_p := pat_placer_cong.search(line):
                result['congestion']['placer'] = f"Level {match_p.group(1)}"
            if match_r := pat_router_cong.search(line):
                result['congestion']['router'] = f"Level {match_r.group(1)}"

        return result
