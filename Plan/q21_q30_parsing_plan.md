# Q21~Q30 상세 파싱 계획서

## 범례

| 기호 | 의미 |
|------|------|
| 📄 | 참조 리포트 |
| 🔍 | 파싱 대상 위치 (줄 번호/섹션) |
| 🧩 | 정규식 / 파싱 로직 |
| 📊 | 추출 결과 필드 |
| ⚖️ | 판정 기준 |
| 💬 | 예상 답변 예시 |

---

## Q21: 구성 메모리 포함 외부 메모리 인터페이스 Parity/ECC 적용 여부

> *구성 메모리를 포함한 외부 메모리 인터페이스에 Parity/ECC 등 오류 검출 기능을 적용했습니까?*

- **답변 유형**: `SEMI` — DDR3 ECC 구성은 MIG 파라미터 확인 필요

📄 **`RAM_Utilization.rpt`** (줄 71) + **`IO_Report.rpt`**

🔍 **파싱 위치**

- `RAM_Utilization.rpt`: `Memory Utilization` 테이블의 `ECC Enabled` 컬럼
- `IO_Report.rpt`: 패드 매핑 테이블 내 `ddr3_dm` / `ddr3_dqs` 신호 수 (ECC 모드 시 DM 비활성, DQS×9=ECC)

🧩 **파싱 로직**

```python
# 1) RAM_Utilization의 ECC Enabled 컬럼 추출
# 헤더 줄에서 컬럼 위치 계산
pattern_ecc_header = r'ECC Enabled'
# 데이터 행에서 ECC 컬럼 위치 값 파싱
pattern_ecc_val = r'\|\s+(True|False|Yes|No|\s*)\s+\|$'  # 마지막 컬럼

# 2) DDR3 DM 신호 수 (ECC 없음이면 ddr3_dm[1:0] 존재)
pattern_ddr3_dm = r'ddr3_dm\[(\d+)\]'
# ddr3_dqs 수: ECC 없으면 2쌍, ECC 있으면 3쌍 (72-bit)

# 3) Configuration Memory 보호 방식 확인
# Artix-7은 CRAM ECC 기능 미지원 (하드웨어 제약)
ARTIX7_CRAM_ECC_SUPPORT = False
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `bram_ecc_enabled_any` | ❌ (모든 항목 공란) |
| `ddr3_dm_count` | 2 (ddr3_dm[1:0]) → ECC 없음 |
| `ddr3_dqs_count` | 2쌍 (16-bit DQ, ECC 미적용) |
| `config_mem_ecc` | N/A (Artix-7 CRAM ECC 미지원) |
| `mig_ecc_mode` | 미검출 (IP 파라미터 확인 필요) |

⚖️ **판정 로직**

```python
def judge_q21(data, criteria):
    issues = []
    if not data['bram_ecc']:
        issues.append("내부 BRAM ECC 미적용")
    if not data['ddr3_ecc']:
        issues.append(f"DDR3 ECC 미적용 (DM[{data['dm_count']-1}:0] 활성, DQ={data['dq_width']}-bit)")
    if not data['config_ecc']:
        issues.append("Configuration Memory ECC: Artix-7 하드웨어 미지원")
    return "REVIEW", "; ".join(issues) + " — 미적용 사유 제출 필요"
```

💬 **예상 답변**
> **REVIEW** — 외부 메모리 ECC **미적용**: DDR3 16-bit 모드(DM[1:0] 활성, ECC시 3쌍 DQS 필요). ⚠️ Configuration Memory: Artix-7은 CRAM ECC 하드웨어 미지원. 미적용 사유 제출 필요(예: 데이터 특성, 재전송 메커니즘 등).

---

## Q22: DPRAM W/R 타이밍 충돌 대응 설계 여부

> *DPRAM 인터페이스 사용 시 내부/외부 RAM 간 W/R 타이밍 충돌 대응 설계를 했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`RAM_Utilization.rpt`** + **`Methodology.rpt`**

🔍 **RAM_Utilization.rpt 파싱 위치**

- `Memory Description` 테이블 — Port 구성별 분류
- `Memory Utilization` 테이블 — Port A/B 동시 존재 여부
- `Single Clock SDP`, `Single Port Write, Multi Port Read`, `True Dual Port` 분류

🔍 **Methodology.rpt 파싱 위치**

- `TIMING` 또는 `RAM` 관련된 Methodology 위반 섹션 (W/R 충돌 관련 경고(Critical Warning/Warning) 발생 여부)

🧩 **파싱 로직**

```python
# 1) DPRAM(True Dual Port) 또는 SDP 메모리 분류
MEMORY_TYPES = {
    'SP': 'Single Clock SP',
    'SDP': 'Single Clock SDP',
    'WRMR': 'Single Port Write, Multi Port Read',
    'TDP': 'True Dual Port'
}
pattern_mem_type = r'\|\s+([^\|]+?)\s+\|\s+(\d+)\s+\|\s+(Single Clock SP|Single Clock SDP|Single Port Write.*?|True Dual Port)\s+\|'

