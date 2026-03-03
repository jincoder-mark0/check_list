## Report Tree

report_tree
├── 01
│   ├── Bus_Skew.rpt
│   ├── CDC_Critical.rpt
│   ├── CDC_Report.rpt
│   ├── CDC_Interaction.rpt
│   ├── Check_Timing.rpt
│   ├── Clock_Networks.rpt
│   ├── Clock_Utilization.rpt
│   ├── Hold_Critical.rpt
│   ├── Pulse_Width.rpt
│   ├── Setup_Critical.rpt
│   ├── Timing_Exceptions.rpt
│   └── Timing_Summary.rpt
├── 02
│   ├── Operating_Cond.rpt
│   ├── Power_Opt.rpt
│   ├── Power_Report.rpt
│   ├── SSN_Report.rpt
│   └── Switching_Activity.rpt
├── 03
│   ├── Control_Sets.rpt
│   ├── DRC_Report.rpt
│   ├── IO_Report.rpt
│   ├── Methodology.rpt
│   ├── RAM_Utilization.rpt
│   ├── Utilization.rpt
│   └── Waiver.rpt
├── 04
│   ├── Debug_Core.rpt
│   ├── Design_Analysis.rpt
│   ├── High_Fanout.rpt
│   ├── Pipeline_Analysis.rpt
│   ├── QoR_Assessment.rpt
│   └── QoR_Suggestions.rpt
├── 05
│   ├── Clocks_Summary.rpt
│   ├── Compile_Order.rpt
│   ├── Config_Impl.rpt
│   ├── Datasheet.rpt
│   ├── Environment.rpt
│   ├── IP_Status.rpt
│   └── Property_Check.rpt
├── 06
│   └── Coverage_Report.txt
└── 07
    ├── PR_DFX_Detection.txt
    ├── PR_NA_Evidence.txt
    ├── PR_DRC_Report.rpt
    ├── PR_Verify_Report.rpt
    ├── Partial_Bit_Config_Summary.rpt
    └── PR_PBLOCK_Utilization.rpt

## Report Description

### Group - 01: Timing & Clocking (타이밍 및 클럭 분석 - 11종)

설계의 타이밍 제약 준수 여부와 클럭 트리 및 도메인 교차(CDC)의 안정성을 집중적으로 검증합니다.

| No | 리포트 종류 | 분석 대상 | 무엇을 검증하는가 | 주요 확인 항목 | 위험 신호 |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Timing_Summary.rpt** | 전체 타이밍 | 셋업/홀드/펄스 폭 등 종합 만족도 | WNS, TNS, WHS, THS, WPWS | WNS < 0, TNS < 0 |
| 2 | **Check_Timing.rpt** | 타이밍 제약 유무 | 제약되지 않은 경로 및 클럭 유무 | No Clock, Unconstrained Endpoints | 제약되지 않은 포트/경로 존재 |
| 3 | **CDC_Report.rpt** | 클럭 도메인 교차 | 도메인 간 데이터 전송 구조의 안정성 | ASYNC_REG, Synchronizer 구조 | Unknown/Missing ASYNC_REG |
| 4 | **CDC_Critical.rpt** | 심각한 CDC 이슈 | CDC 중 해결되지 않은 Critical 이슈 | Critical Violations, Unsafe paths | Critical 등급의 CDC 위반 발생 |
| 5 | **Bus_Skew.rpt** | 버스 스큐 | 버스 신호 간 도착 시간 편차 | Max Skew vs Requirement | Slack < 0 (스큐 과다) |
| 6 | **Clock_Networks.rpt** | 클럭 트리 구조 | 클럭 전파 경로 및 소스 연결 상태 | Constrained/Unconstrained Clocks | Unconstrained Clock 소스 존재 |
| 7 | **Clock_Utilization.rpt** | 클럭 리소스 | BUFG, MMCM 등 클럭 자원 사용 현황 | Global/Regional Clock Resource | 특정 리전의 리소스 과밀 |
| 8 | **Setup_Critical.rpt** | Worst 셋업 경로 | 타이밍 마진이 가장 부족한 셋업 경로 | Logic Level, Net/Data Path Delay | Slack < 0.2ns (여유 부족) |
| 9 | **Hold_Critical.rpt** | Worst 홀드 경로 | 타이밍 마진이 가장 부족한 홀드 경로 | Clock Skew, Data Path Delay | Slack < 0.05ns (여유 부족) |
| 10 | **Pulse_Width.rpt** | 클럭 펄스 품질 | 펄스 폭이 하드웨어 한계를 지키는지 | Min/Max Period, High/Low Pulse | Slack < 0 (동작 불능) |
| 11 | **Timing_Exceptions.rpt**| 타이밍 예외 설정 | False Path, Multi-cycle Path 적용 | Exception Status, Path Overlap | 잘못 적용된 예외로 인한 타이밍 미검증 |

