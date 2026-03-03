"""
Property_Check.rpt 리포트 파서

이 모듈은 Property_Check.rpt 파일을 읽어서 Q27 분석에 쓰이는
하드 매크로 인스턴스의 물리적 속성(Jitter, Value 등) 데이터를 추출합니다.

Attributes:
    없음

## WHY
* 하드 매크로의 설정 속성이 유효한지 벤더 제약 조건과 비교 검증하기 위함

## WHAT
* 인스턴스/항목별 Property, Type, Value 추출

## HOW
* 블록 단위(Property 시작점) 또는 키워드 매칭을 통해 속성 그룹 수집
"""

from typing import Any, Dict, List, Optional
from core.base_parser import BaseParser

class PropertyCheckParser(BaseParser):
    """ Property_Check.rpt 파일 파싱 클래스 (report_property 결과) """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Property_Check.rpt 파일 파싱 후 속성 데이터 반환

        Args:
            file_path: Property_Check.rpt 절대경로

        Returns:
            Dict[str, Any]: 속성 정보 리스트
        """
        result: Dict[str, List[Dict[str, Any]]] = {'properties': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 패턴: Property | Type | Read-only | Value
        # 또는 단순히 키워드 매칭
        pat_prop = self.get_pattern('prop_line', r'^(\w+)\s+(\w+)\s+(\w+)\s+(.*)')

        current_block: Dict[str, Any] = {}

        for line in lines:
            line = line.strip()
            if not line or line.startswith('Property') or line.startswith('-'):
                continue

            match = pat_prop.search(line)
            if match:
                key = match.group(1).strip()
                val = match.group(4).strip()

                # NAME 속성이 나오면 새로운 블록으로 간주 (또는 기존 블록에 추가)
                if key == "NAME":
                    if current_block:
                        result['properties'].append(current_block)
                    current_block = {'name': val}
                else:
                    current_block[key.lower()] = val

        if current_block:
            result['properties'].append(current_block)

        return result
