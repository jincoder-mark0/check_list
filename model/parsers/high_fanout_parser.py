"""
High_Fanout.rpt 리포트 파서

이 모듈은 High_Fanout.rpt 파일을 읽어서 Q15 분석에 쓰이는
설계 내 High Fanout 네트(Net)들의 개수 및 위험 요소 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 과도한 Fanout을 갖는 네트가 타이밍 클로저 및 배선 혼잡에 미치는 영향 확인

## WHAT
* 특정 임계치(예: 10000) 이상의 Fanout 네트 개수 추출

## HOW
* BaseParser를 통해 요약 메시지 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class HighFanoutParser(BaseParser):
    """ High_Fanout.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        High_Fanout.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: High_Fanout.rpt 절대경로

        Returns:
            Dict[str, Any]: High Fanout 네트 통계
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_high_fanout = self.get_pattern('hf_nets', r'Fanout\s*>\s*10000\s*(:)?\s*(\d+) nets')

        for line in lines:
            match = pat_high_fanout.search(line)
            if match:
                # ':'가 있을 수도 없을 수도 있으므로 그룹 인덱스 유의
                val = match.group(2)
                result['high_fanout_nets_over_10k'] = int(val)
                break

        return result
