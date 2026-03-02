"""
FPGA 리포트 파일 동적 탐색 및 매핑

주어진 디렉토리에서 재귀적으로 `.rpt` 및 `.txt` 형식의 FPGA 리포트 파일을 탐색하여,
파일명 기반 키(소문자)와 해당 파일의 절대 경로를 연결하는 딕셔너리 반환

Attributes:
    VALID_EXTENSIONS: 허용되는 리포트 파일 확장자 집합

## WHY
* 하드코딩 경로 대신 동적인 파일 탐색을 통한 다양한 빌드 환경 지원
* 하위 폴더 깊이에 제약 없이 전체 타겟 리포트를 동시 취합 목적

## WHAT
* `.rpt`, `.txt` 확장자를 가진 파일 필터링 수행
* `report_name(소문자)` 키와 `절대 경로` 값을 매핑한 테이블 구성 및 제공

## HOW
* 내장 모듈 `os.walk`를 통한 디렉토리 트리 순회
* `os.path`를 활용해 경로 조합 및 파일 파싱
"""

import os
from typing import Dict

VALID_EXTENSIONS = {'.rpt', '.txt'}

def find_reports(report_dir: str) -> Dict[str, str]:
    """
    디렉토리 경로 내 리포트 파일 재귀적 검색 수행

    검색된 파일의 이름(소문자, 확장자 제외)을 키로, 절대경로를 값으로 담아 딕셔너리 반환

    Logic:
        - os.walk()를 사용하여 `report_dir` 하위 디렉토리 순차 진입
        - 추출된 파일의 확장자를 소문자로 변환해 유효 확장자 확인
        - 확장자 제외된 파일명(소문자화)을 딕셔너리 조회 키로 사용
        - os.path.normpath() 기반 절대경로 반환

    Args:
        report_dir: 탐색의 기준점이 되는 시작 디렉토리 절대 혹은 상대 경로

    Returns:
        Dict[str, str]: 소문자 파일명을 키로 하고, 해당 파일 절대경로를 값으로 갖는 딕셔너리.
            검색 결과가 없으면 빈 딕셔너리(`{}`) 반환.

    Raises:
        FileNotFoundError: 운영체제 파일 권한 문제 또는 삭제된 결손 디렉토리 접근 시 발생 가능

    Examples:
        >>> path = "C:/my_project/reports"
        >>> reports = find_reports(path)
        >>> print(reports.get("timing_summary"))
        'C:\my_project\reports\timing_summary.rpt'
    """
    report_dict: Dict[str, str] = {}

    if not os.path.isdir(report_dir):
        print(f"Warning: The directory '{report_dir}' does not exist or is not a directory.")
        return report_dict

    for root, _, files in os.walk(report_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS:
                name_key = os.path.splitext(file)[0].lower()
                report_dict[name_key] = os.path.normpath(os.path.join(root, file))

    return report_dict