# 2) Port B 존재 + 동시 RW 가능성 (SDP, TDP는 W/R 충돌 가능)
# SDP = Simple Dual Port (Port A: WR, Port B: RD) → 기본적으로 충돌 없음
# TDP = True Dual Port → 동일 주소 동시 WR/RD 시 충돌 위험

# 3) RAM_Utilization의 Port A/B Requirement(ns)
pattern_port_req = r'\|\s+(\d+\.\d+)\s+\|\s+(\d+\.\d+)\s+\|$'  # Port A/B timing req

# 4) Methodology.rpt — 타이밍/W&R 충돌 룰셋 위반 여부 (예: TIMING-##, RAMW-##)
pattern_methodology_ram = r'(?i)(collision|read-before-write|write-first|ramw-\d+|timing-\d+)'
```

📊 **추출 결과**

| 메모리 타입 | 수 | 충돌 위험 |
|------------|---|----------|
| Single Clock SP (u_sys_power_loader BRAM) | 4×512 | 없음 |
| Single Clock SDP (FIFO 계열) | ~8개 | 낮음 (포트 분리) |
| Single Port Write/Multi Read (MIG PHY) | ~4개 | 설계 의존 |
| True Dual Port | 0개 | — |

⚖️ **판정 로직**

```python
def judge_q22(ram_data):
    tdp_count = ram_data.get('TDP', 0)
    sdp_count = ram_data.get('SDP', 0)
    if tdp_count > 0:
        return "REVIEW", f"TDP RAM {tdp_count}개 — 동일 주소 동시 R/W 충돌 설계 확인 필요"
    elif sdp_count > 0:
        return "PASS", f"SDP/FIFO 구조 {sdp_count}개 — 포트 분리로 충돌 없음. TDP 미사용"
    return "PASS", "RAM 충돌 위험 없음"
```

💬 **예상 답변**
> **PASS** — True Dual Port RAM **0개** 사용. 모든 BRAM은 Single Clock SP (전용 포트) 또는 SDP(FIFO, 포트A=WR/포트B=RD 분리) 구조. MIG PHY 내부 FIFO는 Xilinx 설계 보증. W/R 충돌 구조적 방지.

---

## Q23: 내부/외부 RAM 초기화 타이밍·조건·범위 협의

> *내부/외부 RAM 초기화의 타이밍, 조건, 범위를 관계사 및 벤더와 협의하여 합의했습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 참조 리포트 없음 — 외부 협의 문서 필요

💬 **예상 답변**
> **EVIDENCE_NEEDED** — RAM 초기화 타이밍/조건/범위 협의는 리포트에서 확인 불가. 관련 회의록, 사양 합의서를 제출해 주세요.

---

## Q24: RAM 초기화 후 FPGA 동작(I/O, 레지스터) 사양 일치 확인

> *내부/외부 RAM 초기화 후의 FPGA 동작(I/O 및 레지스터 설정)이 요구 사양과 일치합니까?*

- **답변 유형**: `SEMI` — Datasheet에서 초기화 후 IO 타이밍 확인 가능

📄 **`Datasheet.rpt`** + **`IO_Report.rpt`**

🔍 **Datasheet.rpt 파싱 위치**

- `Input Port Setup/Hold` 섹션 (DDR3 초기화 후 DQ 타이밍 안정성)
- `Output Port Clock-to-out` 섹션 (초기화 후 Address/Ctrl 타이밍)

🔍 **IO_Report.rpt 파싱 위치**

- Bank별 `IO Standard` 및 `On-Die Termination (OUT_TERM/IN_TERM)` 설정 확인
- DDR3 Bank 34/35: SSTL135, ODT 설정 매칭

🧩 **파싱 로직**

```python
# 1) 초기화 후 IO Standard 확인
pattern_io_std = r'\|\s+([\w\[\]]+)\s+\|.*?\|\s+(SSTL\w+|LVCMOS\w+|LVDS\w+|DIFF_\w+)\s+\|'

