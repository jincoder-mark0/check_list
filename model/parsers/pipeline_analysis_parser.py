"""
Pipeline_Analysis.rpt 리포트 파서

이 모듈은 Pipeline_Analysis.rpt 파일을 읽어서 Q15 분석에 쓰이는
설계 내 파이프라이닝 최적화 제안 경로 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 타이밍 병목이 발생하는 긴 조합 회로에 대해 파이프라이닝 적용 필요성 검토

## WHAT
* 파이프라이닝 제안 경로 수 추출

## HOW
* BaseParser를 통해 요약 문구 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PipelineAnalysisParser(BaseParser):
    """ Pipeline_Analysis.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Pipeline_Analysis.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: Pipeline_Analysis.rpt 절대경로

        Returns:
            Dict[str, Any]: 파이프라이닝 제안 분석 결과
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_pipeline = self.get_pattern('pipe_sugg', r'Number of paths suggested for pipelining\s*\|\s*(\d+)')

        for line in lines:
            if val := self.extract_value_by_regex(line, pat_pipeline):
                result['suggested_pipeline_paths'] = int(val)
                break

        return result
