# FPGA 리포트 분석 도구 — 구현 계획서 (v2)

## 1. 목표

단일 Python 프로그램(`fpga_report_tool.py`)으로 **두 가지 기능**을 제공한다.

| 기능 | 설명 | 입력 | 출력 |
|------|------|------|------|
| **① 체크리스트 자동 채우기** | 리포트 파싱 → 69개 질문 답변/판정 자동 생성 | 리포트 폴더 + `checklist.md` | `checklist_answers.md` |
| **② 리포트 민감정보 제거** | 변수명·클럭명·넷·인스턴스·호스트 등 마스킹 | 리포트 폴더 | `_redacted/` 폴더 |

---

## 2. 리포트 전체 현황 (38개 파일, 7개 그룹)

### Group 01 — Timing/Clock/CDC (13개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
| :--- | :--- | :--- |
| `Timing_Summary.rpt` | WNS/WHS/TNS/THS, "All constraints met", Clock Summary | 중 (clock/path 이름) |
| `Setup_Critical.rpt` | Setup slack < 0.1ns 경로 top-10 | **높음** (깊은 계층 경로) |
| `Hold_Critical.rpt` | Hold slack < 0.1ns 경로 top-10 | **높음** (깊은 계층 경로) |
| `Check_Timing.rpt` | no_clock 카운트, missing I/O delay | 중 |
| `CDC_Report.rpt` | CDC 경고 유형별 카운트, Waived 내역 | 높음 (인스턴스 경로) |
| `CDC_Critical.rpt` | 심각 CDC 카운트 및 상세 | 높음 |
| `CDC_Unsafe.rpt` | 안전하지 않은 CDC 경로 상세 | 높음 |
| `CDC_Interaction.rpt` | 클럭 도메인 간 상호작용 매트릭스 | 중 |
| `Bus_Skew.rpt` | Worst Bus Skew (WBS) 및 Slack | 중 |
| `Clock_Networks.rpt` | 클럭 트리 구조, 주파수 목록 | 중 (클럭 이름) |
| `Clock_Utilization.rpt` | BUFG/MMCM/PLL/BUFGMUX 사용 수량 | 중 |
| `Pulse_Width.rpt` | Pulse width violation, Waveform, Period | 중 |
| `Timing_Exceptions.rpt` | False path/multicycle/Clock groups 설정 | 중 |

### Group 02 — Power/SSN (5개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
| :--- | :--- | :--- |
| `Power_Report.rpt` | Total/Dynamic/Static Power, Vccint/aux 전류, Confidence | 중 |
| `Power_Opt.rpt` | BRAM/SRL/Register gating 요약 (22K+ lines) | **매우 높음** (전체 인스턴스 경로) |
| `SSN_Report.rpt` | 모든 IO PASS 여부, 마진값, OFFCHIP_TERM | 중 (핀 이름) |
| `Operating_Cond.rpt` | 온도/전압/process corner | 낮음 |
| `Switching_Activity.rpt` | (현재 빈 파일 — 내용 無) | 없음 |

### Group 03 — Resource/DRC/Methodology (7개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
| :--- | :--- | :--- |
| `Utilization.rpt` | LUT/FF/BRAM/DSP 사용률·수량·비율 | 중 (계층별 내역) |
| `DRC_Report.rpt` | Error/Critical/Warning/Advisory 카운트 | 높음 (인스턴스) |
| `Methodology.rpt` | Methodology 위반 severity별 카운트 | 높음 |
| `Control_Sets.rpt` | Control set 수량, unique clock enable | 높음 |
| `RAM_Utilization.rpt` | BRAM/LUTRAM 인스턴스별 사용량, ECC 적용 여부 | **높음** (IP/인스턴스명) |
| `IO_Report.rpt` | IOSTANDARD, 핀 배치, bank별 사용 | 중 (핀/신호명) |
| `Waiver.rpt` | Waiver 적용 규칙별 카운트, 상세 사유/사용자 | 중 |