# 2) DDR3 초기화 완료 신호 (phy_init_done) 확인
# → u_ip_mig_ddr3의 init_calib_complete 신호
pattern_init_done = r'init_calib_complete|phy_init_done'

# 3) Datasheet의 output clock-to-out 값
pattern_clk2out = r'\|\s+([\w\[\]]+)\s+\|.*?\|\s+([\d.-]+)\s*\((\w)\)\s+\|'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `ddr3_io_std` | SSTL135 / DIFF_SSTL135 |
| `ddr3_bank` | Bank 34/35 (Vcco=1.35V) |
| `init_calib_signal` | `init_calib_complete` (MIG 내부) |
| `ddr3_rst_n` | Active-Low, IO Standard 확인 필요 |
| `post_init_clk_to_out` | Datasheet 출력 섹션 확인 가능 |

⚖️ **판정 로직**

```python
def judge_q24(io_data):
    return "REVIEW", ("IO Standard DDR3: SSTL135 확인. "
                     "초기화 완료(init_calib_complete) 이후 정상 동작은 "
                     "시뮬레이션/보드 수준 검증 결과 필요.")
```

💬 **예상 답변**
> **REVIEW** — DDR3 IO: SSTL135 (Bank 34/35, Vcco=1.35V), 초기화 완료 신호 `init_calib_complete`. ⚠️ 초기화 후 레지스터/포트 동작이 요구 사양에 일치하는지는 시뮬레이션 또는 보드 테스트 결과를 통해 별도 확인 필요.

---

## Q25: 외부 메모리 전원 ON/OFF 시퀀스 검증

> *외부 메모리 탑재 시 전원 ON/OFF 시퀀스 및 초기화 동작을 검증했습니까?*

- **답변 유형**: `SEMI` — 전원 조건 확인 가능, 시퀀스 검증은 외부

📄 **`Power_Data.rpt`** + **`Power_Report.rpt`** + **`Datasheet.rpt`** + **`Operating_Cond.rpt`**

🔍 **파싱 위치**

- `Power_Report.rpt` (또는 `Power_Data.rpt`): Vcco 레일 전압 확인 (예: Bank 34/35 DDR3 전원 레일)
- `Datasheet.rpt`: 외부 메모리 인터페이스와의 타이밍, 리셋 시퀀스 특성 (`ddr3_reset_n` 등)

🧩 **파싱 로직**

```python
# 1) DDR3 전원 레일 확인
pattern_ddr3_rail = r'Vcco135\s*\|\s*([\d.]+)\s*\|\s*([\d.*]+)\s*\|'

# 2) ddr3_reset_n 신호 IO Standard 확인
pattern_reset_n = r'\|\s+ddr3_reset_n\s+\|.*?\|\s+(\w+)\s+\|'

# 3) Operating_Cond.rpt — 디바이스 동작 조건
# 줄 패턴: Operating Conditions | Value
pattern_op_cond = r'(Process\s+Corner|Temperature|Voltage)\s+\|\s+([\w.+-]+)'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `ddr3_vcco` | 1.35 V (Vcco135) |
| `ddr3_reset_n_std` | LVCMOS18 또는 SSTL135 |
| `power_on_sequence` | EVIDENCE_NEEDED (PCB 시퀀서 회로 확인 필요) |
| `pmic_control` | 리포트에 미포함 |

⚖️ **판정 로직**

```python
def judge_q25(data, criteria):
    info = f"DDR3 전원 레일 Vcco135={data['vcco']}V 확인."
    return "REVIEW", (info + " ⚠️ 전원 ON/OFF 시퀀스(Tpw, Treset 동작) 및 "
                     "PMC/시퀀서 회로는 PCB/보드 설계 문서 확인 필요.")
