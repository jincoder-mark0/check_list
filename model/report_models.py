"""
파싱 데이터 및 판정 결과 응답용 모델

FPGA 리포트 파싱 결과와 판정 정보를 담는 데이터 구조를 정의.
각 문항(Q01~Q69)에 대한 결과 객체를 표준화하여 취합 및 출력 시 일관성 유지 목적.

Attributes:
    없음

## WHY
* 파싱된 원시 데이터와 판정 결과(PASS/FAIL/WARNING/REVIEW)를 체계적으로 관리
* 딕셔너리 하드코딩 사용을 피하고 정형화된 모델 객체를 통해 타입 안정성 확보

## WHAT
* `ParseResult`: 단일 문항 파싱 결과 데이터 구조 클래스 작성
* `ReportSummary`: 전체 보고서 단위의 결과를 담는 구조 클래스 작성

## HOW
* 파이썬 내장 `dataclasses` 모듈을 사용하여 데이터 홀더 객체 구현
* 타입 힌팅(Type Hinting)을 통한 객체 필드 명시
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ParseResult:
    """
    단일 체크리스트 문항에 대한 파싱 및 판정 결과 클래스.

    특정 문항(예: Q01)의 기준값, 추출값, 판정 상태, 사용된 증빙 파일 목록 등 캡슐화.

    Attributes:
        question_id: 대상 질문 번호 속성 (예: "Q01")
        status: 최종 판정 상태를 나타내는 문자열 ("PASS", "FAIL", "WARNING", "REVIEW")
        extracted_data: 리포트 내에서 파싱/추출된 하위 로우 데이터 딕셔너리
        evidence_files: 해당 판정을 도출하기 위해 사용된 타겟 리포트 경로 또는 파일명 리스트
        reason: 판정의 기준 사유 혹은 부가적인 메시지
    """
    question_id: str
    status: str
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    evidence_files: List[str] = field(default_factory=list)
    reason: Optional[str] = None


@dataclass
class ReportSummary:
    """
    리포트 전체 문항 파싱 종료 후 생성되는 최종 집계/요약 데이터 모델.

    여러 개의 `ParseResult` 객체를 리스트로 묶어 프로젝트 메타데이터와 전체 달성 현황을 관리.

    Attributes:
        project_name: 파싱 대상인 프로젝트/디자인 이름
        total_questions: 점검 대상이 된 총 파싱 문항 개수
        results: 개별 문항(`ParseResult`) 인스턴스를 담는 리스트 보관 필드
    """
    project_name: str
    total_questions: int = 0
    results: List[ParseResult] = field(default_factory=list)

    def add_result(self, result: ParseResult) -> None:
        """
        단일 문항 파싱 완료 결과를 요약 객체 컬렉션에 추가 삽입.

        Args:
            result: 개별 문항에 대한 파싱 및 판정 정보가 담긴 `ParseResult` 인스턴스.
        """
        self.results.append(result)
        self.total_questions += 1