### Group 04 — Design Quality (6개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
| :--- | :--- | :--- |
| `QoR_Assessment.rpt` | QoR Score, Methodology Status | 낮음 |
| `QoR_Suggestions.rpt` | 최적화 제안 항목 | 중 |
| `Design_Analysis.rpt` | 가중치(Rent 지수), Congestion(혼잡도) | 높음 |
| `Pipeline_Analysis.rpt` | 파이프라인 최적화 가능 경로 | 높음 |
| `High_Fanout.rpt` | 높은 fanout 넷 목록 | 높음 (넷 이름) |
| `Debug_Core.rpt` | ILA/VIO 디버그 코어 존재 여부 | 낮음 |

### Group 05 — Environment/IP/Config (7개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
| :--- | :--- | :--- |
| `Environment.rpt` | Vivado 버전, Build, Speed File, OS, Hostname | **높음** (호스트/경로) |
| `IP_Status.rpt` | IP 개수, 업데이트 상태, 버전 | 중 (IP 이름) |
| `Config_Impl.rpt` | Strategy, Directive | 낮음 |
| `Compile_Order.rpt` | 소스 파일 컴파일 순서 | **높음** (파일 경로) |
| `Datasheet.rpt` | IO 타이밍 데이터시트 | 중 (핀 이름) |
| `Clocks_Summary.rpt` | 클럭 정의 요약 (Period/Jitter) | 중 (클럭 이름) |
| `Property_Check.rpt` | 속성 검증 결과 | 낮음 |

### Group 06 — Simulation/Verification (1개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
|------|-----------------|-------------|
| `Coverage_Report.txt` | Statement/Branch/Condition/Toggle 커버리지 | 낮음 |

### Group 07 — PR/DFX (6개)

| 파일 | 핵심 파싱 데이터 | 민감정보 밀도 |
| :--- | :--- | :--- |
| `PR_DFX_Detection.txt` | PR 사용 여부 | 없음 |
| `PR_NA_Evidence.txt` | BUFGMUX/HD.RECONFIGURABLE 카운트 | 없음 |
| `PR_DRC_Report.rpt` | PR 전용 DRC 위반 내역 | 높음 |
| `PR_Verify_Report.rpt` | PR 구성 간 정합성 검증 결과 (PASSED/FAILED) | 낮음 |
| `Partial_Bit_Config_Summary.rpt` | 파셜 비트스트림 구성 정보 | 낮음 |
| `PR_PBLOCK_Utilization.rpt` | PBLOCK별 자원 사용 현황 | 중 |

---

## 3. 질문(Q1~Q69) ↔ 리포트 매핑 및 답변 유형

### 답변 유형 정의

- **분석 범위**: Q01 ~ Q69 (전체 69개 문항)
- **매핑 상태**: **DONE** (전 항목 파싱 및 비즈니스 로직 연동 완료)
- **EVIDENCE**: 외부 증빙(시뮬레이션, 설계문서, 리뷰 기록) 필요

### 📘 상세 파싱 계획서 (구현 기준 문서)

각 문항별 구체적인 리포트 내 파싱 위치, 정규식 로직, 판정 기준(`criteria.json` 연동) 및 예상 답변은 아래 7개의 파싱 상세 계획서에 정의되어 있으며, 파싱 모듈 구현 시 이를 철저히 준수합니다.

- `q01_q10_parsing_plan.md`
- `q11_q20_parsing_plan.md`
- `q21_q30_parsing_plan.md`
- `q31_q40_parsing_plan.md`
- `q41_q50_parsing_plan.md`
- `q51_q60_parsing_plan.md`
- `q61_q69_parsing_plan.md`

### 매핑 요약

### 매핑 요약 (Q1~Q69 전체 최신화)

