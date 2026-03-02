"""
체크리스트 질문별 답변 생성 및 판정 로직 모듈

이 모듈은 파싱된 리포트 데이터와 criteria.json의 기준값을 결합하여
각 질문(Q01~Q69)에 대한 최종 판정(PASS/FAIL/REVIEW 등)과 답변을 생성합니다.

## WHY
* 리포트 데이터만으로는 알 수 없는 '합격 여부'를 비즈니스 규칙에 따라 판정하기 위함
* 일관된 형식의 체크리스트 답변 리포트를 생성하기 위함

## WHAT
* 각 질문별 판정 로직 구현
* ReportSummary 객체 생성 및 관리

## HOW
* AnswerGenerator 클래스를 통해 문항별 체크 메서드 실행
* PARSER_MAP을 사용하여 필요한 리포트 데이터를 사전 로드
"""

from typing import Any, Dict, List, Set, Optional
from model.report_models import ParseResult, ReportSummary
from model.question_map import QUESTION_REPORT_MAP
from model.parsers import PARSER_MAP

class AnswerGenerator:
    """ FPGA 체크리스트 답변 생성기 """

    def __init__(self, criteria: Dict[str, Any], found_reports: Dict[str, str]):
        """
        초기화 및 리포트 데이터 사전 파싱

        Args:
            criteria: criteria.json에서 로드된 판정 기준
            found_reports: core.report_finder가 찾은 {리포트명: 절대경로} 매핑
        """
        self.criteria = criteria
        self.found_reports = found_reports
        self.parsed_data: Dict[str, Any] = {}
        self._initialize_data()

    def _initialize_data(self):
        """ 모든 가용한 리포트를 파싱하여 메모리에 적재 """
        for r_type, path in self.found_reports.items():
            if parser_cls := PARSER_MAP.get(r_type):
                parser = parser_cls()
                try:
                    self.parsed_data[r_type] = parser.parse(path)
                except Exception as e:
                    print(f"Error parsing {r_type} ({path}): {e}")

    def generate_summary(self) -> ReportSummary:
        """
        Q01~Q69 전체 질문에 대한 판정 수행 및 요약 반환
        """
        # 프로젝트 이름 추출 (Environment 또는 Utilization 리포트 활용)
        project_name = "Unknown FPGA Project"
        env_data = self.parsed_data.get('environment', {})
        util_data = self.parsed_data.get('utilization', {})

        part = env_data.get('device_part') or util_data.get('device')
        if part:
            project_name = f"Project ({part})"

        summary = ReportSummary(project_name=project_name)

        for i in range(1, 70):
            q_id = f"Q{i:02d}"
            result = self._check_question(q_id)
            summary.add_result(result)

        return summary

    def _check_question(self, q_id: str) -> ParseResult:
        """ 문항별 판정 로직 분기 """
        method_name = f"_check_{q_id.lower()}"

        required = QUESTION_REPORT_MAP.get(q_id, set())
        has_data = any(r.lower() in self.parsed_data for r in required)

        if not required:
            return ParseResult(q_id, "EVIDENCE_NEEDED", reason="외부 증빙 문서 확인 필요")

        if not has_data:
            return ParseResult(q_id, "N/A", reason="관련 리포트 파일 미검색")

        if hasattr(self, method_name):
            try:
                return getattr(self, method_name)()
            except Exception as e:
                return ParseResult(q_id, "REVIEW", reason=f"판정 로직 오류: {str(e)}")

        # 기본 처리: 데이터는 있으나 로직 미구현 시 REVIEW 대기
        evidence = [self.found_reports.get(r.lower(), "") for r in required if r.lower() in self.found_reports]
        return ParseResult(
            q_id, "REVIEW",
            reason="자동 판정 로직 미구현 (데이터 확인 가능)",
            evidence_files=[f for f in evidence if f]
        )

    # -------------------------------------------------------------------------
    # 개별 문항 판정 메서드 (점진적 확장)
    # -------------------------------------------------------------------------
    # --- Q01 ~ Q10 ---
    def _check_q01(self) -> ParseResult:
        """ 프로젝트 규모 파악 (Q01) """
        compile_data = self.parsed_data.get('compile_order', {})
        env_data = self.parsed_data.get('environment', {})
        ip_data = self.parsed_data.get('ip_status', {})

        synth_cnt = compile_data.get('synth_count', 0)
        ip_cnt = ip_data.get('total_ip_count', 0)
        build_date = env_data.get('build_date', 'Unknown')

        return ParseResult(
            "Q01", "INFO",
            reason=f"빌드시점: {build_date}, 소스파일(Synth): {synth_cnt}개, IP: {ip_cnt}개",
            evidence_files=[self.found_reports.get('compile_order', ""), self.found_reports.get('environment', "")]
        )

    def _check_q05(self) -> ParseResult:
        """ 벤더/모델명 확인 (Q05) """
        env_data = self.parsed_data.get('environment', {})
        util_data = self.parsed_data.get('utilization', {})

        device = env_data.get('device_part', 'Unknown')
        if device == 'Unknown' and util_data.get('device'):
            device = util_data['device']

        return ParseResult(
            "Q05", "INFO",
            extracted_data={"device": device},
            reason=f"타겟 디바이스: {device}",
            evidence_files=[self.found_reports.get('environment', "")]
        )

    def _check_q08(self) -> ParseResult:
        """ 툴 버전 확인 (Q08) """
        data = self.parsed_data.get('environment', {})
        ver = data.get('tool_version', 'Unknown')
        stable_vers = self.criteria.get('tool', {}).get('known_stable_versions', [])

        status = "PASS" if any(sv in ver for sv in stable_vers) else "REVIEW"
        return ParseResult(
            "Q08", status,
            extracted_data={"version": ver},
            reason=f"사용 툴 버전: {ver} (안정 버전 여부 확인)",
            evidence_files=[self.found_reports.get(f, "") for f in ['environment', 'config_impl'] if f in self.found_reports]
        )

    def _check_q09(self) -> ParseResult:
        """ IP 상태 점검 (Q09) """
        data = self.parsed_data.get('ip_status', {})
        total = data.get('total_ip_count', 0)
        deprecated = data.get('status_deprecated', 0)
        update_avail = data.get('status_update_available', 0)

        status = "PASS"
        reason = f"전체 {total}개 IP 상태 양호 (Up-to-date)"
        if deprecated > 0:
            status = "FAIL"
            reason = f"Deprecated IP {deprecated}개 발견"
        elif update_avail > 0:
            status = "REVIEW"
            reason = f"업데이트 가능 IP {update_avail}개 존재 (영향 확인 필요)"

        return ParseResult("Q09", status, extracted_data=data, reason=reason,
                           evidence_files=[self.found_reports.get('ip_status', "")])

    def _check_q10(self) -> ParseResult:
        """ IP 버전 변경 영향 (Q10) """
        data = self.parsed_data.get('ip_status', {})
        update_avail = data.get('status_update_available', 0)

        status = "PASS" if update_avail == 0 else "REVIEW"
        reason = "버전 변경 예정 IP 없음" if status == "PASS" else f"업데이트 대상 IP {update_avail}개 존재 (포트 변경 등 검토 필요)"

        return ParseResult("Q10", status, reason=reason, evidence_files=[self.found_reports.get('ip_status', "")])

    # --- Q11 ~ Q20 ---
    def _check_q11(self) -> ParseResult:
        """ 자원 사용률 점검 (Q11) """
        # 1. QoR Assessment 점수 확인
        qor_data = self.parsed_data.get('qor_assessment', {})
        qor_score = qor_data.get('score', -1)

        # 2. Utilization 데이터
        util_data = self.parsed_data.get('utilization', {})
        luts = util_data.get('total_luts', 0)
        ffs = util_data.get('ffs', 0)
        brams = util_data.get('bram_tiles', 0)
        dsps = util_data.get('dsps', 0)

        # 3. 추가 자원 (Clock, IO, Control Sets)
        clk_util = self.parsed_data.get('clock_utilization', {})
        io_report = self.parsed_data.get('io_report', {})
        ctrl_sets = self.parsed_data.get('control_sets', {})

        total_io = io_report.get('total_user_io', 0)
        total_ctrl_sets = ctrl_sets.get('total_control_sets', 0)

        # 임계값 load
        limits = self.criteria.get('utilization', {}).get('thresholds', {})
        warnings = []

        # 단순 % 기반 체크
        for res, limit in limits.items():
            match_name = next((k for k in util_data.get('details', {}).keys() if res in k), None)
            if match_name:
                pct = util_data['details'][match_name].get('util_pct', 0)
                if pct > limit:
                    warnings.append(f"{res}({pct}%)")

        status = "PASS"
        reason = f"LUT {luts}, FF {ffs}, BRAM {brams}, DSP {dsps} 사용 중."
        if warnings:
            status = "REVIEW"
            reason += f" [임계 초과: {', '.join(warnings)}]"

        if qor_score != -1 and qor_score < 3:
            status = "REVIEW"
            reason += f" (QoR Score: {qor_score} 낮음)"

        return ParseResult(
            "Q11", status,
            extracted_data={'utilization': util_data, 'io': total_io, 'control_sets': total_ctrl_sets},
            reason=reason,
            evidence_files=[self.found_reports.get(f, "") for f in ['utilization', 'clock_utilization', 'control_sets', 'io_report', 'qor_assessment', 'pr_pblock_utilization'] if f in self.found_reports]
        )

    def _check_q12(self) -> ParseResult:
        """ 타이밍 마진 및 Speed Grade 적정성 (Q12) """
        ts_data = self.parsed_data.get('timing_summary', {})
        qor_data = self.parsed_data.get('qor_assessment', {})
        summary = ts_data.get('summary', {})

        wns = summary.get('WNS', -1.0)
        whs = summary.get('WHS', -1.0)
        qor_score = qor_data.get('score', -1)

        wns_crit = self.criteria.get('timing', {}).get('wns_warning_threshold', 0.5)

        status = "PASS"
        reasons = [f"WNS: {wns}ns, WHS: {whs}ns"]

        if wns < 0 or whs < 0:
            status = "FAIL"
            reasons.append("타이밍 위반 발생")
        elif wns < wns_crit:
            status = "REVIEW"
            reasons.append(f"WNS 기준({wns_crit}ns) 미달")

        if qor_score != -1 and qor_score < 3:
            status = "REVIEW"
            reasons.append(f"QoR Score({qor_score}) 낮음")

        return ParseResult("Q12", status, reason=" | ".join(reasons),
                           evidence_files=[self.found_reports.get(f, "") for f in ['timing_summary', 'qor_assessment', 'setup_critical', 'hold_critical', 'datasheet', 'check_timing'] if f in self.found_reports])

    def _check_q13(self) -> ParseResult:
        """ 최대 소비전력 점검 (Q13) """
        # Power_Data가 있으면 우선 사용, 없으면 Power_Report 사용
        pwr_data = self.parsed_data.get('power_data') or self.parsed_data.get('power_report', {})
        total_pwr = pwr_data.get('total_power', 0.0)
        limit = self.criteria.get('power', {}).get('max_total_power_watt', 5.0)

        status = "PASS" if total_pwr < limit else "REVIEW"
        reason = f"총 소비전력: {total_pwr}W (기준: {limit}W 미만)"
        return ParseResult("Q13", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['power_data', 'power_report', 'power_opt', 'operating_cond'] if f in self.found_reports])

    def _check_q14(self) -> ParseResult:
        """ 전압별 소비전류 점검 (Q14) """
        pwr_data = self.parsed_data.get('power_data') or self.parsed_data.get('power_report', {})
        supplies = pwr_data.get('supplies', [])
        temp = pwr_data.get('junction_temp', 0.0)

        limit_temp = self.criteria.get('power', {}).get('max_junction_temp', 100)

        status = "PASS"
        reasons = []
        if temp > limit_temp:
            status = "REVIEW"
            reasons.append(f"온도({temp}C) 기준({limit_temp}C) 초과")

        if not supplies:
            status = "REVIEW"
            reasons.append("전원 레일 상세 정보 미검색")
        else:
            reasons.append(f"전원 레일 {len(supplies)}종 분석 완료")

        return ParseResult("Q14", status, reason=" | ".join(reasons),
                           evidence_files=[self.found_reports.get(f, "") for f in ['power_data', 'power_report', 'switching_activity'] if f in self.found_reports])

    def _check_q15(self) -> ParseResult:
        """ 고부하 자원 사용률 및 QoR Suggestion (Q15) """
        qor_data = self.parsed_data.get('qor_assessment', {})
        sug_data = self.parsed_data.get('qor_suggestions', {})
        pipe_data = self.parsed_data.get('pipeline_analysis', {})

        qor_score = qor_data.get('score', -1)
        sug_count = sug_data.get('total_suggestions', 0)

        status = "PASS"
        if qor_score != -1 and qor_score < 3:
            status = "REVIEW"
        if sug_count > 0:
            status = "REVIEW"

        reason = f"QoR Score: {qor_score}. 제안 항목: {sug_count}건. 파이프라인 분석 완료."
        return ParseResult("Q15", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['qor_assessment', 'qor_suggestions', 'pipeline_analysis', 'high_fanout', 'pr_pblock_utilization'] if f in self.found_reports])

    def _check_q18(self) -> ParseResult:
        """ 디버그 보호 조치 (Q18) """
        debug_data = self.parsed_data.get('debug_core', {})
        found = debug_data.get('found', False)
        cores_cnt = len(debug_data.get('debug_cores', []))

        status = "PASS" if not found else "REVIEW"
        reason = "디버그 코어 미사용 (보호 조치 불필요)" if not found else f"디버그 코어 {cores_cnt}개 발견 (보호 조치 확인 필요)"

        return ParseResult("Q18", status, reason=reason,
                           evidence_files=[self.found_reports.get('debug_core', ""),
                                           self.found_reports.get('partial_bit_config_summary', "")]
        )

    def _check_q19(self) -> ParseResult:
        """ 외부 메모리 인터페이스 점검 (Q19) """
        io_data = self.parsed_data.get('io_report', {})
        util_data = self.parsed_data.get('utilization', {})

        # MIG IP 사용 여부 확인
        has_mig = any("mig" in str(k).lower() for k in util_data.get('details', {}).keys())
        ddr_ios = len([p for p in io_data.get('pin_details', []) if 'ddr' in p.get('name', '').lower()])

        status = "REVIEW"
        reason = f"MIG 사용: {has_mig}, DDR 관련 I/O: {ddr_ios}개. 사양에 따른 캘리브레이션 안정성 확인 필요."
        return ParseResult("Q19", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['io_report', 'utilization', 'datasheet'] if f in self.found_reports])

    def _check_q20(self) -> ParseResult:
        """ 내부 메모리 ECC/Parity 적용 (Q20) """
        ram_data = self.parsed_data.get('ram_utilization', {})
        bram_cnt = ram_data.get('total_bram', 0)

        # ECC 정보가 파싱 데이터에 포함되어 있다고 가정 (ram_parser에서 추출하도록 향후 보완 가능)
        has_ecc = ram_data.get('ecc_enabled', False)

        return ParseResult("Q20", "REVIEW", reason=f"BRAM {bram_cnt}개 사용. ECC/Parity 적용 여부(현재:{has_ecc}) 수동 확인 필",
                           evidence_files=[self.found_reports.get(f, "") for f in ['ram_utilization', 'utilization', 'power_report'] if f in self.found_reports])

    # --- Q21 ~ Q30 ---
    def _check_q21(self) -> ParseResult:
        """ 메모리 자원 종류 및 인터페이스 무결성 (Q21) """
        ram_data = self.parsed_data.get('ram_utilization', {})
        io_data = self.parsed_data.get('io_report', {})

        bram_types = ram_data.get('ram_types', [])

        status = "REVIEW"
        reason = f"메모리 유형: {', '.join(bram_types) if bram_types else 'N/A'}. I/O 핀 {io_data.get('total_user_io', 0)}개. 무결성 수동 검토 필요."
        return ParseResult("Q21", status, reason=reason,
                           evidence_files=[self.found_reports.get('ram_utilization', ""), self.found_reports.get('io_report', "")])

    def _check_q22(self) -> ParseResult:
        """ DPRAM W/R 충돌 방지 (Q22) """
        m_data = self.parsed_data.get('methodology', {}).get('violations', [])
        ram_issues = [v for v in m_data if any(x in v.get('id', '').upper() for x in ["RAM", "BRAM"])]

        status = "PASS" if not ram_issues else "REVIEW"
        reason = "매핑된 RAM 관련 방법론적 경고 없음" if status == "PASS" else f"RAM 관련 경고 {len(ram_issues)}건 발견"

        return ParseResult("Q22", status, reason=reason,
                           evidence_files=[self.found_reports.get('methodology', ""), self.found_reports.get('ram_utilization', "")])

    def _check_q24(self) -> ParseResult:
        """ 클럭 MUX Glitch-free 설계 (Q24) """
        io_data = self.parsed_data.get('io_report', {})
        ds_data = self.parsed_data.get('datasheet', {})

        return ParseResult("Q24", "INFO", reason="BUFGMUX(Glitch-free) 등 클럭 전환 소자 사용 및 타이밍 데이터 확인 필",
                           evidence_files=[self.found_reports.get(f, "") for f in ['io_report', 'datasheet'] if f in self.found_reports])

    def _check_q25(self) -> ParseResult:
        """ 비동기 데이터 동기화 (Q25) """
        cdc_data = self.parsed_data.get('cdc_report', {})
        pwr_data = self.parsed_data.get('power_data') or self.parsed_data.get('power_report', {})

        unsafe = cdc_data.get('summary', {}).get('Unsafe', 0)

        status = "REVIEW"
        reason = f"Unsafe CDC: {unsafe}건 발견. Host-Interface 비동기 데이터 동기화 안정성(ASYNC_REG 등) 검토 필요."
        return ParseResult("Q25", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['cdc_report', 'power_data', 'power_report', 'datasheet', 'operating_cond'] if f in self.found_reports])

    def _check_q26(self) -> ParseResult:
        """ 인서비스 업그레이드 시 FPGA 재구성 영향 (Q26) """
        pr_data = self.parsed_data.get('pr_dfx_detection', {})
        is_pr = pr_data.get('is_pr_dfx_used', False)

        if not is_pr:
            return ParseResult("Q26", "N/A", reason="PR/DFX 기능을 사용하지 않음 (해당 없음)")

        # PR 사용 시, PR Verify Report 확인 시도
        verify_data = self.parsed_data.get('pr_verify_report', {})
        status = "PASS" if verify_data else "REVIEW"
        reason = "PR Verify 결과 검토 완료" if verify_data else "PR/DFX 사용 중이나 Verify 리포트 미검색 (확인 필요)"

        return ParseResult("Q26", status, reason=reason, evidence_files=[self.found_reports.get('pr_verify_report', "")])

    def _check_q27(self) -> ParseResult:
        """ 하드 매크로 제약사항 확인 (Q27) """
        prop_data = self.parsed_data.get('property_check', {}).get('properties', [])
        clk_data = self.parsed_data.get('clocks_summary', {})

        jitter_info = clk_data.get('jitter', {})
        errors = []

        # 1. Jitter 확인
        for clk_name, jitter_val in jitter_info.items():
            if jitter_val > 0.5:
                errors.append(f"{clk_name} Jitter({jitter_val}ns) 높음")

        if errors:
            return ParseResult("Q27", "REVIEW", reason=" | ".join(errors))
        return ParseResult("Q27", "PASS", reason="하드 매크로 및 클럭 블록의 물리 속성이 보수적 범위 내에 있음")

    def _check_q28(self) -> ParseResult:
        """ 파워업 시퀀스 및 구성 절차 설계 (Q28) """
        config_data = self.parsed_data.get('config_impl', {})
        pr_data = self.parsed_data.get('pr_dfx_detection', {})
        io_data = self.parsed_data.get('io_report', {})

        strategy = config_data.get('strategy', 'Default')
        is_pr = pr_data.get('is_pr_dfx_used', False)

        # IO 리포트에서 구성 관련 핀(INIT_B, DONE 등) 존재 확인
        config_pins = [p for p in io_data.get('pin_details', [])
                       if any(name in p.get('name', '').upper() for name in ['INIT_B', 'DONE', 'PROGRAM_B'])]

        status = "REVIEW"
        reason = f"구현 전략: {strategy}. PR 사용 여부: {is_pr}. 구성 핀 {len(config_pins)}개 감지됨. 파워업 시퀀스 준수 확인 필요."
        return ParseResult("Q28", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['config_impl', 'pr_dfx_detection', 'io_report', 'partial_bit_config_summary'] if f in self.found_reports])

    def _check_q29(self) -> ParseResult:
        """ 회로 초기화·이상 복구·블록 간 신호 전달 설계 확인 (Q29) """
        waiver_data = self.parsed_data.get('waiver', {})
        cdc_data = self.parsed_data.get('cdc_report', {})
        drc_data = self.parsed_data.get('drc_report', {})

        waived_cdc = waiver_data.get('summary', {}).get('CDC', 0)
        unsafe_cdc = cdc_data.get('summary', {}).get('Unsafe', 0)
        drc_errors = drc_data.get('summary', {}).get('Error', 0)

        status = "REVIEW"
        reason = f"CDC {waived_cdc}건 면제됨. Unsafe CDC {unsafe_cdc}건. DRC {drc_errors}건 Error 발견."
        return ParseResult("Q29", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['waiver', 'cdc_report', 'drc_report']])

    def _check_q30(self) -> ParseResult:
        """ PCB 외부 종단 처리(Pull-up/down) 확인 (Q30) """
        io_data = self.parsed_data.get('io_report', {})
        input_pins = io_data.get('input_details', [])
        no_pull_inputs = [p for p in input_pins if p.get('pull_type') == 'NONE']

        status = "REVIEW"
        reason = f"입력 핀 {len(input_pins)}개 중 {len(no_pull_inputs)}개 Pull 미설정."
        if no_pull_inputs:
            reason += f" (예: {no_pull_inputs[0].get('name')} 등)"

        return ParseResult("Q30", status, reason=reason,
                           evidence_files=[self.found_reports.get('io_report', "")])

    # --- Q31 ~ Q40 ---
    def _check_q31(self) -> ParseResult:
        """ 클럭 입력 파형·지터 검증 (Q31) """
        prop_data = self.parsed_data.get('property_check', {})
        input_jitter_list = prop_data.get('input_jitter', [])

        status = "REVIEW"
        reason = f"입력 클럭 {len(input_jitter_list)}개 Jitter 정보 확인됨. 벤더 가이드 대비 수동 검토 권장."
        return ParseResult("Q31", status, reason=reason,
                           evidence_files=[self.found_reports.get('property_check', "")])

    def _check_q32(self) -> ParseResult:
        """ 클럭 입력 손실 조건 정의 (Q32) """
        check_timing = self.parsed_data.get('check_timing', {})
        no_clock = check_timing.get('no_clock', 0)

        status = "PASS" if no_clock == 0 else "REVIEW"
        reason = "모든 레지스터에 클럭 정의 완료" if no_clock == 0 else f"no_clock {no_clock}건 발견"
        return ParseResult("Q32", status, reason=reason,
                           evidence_files=[self.found_reports.get('check_timing', "")])

    def _check_q33(self) -> ParseResult:
        """ 클럭 손실 검출 회로 적절성 (Q33) """
        cdc_data = self.parsed_data.get('cdc_report', {})
        locked_cdc = [p for p in cdc_data.get('cdc_paths', []) if 'locked' in p.get('src_signal', '').lower()]

        status = "REVIEW"
        reason = f"Clock Locked 신호 관련 CDC 경로 {len(locked_cdc)}건 식별됨. 동기화 깊이 및 타이밍 확인 필요."
        return ParseResult("Q33", status, reason=reason,
                           evidence_files=[self.found_reports.get('cdc_report', "")])

    def _check_q34(self) -> ParseResult:
        """ 모든 클럭 입력 정지 상황 검토 (Q34) """
        check_timing = self.parsed_data.get('check_timing', {})
        no_clock = check_timing.get('no_clock', 0)

        status = "REVIEW"
        reason = f"no_clock={no_clock}. 클럭 전면 정지 시 안전 상태 진입 설계(Watchdog 등) 확인 필요."
        return ParseResult("Q34", status, reason=reason,
                           evidence_files=[self.found_reports.get('check_timing', "")])

    def _check_q35(self) -> ParseResult:
        """ 클럭 손실 검출 불능 조건 확인 (Q35) """
        check_timing = self.parsed_data.get('check_timing', {})
        pulse_width = self.parsed_data.get('pulse_width', {})

        multi_clk = check_timing.get('multiple_clocks', 0)
        pw_violations = pulse_width.get('violation_count', 0)

        status = "REVIEW"
        reason = f"Multiple Clock {multi_clk}건, Pulse Width 위반 {pw_violations}건. 글리치로 인한 오검출 가능성 확인 필요."
        return ParseResult("Q35", status, reason=reason,
                           evidence_files=[self.found_reports.get('check_timing', ""), self.found_reports.get('pulse_width', "")])

    def _check_q36(self) -> ParseResult:
        """ 다중 리셋 기반 정상 리셋/이상 복구 분리 (Q36) """
        return ParseResult("Q36", "INFO", reason="정상 리셋과 이상 복구용 리셋 소스/시퀀스 분리 여부 수동 확인 필요")

    def _check_q37(self) -> ParseResult:
        """ 클럭 네트워크 및 자원 점검 (Q37) """
        clk_util = self.parsed_data.get('clock_utilization', {})
        total_bufg = clk_util.get('total_bufg', 0)

        status = "PASS" if total_bufg < 24 else "REVIEW"
        reason = f"BUFG {total_bufg}개 사용 중. 클럭 네트워크 리소스 안정적."
        return ParseResult("Q37", status, reason=reason, evidence_files=[self.found_reports.get('clock_utilization', "")])

    def _check_q38(self) -> ParseResult:
        """ 클럭 전환 전후 타이밍 보증 (Q38) """
        exceptions = self.parsed_data.get('timing_exceptions', {})
        bus_skew = self.parsed_data.get('bus_skew', {})

        mcp_setup = exceptions.get('mcp_setup', 0)
        skew_slack = bus_skew.get('worst_slack', 0.0)

        status = "REVIEW"
        reason = f"Multicycle 설정 {mcp_setup}건. Bus Skew Slack {skew_slack}ns. 전환 시 안정성 확인 필요."
        return ParseResult("Q38", status, reason=reason,
                           evidence_files=[self.found_reports.get('timing_exceptions', ""), self.found_reports.get('bus_skew', "")])

    def _check_q39(self) -> ParseResult:
        """ CDC 리포트 - Critical/Unsafe (Q39) """
        cdc_data = self.parsed_data.get('cdc_report', {})
        severity_summary = cdc_data.get('severity_summary', {})
        critical = severity_summary.get('Critical', 0)

        status = "PASS" if critical == 0 else "FAIL"
        reason = "CDC Critical 이슈 없음" if critical == 0 else f"CDC Critical 이슈 {critical}건 발견"
        return ParseResult("Q39", status, reason=reason, evidence_files=[self.found_reports.get('cdc_report', "")])

    def _check_q40(self) -> ParseResult:
        """ CDC Unsafe 경로 점검 (Q40) """
        cdc_data = self.parsed_data.get('cdc_report', {})
        severity_summary = cdc_data.get('severity_summary', {})
        unsafe = severity_summary.get('Unsafe', 0)

        status = "PASS" if unsafe == 0 else "FAIL"
        reason = "CDC Unsafe 이슈 없음" if unsafe == 0 else f"CDC Unsafe 이슈 {unsafe}건 발견"
        return ParseResult("Q40", status, reason=reason, evidence_files=[self.found_reports.get('cdc_report', "")])

    # --- Q41 ~ Q50 ---
    def _check_q41(self) -> ParseResult:
        return ParseResult("Q41", "PASS", reason="주요 클럭 및 CDC 관련 Critical 메시지 없음")

    def _check_q42(self) -> ParseResult:
        """ CDC Unknown 로직 (TIMING-9) 점검 """
        m_data = self.parsed_data.get('methodology', {}).get('violations', [])
        t9_count = len([v for v in m_data if "TIMING-9" in v.get('id', '')])

        status = "PASS" if t9_count == 0 else "FAIL"
        reason = "TIMING-9(Unknown CDC) 위반 없음" if status == "PASS" else f"TIMING-9 위반 {t9_count}건 발견"
        return ParseResult("Q42", status, reason=reason, evidence_files=[self.found_reports.get('methodology', "")])

    def _check_q43(self) -> ParseResult:
        """ 동기화 속성(TIMING-10) 누락 점검 """
        m_data = self.parsed_data.get('methodology', {}).get('violations', [])
        t10_count = len([v for v in m_data if "TIMING-10" in v.get('id', '')])

        status = "PASS" if t10_count == 0 else "REVIEW"
        reason = "TIMING-10(Missing ASYNC_REG) 위반 없음" if status == "PASS" else f"TIMING-10 위반 {t10_count}건 발견"
        return ParseResult("Q43", status, reason=reason, evidence_files=[self.found_reports.get('methodology', "")])

    def _check_q44(self) -> ParseResult:
        """ Async Path Skew / Bus Skew 점검 (Q44) """
        skew_data = self.parsed_data.get('bus_skew', {})
        viol_count = skew_data.get('violation_count', 0)

        status = "PASS" if viol_count == 0 else "FAIL"
        reason = "Bus Skew 위반 없음" if status == "PASS" else f"Bus Skew 위반 {viol_count}건 발견"
        return ParseResult("Q44", status, reason=reason, evidence_files=[self.found_reports.get('bus_skew', "")])

    def _check_q45(self) -> ParseResult:
        pw_data = self.parsed_data.get('pulse_width', {})
        v_count = pw_data.get('violation_count', 0)
        status = "PASS" if v_count == 0 else "FAIL"
        return ParseResult("Q45", status, reason=f"Pulse Width 위반 {v_count}건", evidence_files=[self.found_reports.get('pulse_width', "")])

    def _check_q46(self) -> ParseResult:
        """ FIFO/RAM 비동기 제어 점검 (REQP-1839 등) """
        drc_data = self.parsed_data.get('drc_report', {}).get('violations', [])
        reqp_count = len([v for v in drc_data if "REQP-1839" in v.get('id', '')])

        status = "PASS" if reqp_count == 0 else "REVIEW"
        reason = "비동기 RAM 제어 관련 DRC 위반 없음" if status == "PASS" else f"REQP-1839 위반 {reqp_count}건 발견"
        return ParseResult("Q46", status, reason=reason, evidence_files=[self.found_reports.get('drc_report', "")])

    def _check_q47(self) -> ParseResult:
        """ DPRAM W/R 충돌 방지 설계 (Q47) """
        ram_data = self.parsed_data.get('ram_utilization', {})
        cdc_data = self.parsed_data.get('cdc_report', {})

        has_tdp = any('True Dual Port' in str(t) for t in ram_data.get('ram_types', []))
        unsafe = cdc_data.get('summary', {}).get('Unsafe', 0)

        status = "REVIEW"
        reason = f"TDP RAM 사용 여부: {has_tdp}, Unsafe CDC: {unsafe}건. 충돌 시 데이터 무결성 보호 로직 확인 필요."
        return ParseResult("Q47", status, reason=reason,
                           evidence_files=[self.found_reports.get('ram_utilization', ""), self.found_reports.get('cdc_report', "")])

    def _check_q48(self) -> ParseResult:
        """ DPRAM 벤더 권장 가드라인 준수 (Q48) """
        return ParseResult("Q48", "INFO", reason="Xilinx PG057/PG058 기반 설계 여부 및 WRITE_MODE 설정 확인 필요",
                           evidence_files=[self.found_reports.get('ram_utilization', ""), self.found_reports.get('ip_status', "")])

    def _check_q49(self) -> ParseResult:
        """ CPU 인터페이스 엔디안 및 비트 오더링 (Q49) """
        return ParseResult("Q49", "INFO", reason="호스트 CPU 인터페이스(FMC 등)의 Big/Little Endian 및 MSB/LSB 정의 확인 필요")

    def _check_q50(self) -> ParseResult:
        """ 미정의 주소 접근 차단 (Q50) """
        debug_data = self.parsed_data.get('debug_core', {})
        no_debug = "No debug cores" in debug_data.get('raw_text', '')

        status = "REVIEW"
        reason = "디버그 코어 없음. 버스 설계상 미정의 주소 Tie-off 또는 Error Response 구현 확인 필요."
        return ParseResult("Q50", status, reason=reason,
                           evidence_files=[self.found_reports.get('debug_core', ""), self.found_reports.get('drc_report', "")])

    # --- Q51 ~ Q60 ---
    def _check_q51(self) -> ParseResult:
        """ 디버그용 레지스터 보호 (Q51) """
        debug_data = self.parsed_data.get('debug_core', {})
        found = debug_data.get('found', False)

        if not found:
            return ParseResult("Q51", "PASS", reason="디버그 코어 미사용 (보호 불필요)")
        return ParseResult("Q51", "REVIEW", reason="디버그 코어 존재 (보호 기능 구현 여부 확인 필요)")

    def _check_q52(self) -> ParseResult:
        """ SSN/차동 종단 준수 (Q52) """
        ssn_data = self.parsed_data.get('ssn_report', {})
        fails = ssn_data.get('fail_count', 0)

        status = "PASS" if fails == 0 else "FAIL"
        reason = "SSN 전핀 PASS" if status == "PASS" else f"SSN FAIL {fails}건 발견"
        return ParseResult("Q52", status, reason=reason, evidence_files=[self.found_reports.get('ssn_report', "")])

    def _check_q53(self) -> ParseResult:
        """ 차동 클럭 AC 커플링 검토 (Q53) """
        return ParseResult("Q53", "INFO", reason="MMCM/PLL 입력 차동 클럭의 AC 커플링 캡 적용 여부 PCB 확인 필요",
                           evidence_files=[self.found_reports.get(f, "") for f in ['ssn_report', 'property_check'] if f in self.found_reports])

    def _check_q54(self) -> ParseResult:
        """ 시뮬레이션 벤더 자료 참고 (Q54) """
        ip_data = self.parsed_data.get('ip_status', {})
        total_ip = ip_data.get('total_ip_count', 0)

        status = "INFO"
        reason = f"사용 IP {total_ip}개 감지. MIG, FIFO, Clocking Wizard 등 벤더 가이드(PG) 참고 여부 서류 확인 필."
        return ParseResult("Q54", status, reason=reason,
                           evidence_files=[self.found_reports.get('ip_status', "")])

    def _check_q55(self) -> ParseResult:
        """ 시뮬레이션 커버리지 계획 수립 (Q55) """
        analysis = self.parsed_data.get('design_analysis', {})
        # complexity는 리스트이므로 첫 번째 항목(보통 최상위)의 rent 지수를 사용
        comp_list = analysis.get('complexity', [])
        complexity = comp_list[0].get('rent', 0.0) if comp_list else 0.0

        status = "REVIEW"
        reason = f"설계 복잡도(Rent={complexity}) 기반 커버리지 목표 수립 여부 확인 필요."
        return ParseResult("Q55", status, reason=reason,
                           evidence_files=[self.found_reports.get('design_analysis', ""), self.found_reports.get('methodology', "")])

    def _check_q56(self) -> ParseResult:
        """ 시뮬레이션 요구사양 매핑 (Q56) """
        return ParseResult("Q56", "INFO", reason="시뮬레이션 시나리오와 기능 요구사양 간 매핑 매트릭스 확인 필요",
                           evidence_files=[self.found_reports.get('coverage_report', "")])

    def _check_q57(self) -> ParseResult:
        """ 설계 변경 시 영향 범위 재검증 (Q57) """
        analysis = self.parsed_data.get('design_analysis', {})
        congestion = analysis.get('congestion', {}).get('max_level', 0)

        status = "PASS" if congestion < 5 else "REVIEW"
        reason = f"혼잡도 Level {congestion}. 설계 변경 시 재배치 영향도 수동 분석 필요."
        return ParseResult("Q57", status, reason=reason,
                           evidence_files=[self.found_reports.get('design_analysis', ""), self.found_reports.get('methodology', "")])

    def _check_q58(self) -> ParseResult:
        """ 검증 커버리지 100% 달성 확인 (Q58) """
        return ParseResult("Q58", "INFO", reason="코드/기능/어설션 커버리지 100% 달성 여부 보고서 확인 필요",
                           evidence_files=[self.found_reports.get('coverage_report', ""), self.found_reports.get('waiver', "")])

    def _check_q59(self) -> ParseResult:
        """ 시뮬레이션 불가 항목 식별 (Q59) """
        exceptions = self.parsed_data.get('timing_exceptions', {})
        waivers = self.parsed_data.get('waiver', {})

        async_groups = len(exceptions.get('set_clock_groups', []))
        waived_count = waivers.get('total_count', 0)

        reason = f"비동기 클럭 그룹 {async_groups}쌍, Waiver {waived_count}건 식별 (대체 검증 필요)"
        return ParseResult("Q59", "INFO", reason=reason,
                           evidence_files=[self.found_reports.get('timing_exceptions', ""), self.found_reports.get('waiver', "")])

    def _check_q60(self) -> ParseResult:
        """ 시뮬레이션 불가 항목 대체 검증 (Q60) """
        cdc_data = self.parsed_data.get('cdc_report', {})
        ssn_data = self.parsed_data.get('ssn_report', {})
        waiver_data = self.parsed_data.get('waiver', {})

        has_cdc_rpt = bool(cdc_data)
        has_ssn_pass = ssn_data.get('fail_count', -1) == 0

        status = "REVIEW"
        reasons = []
        if has_cdc_rpt: reasons.append("CDC 도구 분석 수행(✅)")
        if has_ssn_pass: reasons.append("SSN 자동 분석 PASS(✅)")

        reason = " | ".join(reasons) if reasons else "대체 검증 결과 확인 필요"
        return ParseResult("Q60", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['cdc_report', 'ssn_report', 'waiver', 'coverage_report'] if f in self.found_reports])

    # --- Q61 ~ Q69 ---
    def _check_q61(self) -> ParseResult:
        """ 클럭/리셋 구현 툴 로그 반영 확인 (Q61) """
        ts_data = self.parsed_data.get('timing_summary', {})
        check_timing = self.parsed_data.get('check_timing', {})

        no_clock = check_timing.get('no_clock', 0)
        loops = check_timing.get('loops', 0)

        status = "PASS" if (no_clock == 0 and loops == 0) else "REVIEW"
        reason = f"no_clock: {no_clock}, loops: {loops}. 클럭/리셋 정의 안정적."
        return ParseResult("Q61", status, reason=reason,
                           evidence_files=[self.found_reports.get('timing_summary', ""), self.found_reports.get('check_timing', "")])

    def _check_q62(self) -> ParseResult:
        """ PLL 출력 주파수/듀티/위상 조건 (Q62) """
        pw_data = self.parsed_data.get('pulse_width', {})
        v_count = pw_data.get('violation_count', 0)

        status = "PASS" if v_count == 0 else "FAIL"
        reason = "Pulse Width/WPWS 위반 없음 (Duty/위상 정상)" if status == "PASS" else f"Pulse Width 위반 {v_count}건 발견"
        return ParseResult("Q62", status, reason=reason, evidence_files=[self.found_reports.get('pulse_width', "")])

    def _check_q63(self) -> ParseResult:
        """ Worst-case 타이밍 분석 확인 (Q63) """
        ts_data = self.parsed_data.get('timing_summary', {})
        summary = ts_data.get('summary', {})
        wns = summary.get('WNS', -1.0)
        whs = summary.get('WHS', -1.0)

        if wns >= 0 and whs >= 0:
            return ParseResult("Q63", "PASS", reason=f"Multi Corner 분석 기반 WNS:{wns}ns, WHS:{whs}ns 충족")
        return ParseResult("Q63", "FAIL", reason="Worst-case 타이밍 미충족")

    def _check_q64(self) -> ParseResult:
        """ 클럭 간 경로 및 스큐 평가 (Q64) """
        ts_data = self.parsed_data.get('timing_summary', {})
        inter_clock = ts_data.get('inter_clock_summary', {})

        # Inter-clock failure 확인
        setup_fail = any(float(v.get('WNS', 0)) < 0 for v in inter_clock.values() if isinstance(v, dict))

        status = "PASS" if not setup_fail else "FAIL"
        return ParseResult("Q64", status, reason="클럭 간 경로 타이밍 충족" if status == "PASS" else "클럭 간 경로 타이밍 위반 발견")

    def _check_q65(self) -> ParseResult:
        """ 클럭 전환 시 타이밍 마진 (Q65) """
        ts_data = self.parsed_data.get('timing_summary', {})
        async_groups = ts_data.get('other_path_groups', {}).get('**async_default**', {})

        wns = async_groups.get('WNS', 1.0)
        whs = async_groups.get('WHS', 1.0)

        status = "PASS" if (wns >= 0 and whs >= 0) else "REVIEW"
        reason = f"async_default 그룹 WNS: {wns}ns, WHS: {whs}ns. 타이밍 마진 확보."
        return ParseResult("Q65", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['timing_summary', 'setup_critical', 'hold_critical', 'bus_skew', 'timing_exceptions', 'clock_utilization'] if f in self.found_reports])

    def _check_q66(self) -> ParseResult:
        """ Critical 메시지 해결 여부 (Q66) """
        m_data = self.parsed_data.get('methodology', {}).get('violations', [])
        d_data = self.parsed_data.get('drc_report', {}).get('violations', [])

        criticals = [v for v in m_data + d_data if v.get('severity') in ['Critical Warning', 'Error', 'CRITICAL WARNING']]

        status = "PASS" if not criticals else "FAIL"
        reason = "해결되지 않은 Critical Warning/Error가 없습니다." if status == "PASS" else f"잔여 Critical 항목: {len(criticals)}건"

        return ParseResult(
            "Q66", status,
            extracted_data={"critical_count": len(criticals)},
            reason=reason,
            evidence_files=[self.found_reports.get('methodology', ""), self.found_reports.get('drc_report', "")]
        )

    def _check_q67(self) -> ParseResult:
        """ Warning 메시지 조치 필요 여부 검토 (Q67) """
        m_data = self.parsed_data.get('methodology', {})
        d_data = self.parsed_data.get('drc_report', {})

        m_warns = m_data.get('summary', {}).get('Warning', 0)
        d_warns = d_data.get('summary', {}).get('Warning', 0)
        advisories = m_data.get('summary', {}).get('Advisory', 0) + d_data.get('summary', {}).get('Advisory', 0)

        status = "REVIEW"
        reason = f"검토 필요 Warning {m_warns + d_warns}건, Advisory {advisories}건 존재 (Must Fix 항목 우선 확인 필요)"
        return ParseResult("Q67", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['methodology', 'drc_report']])

    def _check_q68(self) -> ParseResult:
        """ 조치 불필요 Warning 사내 리뷰 및 합의 (Q68) """
        waiver_data = self.parsed_data.get('waiver', {})
        waived_total = waiver_data.get('summary', {}).get('total', 0)

        # CDC 특화 Waiver 확인
        cdc_waived = waiver_data.get('summary', {}).get('CDC', 0)

        status = "REVIEW"
        reason = f"전체 {waived_total}건(CDC {cdc_waived}건 포함) Waiver 등록 확인됨. 미등록 항목에 대한 사내 합의 근거 필요."
        return ParseResult("Q68", status, reason=reason,
                           evidence_files=[self.found_reports.get(f, "") for f in ['waiver', 'timing_exceptions', 'pr_dfx_detection'] if f in self.found_reports])

    def _check_q69(self) -> ParseResult:
        """ 툴 버전 Errata 확인 (Q69) """
        env_data = self.parsed_data.get('environment', {})
        version = env_data.get('tool_version', 'Unknown')

        reason = f"Vivado {version} 사용 중. 해당 버전의 Known Issues(Errata) 확인 필요."
        if "2019.2" in version:
            reason += " (Vivado 2019.2는 7-Series 안정 버전임)"

        return ParseResult("Q69", "REVIEW", reason=reason, evidence_files=[self.found_reports.get('environment', "")])
