"""
QoR_Assessment.rpt 리포트 파서

이 모듈은 QoR_Assessment.rpt 파일을 읽어서 Q11, Q12, Q15 분석에 쓰이는
설계 품질 점수(QoR Score) 및 주요 자원/타이밍 임계치 위반 데이터를 추출합니다.

Attributes:
    없음

## WHY
* Vivado가 평가한 전반적인 설계 성숙도 및 수정 권고 사항 파악

## WHAT
* QoR Assessment Score, WNS/WHS/THS 요약, 자원별 가용성 평가 데이터 추출

## HOW
* BaseParser를 통해 품질 점수 요약 및 상세 평가 테이블 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class QoRAssessmentParser(BaseParser):
    """ QoR_Assessment.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        QoR_Assessment.rpt 파일 파싱 후 품질 데이터 반환

        Logic:
            - QoR Assessment Score 문장에서 점수와 설명 추출
            - 세부 평가 테이블에서 각 리소스/타이밍 항목의 Status 추출

        Args:
            file_path: QoR_Assessment.rpt 절대경로

        Returns:
            Dict[str, Any]: QoR 평가 정보
        """
        result: Dict[str, Any] = {'details': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_score = self.get_pattern('qor_score', r'QoR Assessment Score\s*\|\s*(\d+)\s*-\s*(.*?)\s*\|')
        # 테이블 행: | Name | Threshold | Actual | Used | Available | Status |
        pat_qor_row = self.get_pattern('qor_row', r'\|\s+([\w\s]+?)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|')

        for line in lines:
            if match := pat_score.search(line):
                result['score'] = int(match.group(1))
                result['score_description'] = match.group(2).strip()

            match_row = pat_qor_row.search(line)
            if match_row:
                result['details'].append({
                    'name': match_row.group(1).strip(),
                    'threshold': float(match_row.group(2)),
                    'actual': float(match_row.group(3)),
                    'used': int(match_row.group(4)),
                    'available': int(match_row.group(5)),
                    'status': match_row.group(6)
                })

        return result