| Q번호 | 주요 키워드 | 관련 리포트 (AUTO/SEMI 참조) | 답변유형 |
|-------|-----------|-----------------|---------|
| 1 | 개발 규모/일정 | **Compile_Order**, **IP_Status**, **Environment** | SEMI |
| 2~4 | 리뷰 계획/결함이력 | (없음) | EVIDENCE |
| 5 | 벤더/모델명 | **Environment** (Device/Part) | **AUTO** |
| 6~7 | 선정 사양 리뷰 | (없음) | EVIDENCE |
| 8 | 툴 버전 | **Environment**, **Config_Impl** | **AUTO** |
| 9~10 | IP 상태/복구 영향 | **IP_Status** | SEMI |
| 11 | 자원 사용률 | **Utilization, Clock_Utilization, Control_Sets, IO_Report, PR_PBLOCK_Utilization, QoR_Assessment** | **AUTO** |
| 12 | 타이밍 성능/마진 | **Timing_Summary, Setup_Critical, Hold_Critical, QoR_Assessment, Datasheet** | **AUTO** |
| 13 | 최대 소비전력 | **Power_Data, Power_Report, Power_Opt, Operating_Cond** | SEMI |
| 14 | 레일별 소비전류 | **Power_Data, Power_Report, Switching_Activity** | SEMI |
| 15 | 기능 사양/QoR | **QoR_Assessment, QoR_Suggestions, Pipeline_Analysis, High_Fanout, PR_PBLOCK_Utilization** | SEMI |
| 16~17 | 비표준 기능 추가 | (없음) | EVIDENCE |
| 18 | 디버그 보호 | **Debug_Core, Partial_Bit_Config_Summary** | **AUTO** |
| 19 | 외부 메모리 I/F | **IO_Report, Datasheet, Utilization** (MIG 확인) | SEMI |
| 20 | 내부 메모리 ECC | **Utilization, Power_Report** | SEMI |
| 21 | 외부/구성 메모리 ECC | **RAM_Utilization, IO_Report** | SEMI |
| 22 | DPRAM W/R 충돌 | **RAM_Utilization, Methodology** | **AUTO** |
| 23 | RAM 초기화 협의 | (없음) | EVIDENCE |
| 24 | RAM 초기화 후 동작 | **Datasheet, IO_Report** | SEMI |
| 25 | 전원 ON/OFF 시퀀스 | **Power_Data, Power_Report, Datasheet, Operating_Cond** | SEMI |
| 26 | 재구성 영향 | **PR_Verify_Report, Partial_Bit_Config_Summary** | SEMI |
| 27 | 하드매크로 제약 | **Clocks_Summary, Property_Check, PR_DRC_Report** | **AUTO** |
| 28 | 파워업/Config 절차 | **Config_Impl, Partial_Bit_Config_Summary** | SEMI |
| 29 | 이상복구/CDC/DRC | **Waiver, CDC_Report, DRC_Report** | EVIDENCE |
| 30 | PCB 외부 종단 | **IO_Report** | SEMI |
| 31~36 | 회로 보호/리셋 | (없음) | EVIDENCE |
| 37 | 클럭 스위칭 회로 | **Clock_Utilization, Clock_Networks** | **AUTO** |
| 38 | 클럭 스위칭 타이밍 | **Bus_Skew, Timing_Exceptions** | SEMI |
| 39~40 | CDC 안전성 | **CDC_Report, CDC_Critical, CDC_Unsafe, CDC_Interaction** | SEMI |
| 41 | 클럭 전환 글리치 | **Clock_Networks, Clock_Utilization, CDC_Report, Pulse_Width** | SEMI |
| 42 | CDC 회로 사용 여부 | **CDC_Report, Timing_Exceptions** | SEMI |
| 43 | 비동기 메모리 위상 | **CDC_Report, Timing_Exceptions** | SEMI |
| 44 | 비동기 CLK-Data | **CDC_Report, Bus_Skew, Timing_Exceptions** | SEMI |
| 45 | PLL 출력 Duty | **Pulse_Width, Clock_Utilization** | **AUTO** |
| 46 | 동기 RAM 설계 | **RAM_Utilization, Check_Timing** | **AUTO** |
| 47~48 | DPRAM 충돌/권장 | **RAM_Utilization, CDC_Report, Methodology** | SEMI |
| 49~51 | 엔디안/레지스터/보호 | **Debug_Core, DRC_Report, Methodology** | EVIDENCE |
| 52~53 | 고속/차동 종단, AC | **SSN_Report, IO_Report, Property_Check** | SEMI |
| 54 | 시뮬레이션 사명 | **IP_Status** (벤더PG 참고용) | EVIDENCE |
| 55~56 | 커버리지 계획/사양 | **Design_Analysis, DRC_Report, Methodology, Coverage_Report** | SEMI |
| 57 | 설계변경 영향 | **Design_Analysis, Methodology** | SEMI |
| 58 | 커버리지 100% | **Coverage_Report, Waiver, DRC_Report, Methodology** | SEMI |
| 59~60 | 시뮬 불가 항목 | **CDC_Report, SSN_Report, Waiver, Methodology** | **AUTO** |
| 61 | 클럭/리셋 로그 | **Timing_Summary, Check_Timing, CDC_Report** | **AUTO** |
| 62 | PLL 출력 스펙 만족 | **Pulse_Width, Clocks_Summary, Property_Check** | **AUTO** |
| 63 | Worst-case 타이밍 | **Timing_Summary, Setup_Critical, Hold_Critical** | **AUTO** |
| 64 | 클럭 경로 마진 | **Timing_Summary, Setup_Critical, Hold_Critical, Bus_Skew** | **AUTO** |
| 65 | 클럭 스위칭 조합 | **Setup_Critical, Hold_Critical, Bus_Skew, Timing_Summary** | **AUTO** |
| 66 | Error/Critical 해결 | **Check_Timing, Methodology, DRC_Report** | **AUTO** |
| 67 | Warning 조치 검토 | **Check_Timing, Methodology, DRC_Report** | **AUTO** |
| 68 | Warning 내부 합의 | **Waiver, Timing_Exceptions** | SEMI |
| 69 | 툴 버전 Errata | **Environment, IP_Status** | **AUTO** |

