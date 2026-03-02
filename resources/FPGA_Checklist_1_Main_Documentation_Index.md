# FPGA_Checklist_1_Main_Documentation_Index.md

**FPGA Project Documentation Master Index**

- 프로젝트명: LCoS 기반 WSS 제어 시스템
- Tool: Xilinx Vivado 2019.2
- Device: Artix-7
- 문서 버전: v0.1
- 작성일: 2026-02-26
- 작성자: K.J Lee
- 검토자: (TBD)
- 승인자: (TBD)

---

## 0. 머릿말

본 문서는 FPGA Checklist 전체 중 **최상위 인덱스(Entry Point)** 로서, 다음 역할을 수행한다.

- 전체 문서·데이터 패키지 구조 정의
- 각 문서·폴더의 역할 명확화
- Checklist(1~69) 항목과 제출 Evidence 간의 1:1 매핑 구조 정의
- Vivado 자동 리포트(Group 01~07)와 System Evidence(Group 08)의 상호 관계 정리
- 제출자가 아닌 제3자(검증/감사/리뷰)가 패키지를 열었을 때 **전체 구조를 즉시 이해할 수 있도록** 하는 목적

---

## 1. 문서 세트 구성

아래와 같은 3개의 문서로 구성된다.

| 번호 | 문서명 | 목적 |
|------|--------|------|
| **1** | **FPGA_Checklist_1_Main_Documentation_Index.md** *(본 문서)* | 전체 패키지의 인덱스/구조 정의 |
| 2 | FPGA_Checklist_2_Vivado_Automated_Reports_Guide.md | Group 01~07 자동 리포트 생성/검증 가이드 |
| 3 | FPGA_Checklist_3_System_Evidence_Guide.md | Group 08 실측, 정책 기반 증빙 가이드 |

---

## 2. FPGA Checklist

각 항목의 실제 답변, 증빙, 근거 위치는 Checklist_Mapping.xlsx 파일에서 관리한다.

### 2.1 Table

