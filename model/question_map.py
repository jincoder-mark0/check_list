"""
질문 번호와 대상 리포트 간 매핑 체계 모델링 모듈

분석할 질문 번호(Q01~Q69)가 어떠한 리포트 파일을 입력으로 필요로 하는지
매핑 정보를 제공하며, 필요에 따라 비즈니스 매핑 분기 로직 지원.

Attributes:
    QUESTION_REPORT_MAP: 질문 번호를 키, 대상 리포트 타입 집합을 값으로 갖는 전역 변수

## WHY
* 하드코딩된 조건문 배제 및 유연한 맵핑 룰 확장성 확보 목적
* 리포트 파일 종류 추가 및 질문 개정 시 단일 지점(SPoF) 구조에서의 관리 편의성

## WHAT
* 체크리스트 대상 각 문항과 연관된 리포트 카테고리의 관계 사전 정의
* 분기 규칙 및 조회 기능을 하는 메서드 지원

## HOW
* 파이썬 정적 딕셔너리로 기본 맵핑 테이블 구현
* 데이터 조회 속도를 위해 해시 테이블 구조인 딕셔너리 및 Set 사용
"""

from typing import Dict, Set

# ---------------------------------------------------------------------
# 1. 1차 매핑 테이블 정의 구역
# ---------------------------------------------------------------------
# 분석 대상 파일 매핑용 딕셔너리
# 각 키는 "Q" + 번호 문자열, 값은 해당 문항이 참조하는 리포트 확장자나 종류를 의미
# TODO: 실제 파싱 계획서에 맞춰 정확한 리포트 키워드로 갱신 필요
QUESTION_REPORT_MAP: Dict[str, Set[str]] = {
    # -------------------------------------------------------------------------
    # Q01 ~ Q10: 프로젝트 관리 및 툴 버전
    # -------------------------------------------------------------------------
    "Q01": {"Compile_Order", "IP_Status", "Environment"},
    "Q02": set(), "Q03": set(), "Q04": set(),  # EVIDENCE
    "Q05": {"Environment"},
    "Q06": set(), "Q07": set(),                # EVIDENCE
    "Q08": {"Environment", "Config_Impl"},
    "Q09": {"Environment", "IP_Status"},
    "Q10": {"IP_Status"},

    # -------------------------------------------------------------------------
    # Q11 ~ Q20: 자원 및 기본 성능
    # -------------------------------------------------------------------------
    "Q11": {"Utilization", "Clock_Utilization", "Control_Sets", "IO_Report", "QoR_Assessment", "PR_NA_Evidence", "PR_DFX_Detection", "PR_PBLOCK_Utilization"},
    "Q12": {"Timing_Summary", "Setup_Critical", "Hold_Critical", "QoR_Assessment", "Datasheet", "Check_Timing"},
    "Q13": {"Power_Report", "Power_Data", "Power_Opt", "Operating_Cond"},
    "Q14": {"Power_Report", "Power_Data", "Switching_Activity"},
    "Q15": {"QoR_Assessment", "QoR_Suggestions", "Pipeline_Analysis", "High_Fanout", "PR_NA_Evidence", "PR_DFX_Detection", "PR_PBLOCK_Utilization"},
    "Q16": set(), "Q17": set(),                # EVIDENCE
    "Q18": {"Debug_Core", "Partial_Bit_Config_Summary"},
    "Q19": {"IO_Report", "Datasheet", "Utilization"},
    "Q20": {"Utilization", "Power_Report"},

    # -------------------------------------------------------------------------
    # Q21 ~ Q30: 메모리 및 외부 인터페이스
    # -------------------------------------------------------------------------
    "Q21": {"RAM_Utilization", "IO_Report"},
    "Q22": {"RAM_Utilization", "Methodology"},
    "Q23": set(),                              # EVIDENCE
    "Q24": {"Datasheet", "IO_Report"},
    "Q25": {"Power_Report", "Power_Data", "Datasheet", "Operating_Cond", "CDC_Report"},
    "Q26": {"PR_NA_Evidence", "PR_DFX_Detection", "PR_Verify_Report", "Partial_Bit_Config_Summary"},
    "Q27": {"Clocks_Summary", "Property_Check", "PR_NA_Evidence", "PR_DFX_Detection", "PR_DRC_Report"},
    "Q28": {"Config_Impl", "Partial_Bit_Config_Summary", "PR_DFX_Detection", "IO_Report"},
    "Q29": {"Waiver", "CDC_Report", "DRC_Report"},
    "Q30": {"IO_Report"},

    # -------------------------------------------------------------------------
    # Q31 ~ Q40: 리셋 및 클럭 안전성 (CDC 포함)
    # -------------------------------------------------------------------------
    "Q31": {"Property_Check", "Clock_Utilization"},
    "Q32": {"Clock_Networks", "Check_Timing"},
    "Q33": {"CDC_Report", "Clock_Networks"},
    "Q34": {"Check_Timing", "Clock_Utilization"},
    "Q35": {"Check_Timing", "Pulse_Width"},
    "Q36": {"CDC_Report"},
    "Q37": {"Clock_Utilization", "Clock_Networks", "Timing_Exceptions"},
    "Q38": {"Bus_Skew", "Timing_Exceptions"},
    "Q39": {"CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q40": {"CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},

    # -------------------------------------------------------------------------
    # Q41 ~ Q50: 상세 설계 및 버스 인터페이스
    # -------------------------------------------------------------------------
    "Q41": {"Clock_Networks", "CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q42": {"CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q43": {"CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q44": {"Bus_Skew", "CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q45": {"Pulse_Width", "Clock_Utilization"},
    "Q46": {"RAM_Utilization", "Check_Timing"},
    "Q47": {"RAM_Utilization", "CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q48": {"RAM_Utilization", "IP_Status"},
    "Q49": {"Debug_Core"},
    "Q50": {"Debug_Core", "DRC_Report"},

    # -------------------------------------------------------------------------
    # Q51 ~ Q60: 보호 기능 및 검증 (커버리지)
    # -------------------------------------------------------------------------
    "Q51": {"Debug_Core", "Methodology"},
    "Q52": {"SSN_Report", "IO_Report"},
    "Q53": {"SSN_Report", "Property_Check"},
    "Q54": {"IP_Status"},                              # EVIDENCE (IP 기반 벤더 가이드 생성)
    "Q55": {"Design_Analysis", "DRC_Report", "Methodology", "Coverage_Report"},
    "Q56": {"Coverage_Report"},
    "Q57": {"Design_Analysis", "Methodology"},
    "Q58": {"Coverage_Report", "Waiver", "DRC_Report", "Methodology"},
    "Q59": {"SSN_Report", "Waiver", "Methodology", "CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q60": {"CDC_Report", "SSN_Report", "Waiver", "Methodology", "Coverage_Report"},

    # -------------------------------------------------------------------------
    # Q61 ~ Q69: 최종 구현 로그 및 툴 품질
    # -------------------------------------------------------------------------
    "Q61": {"Timing_Summary", "CDC_Report", "CDC_Critical", "CDC_Interaction", "Timing_Exceptions"},
    "Q62": {"Pulse_Width", "Clocks_Summary", "Property_Check", "Timing_Summary", "Check_Timing"},
    "Q63": {"Timing_Summary", "Setup_Critical", "Hold_Critical"},
    "Q64": {"Timing_Summary", "Setup_Critical", "Hold_Critical", "Bus_Skew"},
    "Q65": {"Setup_Critical", "Hold_Critical", "Bus_Skew", "Timing_Summary", "Timing_Exceptions"},
    "Q66": {"Check_Timing", "Methodology", "DRC_Report"},
    "Q67": {"Check_Timing", "Methodology", "DRC_Report"},
    "Q68": {"Check_Timing", "Methodology", "Waiver", "Timing_Exceptions"},
    "Q69": {"Environment", "IP_Status"},
}


def get_required_reports(question_id: str) -> Set[str]:
    """
    특정 질문 번호를 위해 파싱해야 할 리포트 타입 집합 조회

    해당 질문이 분석을 위해 어떠한 부류의 리포트를 필요로 하는지 반환.

    Logic:
        - 맵핑 테이블에서 질문 ID를 조회하여 관련 리포트 Set 반환
        - 테이블에 일치하는 질문이 없을 경우 빈 Set 반환하여 예외 우회

    Args:
        question_id: 조회할 대상 질문 식별자 (예: "Q01")

    Returns:
        Set[str]: 파싱해야 할 대상 리포트 카테고리 또는 이름 집합. 미존재 시 빈 Set 반환.

    Examples:
        >>> get_required_reports("Q41")
        {'utilization'}
    """
    if question_id in QUESTION_REPORT_MAP:
        # 정상 등록된 문항이어서 맵핑된 결과 리턴
        return QUESTION_REPORT_MAP[question_id]

    # 알 수 없는 문항 또는 수동 점검 항목 처리 분기
    # 빈 집합을 반환해 후속 파서가 작동을 건너뛰게끔 비즈니스 로직 유도
    return set()