> **최종 요약 (파싱 완료 기준):** AUTO 25개, SEMI 31개, EVIDENCE_NEEDED 13개 (총 69문항)

---

## 4. Python 코드 구조 및 범용성 설계

프로그램은 다양한 프로젝트와 다른 폴더 구조에서도 동작할 수 있도록 **범용 프레임워크**로 설계합니다.

1. **동적 리포트 탐색**: 특정 폴더(예: `01/`, `03/`)에 의존하지 않고 `--report-dir` 아래의 모든 `.rpt` 파일을 재귀적으로 검색하여 이름을 기준으로 매핑합니다.
2. **판정 기준 외부 관리**: 코드 수정 없이 판단 로직(임계값 설정 등)을 바꿀 수 있도록 판정 기준을 별도 설정 파일(`config/criteria.json`)로 분리합니다.

```
fpga_check_list/
  ├── fpga_report_tool.py          # CLI 진입점 (checklist | redact | all)
  ├── config/
  │   ├── config_loader.py         # ⚙️ criteria.json 로더
  │   └── criteria.json            # ⚙️ 합격/경고/실패 판정 기준 및 임계값(Threshold) 설정
  ├── core/
  │   ├── __init__.py
  │   ├── base_parser.py           # 공통 유틸리티 기반 클래스 (파일 읽기, 정규식 캐싱)
  │   └── report_finder.py         # 🔍 주어진 경로에서 .rpt 파일을 재귀적으로 동적 탐색
  ├── model/
  │   ├── __init__.py
  │   ├── report_models.py         # 파싱 결과 및 리포트 요약 데이터 구조 (Dataclass)
  │   ├── question_map.py          # Q1~Q69 질문과 필요 리포트 타입 매핑
  │   └── parsers/                 # 📂 개별 리포트 전담 파서 모듈 (리포트 중심 설계)
  │       ├── __init__.py
  │       ├── bus_skew_parser.py    # Bus_Skew.rpt 전담
  │       ├── cdc_critical_parser.py  # CDC_Critical.rpt 전담
  │       ├── cdc_interaction_parser.py  # CDC_Interaction.rpt 전담
  │       ├── cdc_report_parser.py  # CDC_Report.rpt 전담
  │       ├── cdc_unsafe_parser.py  # CDC_Unsafe.rpt 전담
  │       ├── check_timing_parser.py  # Check_Timing.rpt 전담
  │       ├── clock_networks_parser.py  # Clock_Networks.rpt 전담
  │       ├── clock_utilization_parser.py  # Clock_Utilization.rpt 전담
  │       ├── clocks_summary_parser.py  # Clocks_Summary.rpt 전담
  │       ├── compile_order_parser.py  # Compile_Order.rpt 전담
  │       ├── config_impl_parser.py  # Config_Impl.rpt 전담
  │       ├── control_sets_parser.py  # Control_Sets.rpt 전담
  │       ├── coverage_report_parser.py  # Coverage_Report.rpt 전담
  │       ├── datasheet_parser.py  # Datasheet.rpt 전담
  │       ├── debug_core_parser.py  # Debug_Core.rpt 전담
  │       ├── design_analysis_parser.py  # Design_Analysis.rpt 전담
  │       ├── drc_report_parser.py  # DRC_Report.rpt 전담
  │       ├── env_parser.py  # Environment.rpt 전담
  │       ├── high_fanout_parser.py  # High_Fanout.rpt 전담
  │       ├── hold_critical_parser.py  # Hold_Critical.rpt 전담
  │       ├── io_report_parser.py  # IO_Report.rpt 전담
  │       ├── ip_status_parser.py  # IP_Status.rpt 전담
  │       ├── methodology_parser.py  # Methodology.rpt 전담
  │       ├── operating_cond_parser.py  # Operating_Cond.rpt 전담
  │       ├── partial_bit_config_parser.py  # Partial_Bit_Config.rpt 전담
  │       ├── pblock_utilization_parser.py  # Pblock_Utilization.rpt 전담
  │       ├── pipeline_analysis_parser.py  # Pipeline_Analysis.rpt 전담
  │       ├── power_opt_parser.py  # Power_Opt.rpt 전담
  │       ├── power_report_parser.py  # Power_Report.rpt 전담
  │       ├── pr_drc_report_parser.py  # PR_DRC_Report.rpt 전담
  │       ├── pr_verify_report_parser.py  # PR_Verify_Report.rpt 전담
  │       ├── property_check_parser.py  # Property_Check.rpt 전담
  │       ├── pulse_width_parser.py  # Pulse_Width.rpt 전담
  │       ├── qor_assessment_parser.py  # QOR_Assessment.rpt 전담
  │       ├── qor_suggestions_parser.py  # QOR_Suggestions.rpt 전담
  │       ├── ram_utilization_parser.py  # RAM_Utilization.rpt 전담
  │       ├── setup_critical_parser.py  # Setup_Critical.rpt 전담
  │       ├── ssn_report_parser.py  # SSN_Report.rpt 전담
  │       ├── switching_activity_parser.py  # Switching_Activity.rpt 전담
  │       ├── timing_exceptions_parser.py  # Timing_Exceptions.rpt 전담
  │       ├── timing_summary_parser.py  # Timing_Summary.rpt 전담
  │       ├── utilization_parser.py  # Utilization.rpt 전담
  │       └── waiver_parser.py  # Waiver.rpt 전담
  ├── checklist/
  │   ├── __init__.py
  │   └── answer_generator.py      # 파싱 결과와 criteria.json을 결합 → Markdown 답변 판정
  │── redactor/
  │   ├── __init__.py
  │   ├── pattern_registry.py      # 6개 카테고리 정규식 등록
  │   ├── name_mapper.py           # 원본→더미 일관 매핑 (전역 dict)
  │   └── report_redactor.py       # 파일별 읽기→치환→저장 엔진
  └── resources/
      ├── checklist.md             # 체크리스트
      ├── report_file_tree.md      # 리포트 파일 트리
      ├── FPGA_Checklist_1_Main_Documentation_Index.md # 메인 문서 인덱스
      └── FPGA_Checklist_2_Vivado_Automated_Reports_Guide.md # 비바도 자동 리포트 가이드

```