```

💬 **예상 답변**
> **REVIEW** — DDR3 전원 레일 Vcco135=1.35V 확인. `ddr3_reset_n` 신호 존재. ⚠️ JEDEC DDR3 전원 시퀀스(Vdd → Vddq → Reset_n 해제) 및 검증 결과(시뮬레이션 또는 보드 테스트)를 별도 제출해 주세요.

---

## Q26: 인서비스 업그레이드 시 재구성 영향 확인

> *인서비스 업그레이드 시 FPGA 재구성(Reconfiguration)이 요구 사양 동작에 영향을 주지 않음을 확인했습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **`PR_Verify_Report.rpt`** + **`Partial_Bit_Config_Summary.rpt`**

🔍 **PR_Verify_Report.rpt 파싱 위치**

- 리포트 헤더 및 `PR Verify Summary` 등 PR 검증 관련 섹션 탐색

🔍 **Partial_Bit_Config_Summary.rpt 파싱 위치**

- 부분 비트스트림(`Partial Bitstream`) 요약 정보에 부분 파티션(`pblock`)이나 PR 식별 플래그 확인

🧩 **파싱 로직**

```python
# 1) PR 관련 리포트 본문 내에서 사용 여부 키워드 검색
pattern_pr_na = r'(?i)(not applicable|no partial|no pr regions|N/A|PR.*not.*used)'
pattern_pr_used = r'(?i)(partial reconfiguration|pr_verify|dfx region)'

# (보조 구조로 07/ 폴더 하위 PR_NA_Evidence.txt 파일 존재 확인 로직 결합)
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `PR_NA_Evidence.txt` | 존재 (07/ 폴더) |
| `PR_DFX_Detection.txt` | 존재 (07/ 폴더) |
| `pr_used` | 미사용 (파일 내용 확인 필요) |
| `in_service_reconfig` | EVIDENCE_NEEDED |

⚖️ **판정 로직**

```python
def judge_q26(pr_data):
    if not pr_data['pr_used']:
        return "REVIEW", "Partial Reconfiguration 미사용 확인(PR_NA_Evidence). 인서비스 업그레이드가 전체 재구성 방식이라면 업그레이드 중 서비스 중단/복구 절차 제출 필요."
    return "REVIEW", "PR 사용 시 재구성 영향 검증 근거 제출 필요"
```

💬 **예상 답변**
> **REVIEW** — `PR_NA_Evidence.txt` 존재: Partial Reconfiguration 미사용. 인서비스 업그레이드는 전체 재구성(Full Configuration) 방식으로 추정. ⚠️ 업그레이드 중 서비스 영향(중단 시간, 복구 절차)을 사양서와 비교한 검증 결과 필요.

---

## Q27: FPGA 하드 매크로 활성화 조건·제약 벤더 확인

> *FPGA 하드 매크로의 활성화 조건, 설정값, 제약 사항에 대해 벤더와 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Clocks_Summary.rpt`** + **`Property_Check.rpt`** + **`PR_DRC_Report.rpt`**

🔍 **주요 파싱 위치**

- `Clocks_Summary.rpt`: 클럭 트리 및 생성된 하드 매크로(PLL/MMCM) 활성 조건 요약
- `Property_Check.rpt`: 하드 매크로의 물리적 파라미터(Jitter, Duty Cycle, 범위 등) 속성 검사
- `PR_DRC_Report.rpt`: Partial Reconfiguration 적용 시 하드 매크로 제약 위반 여부

🧩 **파싱 로직**

```python
# 1) 각 하드 매크로 클럭 블록 파싱 (NAME 기준 grouping)
pattern_clk_block_name = r'NAME\s+string\s+true\s+(\S+)'
pattern_clk_period = r'PERIOD\s+double\s+true\s+([\d.]+)'
pattern_clk_jitter = r'INPUT_JITTER\s+double\s+true\s+([\d.]+)'
pattern_clk_multiply = r'MULTIPLY_BY\s+int\s+true\s+(\d+)'
pattern_clk_divide = r'DIVIDE_BY\s+int\s+true\s+(\d+)'
pattern_master = r'MASTER_CLOCK\s+clock\s+true\s+(\S+)'