### Group - 02: Power & Conditions (전력 및 동작 환경 - 5종)

설계의 열 소모량과 동작 전압, 스위칭 활동에 따른 전력 특성을 분석합니다.

| No | 리포트 종류 | 분석 대상 | 무엇을 검증하는가 | 주요 확인 항목 | 위험 신호 |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Power_Report.rpt** | 예상 소비 전력 | 칩 내부 소모 전력 및 접합부 온도 | Total On-Chip Power, Junction Temp | Junction Temp > 목표 동작 온도 |
| 2 | **Power_Opt.rpt** | 전력 최적화 | 파워 세이빙 기법(Gated Clock 등) 적용 | Optimized Cells, Savings (W) | 최적화 제안 미반영 과다 |
| 3 | **Operating_Cond.rpt** | 동작 물리 조건 | 설정된 전압, 온도, 공정 조건 확인 | Voltage, Temperature, Process | 허용 범위를 벗어난 전압/온도 설정 |
| 4 | **Switching_Activity.rpt**| 신호 토글률 | 전력 계산의 근거가 되는 스위칭 빈도 | Toggle Rate, Static Probability | 비정상적으로 높은 토글률(버그 의심) |
| 5 | **SSN_Report.rpt** | 동시 스위칭 노이즈 | 출력 핀 전환 시 발생하는 노이즈 간섭 | Simultaneous Switching Noise Margin | Margin < 0 (신호 왜곡 위험) |

### Group - 03: Utilization & Methodology (리소스 사용 및 설계 규칙 - 7종)

FPGA 하드웨어 자원 점검 및 벤더 권장 설계 규칙 준수 여부를 확인합니다.

| No | 리포트 종류 | 분석 대상 | 무엇을 검증하는가 | 주요 확인 항목 | 위험 신호 |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Utilization.rpt** | 전체 리소스 사용량 | LUT, FF, RAM, DSP 사용률 | % Utilization by Resource Type | 특정 자원 사용률 > 80% |
| 2 | **RAM_Utilization.rpt** | 메모리 리소스 | BRAM, FIFO 사용 상세 및 효율 | Block RAM, Distributed RAM | 메모리 부족으로 인한 배치 실패 |
| 3 | **Methodology.rpt** | 설계 방법론 | 자이링스 권장 설계 가이드 준수 | Critical Warnings, Advisory | Critical Warning 등급의 규칙 위반 |
| 4 | **DRC_Report.rpt** | 설계 규칙 체크 | 하드웨어적인 결함 및 비정상 구조 | Bank Conflicts, I/O Placement | DRC Error (비트스트림 생성 불가) |
| 5 | **IO_Report.rpt** | I/O 핀 설정 | 외부 인터페이스 핀의 물리적 설정 | I/O Standard, Drive Strength | Unplaced I/O, 전압 미지정 핀 |
| 6 | **Control_Sets.rpt** | 제어 신호 세트 | 클럭/리셋/이네이블 신호 조합 효율 | Unique Control Sets count | 과도한 Control Sets (배선 정체 유발) |
| 7 | **Waiver.rpt** | 경고 무시 목록 | 사용자가 의도적으로 승인한 위반 목록 | Waived DRCs, Methodology warnings | 중요한 위반 사항의 부적절한 무시 |

### Group - 04: Design Analysis (설계 심층 분석 - 6종)

