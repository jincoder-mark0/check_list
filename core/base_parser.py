"""
데이터 파서를 위한 기본(Base) 추상 구조 및 공통 파싱 로직

파일 입출력, 반복되는 텍스트 및 정규식 치환 등 파싱 중 빈번하게 일어나는
공통적인 연산을 한 곳에 모아 후손 파서의 코드 중복 방지

Attributes:
    없음

## WHY
* 여러 파서 간 동일한 파일 오픈, 라인 순회, 정규식 객체 검사 코드 중복 제거
* 텍스트 클리닝 등 모든 리포트에 필요한 사전 처리의 일관성 확보

## WHAT
* 정규표현식 지원 유틸리티 메서드 제공
* 텍스트 블록 추출 등의 헬퍼 목적 베이스 클래스 구현

## HOW
* 파이썬 내장 `re` 모듈 활용 및 객체 지향 방식 상속 구조 도입
* 오버라이딩을 위한 인터페이스 함수 및 프로퍼티 활용
"""

import re
import os
from typing import List, Optional, Pattern, Dict

class BaseParser:
    """
    각 영역별 파서(Parser)의 부모가 되는 핵심 공통 베이스 클래스.

    타겟 리포트의 파일 읽기, 정규식 컴파일 보관, 블록 단위 데이터 추출 등
    파생 파서가 즉시 사용 가능한 표준 툴킷. (추상 구조)

    Attributes:
        _compiled_patterns (Dict[str, Pattern]): 모듈에서 반복 호출되는 정규식 자원 캐싱 저장소
    """

    def __init__(self) -> None:
        self._compiled_patterns: Dict[str, Pattern] = {}

    def get_pattern(self, name: str, regex_str: str) -> Pattern:
        """
        정규표현식 문자열 캐싱 및 컴파일된 객체 반환 함수.

        매칭 연산 속도 향상을 위해 한 번 사용된 정규식을 컴파일하여 보관.

        Logic:
            - 캐시 내부 확인
            - 미존재 시 정규식 컴파일 후 딕셔너리 적재

        Args:
            name: 캐시에 저장될 정규표현식 식별용 임의 문자열 키.
            regex_str: 대상 탐색에 쓰일 정규표현식 원시 문자열.

        Returns:
            Pattern: 컴파일 된(re.compile) 파이썬 정규식 객체.

        Examples:
            >>> parser = BaseParser()
            >>> p = parser.get_pattern("date", r"^\d{4}-\d{2}-\d{2}")
        """
        if name not in self._compiled_patterns:
            # ---------------------------------------------------------
            # 매번 re.compile()을 호출하지 않기 위한 최적화 영역 (인라인 주석)
            # ---------------------------------------------------------
            self._compiled_patterns[name] = re.compile(regex_str, re.IGNORECASE)
        return self._compiled_patterns[name]

    def read_file_lines(self, filepath: str) -> List[str]:
        """
        대상 파일을 읽고, 텍스트 라인 리스트 반환 처리.

        Args:
            filepath: 대상 타겟 파일의 시스템 절대경로 문자열.

        Returns:
            List[str]: 개행 문자가 보존된 혹은 전처리된 각 라인의 문자열 결합본 리스트.
                파일 열기 실패 시 빈 리스트 반환.
        """
        # 파일 존재 검증 분기
        if not os.path.isfile(filepath):
            return []

        try:
            # 텍스트 파일 읽기 및 강제 인코딩 치환 (오류 문자열 회피)
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                return f.readlines()
        except IOError:
            return []

    def read_file_content(self, filepath: str) -> str:
        """
        대상 파일을 읽고, 텍스트 전체를 문자열로 반환 처리.

        Args:
            filepath: 대상 타겟 파일의 시스템 절대경로 문자열.

        Returns:
            str: 파일 전체 내용. 파일 열기 실패 시 빈 문자열 반환.
        """
        if not os.path.isfile(filepath):
            return ""

        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except IOError:
            return ""

    def extract_value_by_regex(self, line: str, pattern: Pattern) -> Optional[str]:
        """
        정해진 정규표현식에 부합하는 라인에서 그룹핑 단절 텍스트 단건 추출.

        Args:
            line: 대상 단일 텍스트 문자열.
            pattern: 이미 컴파일 완료된 정규식 구조체 객체.

        Returns:
            Optional[str]: 파싱 결과 첫 번째 그룹 텍스트. 발견 실패 시 None 반환.
        """
        match = pattern.search(line)
        if match and match.groups():
            # 보통 단일 값 추출 시 첫 번째 group(1)을 밸류로 본다 (strip 적용)
            return match.group(1).strip()
        return None