# 2) 하드 매크로별 분류
HARD_MACRO_CLOCKS = {
    'MMCM': ['mmcm_adv_inst', 'mmcm_i', 'ip_clk_wiz'],
    'PLL': ['plle2_i', 'plle2_adv', 'ip_clk_wiz_power_loader'],
    'MIG_PHY': ['phaser_out', 'phaser_in', 'oserdes', 'iserdes']
}
```

📊 **추출 결과**

| 하드 매크로 | 클럭명 | Period | Master | Jitter |
|------------|--------|--------|--------|--------|
| MMCM #1 (FMC) | `clk_out1_ip_clk_wiz_fmc_clk` | 11.574ns | `pin_i_fmc_clk` | 0.231ns |
| MMCM #2 (LCOS) | `clk_out1_ip_clk_wiz_lcos_sftcck` | 10.121ns | `pin_i_clk_78m` | 0.128ns |
| MMCM #3 (DDR3) | `clk_out2_ip_clk_wiz_ddr3_clk` | 5.000ns | `pin_i_clk_100m` | 0.100ns |
| PLL #1 (PWR) | `clk_out1_ip_clk_wiz_power_loader` | 3.205ns | (cascade) | — |
| PLL #2 (MIG) | `mem_refclk` | 3.077ns | `clk_out1…ddr3` | — |
| PHASER | `oserdes_clk` | 3.077ns | `mem_refclk` | — |

⚖️ **판정 로직**

```python
def judge_q27(hard_macro_data, criteria):
    jitter_threshold_pct = criteria['clocking']['jitter_threshold_pct'] # 예: 0.1 (10%)
    violations = []
    # 각 MMCM/PLL의 Jitter·Period가 Xilinx 제약 이내인지 확인
    for clk in hard_macro_data:
        if clk['jitter'] > clk['period'] * jitter_threshold_pct:
            violations.append(f"{clk['name']}: Jitter {clk['jitter']}ns > {jitter_threshold_pct*100}% of period")
    if violations:
        return "REVIEW", "; ".join(violations)
    return "PASS", f"하드 매크로 {len(hard_macro_data)}개 파라미터 확인. 벤더 제약 이내."
```

💬 **예상 답변**
> **PASS** — MMCM 5개, PLL 2개, PHASER 18개 하드 매크로 클럭 파라미터 확인. Jitter: FMC 0.231ns/23.1ns(1%), 20M 0.5ns/50ns(1%), 100M 0.1ns/10ns(1%) — Xilinx 권장 범위 이내. Vivado Property_Check 완료, 하드 매크로 설정 적절.

---

## Q28: 파워업 시퀀스 및 구성 절차 설계 반영 확인

> *파워업 시퀀스 및 구성 절차(Partial Reconfiguration 포함)를 고려하여 설계했습니까?*

- **답변 유형**: `SEMI` — 구성 전략/모드 확인 가능

📄 **`Config_Impl.rpt`** + **`Partial_Bit_Config_Summary.rpt`**

🔍 **주요 파싱 위치**

- `Config_Impl.rpt`: 전원/설정 절차 일관성 및 FPGA Configuration 모드 설정(JTAG/SPI 등)
- `Partial_Bit_Config_Summary.rpt`: PR 적용 시 구성 시퀀스 무결성 파악

🧩 **파싱 로직**

```python
# 1) Config Impl 설정
pattern_run_name = r'Run Name\s+:\s+(\S+)'
pattern_strategy = r'Strategy\s+:\s+(.+)'
pattern_status = r'Run Status\s+:\s+(.+)'
pattern_version = r'Vivado Version\s+:\s+([\d.]+)'

# 2) Configuration Mode 확인 (xdc constraint에서)
# set_property CONFIG_MODE Slave_selectmap/Master_SPI/JTAG 등
# → xdc 파일 미포함 시 리포트에서만 유추

# 3) INIT_B, DONE 핀 활성화 확인
# → IO_Report.rpt에서 INIT_B, DONE, PROGRAM_B 핀 확인
pattern_config_pins = r'\|\s+(INIT_B|DONE|PROGRAM_B|TCK|TMS|TDI|TDO)\s+\|'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `run_name` | `ip_blk_tdpram_16x512_impl_1` |
| `strategy` | Vivado Implementation Defaults |
| `place_directive` | Default |
| `route_directive` | Default |
| `run_status` | **Not started** ⚠️ |
| `max_threads` | 8 |
| `vivado_version` | 2019.2 |
| `pr_used` | No (PR_NA_Evidence) |

