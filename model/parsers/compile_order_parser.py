"""
Compile_Order.rpt 리포트 파서

이 모듈은 Compile_Order.rpt 파일을 읽어서 Q01(프로젝트 규모) 분석에 쓰이는
소스 파일 수 및 파일 유형 통계 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 디자인에 포함된 소스 코드의 규모와 구성을 파악하기 위함

## WHAT
* Synthesis/Simulation에 사용된 소스 파일 개수 및 유형별 집계

## HOW
* BaseParser를 상속받아 테이블 형태의 라인 정규식 매칭 수행
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class CompileOrderParser(BaseParser):
    """ Compile_Order.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Compile_Order.rpt 파일 파싱 후 통계 데이터 반환

        Logic:
            - 테이블 행에서 파일 용도(Used In)와 타입(File Type) 추출하여 카운트

        Args:
            file_path: Compile_Order.rpt 절대경로

        Returns:
            Dict[str, Any]: 소스 파일 통계 정보
        """
        result: Dict[str, Any] = {
            'synth_count': 0,
            'sim_count': 0,
            'file_types': {}
        }
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_src = self.get_pattern('src_line', r'^\s*\d+\s+\S+\s+(Synth.*?|Sim)\s+(\w+)\s+')

        for line in lines:
            match = pat_src.search(line)
            if match:
                used_in = match.group(1).upper()
                file_type = match.group(2).upper()

                if 'SYNTH' in used_in:
                    result['synth_count'] += 1
                elif 'SIM' in used_in:
                    result['sim_count'] += 1

                result['file_types'][file_type] = result['file_types'].get(file_type, 0) + 1

        return result
