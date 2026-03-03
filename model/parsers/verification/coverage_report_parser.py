"""
Coverage_Report 리포트 파서

이 모듈은 시뮬레이션 커버리지 리포트(html 또는 txt)를 읽어서 Q55, Q58, Q60 분석에 쓰이는
테스트 커버리지 수치 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 설계의 기능 검증이 얼마나 충분히 수행되었는지 정량적으로 평가

## WHAT
* Statement(Line), Branch, Condition, Toggle, FSM 커버리지 수치(%) 추출

## HOW
* BaseParser를 상속받아 일반적인 텍스트 형식의 커버리지 요약 행 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class CoverageReportParser(BaseParser):
    """ Coverage_Report (.txt/.html) 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Coverage 리포트 파일 파싱 후 커버리지 데이터 반환

        Args:
            file_path: Coverage_Report 절대경로

        Returns:
            Dict[str, Any]: 커버리지 항목별 수치
        """
        result: Dict[str, Any] = {
            'scores': {}
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 커버리지 요약 패턴 (일반적인 시뮬레이션 툴 형식 가정)
        # 예: Statement Coverage: 85.5%
        #     Line Coverage: 90.0
        patterns = {
            'statement': self.get_pattern('cv_stmt', r'(?i)(Statement|Line)\s+(?:Coverage|Score)\s*:?\s*([\d.]+)'),
            'branch': self.get_pattern('cv_branch', r'(?i)Branch\s+(?:Coverage|Score)\s*:?\s*([\d.]+)'),
            'condition': self.get_pattern('cv_cond', r'(?i)Condition\s+(?:Coverage|Score)\s*:?\s*([\d.]+)'),
            'toggle': self.get_pattern('cv_toggle', r'(?i)Toggle\s+(?:Coverage|Score)\s*:?\s*([\d.]+)'),
            'fsm': self.get_pattern('cv_fsm', r'(?i)FSM\s+(?:Coverage|Score)\s*:?\s*([\d.]+)')
        }

        for line in lines:
            for key, pat in patterns.items():
                match = pat.search(line)
                if match:
                    result['scores'][key] = float(match.group(2))

        return result