> ⚠️ **`Config_Impl.rpt`의 Run Status "Not started"**: 이 파일은 특정 IP(ip_blk_tdpram_16x512)의 서브 구현 설정으로, 메인 설계의 구성 전략이 아님. 주 설계는 별도 Top-Level Config 참조.

⚖️ **판정 로직**

```python
def judge_q28(config_data):
    issues = []
    if config_data['status'] == 'Not started':
        issues.append("Config_Impl.rpt: IP 서브구현 미실행 상태 (IP 전용 설정 파일)")
    if not config_data['pr_used']:
        issues.append("Partial Reconfiguration 미사용")
    return "REVIEW", ("전략: Defaults. PR: 미사용. "
                     "주 설계 파워업 시퀀스(INIT_B, DONE 핀 제어, 구성 모드) 확인 필요.")
```

💬 **예상 답변**
> **REVIEW** — 구현 전략: Vivado Implementation Defaults. PR(부분 재구성) 미사용. ⚠️ Config_Impl.rpt는 IP 전용 파일(Not started). 메인 설계의 Config Mode(Master SPI/JTAG 등), INIT_B/DONE 핀 제어, 파워업 시퀀스는 XDC/보드 설계에서 별도 확인 필요.

---

## Q29: 회로 초기화·이상 복구·블록 간 신호 전달 설계 확인

> *회로 초기화, 이상 상태 복구, 기능 블록 간 신호 전달 설계에 문제가 없음을 확인했습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **`Waiver.rpt`** + **`CDC_Report.rpt`** + **`DRC_Report.rpt`**

🔍 **Waiver.rpt 파싱 위치**

- `Waiver Summary` 섹션 내 CDC / DRC 타입별 구조화된 예외 처리(Waived) 건수

🔍 **CDC_Report.rpt 파싱 위치**

- `Clock Domain Crossing` 요약 테이블 (Safe/Unsafe 매핑 및 Unknown/No Common Primary Clock 검출)

🔍 **DRC_Report.rpt 파싱 위치**

- `DRC Violations` 요약 또는 상단 Summary 섹션의 규칙 위반 심각도별 건수 (Error, Critical Warning)

🧩 **파싱 로직**

```python
# 1) Waiver Summary 파싱
pattern_waiver_cdc = r'\|\s*CDC\s*\|\s*(\d+)\s*\|'

# 2) CDC_Report의 위험성 경로 추출
pattern_cdc_unsafe = r'(?i)Total\s+Unsafe\s*\|\s*(\d+)'

# 3) DRC_Report 심각도 요약 추출
pattern_drc_errors = r'(?i)Errors\s*:\s*(\d+)'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `waiver_cdc_count` | 69 |
| `cdc_unsafe_endpoints` | 0 |
| `drc_violations_active` | 9359 |

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 회로 초기화 시퀀스 및 이상 복구 설계는 설계 문서 검토 필요. 참고 추적 정보: CDC 69건 Waived (비동기 신호 존재), DRC 9359건 미해결 상태. 각 항목에 대한 설계 검토 및 복구 시퀀스 결과 보고서를 제출해 주세요.

---

## Q30: PCB 외부 종단 처리(Pull-up/down) 구성 전 상태 포함 규정 여부

> *보드 상의 외부 종단 처리(Pull-up/down)가 FPGA 구성 전의 동작 상태를 포함하여 규정되었습니까?*

- **답변 유형**: `SEMI` — IO 기본 상태 확인 가능

📄 **`IO_Report.rpt`**

🔍 **파싱 위치**

- IO Report의 `SLEW`, `DRIVE`, `PULLTYPE`, `IN_TERM`, `OUT_TERM` 컬럼
- 특히 미설정(공란) 핀의 Pull-up/down 상태

🧩 **파싱 로직**

```python
# 1) IO Pull 설정 확인
pattern_io_pull = r'\|\s+(\S+)\s+\|.*?\|\s+(PULLUP|PULLDOWN|KEEPER|NONE|\s*)\s+\|'