### 4.1 공통 베이스 파서 (`core/base_parser.py`)

모든 리포트 파서의 부모 클래스로서 공통 기능 제공:

- 파일 라인 단위 읽기 (UTF-8/Error replacement)
- 컴파일된 정규식 패턴 캐싱 (`get_pattern`)
- 정규식 기반 단일 값 추출 유틸리티 (`extract_value_by_regex`)

```python
def parse_header(filepath) -> dict:
    """모든 리포트에 공통인 헤더 정보 파싱"""
    return {
        "tool_version": "Vivado v.2019.2",
        "date": "Thu Feb 26 11:44:36 2026",
        "host": "lc-kjlee-pc",
        "host_os": "64-bit Ubuntu 24.04.3 LTS",
        "command": "report_timing ...",
        "design": "top_with_ddr3",
        "device": "7a100t-fgg676",     # 또는 "xc7a100tfgg676-2"
        "speed_file": "-2 PRODUCTION 1.23",
    }
```

### 4.2 체크리스트 답변 생성 (`answer_generator.py`)

**출력 형식 (`checklist_answers.md`):**

```markdown
| No | 질문 개요 | 판정 | 답변 요약 | 근거 리포트 |
|----|-----------|------|-----------|-------------|
| 5 | 벤더/모델명 | INFO | Xilinx xc7a100tfgg676-2 (Artix-7) | Environment.rpt |
| 8 | 툴 버전 | INFO | Vivado v.2019.2 (lin64) | Environment.rpt |
| 11 | 자원 사용률 | REVIEW | LUT 58.63%, BRAM 38.52%, DSP 55.42% | Utilization.rpt |
| 12 | Speed Grade | PASS | WNS=0.093ns, WHS=0.037ns, 모든 타이밍 MET | Timing_Summary.rpt |
| 13 | 최대 소비전력 | REVIEW | Total=2.236W (Confidence: Low) | Power_Report.rpt |
| 18 | 디버그 코어 | PASS | No debug cores found | Debug_Core.rpt |
| 39 | CDC 비동기 | REVIEW | CDC-1: 63건, CDC-10: 2건, CDC-13: 4건 | CDC_Critical.rpt |
| 66 | Error/Critical | REVIEW | DRC Warning 202건, Advisory 7건 확인 필요 | DRC_Report.rpt |
```

