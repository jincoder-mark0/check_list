"""
Partial_Bit_Config_Summary.rpt 리포트 파서

이 모듈은 Partial_Bit_Config_Summary.rpt 파일을 읽어서 Q18 분석에 쓰이는
부분 재구성(PR) 비트스트림의 설정 요약 및 보안 관련 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 부분 재구성 로직의 설정 유효성 및 디버그 보호 지침 준수 여부 확인

## WHAT
* PR 관련 비트스트림 구성 요약 정보 추출

## HOW
* BaseParser를 이용해 설정 요약 섹션 매칭 수행
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class PartialBitConfigParser(BaseParser):
    """ Partial_Bit_Config_Summary.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Partial_Bit_Config_Summary.rpt 파일 파싱 후 요약 정보 반환

        Args:
            file_path: Partial_Bit_Config_Summary.rpt 절대경로

        Returns:
            Dict[str, Any]: 비트스트림 설정 데이터
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 비트스트림 설정 관련 핵심 키워드 탐색 (예시)
        pat_config = self.get_pattern('pr_cfg', r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|')

        for line in lines:
            match = pat_config.search(line)
            if match:
                key = match.group(1).strip().lower().replace(' ', '_')
                result[key] = match.group(2).strip()

        return result