# 2) 구성 전 상태 분류
# - Config 핀 (TCK, TMS, TDO, TDI, INIT_B, DONE, PROGRAM_B): Xilinx 기본 Pull
# - 사용자 IO: PCB 설계 의존

# 3) IO Bank별 Drive/Slew 설정
pattern_io_drive = r'\|\s+\d+\s+\|\s+(\w+)\s+\|\s+(\w+)\s+\|\s+(\d+)\s+\|'
# Encoding: Bank, IO Standard, Drive, Slew

# 4) 입력 전용 핀의 Pull 상태 확인
pattern_input_only = r'\|\s+(\S+)\s+\|\s+I\s+\|.*?\|\s+(PULLUP|PULLDOWN|NONE)\s+\|'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `pullup_count` | 확인 필요 (IO_Report 상세 분석 필요) |
| `pulldown_count` | 확인 필요 |
| `no_pull_input_count` | 확인 필요 |
| `config_pins_pull` | Xilinx 기본값 (INIT_B: Pull-up, PROGRAM_B: Pull-up) |
| `pre_config_state` | EVIDENCE_NEEDED (PCB 설계 문서 필요) |

⚖️ **판정 로직**

```python
def judge_q30(io_data):
    unspecified = [p for p in io_data['input_pins'] if p['pull'] == 'NONE']
    if unspecified:
        return "REVIEW", (f"Pull 미설정 입력 핀 {len(unspecified)}개. "
                         "구성 전 플로팅 상태 위험. PCB Pull-up/down 설계 확인 필요.")
    return "REVIEW", "IO Pull 설정 확인. 구성 전 상태는 PCB 회로도 대비 별도 검토 필요."
```

💬 **예상 답변**
> **REVIEW** — IO_Report에서 PULLTYPE 컬럼 확인. ⚠️ FPGA 구성 전(Pre-configuration) 상태에서 IO 핀의 High-Z 및 Pull-up/down 설정이 오작동을 유발하지 않는지 PCB 회로도 기반 별도 검토 필요. Configuration 핀(INIT_B, PROGRAM_B)은 Xilinx 기본 Pull-up 내장.

---

## 요약 — Q21~Q30 파싱 구현 우선순위

| 우선순위 | 문항 | 답변 유형 | 파서 구현 | 리포트 |
|---------|------|----------|----------|------------|
| ⬆️ 높음 | Q22 | AUTO | `ram_parser.py` | RAM_Utilization, Methodology |
| ⬆️ 높음 | Q27 | AUTO | `clock_parser.py` 등 | Clocks_Summary, Property_Check, PR_DRC_Report |
| 🔹 중간 | Q21 | SEMI | Q20 파서 확장 + ECC 컬럼 검사 | RAM_Utilization, IO_Report |
| 🔹 중간 | Q24 | SEMI | `io_parser.py` 재사용 | Datasheet, IO_Report |
| 🔹 중간 | Q25 | SEMI | `power_parser.py` 등 | Power_Data, Power_Report, Datasheet, Operating_Cond |
| 🔹 중간 | Q26 | SEMI | `pr_parser.py` 등 | PR_Verify_Report, Partial_Bit_Config_Summary |
| 🔹 중간 | Q28 | SEMI | `environment_parser.py` 등 | Config_Impl, Partial_Bit_Config_Summary |
| 🔹 중간 | Q30 | SEMI | `io_parser.py` 재사용 | IO_Report |
| ⬇️ 낮음 | Q29 | EVIDENCE_NEEDED | 없음 (Waiver 참고) | Waiver, CDC_Report, DRC_Report |
| ⬇️ 낮음 | Q23 | EVIDENCE_NEEDED | 없음 | — |

## 주요 관찰 사항

> **Q22 (DPRAM)**: True Dual Port RAM 0개 → **PASS** 가능
>
> **Q27 (하드 매크로)**: Property_Check.rpt에 18개 클럭 완전 기술 → **PASS** 자동화 가능
>
> **Q26 (인서비스)**: `PR_NA_Evidence.txt` 존재 — PR 미사용 확인되나 Full Reconfiguration 방식 설명 필요
>
> **Q29**: CDC 69개 Waived (4 Waiver Rules), DRC 9359건 미해결 — 설계 검토 근거 필요
