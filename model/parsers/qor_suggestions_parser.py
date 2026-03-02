"""
QoR_Suggestions.rpt 리포트 파서

이 모듈은 QoR_Suggestions.rpt 파일을 읽어서 Q15 분석에 쓰이는
Vivado의 자동화된 설계 품질 개선 제안 사항들을 추출합니다.

Attributes:
    없음

## WHY
* 타이밍 충족을 위해 툴이 제안한 최적화 방안의 유무 및 내용 파악

## WHAT
* 제안된 Suggestion의 개수 및 핵심 메시지 추출

## HOW
* BaseParser를 통해 요약 섹션 및 제안 리스트 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class QoRSuggestionsParser(BaseParser):
    """ QoR_Suggestions.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        QoR_Suggestions.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: QoR_Suggestions.rpt 절대경로

        Returns:
            Dict[str, Any]: 제안된 수정 사항 요약
        """
        result: Dict[str, Any] = {'suggestions': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 단순 카운팅 및 리스트 수집
        pat_suggestion_row = self.get_pattern('qor_sugg_row', r'\|\s+(\d+)\s+\|\s+(.*?)\s*\|')

        for line in lines:
            match = pat_suggestion_row.search(line)
            if match:
                result['suggestions'].append({
                    'id': int(match.group(1)),
                    'description': match.group(2).strip()
                })

        result['suggestion_count'] = len(result['suggestions'])
        return result
