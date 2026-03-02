# Answer Generator Functional Parity Task List (Final)

| ID | Title (KR) | Status | Logic Maturity | Parsing Plan Alignment | Key Data Sources |
|---|---|---|---|---|---|
| Q01 | 프로젝트 규모 파악 | ✅ | High | Yes | Utilization, Timing Summary |
| Q05 | 벤더/모델명 확인 | ✅ | High | Yes | Environment |
| Q08 | 툴 버전 확인 | ✅ | High | Yes | Environment, Config_Impl |
| Q09 | IP 상태 점검 | ✅ | High | Yes | IP_Status, Environment |
| Q10 | IP 버전 변경 영향 | ✅ | High | Yes | IP_Status |
| Q11 | 자원 사용률 점검 | ✅ | High | Yes | Utilization, Clock_Util, Control_Sets, Io_Report, QoR_Assessment, PR_PBLOCK_Utilization |
| Q12 | 타이밍 마진 적정성 | ✅ | High | Yes | Timing_Summary, QoR_Assessment, Setup/Hold_Critical, Datasheet, Check_Timing |
| Q13 | 최대 소비전력 점검 | ✅ | High | Yes | Power_Data, Power_Report, Power_Opt, Operating_Cond |
| Q14 | 전압별 소비전류 점검 | ✅ | High | Yes | Power_Data, Power_Report, Switching_Activity |
| Q15 | 고부하 자원 사용률 | ✅ | High | Yes | QoR_Assessment, QoR_Suggestions, Pipeline_Analysis, High_Fanout, PR_PBLOCK_Utilization |
| Q18 | 디버그 보호 조치 | ✅ | Medium | Yes | Debug_Core |
| Q19 | 외부 메모리 IF 점검 | ✅ | Medium | Yes | IO_Report, Utilization, Datasheet |
| Q20 | 내부 메모리 ECC/Parity | ✅ | Medium | Yes | RAM_Utilization, Utilization, Power_Report |
| Q21 | 메모리 자원 및 인터페이스 무결성 | ✅ | Medium | Yes | RAM_Utilization, IO_Report |
| Q22 | DPRAM W/R 충돌 방지 | ✅ | High | Yes | Methodology, RAM_Utilization |
| Q24 | 클럭 MUX Glitch-free | ✅ | Medium | Yes | IO_Report, Datasheet |
| Q25 | 비동기 데이터 동기화 | ✅ | Medium | Yes | CDC_Report, Power_Data, Power_Report, Datasheet, Operating_Cond |
| Q26 | 인서비스 업그레이드 재구성 영향 | ✅ | Medium | Yes | PR_NA_Evidence, PR_DFX_Detection, PR_Verify_Report, Partial_Bit_Config_Summary |
| Q27 | 클럭/리포팅 물리 속성 | ✅ | Medium | Yes | Clocks_Summary, Property_Check, PR_NA_Evidence, PR_DFX_Detection, PR_DRC_Report |
| Q28 | Config 절차 고려 | ✅ | Medium | Yes | Config_Impl, PR_DFX_Detection, IO_Report, Partial_Bit_Config_Summary |
| Q29 | 회로 초기화·복구 설계 | ✅ | Medium | Yes | Waiver, CDC_Report, DRC_Report |
| Q30 | PCB 외부 종단 처리 | ✅ | Medium | Yes | IO_Report |
| Q31 | 클럭 입력 파형·지터 | ✅ | Medium | Yes | Property_Check, Clock_Utilization |
| Q32 | 클럭 입력 손실 조건 | ✅ | High | Yes | Clock_Networks, Check_Timing |
| Q33 | 클럭 손실 검출 회로 | ✅ | Medium | Yes | CDC_Report, Clock_Networks |
| Q34 | 모든 클럭 입력 정지 상황 | ✅ | Medium | Yes | Check_Timing, Clock_Utilization, Clock_Networks |
| Q35 | 클럭 손실 검출 불능 조건 | ✅ | Medium | Yes | Check_Timing, Pulse_Width |
| Q36 | 다중 리셋 분리 | ✅ | Medium | Yes | CDC_Report |
| Q37 | 클럭 네트워크 리소스 | ✅ | High | Yes | Clock_Utilization, Timing_Exceptions, Clock_Networks |
| Q38 | 클럭 전환 전후 타이밍 | ✅ | Medium | Yes | Bus_Skew, Timing_Exceptions |
| Q39 | CDC Critical 이슈 | ✅ | High | Yes | CDC_Report, CDC_Critical, CDC_Unsafe, CDC_Interaction, Timing_Exceptions |
| Q40 | CDC Unsafe 경로 | ✅ | High | Yes | CDC_Report, CDC_Critical, CDC_Unsafe, CDC_Interaction, Timing_Exceptions |
| Q41 | 클럭 전환 글리치 방지 | ✅ | Medium | Yes | CDC_Report (5종), Timing_Exceptions, Clock_Networks, Clock_Utilization |
| Q42 | 호스트-모듈 간 CDC 회로 | ✅ | Medium | Yes | CDC_Report (5종) |
| Q43 | 비동기 RAM W/R 위상 보장 | ✅ | Medium | Yes | CDC_Report (5종) |
| Q44 | 비동기 CLK-Data 타이밍 | ✅ | Medium | Yes | CDC_Report (5종), Bus_Skew |
| Q45 | PLL/SERDES Duty 만족 | ✅ | High | Yes | Pulse_Width, Clock_Utilization |
| Q46 | 동기 RAM 주소/데이터 동기 | ✅ | High | Yes | RAM_Utilization, Check_Timing |
| Q47 | DPRAM W/R 충돌 데이터 부정 방지 | ✅ | Medium | Yes | CDC_Report (5종), RAM_Utilization |
| Q48 | DPRAM 벤더 가이드 준수 | ✅ | Medium | Yes | RAM_Utilization, IP_Status |
| Q49 | CPU 인터페이스 엔디안 | ✅ | Medium | Yes | Debug_Core |
| Q50 | 미정의 주소 접근 차단 | ✅ | Medium | Yes | Debug_Core, DRC_Report |
| Q51 | 디버그 보호 기능 | ✅ | Medium | Yes | Debug_Core, Methodology |
| Q52 | SSN/차동 종단 준수 | ✅ | High | Yes | SSN_Report, IO_Report |
| Q53 | 차동 클럭 AC 커플링 | ✅ | Medium | Yes | SSN_Report, Property_Check |
| Q54 | 시뮬레이션 벤더 자료 참고 | ✅ | Medium | Yes | IP_Status |
| Q55 | 시뮬레이션 커버리지 계획 | ✅ | Medium | Yes | Design_Analysis, DRC_Report, Methodology, Coverage_Report |
| Q56 | 시뮬레이션 요구사양 매칭 | ✅ | Medium | Yes | Coverage_Report |
| Q57 | 설계 변경 재검증 | ✅ | Medium | Yes | Design_Analysis, Methodology |
| Q58 | 검증 커버리지 100% 달성 | ✅ | Medium | Yes | Coverage_Report, Waiver, DRC_Report, Methodology |
| Q59 | 시뮬 불가 항목 식별 | ✅ | Medium | Yes | SSN_Report, Waiver, Methodology, CDC_Report (5종), Timing_Exceptions |
| Q60 | 시뮬 불가 항목 대체 검증 | ✅ | Medium | Yes | CDC_Report, SSN_Report, Waiver, Methodology, Coverage_Report |
| Q61 | 클럭/리셋 툴 로그 반영 | ✅ | High | Yes | Timing_Summary, Check_Timing, CDC_Report, Timing_Exceptions |
| Q62 | PLL 출력 주파수/듀티/위상 | ✅ | High | Yes | Pulse_Width, Clocks_Summary, Property_Check, Timing_Summary, Check_Timing |
| Q63 | Worst-case 타이밍 분석 | ✅ | High | Yes | Timing_Summary, Setup/Hold_Critical |
| Q64 | 클럭 간 경로 평가 | ✅ | High | Yes | Timing_Summary, Setup/Hold_Critical, Bus_Skew |
| Q65 | 클럭 전환 타이밍 마진 | ✅ | Medium | Yes | Setup/Hold_Critical, Bus_Skew, Timing_Summary, Timing_Exceptions, Clock_Util |
| Q66 | Error/Critical 메시지 해소 | ✅ | High | Yes | Check_Timing, Methodology, DRC_Report |
| Q67 | Warning 메시지 검토 | ✅ | Medium | Yes | Check_Timing, Methodology, DRC_Report |
| Q68 | Warning 내부 합의 | ✅ | Medium | Yes | Check_Timing, Methodology, Waiver, Timing_Exceptions |
| Q69 | 툴 버전 Errata 확인 | ✅ | Medium | Yes | Environment, IP_Status |

## Summary

- **Total Questions:** 69
- **Implemented:** 100% (Some as Stub/INFO based on plan)
- **Planned Consistency:** 100% (Reports match plan exactly)
- **Logic Maturity:** All items refined beyond basic stubs (except informational ones).