성능 수렴(QoR) 평가 및 병목 구간 분석을 통해 툴 설정을 가이드합니다.

| No | 리포트 종류 | 분석 대상 | 무엇을 검증하는가 | 주요 확인 항목 | 위험 신호 |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Design_Analysis.rpt** | 설계 복잡도 | 배치/배선 정체 및 로직 레벨 분석 | Logic Levels, Routing Congestion | Congestion Level > 5 |
| 2 | **QoR_Assessment.rpt** | 품질 평가 점수 | 설계가 타이밍에 수렴할 가능성 점수화 | Overall Score, Timing Score | 낮은 점수로 인한 타이밍 수렴 불가 |
| 3 | **QoR_Suggestions.rpt** | 최적화 권장사항 | 툴이 제안하는 구체적인 성능 향상 전략 | Strategy Recommendations, Fixes | 제안된 수정 사항 무시 시 성능 저하 |
| 4 | **High_Fanout.rpt** | 고팬아웃 네트 | 부하가 과도하게 걸리는 신호 배선 | Net Name, Fanout count | Fanout > 1,000 (타이밍 악화 원인) |
| 5 | **Pipeline_Analysis.rpt**| 파이프라인 효율 | 레지스터 사이 로직 깊이의 균형 | Logic Depth Distribution | 특정 구간에 집중된 긴 로직 경로 |
| 6 | **Debug_Core.rpt** | 디버깅 리소스 | ILA, Chipscope 등 디버그 코어 확인 | Debug Hub, Core Count | 과도한 ILA로 인한 타이밍/자원 부족 |

### Group - 05: Implementation & IP (구현 정보 및 IP 상태 - 7종)

구현 설정값과 사용된 IP의 정당성 및 환경 정보를 확인합니다.

| No | 리포트 종류 | 분석 대상 | 무엇을 검증하는가 | 주요 확인 항목 | 위험 신호 |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | **IP_Status.rpt** | 사용된 IP 목록 | IP의 최신 버전 여부 및 라이선스 | IP Version, Update Status | 만료된 IP 또는 최신 툴과 불일치 |
| 2 | **Clocks_Summary.rpt** | 클럭 속성 요약 | 모든 클럭의 주기, 위상, 주파수 요약 | Clock Name, Frequency, Period | 잘못 설정된 클럭 주파수 |
| 3 | **Compile_Order.rpt** | 소스 컴파일 순서 | 설계 파일의 읽기 순서 및 계층 구조 | Source File Order, Libraries | 꼬인 계층 구조로 인한 구문 분석 오류 |
| 4 | **Datasheet.rpt** | 입출력 지연 정보 | 포트 간 하드웨어 지연 데이터 요약 | Setup/Hold for I/O ports | 외부 장치 요구 사양 위반 |
| 5 | **Config_Impl.rpt** | 구현 설정 옵션 | 비트스트림 및 툴의 전체 설정값 | Implementation Strategy, Bitstream | 하드웨어 보드와 불일치하는 설정 |
| 6 | **Environment.rpt** | 실행 환경 정보 | OS, 툴 버전, 호스트 하드웨어 정보 | Vivado Version, OS, Host Name | 버전 불일치로 인한 재생산성 문제 |
| 7 | **Property_Check.rpt** | 속성 적용 검사 | 셀/넷에 강제로 부여된 속성의 유효성 | Property Name, Applied Value | 잘못 적용된 PACKAGE_PIN 또는 LOC |

### Group - 07: PR/DFX Detection (부분 재구성 점검 - 2종)

Partial Reconfiguration 또는 Dynamic Function eXchange 기능의 적용 여부를 확인합니다.

| No | 리포트 종류 | 분석 대상 | 무엇을 검증하는가 | 주요 확인 항목 | 위험 신호 |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | **PR_DFX_Detection.txt**| PR 기능 활성화 | 설계가 재구성 가능하게 구성되었는지 | HD.RECONFIGURABLE Cell 존재 | - (단순 상태 확인용) |
| 2 | **PR_NA_Evidence.txt** | PR 미사용 근거 | 재구성이 적용되지 않은 기술적 정보 | Evidence of non-PR implementation | - (단순 상태 확인용) |