**판정 등급:** `PASS` / `FAIL` / `REVIEW` / `N/A` / `INFO` / `EVIDENCE_NEEDED`

### 4.3 설정 파일 (`config/criteria.json`) 스키마 정의

판정 로직에서 사용하는 모든 임계값 및 판단 기준은 외부에서 설정 가능하도록 `criteria.json`으로 관리합니다.

```json
{
  "tool": {
    "known_stable_versions": ["2019.2", "2020.2", "2022.2", "2023.2"]
  },
  "utilization": {
    "thresholds": {"LUT": 70, "FF": 50, "BRAM": 80, "DSP": 80, "IO": 85, "MMCM": 100}
  },
  "timing": {
    "wns_warning_threshold": 0.5,
    "whs_warning_threshold": 0.020
  },
  "power": {
    "max_junction_temp": 100
  },
  "clocking": {
    "jitter_max_pct": 3.0,
    "duty_tolerance_pct": 2.0
  },
  "keywords": {
    "pr_na": ["not applicable", "no partial", "N/A", "PR not used"]
  }
}
```

### 4.4 민감정보 제거 — 6개 카테고리 상세

| # | 카테고리 | 정규식 패턴 | 치환 결과 |
|---|---------|-----------|----------|
| 1 | **계층 인스턴스 경로** | `(?:[a-zA-Z_]\w*(?:\[\d+\])?/){2,}[a-zA-Z_]\w*(?:\[\d+\])?` | 깊이 보존 더미: `inst_A/inst_B/inst_C` |
| 2 | **신호/핀 이름** | `\b(?:pin_[io]_\w+\|ddr3_\w+\|pin_io_\w+)(?:\[\d+\])?\b` | `sig_001`, `sig_002` ... |
| 3 | **클럭 이름** | `\b(?:clk_out\d+_ip_clk_wiz_\w+\|pin_i_clk_\w+)\b` | 주파수 보존: `CLK_78MHz` |
| 4 | **IP 인스턴스명** | `\bip_(?:blk\|fifo\|mig\|clk_wiz)\w*\b` | IP 종류만 보존: `[BlockMem_01]` |
| 5 | **호스트/경로** | `lc-kjlee-pc`, `/home/.../MLC_FPGA/...` | `[HOST]`, `[PATH]` |
| 6 | **프로젝트/디자인/MAC** | `top_with_ddr3`, `MLC_FPGA`, MAC주소 패턴 | `[DESIGN]`, `[PROJECT]`, `[REDACTED]` |

