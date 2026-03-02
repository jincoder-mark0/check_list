# FPGA 체크리스트 자동 판정 결과

- **대상 프로젝트**: Project (7a100tfgg676-2)
- **총 점검 문항**: 69

| No | 질문 개요 | 판정 | 답변 요약 | 근거 리포트 |
|:--:|:----------|:----:|:----------|:------------|
| Q01 | FPGA 개발 프로세스 및 일정(스케줄) 개요를 제시해 주세요. | **INFO** | 빌드시점: Thu Feb 26 11:47:33 2026, 소스파일(Synth): 904개, IP: 52개 | Compile_Order.rpt, Environment.rpt |
| Q02 | 개발 프로세스와 연계하여 개발팀 내부에서 수행할 리뷰 계획을 제시해 주세요. | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q03 | 리뷰 결과는 모든 관계자에게 공유되고 있습니까? | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q04 | FPGA 기인 결함 발생 시, 조사 결과 및 전체 리뷰 결과 제출을 요청받을 수 있습니다. | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q05 | 선정한 FPGA/PLD의 벤더와 모델명을 명시해 주세요. | **INFO** | 타겟 디바이스: 7a100tfgg676-2 | Environment.rpt |
| Q06 | FPGA/PLD 선정 근거에 대한 리뷰를 수행했습니까? | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q07 | 디바이스 선정 시 참고한 문서 및 자료 정보를 알려주세요. | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q08 | 사용 툴 버전을 알려주세요. 최신 버전을 사용합니까? 혹은 구버전이라도 안정성이 검증된 버전을 사용합니까? | **PASS** | 사용 툴 버전: v.2019.2 (안정 버전 여부 확인) | Environment.rpt, Config_Impl.rpt |
| Q09 | 사용 디바이스 및 툴 각각의 결함 정보(Errata, Issue 등)를 확인했습니까? | **PASS** | 전체 52개 IP 상태 양호 (Up-to-date) | IP_Status.rpt |
| Q10 | 구현 툴 버전을 변경할 경우, IP 재생성에 따른 포트 변경, 기능 확장/축소, Errata 영향을 확인했습니까? | **PASS** | 버전 변경 예정 IP 없음 | IP_Status.rpt |
| Q11 | 자원 사용률(FF, LUT, RAM, 클럭 시스템, 전압별 IO, SerDes 채널 등)이 과거 사례 대비 예측 가능한 범위 내에 있습니까? | **PASS** | LUT 37174, FF 37601, BRAM 107.0, DSP 133 사용 중. | Utilization.rpt, Clock_Utilization.rpt, Control_Sets.rpt, IO_Report.rpt, QoR_Assessment.rpt |
| Q12 | FPGA/PLD 스피드 그레이드가 요구 타이밍 성능(주파수, IO 타이밍 등)에 적절함을 확인했습니까? | **REVIEW** | WNS: 0.093ns, WHS: 0.01ns | WNS 기준(0.5ns) 미달 | Timing_Summary.rpt, QoR_Assessment.rpt, Setup_Critical.rpt, Hold_Critical.rpt, Datasheet.rpt, Check_Timing.rpt |
| Q13 | FPGA/PLD의 최대 소비전력이 요구 사양을 초과하지 않음을 확인했습니까? | **PASS** | 총 소비전력: 2.236W (기준: 5.0W 미만) | Power_Report.rpt, Power_Opt.rpt, Operating_Cond.rpt |
| Q14 | FPGA/PLD 각 전압 레일별 소비전류가 전원 공급 사양 이하임을 확인했습니까? | **PASS** | 전원 레일 18종 분석 완료 | Power_Report.rpt, Switching_Activity.rpt |
| Q15 | FPGA/PLD로 구현되는 기능이 요구 사양을 만족함을 리뷰로 확인했습니까? | **PASS** | QoR Score: 5. 제안 항목: 0건. 파이프라인 분석 완료. | QoR_Assessment.rpt, QoR_Suggestions.rpt, Pipeline_Analysis.rpt, High_Fanout.rpt |
| Q16 | 요구 사양에 없는 독자적인 기능을 추가하지 않았습니까? | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q17 | 16번 항목의 구현 기능은 디버그 목적입니까? | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q18 | 디버그 등 테스트 기능의 경우, 정상 운용 중 오작동하지 않도록 보호(패스워드 등)되어 있습니까? (임의의 리셋 조건 추가로 인한 무한 재부팅 사례 유의) 추가 기능 시 상세 정보를 제공해 주세요. | **PASS** | 디버그 코어 미사용 (보호 조치 불필요) | Debug_Core.rpt |
| Q19 | 외부 메모리(DDR, SSRAM, Flash 등) 인터페이스의 기동, 리셋, 초기화, 캘리브레이션, 제어 방법을 검증 및 평가했습니까? | **REVIEW** | MIG 사용: False, DDR 관련 I/O: 0개. 사양에 따른 캘리브레이션 안정성 확인 필요. | IO_Report.rpt, Utilization.rpt, Datasheet.rpt |
| Q20 | 내부 메모리 블록에 Parity/ECC 등 오류 검출 기능 및 소프트에러 대응을 적용했습니까? 적용하지 않았다면 그 사유를 제시해 주세요. | **REVIEW** | BRAM 0개 사용. ECC/Parity 적용 여부(현재:False) 수동 확인 필 | RAM_Utilization.rpt, Utilization.rpt, Power_Report.rpt |
| Q21 | 구성 메모리를 포함한 외부 메모리 인터페이스에 Parity/ECC 등 오류 검출 기능을 적용했습니까? 미적용 시 사유를 제시해 주세요. | **REVIEW** | 메모리 유형: Single Clock SP, , 16x42, 16x6, 16x48, 9x80, 9x6, 9x2, 9x72, 9x78, 4x66, 4x6, 256x1. I/O 핀 184개. 무결성 수동 검토 필요. | RAM_Utilization.rpt, IO_Report.rpt |
| Q22 | DPRAM 인터페이스 사용 시, 내부/외부 RAM 간 W/R 타이밍 충돌을 방지하거나 대응하도록 설계했습니까? | **PASS** | 매핑된 RAM 관련 방법론적 경고 없음 | Methodology.rpt, RAM_Utilization.rpt |
| Q23 | 내부/외부 RAM 초기화의 타이밍, 조건, 범위에 대해 관계사 및 벤더와 협의하여 합의했습니까? | **EVIDENCE_NEEDED** | 외부 증빙 문서 확인 필요 |  |
| Q24 | 내부/외부 RAM 초기화 후의 FPGA 동작(I/O 및 레지스터 설정)이 요구 사양과 일치합니까? | **INFO** | BUFGMUX(Glitch-free) 등 클럭 전환 소자 사용 및 타이밍 데이터 확인 필 | IO_Report.rpt, Datasheet.rpt |
| Q25 | 외부 메모리 탑재 시 전원 ON/OFF 시퀀스 및 초기화 동작을 검증했습니까? | **REVIEW** | Unsafe CDC: 0건 발견. Host-Interface 비동기 데이터 동기화 안정성(ASYNC_REG 등) 검토 필요. | CDC_Report.rpt, Power_Report.rpt, Datasheet.rpt, Operating_Cond.rpt |
| Q26 | 인서비스 업그레이드 시 FPGA 재구성(Reconfiguration)이 요구 사양 동작에 영향을 주지 않음을 확인했습니까? | **N/A** | PR/DFX 기능을 사용하지 않음 (해당 없음) |  |
| Q27 | FPGA 하드 매크로의 활성화 조건, 설정값, 제약 사항에 대해 벤더와 확인했습니까? | **PASS** | 하드 매크로 및 클럭 블록의 물리 속성이 보수적 범위 내에 있음 |  |
| Q28 | 파워업 시퀀스 및 구성 절차(Partial Reconfiguration 포함)를 고려하여 설계했습니까? | **REVIEW** | 구현 전략: Vivado Implementation Defaults. PR 사용 여부: False. 구성 핀 0개 감지됨. 파워업 시퀀스 준수 확인 필요. | Config_Impl.rpt, PR_DFX_Detection.txt, IO_Report.rpt |
| Q29 | 회로 초기화, 이상 상태 복구, 기능 블록 간 신호 전달 설계에 문제가 없음을 확인했니까? | **REVIEW** | CDC 0건 면제됨. Unsafe CDC 0건. DRC 0건 Error 발견. | Waiver.rpt, CDC_Report.rpt, DRC_Report.rpt |
| Q30 | 보드 상의 외부 종단 처리(Pull-up/down)가 FPGA 구성 전의 동작 상태를 포함하여 규정되었습니까? | **REVIEW** | 입력 핀 0개 중 0개 Pull 미설정. | IO_Report.rpt |
| Q31 | 버짓 시뮬레이션이나 평가 보드를 통해 동작 특성(파형, 지터 등)을 확인하는 프로세스가 있습니까? | **REVIEW** | 입력 클럭 0개 Jitter 정보 확인됨. 벤더 가이드 대비 수동 검토 권장. | Property_Check.rpt |
| Q32 | FPGA로 입력되는 클럭이 단절(Loss)되는 조건이 명확합니까? | **PASS** | 모든 레지스터에 클럭 정의 완료 | Check_Timing.rpt |
| Q33 | 클럭 단절 감지 및 처리 회로가 적절하게 설계되었습니까? | **REVIEW** | Clock Locked 신호 관련 CDC 경로 0건 식별됨. 동기화 깊이 및 타이밍 확인 필요. | CDC_Report.rpt |
| Q34 | 모든 클럭 입력이 정지할 가능성을 고려하여 회로를 설계했습니까? | **REVIEW** | no_clock=0. 클럭 전면 정지 시 안전 상태 진입 설계(Watchdog 등) 확인 필요. | Check_Timing.rpt |
| Q35 | 클럭 단절 감지가 불가능해지는 조건이 있습니까? 있다면 명시해 주세요. | **REVIEW** | Multiple Clock 0건, Pulse Width 위반 0건. 글리치로 인한 오검출 가능성 확인 필요. | Check_Timing.rpt, Pulse_Width.rpt |
| Q36 | 다중 리셋이 입력되어도 정상적으로 리셋 및 복구되도록 설계되었습니까? | **INFO** | 정상 리셋과 이상 복구용 리셋 소스/시퀀스 분리 여부 수동 확인 필요 |  |
| Q37 | 클럭 전환(Switching) 회로를 사용합니까? (가급적 사용하지 않는 것을 권장함) | **PASS** | BUFG 0개 사용 중. 클럭 네트워크 리소스 안정적. | Clock_Utilization.rpt |
| Q38 | 클럭 전환 회로 사용 시, 전환 전후의 각 클럭에 대해 타이밍이 보장됩니까? | **REVIEW** | Multicycle 설정 0건. Bus Skew Slack 0.0ns. 전환 시 안정성 확인 필요. | Timing_Exceptions.rpt, Bus_Skew.rpt |
| Q39 | FPGA 내부에 비동기 클럭 회로가 있습니까? | **PASS** | CDC Critical 이슈 없음 | CDC_Report.rpt |
| Q40 | 클럭 도메인 변경(CDC)을 포함하여 비동기 클럭을 사용하는 메모리 회로가 있습니까? | **PASS** | CDC Unsafe 이슈 없음 | CDC_Report.rpt |
| Q41 | 클럭 전환 회로가 글리치, 해저드, 듀티 불균형 등을 방지하도록 구성되었습니까? | **PASS** | 주요 클럭 및 CDC 관련 Critical 메시지 없음 |  |
| Q42 | 호스트-모듈 간 또는 모듈 내부에서 클럭 도메인 변경(CDC) 회로를 사용합니까? | **FAIL** | TIMING-9 위반 1건 발견 | Methodology.rpt |
| Q43 | 비동기 클럭 메모리 회로 사용 시, 파워온/리셋 시에도 W/R 위상 관계가 보장(최적 위상)됩니까? | **REVIEW** | TIMING-10 위반 1건 발견 | Methodology.rpt |
| Q44 | 비동기 클럭 사용 시 CLK-Data 간의 타이밍이 보장됩니까? | **PASS** | Bus Skew 위반 없음 | Bus_Skew.rpt |
| Q45 | PLL/SerDes 출력 클럭의 듀티비(통상 50%)가 사용 조건을 만족합니까? | **PASS** | Pulse Width 위반 0건 | Pulse_Width.rpt |
| Q46 | 동기 RAM에서 주소(Address) 및 데이터(Data) 신호가 동기식으로 설계되었음을 확인했습니까? | **PASS** | 비동기 RAM 제어 관련 DRC 위반 없음 | DRC_Report.rpt |
| Q47 | DPRAM 사용 시 W/R 충돌로 인한 데이터 부정 현상을 방지하거나 그 영향을 고려했습니까? | **REVIEW** | TDP RAM 사용 여부: False, Unsafe CDC: 0건. 충돌 시 데이터 무결성 보호 로직 확인 필요. | RAM_Utilization.rpt, CDC_Report.rpt |
| Q48 | DPRAM 사용 시 벤더의 권장 설계 사례 및 주의사항을 확인했습니까? | **INFO** | Xilinx PG057/PG058 기반 설계 여부 및 WRITE_MODE 설정 확인 필요 | RAM_Utilization.rpt, IP_Status.rpt |
| Q49 | CPU 내장 FPGA 또는 CPU 연결 시, 레지스터의 엔디안(Big/Little) 및 MSB/LSB 구성이 명확합니까? | **INFO** | 호스트 CPU 인터페이스(FMC 등)의 Big/Little Endian 및 MSB/LSB 정의 확인 필요 |  |
| Q50 | 요구 사양에 없는 레지스터 주소에 대해 R/W 동작이 수행되지 않음을 확인했습니까? (디버그용 제외) | **REVIEW** | 디버그 코어 없음. 버스 설계상 미정의 주소 Tie-off 또는 Error Response 구현 확인 필요. | Debug_Core.rpt, DRC_Report.rpt |
| Q51 | 디버그용 레지스터를 설계할 경우 보호 기능을 적용하십시오. | **PASS** | 디버그 코어 미사용 (보호 불필요) |  |
| Q52 | 차동 신호 및 1GHz 이상 고속 클럭의 종단 회로가 벤더 가이드라인에 부합합니까? | **PASS** | SSN 전핀 PASS | SSN_Report.rpt |
| Q53 | 차동 클럭의 AC 커플링 필요 여부를 확인했습니까? (미적용 시 PLL 오작동 사례 유의) | **INFO** | MMCM/PLL 입력 차동 클럭의 AC 커플링 캡 적용 여부 PCB 확인 필요 | SSN_Report.rpt, Property_Check.rpt |
| Q54 | 시뮬레이션 사양 검토 시 벤더 자료를 참고했습니까? 참고 문헌을 명시해 주세요. | **INFO** | 사용 IP 52개 감지. MIG, FIFO, Clocking Wizard 등 벤더 가이드(PG) 참고 여부 서류 확인 필. | IP_Status.rpt |
| Q55 | 시뮬레이션 검증 항목과 실기(Board) 검증 항목을 명확히 구분했습니까? | **REVIEW** | 설계 복잡도(Rent=1.0) 기반 커버리지 목표 수립 여부 확인 필요. | Design_Analysis.rpt, Methodology.rpt |
| Q56 | 요구 사양서를 바탕으로 시뮬레이션 사양(항목, 환경, 조건 등)을 리뷰했습니까? | **N/A** | 관련 리포트 파일 미검색 |  |
| Q57 | 설계 변경 사항 및 그 영향 범위에 대해 검증을 완료했습니까? | **PASS** | 혼잡도 Level 0. 설계 변경 시 재배치 영향도 수동 분석 필요. | Design_Analysis.rpt, Methodology.rpt |
| Q58 | 검증 커버리지가 100%입니까? 확인 방법도 함께 알려주세요. | **INFO** | 코드/기능/어설션 커버리지 100% 달성 여부 보고서 확인 필요 | Waiver.rpt |
| Q59 | 비동기 영역 등 시뮬레이션으로 확인 불가능한 검증 항목을 명확히 정의했습니까? | **INFO** | 비동기 클럭 그룹 0쌍, Waiver 0건 식별 (대체 검증 필요) | Timing_Exceptions.rpt, Waiver.rpt |
| Q60 | 시뮬레이션 불가 항목을 실기 검증 등 대체 수단으로 검증했습니까? | **REVIEW** | CDC 도구 분석 수행(✅) | CDC_Report.rpt, SSN_Report.rpt, Waiver.rpt |
| Q61 | 클럭 및 리셋 사양이 명확하며, 이것이 구현 툴 로그에 올바르게 반영되었음을 확인했습니까? | **PASS** | no_clock: 0, loops: 0. 클럭/리셋 정의 안정적. | Timing_Summary.rpt, Check_Timing.rpt |
| Q62 | PLL 사용 시 출력 주파수, 듀티(통상 50%), 위상 등의 조건이 명확하며 만족함을 확인했니까? | **PASS** | Pulse Width/WPWS 위반 없음 (Duty/위상 정상) | Pulse_Width.rpt |
| Q63 | 변동 및 지터를 고려한 최악의 조건(Worst-case)에서 타이밍 분석 및 보증을 확인했습니까? | **PASS** | Multi Corner 분석 기반 WNS:0.093ns, WHS:0.01ns 충족 |  |
| Q64 | 클럭 간 경로(Master-to-Sub 등)를 식별하고, 스큐 및 지연 등 마진 평가를 실시했습니까? | **PASS** | 클럭 간 경로 타이밍 충족 |  |
| Q65 | 클럭 전환 시, 각 클럭 조합에 대해 정상 동작 및 타이밍 마진을 확인/보증했습니까? | **PASS** | async_default 그룹 WNS: 1.0ns, WHS: 1.0ns. 타이밍 마진 확보. | Timing_Summary.rpt, Setup_Critical.rpt, Hold_Critical.rpt, Bus_Skew.rpt, Timing_Exceptions.rpt, Clock_Utilization.rpt |
| Q66 | 구현 로그의 주요 메시지(Error/Critical)가 모두 해결되었음을 확인했습니까? | **PASS** | 해결되지 않은 Critical Warning/Error가 없습니다. | Methodology.rpt, DRC_Report.rpt |
| Q67 | Warning 메시지에 대해서도 조치 필요 여부를 검토했습니까? | **REVIEW** | 검토 필요 Warning 0건, Advisory 0건 존재 (Must Fix 항목 우선 확인 필요) | Methodology.rpt, DRC_Report.rpt |
| Q68 | 조치가 불필요하다고 판단한 Warning 항목에 대해 사내 리뷰 및 관계자 합의를 마쳤습니까? | **REVIEW** | 전체 0건(CDC 0건 포함) Waiver 등록 확인됨. 미등록 항목에 대한 사내 합의 근거 필요. | Waiver.rpt, Timing_Exceptions.rpt, PR_DFX_Detection.txt |
| Q69 | 설계 초기와 구현 시점의 툴 버전이 다를 경우, 실제 사용 버전의 결함 정보를 확인했습니까? | **REVIEW** | Vivado v.2019.2 사용 중. 해당 버전의 Known Issues(Errata) 확인 필요. (Vivado 2019.2는 7-Series 안정 버전임) | Environment.rpt |