| No | Item | Question Summary | Answer | Evidence | File Name |
|:--:|:---|:---|:---|:---|:---|
| 1  | Please provide an overview of the FPGA development process/schedule. | FPGA 개발 프로세스/일정 개요 | | | |
| 2  | Provide a review plan to be implemented within the development team in conjunction with the development process. | 내부 리뷰 계획 제시 | | | |
| 3  | Are the review results shared with everyone involved? | 리뷰 결과 공유 여부 | | | |
| 4  | In case of FPGA-induced failure, investigation results and full review results may be submitted. | 장애 발생 시 조사 결과 제출 | | | |
| 5  | What is the vendor and model number of the selected FPGA/PLD? | FPGA 벤더 및 모델명 | | | |
| 6  | Have you reviewed the rationale for selecting FPGAs/PLDs? | FPGA 선정 근거 검토 | | | |
| 7  | Please tell me the information such as the documents referred to when selecting the device. | 참고 문서/자료 정보 | | | |
| 8  | What version of tool do you use? Are you using the latest version? Or are you using an old version that doesn't have any issue? | 사용 툴 버전 | | | |
| 9  | Have you checked the defect information (Errata, Issue, etc.) for each device and tool used? | 디바이스/툴 결함 확인 | | | |
| 10 | If you change the implementation tool version you use, do you see port changes through IP regeneration, enhancements/reductions, and errata? | 툴 버전 변경 시 영향 | | | |
| 11 | Is the utilization of resources (FF, LUT, RAM, clock system (CMT, BUFG/MMCM/PLL, etc.), IO pins per voltage, Serdes CH Count within a range consistent with past developments? | 자원 사용량 유사 범위 | | | |
| 12 | Have you confirmed that the FPGA/PLD speed grade (clock, delay) is appropriate for the required timing performance (clock frequency, IO timing, etc.)? | Speed Grade 적절성 | | | |
| 13 | Has it been verified that the maximum power consumption of the FPGA/PLD does not exceed the maximum power consumption of the required specifications? | 최대 소비전력 검증 | | | |
| 14 | Have you checked that the power consumption for each voltage used in the FPGA/PLD is below the supply current specification? | 전압 레일별 소비전류 | | | |
| 15 | Has the review confirmed that the features implemented in the FPGA/PLD meet the required specifications? | 요구 사양 만족 리뷰 | | | |
| 16 | Have you added any unique features that are not in the required specifications? | 요구 사양 외 독자 기능 | | | |
| 17 | Are the implementation features in Section 16 for debugging purposes? | 독자 기능의 목적 | | | |
| 18 | If it is a test function such as debugging, is the password protected so that it cannot be used in normal operation? In one case, the FPGA repeatedly rebooted as a result of adding a reset condition (circuit) that was not mentioned in the requirements specification. Please provide details of any additional features. | 디버그 기능 보호 로직 | | | |
| 19 | If there is an interface with the external memory (DDR_DRAM, SSRAM, Flash, etc.), have the startup, reset/initialization, calibration, and control methods been checked (validated) and evaluated? | 외부 메모리 초기화 검증 | | | |
| 20 | Has a failure detection function such as Parity/ECC function and a soft error countermeasure been added to the internal memory block? If it is not added, please provide the reason why it is not necessary. | 내부 RAM 오류 대응 | | | |
| 21 | Has a failure detection function such as Parity/ECC function been added to the external memory interface part including Configuration Memory? If it is not added, please provide the reason why it is not necessary. | 외부 메모리 오류 대응 | | | |
| 22 | In the case of a DPRAM interface, is it designed to cope with W/R timing conflict between internal and external RAMs? Please check if the DPRAM interface is designed so that read and write are not accessed at the same time. | DPRAM 타이밍 충돌 고려 | | | |
| 23 | Have the Fj/vendors discussed and agreed upon the timing, conditions, and scope of initialization of internal/external RAM? | RAM 초기화 합의 | | | |
| 24 | Is the FPGA/PLD operation (I/O pin setting, register setting) after the internal/external RAM initialization in accordance with the required specifications? | 초기화 이후 동작 일치 | | | |
| 25 | When DDR_DRAM, SSRAM, Flash, etc. are installed as external memories, have the power ON/OFF sequence and initialization operation of external memories been verified? | 메모리 전원 시퀀스 검증 | | | |
| 26 | Have you confirmed that the operation described in the request specification is not affected in the FPGA/PLD reconfiguration during the in-service upgrade? (behavior during download and load upgrade behavior, etc.) | 서비스 중 재구성 영향 | | | |
| 27 | Have you reviewed with the FPGA/PLD vendor whether or not the hard macros of the candidate FPGA/PLD have activation conditions, set values, or restrictions? | 하드 매크로 제약 리뷰 | | | |
| 28 | Have you confirmed that the design considers FPGA/PLD power-up sequences and configuration procedures (including partial)? | 전원 인가 시퀀스 고려 | | | |
| 29 | Has it been confirmed that there were no problems in the design of circuit initialization operation, restoration from abnormal conditions, and signal transfer between each function block? | 이상 상태 복구 설계 | | | |
| 30 | Are external terminations (Pull-up/down) on the PCB considered and specified? (Including operations PRIOR to FPGA/PLD configuration) | PCB 외부 종단 고려 | | | |
| 31 | Is there a process to check operating characteristics (Waveform, jitter characteristics, etc.) using budget simulation or evaluation board? | 파형/지터 시뮬레이션 | | | |
| 32 | Is the condition that the clock input to the FPGA/PLD is rejected clear? | Clock 차단 조건 명확화 | | | |
| 33 | Is the clock interruption detection processing circuit designed appropriately? | Clock 중단 감지 회로 | | | |
| 34 | Is it made clear whether all/arbitrary clock inputs may stop? | 일부 Clock 정지 가능성 | | | |
| 35 | Are there any conditions that prevent clock loss detection? If so, specify the condition. | Clock 상실 감지 방해 조건 | | | |
| 36 | Is the FPGA/PLD designed to reset and recover normally even if multiple resets are entered? | 다중 Reset 복구 설계 | | | |
| 37 | Does the clock used by the FPGA/PLD use a clock switching circuit inside or outside the device? It is expected that no clock switching circuit is used. | Clock 스위칭 회로 사용 | | | |
| 38 | If a clock switching circuit is used, the timing of each CLK before and after the switch must be guaranteed. | Clock 스위칭 타이밍 보장 | | | |
| 39 | Is there an asynchronous clock circuit in the FPGA? | 내부 Ansync Clock 회로 | | | |
| 40 | Are there any memory circuits that use asynchronous clocks, including clock replacements? | Ansync Clock 메모리 회로 | | | |
| 41 | Is the clock switching circuit configured so that glitches, hazard/duty cracks, and other abnormalities do not occur? | 스위칭 글리치 방지 구성 | | | |
| 42 | Is a circuit used to replace the asynchronous clock between the host and the module or within the module? | Ansync 데이터 synchronization  | | | |
| 43 | If there is a memory circuit that uses an asynchronous clock, have you checked that the WRITE/READ phase relationship is guaranteed even when the power is turned on or reset? (Is it centered or in optimal phase?) | 전원 ON 시 W/R Phase 보장 | | | |
| 44 | Is timing between CLK/Data guaranteed if asynchronous clocks are used? | Ansync CLK/Data 타이밍 | | | |
| 45 | When using the PLL/SERDES output clock, does the DUTY of the output clock satisfy the usage conditions? (Basically, output DUTY is used at 50%.) | PLL 출력 Duty(50%) 만족 | | | |
| 46 | Check whether the Address signal is synchronous in the synchronous RAM. Have you also confirmed that the Data signal is designed to be synchronous? | RAM 주소/데이터 Sync | | | |
| 47 | In one case, DPRAM was used and the RAM value became indeterminate due to a WRITE/READ conflict. If there is contention in WRITE/READ of RAM when DPRAM is used, is the design taken into account the guarantee of contention and the scope of spread? | DPRAM W/R 충돌 고려 | | | |
| 48 | Have you checked the FPGA/PLD vendor design guidelines for recommended design examples and precautions when using DPRAM? | DPRAM 벤더 가이드 준수 | | | |
| 49 | Whether an FPGA with CPU functions is used, or if there is a connection between the FPGA and the CPU, whether the bit configuration of the register specifies big-endian (Motorola CPU)/little-endian (intel CPU). Or, is the MSB/LSB clear? | 엔디안(Endian) 정의 | | | |
| 50 | Check whether the Read/Write operation is not performed for register addresses that are not in the request specification (except for debug registers). | 미정의 주소 접근 차단 | | | |
| 51 | Protection shall be provided if a debug register is provided. | 디버그 레지스터 보호 | | | |
| 52 | Are the termination circuits for differential signals and high-speed CLK signals above 1 GHz designed in accordance with the FPGA/PLD vendor design guidelines? | 고속 신호 종단 회로 | | | |
| 53 | Since there was a problem that the PLL did not operate normally because the differential clock was not AC coupled, check the necessity of AC coupling. | 차동 Clock AC 커플링 검토 | | | |
| 54 | Did you refer to the FPGA/PLD vendor's materials when examining the simulation specifications? If there is a reference, please indicate the name of the document. | 시뮬레이션 벤더 자료 참고 | | | |
| 55 | Have you properly defined and separated the verification scope between simulation and hardware validation? | 시뮬레이션/실기 검증 범위 분리 정의 | | | |
| 56 | Have you reviewed the simulation specifications (items, environment, conditions, etc.) based on the requirements specification? | 요구사항 기반 시뮬레이션 사양 리뷰 | | | |
| 57 | Is it possible to verify the design changes and their influence areas? | 설계 변경 영향 검증 | | | |
| 58 | Is the FPGA/PLD validation coverage (coverage) 100%? Please tell me how to check it. | 검증 커버리지 확인 방법 | | | |
| 59 | Are items that cannot be confirmed by simulation, such as validation items in the asynchronous part, clarified? | 시뮬레이션 불가 항목 정의 | | | |
| 60 | Are items that cannot be confirmed by simulation verified by alternative means such as actual machine verification? | 실기 검증 대체 방법 | | | |
| 61 | Is the type and frequency of the clock and the type of reset clear? Did the implementation tool log confirm that the specifications were correctly reflected? | 구현 툴 로그 확인 | | | |
| 62 | When a PLL circuit is built in, is the output clock frequency and the output duty (Normally 50%) and phase of the clock output specified clearly? Have you confirmed that the specifications are satisfied? | PLL Frequency/Duty/Phase 만족 | | | |
| 63 | Is the timing analysis conducted under the worst-case conditions that take into account jitter and variations in operating conditions? Is it confirmed that the performance is guaranteed under the conditions? | Worst-case 타이밍 분석 | | | |
| 64 | Whether the CO discloses the subclock from the master clock or the path between subclocks from the subclock, and performs margin evaluation such as skew between CLK and CLK/Data, and CLK delay. | Clock 파생 경로 정의 | | | |
| 65 | If there is clock switching, is the normal operation and timing margin for each clock combination checked or guaranteed? | Clock 스위칭 타이밍 마진 | | | |
| 66 | Have you checked that all messages (Error/Critical) that need to be addressed have been resolved? | Critical 메시지 해결 | | | |
| 67 | Have you checked whether action is required for Warning? | Warning 조치 필요 검토 | | | |
| 68 | Does the company internally review that there is no problem with the items that are deemed unnecessary in the Warning message and agree with the relevant parties? | Warning 내부 합의 여부 | | | |
| 69 | When changing the device selection and the imprint tool, have you checked the defect information of the tool actually used? | 툴 변경 시 Errata 확인 | | | |

---

## 3. 제출 패키지 상위 구조 (FPGA_Report + System Evidence)

제출 패키지는 다음과 같이 구성된다.

```
Submission_Package_LCoS_WSS/
  ├─ 00_Index_and_Readme/
  │    ├─ README.md
  │    └─ Checklist_Mapping.xlsx
  ├─ 01_Timing_CDC/
  ├─ 02_Power_Thermal/
  ├─ 03_Resources_DRC/
  ├─ 04_Design_Analysis/
  ├─ 05_Environment_IP/
  ├─ 06_Verification/
  ├─ 07_PR_Evidence/        (PR 미사용 시 N/A)
  ├─ 08_System_Evidence/
  │    ├─ Lab_Measurement_Data.pdf
  │    ├─ ...
  │    └─ 21종 문서
  └─ LICENSE_AND_WAIVERS/
```
- **README.md:** 프로젝트 개요/버전/생성일, 폴더 요약, PASS 기준/waiver 정책, 환경 스냅샷(툴/OS/패치/라이선스), `write_project_tcl -all_properties`로 생성한 스냅샷 스크립트 경로.
  **추가(권장):**
  - **Implement Strategy/Seed 잠금 정책**(placer/router/phys_opt directive/seed 명시)
  - **Git Tag/Commit + Bitstream SHA256** 체크섬(양산/릴리스별)과 Run Snapshot 매핑
  - **XDC 적용 순서/우선순위 정책**(중복/충돌 방지 규칙 및 `check_timing` Zero‑no_clock 목표)
  - **Coverage 리포트 HTML + 텍스트 동시 제출** 안내(HTML 미지원 환경 대비)
  - **PR 미사용 N/A 증빙 파일 경로**(BUFGMUX/HD.RECONFIGURABLE 카운트 0 결과 텍스트)
- **Checklist_Mapping.xlsx:** Checklist No <-> Report 파일 <-> 근거 위치(Page/Line/Signal/TC) <-> PASS/FAIL/WAIVER (하이퍼링크 포함).
  **권장 컬럼:** Reviewer/Approval_Date/Waiver_ID/Waiver_Expiry
- **LICENSE_AND_WAIVERS:** 라이선스/저작권, `report_waivers` 및 승인 기록.

---

## 4. Group 01~08 요약 (Summary)

Group별 상세 기준은 문서 2/3에서 정의되며,
본 Index 문서에서는 **역할 / PASS 조건 / 체크리스트 대응 항목**만 요약한다.

---

### **4.1 Group 01 - Timing & CDC (post_route)**
**Checklist:** 12, 32~45, 59, 61~65
**PASS 기준:**
  - WNS/WHS >= 0
  - Unconstrained Path = 0
  - CDC Unsafe = 0 **(권장: Critical/Unsafe/전체 3종 리포트 분리 제출)**
  - Pulse Width Violation = 0

---

### **4.2 Group 02 - Power & Thermal**
**Checklist:** 13, 14, 25, 52, 53
**PASS 기준:**
  - Total Power <= PSU 설계 제한
  - Rail Current <= 공급 스펙
  - Junction Temp OK
  - SSN/AC Coupling 이상 없음
  - *(생성 가이드 참고: XPE 데이터는 `write_xpe` 사용 권장)*

---

### **4.3 Group 03 - Resources & DRC**
**Checklist:** 11, 22, 30, 47, 48, 66~68
**PASS 기준:**
  - DRC Critical = 0
  - Methodology High = 0
  - DPRAM Conflict = 없음

---

### **4.4 Group 04 - QoR / Design Analysis**
**Checklist:** 15~18, 50, 51, 57
**PASS 기준:**
  - QoR: “Likely to meet timing” 이상
  - Debug Core: 양산 영향 없음

---

### **4.5 Group 05 - Environment & IP**
**Checklist:** 1~10, 19, 27, 28, 69
**PASS 기준:**
  - 환경 스냅샷(Vivado/OS/License) 명확
  - 모든 IP Version Tracking 완료
  - IP 재생성 영향 평가 완료

---

### **4.6 Group 06 - Verification**
**Checklist:** 55, 56, 58, 59, 60
**PASS 기준:**
  - FuncCov >= 90%
  - CodeCov >= 95%
  - Assertion Fail = 0
  - **Coverage Report: HTML + 텍스트 동시 제출(HTML 불가 환경 대비)**

---

### **4.7 Group 07 - PR Evidence**
**Checklist:** 11, 15, 18, 26~28
**PASS 기준:**
  - pr_verify PASS
  - PR DRC High = 0
  - Partial Bitstream Checksum OK
  - (PR 미사용 시 자동 N/A 처리) **+ N/A 증빙으로 BUFGMUX/HD.RECONFIGURABLE 카운트 0 결과 텍스트 포함**

---

### **4.8 Group 08 - System Evidence**
**Checklist:** 2, 3, 4, 6, 7, 18, 20, 21, 26, 28, 31, 32~36, 43, 44, 46, 47, 49~51, 54~56, 60, 67, 68
**PASS 기준:**
  - PNG + CSV + SET 포함
  - 측정환경/장비/포인트/불확도 기록
  - 정책 문서는 승인자 포함
  - **인터페이스별 Duty/지터 기준 표 포함(예: DDR CK, Panel CLK 등)**
  - **PSU Ripple 측정 시 부하 시나리오(Idle/Max/Use‑case) 명시**

---

## 5. Run Snapshot & Naming 규칙

### 5.1 Run Snapshot 폴더명
```
<STAGE>_<REV>_<YYYYMMDD_HHMMSS>/
예: post_route_revA_20260224_103512/
```

### 5.2 Group 폴더명
```
<GroupNo>_<GroupName>/
예: 01_Timing_CDC/
```

### 5.3 Report 파일명 규칙
- BaseName + ext 형태 유지
```
01_Timing_CDC/Timing_Summary.rpt
02_Power_Thermal/Power_Report.rpt
```

---

## 6. PASS/FAIL 기준 표준 템플릿

| 그룹 | PASS 기준 | FAIL 시 조치 |
|------|-----------|--------------|
| Timing | WNS/WHS >= 0 | 구조 변경/제약 보완 |
| Power | PSU 여유 범위 내 | Drive/Slew/QoR 개선 |
| DRC | Critical=0 | Waiver 또는 수정 |
| Verification | Func>=90%, Code>=95% | TC/Stimulus 보강 |
| System Evidence | 실측 RAW 포함 | 재측정/절차 개선 |

---

## 7. 문서 버전

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| v0.1 | 2026-02-26 | K.J Lee | 최초 작성 |

---

## 8. 변경 이력(Change Log)

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| v0.1 | 2026-02-26 | K.J Lee | 최초 작성 |

---

## Note

- 본 문서는 FPGA 제출 패키지의 **최상위 인덱스**이며,
  기술적 상세는 다음 문서에 포함된다.
  - Vivado_Automated_Reports_Guide
  - System_Evidence_Guide