**특수 처리 사항:**

- `Setup_Critical.rpt`/`Hold_Critical.rpt`: 경로당 30줄 이상의 깊은 계층 경로 → 가장 민감
- `Power_Opt.rpt`: 22,000줄 이상, BRAM/SRL/Register 인스턴스 전체 나열 → 대량 치환 필요
- `Switching_Activity.rpt`: 빈 파일 → 그대로 복사
- 헤더의 `Command` 줄: 전체 경로 포함 → 경로 부분만 `[PATH]` 치환
- 수치(ns, W, %, 개수)는 **절대 변경 금지**

---

## 5. CLI 사용법

```bash
# 체크리스트 자동 채우기
python fpga_report_tool.py checklist \
  --report-dir ./post_route_revA_20260226_113801 \
  --output checklist_answers.md

# 민감정보 제거
python fpga_report_tool.py redact \
  --report-dir ./post_route_revA_20260226_113801 \
  --output-dir ./post_route_revA_20260226_113801_redacted

# 둘 다 실행
python fpga_report_tool.py all \
  --report-dir ./post_route_revA_20260226_113801
```

---

## 6. 검증 계획

| 검증 항목 | 방법 | 기준 |
|-----------|------|------|
| 파서 정확도 | 알려진 값(WNS=0.093, Power=2.236W 등)과 비교 | 100% 일치 |
| 답변 완전성 | 69개 질문 모두 답변 생성 확인 | 누락 0 |
| 민감정보 잔류 | `_redacted/` 폴더에서 원본 인스턴스/신호명 grep | 검출 0건 |
| 수치 보존 | 치환 전후 핵심 수치(WNS, Power, Utilization %) diff | 변경 0 |
| 일관성 | 동일 원본이 모든 파일에서 같은 더미명 매핑 | 매핑 테이블 검증 |
| 대용량 처리 | Power_Opt.rpt (22K+ lines) 정상 처리 | 오류 없이 완료 |

---

## 7. 작업 순서

| 순서 | 작업 | 산출물 | 상태 |
| :--- | :--- | :--- | :--- |
| **0** | 전체 69문항 상세 파싱 계획 수립 | `Plan/*.md` 등 7개 문서 | 완료 ✅ |
| **1** | `base_parser.py` + 44종 개별 파서 구현 | `parsers/*.py` | 완료 ✅ |
| **2** | `question_map.py` + `answer_generator.py` 구현 | `checklist/*.py` | 완료 ✅ |
| **3** | `fpga_report_tool.py` CLI 통합 및 테스트 | 진입점 | 완료 ✅ |
| **4** | `pattern_registry.py` + `name_mapper.py` + `report_redactor.py` 구현 | `redactor/*.py` | 완료 ✅ |
| **5** | 실제 리포트로 통합 검증 (38개 파일) | 검증 결과 | 완료 ✅ |
