# Q31~Q40 상세 파싱 계획서

## 범례

| 기호 | 의미 |
|------|------|
| 📄 | 참조 리포트 |
| 🔍 | 파싱 대상 위치 |
| 🧩 | 정규식 / 파싱 로직 |
| 📊 | 추출 결과 필드 |
| ⚖️ | 판정 기준 |
| 💬 | 예상 답변 예시 |

---

## Q31: 클럭 입력 파형·지터 검증 절차 수립

> *버짓 시뮬레이션이나 평가 보드를 통해 동작 특성(파형, 지터 등)을 확인하는 프로세스가 있습니까?*

- **답변 유형**: `SEMI` — MMCM/PLL 파라미터에서 Jitter 확인 가능

📄 **`Property_Check.rpt`** (05/) + **`Clock_Utilization.rpt`** (01/)

🔍 **파싱 위치**

- `Property_Check.rpt`: 각 클럭 블록의 `INPUT_JITTER` / `SYSTEM_JITTER` / `PERIOD` 값
- `Clock_Utilization.rpt`: MMCM/PLL 섹션의 Input Frequency, VCO 주파수, Phase 파라미터

🧩 **파싱 로직**

```python
# 1) Property_Check에서 클럭별 Jitter 추출
# 각 클럭 블록: NAME → period, input_jitter, system_jitter
pattern_name   = r'NAME\s+string\s+true\s+(\S+)'
pattern_period = r'PERIOD\s+double\s+true\s+([\d.]+)'
pattern_jitter = r'INPUT_JITTER\s+double\s+true\s+([\d.]+)'
pattern_sys_jitter = r'SYSTEM_JITTER\s+double\s+true\s+([\d.]+)'

# 2) Jitter 비율 계산 (Jitter / Period × 100%)
# Xilinx 권장: Input Jitter < 3% of period
def jitter_ratio(j, p): return round(j/p*100, 2)

# 3) Clock_Utilization에서 MMCM 상세 파라미터
pattern_vco = r'VCO Frequency\s*\(MHz\)\s*\|.*?\|\s*([\d.]+)\s*\|'
pattern_input_freq = r'Input Frequency\s*\(MHz\)\s*\|.*?\|\s*([\d.]+)'
```

📊 **추출 결과**

| 클럭 입력 | Period (ns) | Input Jitter (ns) | Jitter% |
|----------|------------|------------------|---------|
| `pin_i_fmc_clk` | 23.148 | 0.231 | 1.0% |
| `pin_i_clk_78m` | 12.820 | 0.128 | 1.0% |
| `pin_i_clk_20m` | 50.000 | 0.500 | 1.0% |
| `pin_i_clk_100m` | 10.000 | 0.100 | 1.0% |

⚖️ **판정 로직**

```python
def judge_q31(clk_list, criteria):
    jitter_th = criteria['clocking']['jitter_max_pct'] # 예: 3.0
    violations = [c for c in clk_list if c['jitter_pct'] > jitter_th]
    if violations:
        return "REVIEW", f"Jitter > {jitter_th}% clk: {[c['name'] for c in violations]}"
    return "REVIEW", (
        "입력 클럭 4개 Jitter 모두 1.0% — 파라미터 이내. "
        "⚠️ 실제 클럭 파형/지터 검증(오실로스코프/스펙트럼 분석기)은 "
        "보드 레벨 측정 결과 제출 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — 입력 클럭 4개(FMC 43.2MHz, 78MHz, 20MHz, 100MHz) INPUT_JITTER 모두 1.0% 이내. MMCM/PLL 파라미터 이내. ⚠️ 실제 보드 파형/지터 측정 결과(오실로스코프 캡처, Clock Jitter Cleaner 사용 여부 등) 별도 제출 필요.

---

## Q32: 클럭 입력 손실 조건 명확 정의 여부

> *FPGA로 입력되는 클럭이 단절(Loss)되는 조건이 명확합니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Clock_Networks.rpt`** (01/) + **`Check_Timing.rpt`** (01/)

🔍 **파싱 위치**

- `Clock_Networks.rpt`: 사용자 클럭 포트 목록, 주파수 및 엔드포인트 테이블
- `Check_Timing.rpt`: `checking no_clock` 섹션의 검사 결과 (모든 레지스터에 클럭이 인가되는지)

🧩 **파싱 로직**

```python
# 1) Constrained 클럭 목록 추출
pattern_clk_port = r'Clock (\S+) \(([\d.]+)MHz\)\(endpoints: (\d+) clock, (\d+) nonclock\)'
# → 포트명, 주파수, clock endpoint 수, nonclock endpoint 수

# 2) no_clock 항목 수 확인
pattern_no_clock = r'There are (\d+) register/latch pins with no clock'

# 3) constant_clock 항목 수 확인
pattern_const_clock = r'There are (\d+) register/latch pins with constant_clock'
```

📊 **추출 결과**

| 클럭 포트 | 주파수 | Clock EP | Nonclock EP |
|----------|-------|---------|------------|
| `pin_i_fmc_clk` | 43.2 MHz | 2258 | 1 |
| `pin_i_clk_78m` | 78.0 MHz | 214 | 1 |
| `pin_i_clk_20m` | 20.0 MHz | 33815 | 2 |
| `pin_i_clk_100m` | 100.0 MHz | 5615 | 146 |

| 항목 | 값 |
|-----|---|
| `no_clock` 핀 수 | **0** ✅ |
| `constant_clock` 핀 수 | **0** ✅ |
| `loops` 수 | **0** ✅ |

⚖️ **판정 로직**

```python
def judge_q32(data, criteria):
    if data['no_clock'] == 0 and data['const_clock'] == 0:
        return "PASS", (
            f"클럭 {data['clk_count']}개 정의: "
            f"FMC 43.2MHz, 78MHz, 20MHz, 100MHz. "
            f"no_clock=0, constant_clock=0. 모든 플립플롭에 클럭 정의 완료."
        )
    return "REVIEW", f"no_clock={data['no_clock']}, constant_clock={data['const_clock']} 점검 필요"
```

💬 **예상 답변**
> **PASS** — 클럭 4개 정의: FMC(43.2MHz), 78MHz, 20MHz, 100MHz. no_clock=0 / constant_clock=0. 모든 플립플롭에 클럭 제약 완전 정의. 클럭 입력 손실 조건이 XDC에서 명확히 정의됨.

---

## Q33: 클럭 손실 검출 회로 적절성 확인

> *클럭 단절 감지 및 처리 회로가 적절하게 설계되었습니까?*

- **답변 유형**: `SEMI` — locked 신호 존재 확인 가능

📄 **`CDC_Report.rpt`** (01/) + **`Clock_Networks.rpt`** (01/)

🔍 **파싱 위치**

- `CDC_Report.rpt`: MMCM/PLL `locked` 관련 레지스터(예: `r_fmc_clk_locked_reg` 등)가 타 도메인으로 교차(CDC)하는 항목 추적
  → 클럭 locked 신호가 다른 도메인으로 동기화됨을 파악하여 클럭 단절 감지 회로 유무 확인
- `Clock_Networks.rpt`: 클럭 루트 구조 및 MMCM 생성 블록 확인

🧩 **파싱 로직**

```python
# 1) 'locked' 신호 CDC 경로 탐색
pattern_locked_cdc = r'(\S*locked\S*|LOCKED)'

# 2) MMCM locked 신호 존재 여부
import re
# 파일 경로는 report_finder를 통해 동적으로 전달받음
with open(report_paths['CDC_Report.rpt'], 'r') as f:
    cdc_text = f.read()
locked_signals = re.findall(r'(\S*(?:locked|LOCKED|clk_lock)\S*)', cdc_text)

# 3) r_fmc_clk_locked 관련 CDC 경로 확인 (줄 239)
# → CDC-3 Info: 1-bit synchronized ASYNC_REG property depth=3
# Source: u_phy_fmc/r_fmc_clk_locked_reg
# Dest: u_sys_top_with_ddr3/u_sys_clock_lock_reg/r_fmc_clk_locked_meta_reg
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `fmc_locked_cdc` | CDC-3 Info, depth=3, ASYNC_REG OK |
| `mmcm_locked_signals` | `r_fmc_clk_locked_reg` (FMC MMCM) |
| `init_calib_complete` | CDC-2 Warning (missing ASYNC_REG, DDR3 MIG) |
| `clock_lock_monitor` | `u_sys_clock_lock_reg` 존재 |

⚖️ **판정 로직**

```python
def judge_q33(cdc_data):
    issues = []
    if cdc_data.get('init_calib_cdc_type') == 'CDC-2':  # missing ASYNC_REG
        issues.append("DDR3 init_calib_complete: CDC-2 (ASYNC_REG 미설정)")
    return "REVIEW", (
        f"FMC 클럭 locked → u_sys_clock_lock_reg 동기화 설계 확인(CDC-3/ASYNC_REG). "
        + ("; ".join(issues) + " — 보완 필요." if issues else " 설계 적절.")
    )
```

💬 **예상 답변**
> **REVIEW** — FMC 클럭 locked(`r_fmc_clk_locked_reg`) → `u_sys_clock_lock_reg` 동기화 설계 확인(CDC-3, ASYNC_REG depth=3, 적정). ⚠️ DDR3 `init_calib_complete`는 CDC-2(ASYNC_REG 미설정 Warning) — ASYNC_REG 속성 추가 권장. 78MHz/20MHz/100MHz 클럭 손실 검출 회로 존재 여부는 RTL 확인 필요.

---

## Q34: 모든 클럭 입력 정지 상황 검토

> *모든 클럭 입력이 정지할 가능성을 고려하여 회로를 설계했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Check_Timing.rpt`** (01/) + **`Clock_Networks.rpt`** (01/)

🔍 **파싱 위치**

- `Check_Timing.rpt`: `checking no_clock` 섹션의 핀 수 (클럭 공백 여부 판단)
- `Check_Timing.rpt`: `checking constant_clock` 섹션의 핀 수 (완전 고정 시계열 오류 판단)
- `Clock_Networks.rpt`: 모든 프라이머리/기본 클럭 리소스의 소스 패드(`Port`) 유무

🧩 **파싱 로직**

```python
# 1) 외부 클럭 포트 목록 확인 (모두 외부 입력)
pattern_port = r'Port (pin_i_\w+)'
clk_ports = re.findall(pattern_port, clock_networks_text)
# → ['pin_i_fmc_clk', 'pin_i_clk_78m', 'pin_i_clk_20m', 'pin_i_clk_100m']

# 2) 내부 생성 클럭 없음 (IS_USER_GENERATED=False for all)
# 모든 클럭은 외부 포트 기원 → 단일 클럭 공급 중단 시 영향 분석 필요

# 3) 판정 기준: 클럭 전체 정지는 설계 레벨 확인 사항 (RTL 구현 필요)
ALL_CLOCKS_EXTERNAL = len(clk_ports) == 4 and all('pin_i' in p for p in clk_ports)
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| 외부 클럭 포트 | 4개 (모두 `pin_i_` 접두사) |
| 내부 생성 클럭 | 4개 MMCM + 다수 PLL 파생 클럭 |
| `no_clock` | 0 ✅ |
| 클럭 전체 정지 설계 | EVIDENCE_NEEDED (RTL 검토 필요) |

⚖️ **판정 로직**

```python
def judge_q34(data, criteria):
    return "REVIEW", (
        "외부 클럭 4개 모두 정의됨. "
        "MMCM/PLL lock 손실 시 downstream 클럭 자동 정지. "
        "⚠️ 클럭 전체 정지(모든 4개 동시 손실 시) 대응 설계(watchdog, 안전 상태)는 "
        "RTL 검토 및 안전 요구사항 문서 확인 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — 클럭 4개 모두 외부 입력 포트. MMCM/PLL 미잠금(lock=0) 시 파생 클럭 정지 → 플립플롭 고정. ⚠️ 모든 클럭 동시 손실 대응(예: PROG_B 재구성, 외부 Watchdog, 안전 상태 유지) 은 RTL 및 시스템 안전 설계 문서에서 확인 필요.

---

## Q35: 클럭 손실 검출 불능 조건 확인

> *클럭 단절 감지가 불가능해지는 조건이 있습니까? 있다면 명시해 주세요.*

- **답변 유형**: `SEMI` — Timing Check 결과로 부분 확인

📄 **`Check_Timing.rpt`** (01/) + **`Pulse_Width.rpt`** (01/)

🔍 **파싱 위치**

- `Check_Timing.rpt`: `checking multiple_clock` 섹션 (복수 클럭 할당 오류를 통한 검출 회로 레이스 가능성 타제)
- `Check_Timing.rpt`: `checking latch_loops` 섹션 (래치 기반 루프 구조 검색)
- `Pulse_Width.rpt`: 최소/최대 펄스 폭 위반 항목 (글리치 등의 위험 요소 확인)

🧩 **파싱 로직**

```python
# 1) multiple_clock 핀 수 (복수 클럭 → 검출 회로에 잠재 Race 조건)
pattern_multi_clk = r'There are (\d+) register/latch pins with multiple clocks'

# 2) latch_loops 확인
pattern_latch = r'There are (\d+) combinational latch loops'

# 3) Pulse_Width.rpt에서 위반 항목 수 파악
# → 펄스 폭 위반은 클럭 손실 직전 글리치 조건에 해당할 수 있음
pattern_pw_fail = r'(CRITICAL WARNING|ERROR).*?WPW|Pulse_Width'
```

📊 **추출 결과**

| 항목 | 값 |
|-----|---|
| `multiple_clock` 핀 | 0 ✅ |
| `latch_loops` | 0 ✅ |
| `combinational loops` | 0 ✅ |
| `Pulse_Width.rpt` | 별도 분석 필요 (41879 bytes) |
| 글리치/Race 조건 | SEMI — RTL 기반 추가 확인 필요 |

⚖️ **판정 로직**

```python
def judge_q35(data, criteria):
    return "REVIEW", (
        "multiple_clock=0, latch_loops=0, combinational_loops=0 — 구조적 Race 없음. "
        "⚠️ Pulse_Width 위반/글리치 조건 및 MMCM 재잠금 구간 동안 "
        "locked=0인 상태에서의 클럭 손실 미검출 가능성은 시나리오 검토 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — multiple_clock=0, latch_loops=0 — 구조적 Race 조건 없음. ⚠️ MMCM 재잠금 과정(locked glitch 구간)에서 클럭 손실 미검출 가능성, 클럭 전환 직후 글리치 시나리오에 대한 시뮬레이션/검토 결과 제출 필요.

---

## Q36: 다중 리셋 기반 정상 리셋/이상 복구 분리 여부

> *다중 리셋이 입력되어도 정상적으로 리셋 및 복구되도록 설계되었습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **`CDC_Report.rpt`** 참고 (리셋 CDC 경로 확인)

🔍 **참고 정보**

- `CDC_Report.rpt`: 비동기 리셋 동기화 관련 항목 (`CDC-9 Info`, `CDC-8 Warning` 구조 파악)
  - `ASYNC_REG` 속성이 올바르게 매핑되어 동기화 메커니즘을 탔는지 교차 확인

📊 **관련 데이터**

| 항목 | 값 |
|-----|---|
| `CDC-8` (비동기 리셋 ASYNC_REG 미설정) | **1건** ⚠️ |
| `CDC-9` (비동기 리셋 ASYNC_REG 정상) | 2건 ✅ |
| 정상/비정상 리셋 분리 설계 | RTL 확인 필요 |

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 참고: CDC-8 Warning(비동기 리셋 ASYNC_REG 미설정) 1건 — 보완 필요. 정상 리셋과 이상 복구 리셋의 분리 설계(별도 리셋 소스, 우선순위 로직, 리셋 시퀀서)는 RTL 구조 및 설계 문서 확인 필요.

---

## Q37: 클럭 전환 회로 사용 여부 및 회피/타당성 확인

> *클럭 전환(Switching) 회로를 사용합니까? (가급적 사용하지 않는 것을 권장함)*

- **답변 유형**: `SEMI` — Clock Utilization 및 Clock Networks 확인, Timing_Exceptions에서 clock_group 확인

📄 **`Clock_Utilization.rpt`** + **`Timing_Exceptions.rpt`** + **`Clock_Networks.rpt`**

🔍 **주요 파싱 위치**

- `Clock_Utilization.rpt`: `BUFGMUX`, `BUFCTRL` 등 클럭 믹스/전환 컴포넌트 프리미티브 사용 건수 파악
- `Timing_Exceptions.rpt`: `set_clock_groups` 예외 파악을 통한 클럭 격리 또는 멀티플렉스 확인
- `Clock_Networks.rpt`: 클럭 트리 노드상 스위칭/오버랩 구간 파악

🧩 **파싱 로직**

```python
# 1) set_clock_groups 예외 쌍 파악 (비동기 클럭 그룹 선언)
pattern_clk_group = r'\d+\s+\[get_clocks \{([^\}]+)\}\]\s+\[get_clocks \{([^\}]+)\}\]\s+clock_group'
clk_groups = re.findall(pattern_clk_group, exceptions_text)

# 2) BUFGMUX (클럭 전환 버퍼) 사용 여부 확인
# → Clock_Utilization.rpt에서 BUFGMUX 인스턴스 탐색
pattern_bufgmux = r'BUFGMUX|CLK_SWITCH'

# 3) 클럭 전환 회로 패턴 탐색
pattern_clk_sel = r'clk_sel|clk_switch|CLK_SEL|CLOCK_MUX'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `set_clock_groups` 쌍 | 49쌍 (비동기 그룹 선언) |
| 상태 | Non-existent path가 대부분 |
| `BUFGMUX` 사용 | 확인 필요 (Clock_Utilization 분석) |
| 클럭 전환 신호 | CDC_Report에서 미검출 |

⚖️ **판정 로직**

```python
def judge_q37(data, criteria):
    if data.get('bufgmux_count', 0) > 0:
        return "REVIEW", f"BUFGMUX {data['bufgmux_count']}개 사용 — 클럭 전환 타이밍 검증 필요"
    return "REVIEW", (
        "set_clock_groups 49쌍 선언 → 클럭 도메인 격리 완료. "
        "Non-existent path 다수(실제 경로 없음). "
        "BUFGMUX 사용 여부 Clock_Utilization 추가 확인 권장."
    )
```

💬 **예상 답변**
> **REVIEW** — set_clock_groups 49쌍 선언, 대부분 Non-existent path(실제 교차 없음). 4개 클럭 도메인은 MMCM 출력으로 독립 유지 설계. ⚠️ BUFGMUX(클럭 전환 MUX) 사용 여부는 Clock_Utilization.rpt 추가 확인 권장. 클럭 전환 회로 사용 시 Glitch-Free 설계 근거 제출 필요.

---

## Q38: 클럭 전환 전후 타이밍 보증

> *클럭 전환 회로 사용 시, 전환 전후의 각 클럭에 대해 타이밍이 보장됩니까?*

- **답변 유형**: `SEMI` — Timing_Exceptions에서 일부 확인

📄 **`Timing_Exceptions.rpt`** (01/) + **`Bus_Skew.rpt`** (01/)

🔍 **파싱 위치**

- `Bus_Skew.rpt`: 대용량 리포트 내의 `WBS(Worst Bus Skew)` 요약 분석 결과
- `Timing_Exceptions.rpt`: `set_multicycle_path` 파라미터(설정 `cycles=6` 등 타이밍 마진 조율 패턴 확인)
- `Timing_Exceptions.rpt`: `set_clock_groups` 선언 내역 (전환 과정 타임 위반 방어 논리)

🧩 **파싱 로직**

```python
# 1) Multicycle Path 설정 (클럭 간 타이밍 여유)
pattern_mcp = r'\d+\s+\[get_cells.*?\]\s+.*?cycles=(\d+(?:\(start\))?)'
multicycle_paths = re.findall(pattern_mcp, exceptions_text)

# 2) Bus_Skew에서 위반 항목 확인
# Bus_Skew.rpt는 263KB로 대용량 → 헤더/요약 줄만 파싱
pattern_skew_fail = r'WBS\s+([\d.-]+)\s+ns'  # Worst Bus Skew
pattern_skew_slack = r'Slack\s*:\s*([\d.-]+)\s*ns'  # 음수이면 위반

# 3) set_max_delay in Timing_Exceptions
pattern_max_delay = r'max_dpo=(\d+)'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| Multicycle Path | MIG PHY: Setup cycles=6, Hold cycles=5 |
| max_dpo | 5 (rstdiv0 → PHY_CONTROL RESET) |
| set_clock_groups | 49쌍 (타이밍 제외 선언) |
| Bus Skew | 별도 분석 필요 (263KB) |
| False Path | MIG 내부 + u_sys_power_loader |

⚖️ **판정 로직**

```python
def judge_q38(data, criteria):
    return "REVIEW", (
        "MIG PHY multicycle 설정(Setup×6/Hold×5) — 벤더 기본 제약. "
        "set_clock_groups으로 비동기 도메인 간 타이밍 예외 선언. "
        "⚠️ Bus_Skew.rpt 세부 분석 및 실제 클럭 전환 시나리오 타이밍 검증 결과 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — MIG PHY 내부 multicycle 경로 설정(Setup=6, Hold=5, Xilinx 표준). 비동기 클럭 간 set_clock_groups 선언으로 타이밍 분석 제외. ⚠️ Bus_Skew.rpt 상세 분석 및 클럭 전환 전후 설정·보류 시간 보증(측정값)을 제출해 주세요.

---

## Q39: FPGA 내부 비동기 클럭 회로 분류 및 확인

> *FPGA 내부에 비동기 클럭 회로가 있습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`**

🔍 **주요 파싱 위치**

- `CDC_Report.rpt`, `CDC_Critical.rpt`, : 비동기 클럭 교차(CDC) 유형 요약 및 안전하지/위험도 높은 CDC 식별
- `CDC_Interaction.rpt`: 도메인별 결합 상태 파악
- 각 CDC 유형별 건수 및 Waived 건수
- `Timing_Exceptions.rpt`: `set_clock_groups`, `set_false_path` 등 예외 적용 상황

🧩 **파싱 로직**

```python
# 1) CDC 요약 테이블 파싱
pattern_cdc_summary = r'(CDC-\d+)\s+(Warning|Info)\s+(\d+)\s+(.*)'
# → [(id, severity, count, description), ...]

# 2) Waived CDC 항목 파싱
pattern_waived = r'(CDC-\d+)\s+(\d+)'  # in waived section
# Results: CDC-1: 63, CDC-10: 2, CDC-13: 4

# 3) 비동기 클럭 도메인 쌍 추출 (Timing_Exceptions)
# 실제 경로 있는 set_clock_groups 쌍만 (Non-existent 제외)
pattern_actual_path = r'\[get_clocks \{([^\}]+)\}\]\s+\[get_clocks \{([^\}]+)\}\]\s+clock_group\s+clock_group\s*$'
```

📊 **추출 결과**

| CDC 유형 | Severity | 건수 | 설명 |
|---------|---------|-----|------|
| CDC-2 | Warning | 2 | 1-bit sync, ASYNC_REG 미설정 |
| CDC-3 | Info | 40 | 1-bit sync, ASYNC_REG 정상 |
| CDC-6 | Warning | 21 | Multi-bit sync, ASYNC_REG 있음 |
| CDC-8 | Warning | 1 | 비동기 리셋 ASYNC_REG 미설정 |
| CDC-9 | Info | 2 | 비동기 리셋 ASYNC_REG 정상 |
| CDC-15 | Warning | 475 | Clock Enable 제어 CDC |
| **합계** | | **541** | |
| **Waived** | | **69** | CDC-1: 63, CDC-10: 2, CDC-13: 4 |

**실제 교차 경로 클럭 도메인 쌍:**

- `lcos_pclk` ↔ `fmc_clk`
- `ddr3_clk` ↔ `lcos_pclk`
- `clk_pll_i` ↔ `lcos_pclk`
- `lcos_pclk` ↔ `lcos_sftcck`
- `lcos_pclk` ↔ `power_loader`

⚖️ **판정 로직**

```python
def judge_q39(cdc_data):
    warning_cnt = sum(c['count'] for c in cdc_data if c['severity'] == 'Warning')
    info_cnt = sum(c['count'] for c in cdc_data if c['severity'] == 'Info')
    problem = []
    if cdc_data.get('CDC-2', 0) > 0: problem.append(f"CDC-2 {cdc_data['CDC-2']}건(ASYNC_REG 미설정)")
    if cdc_data.get('CDC-8', 0) > 0: problem.append(f"CDC-8 {cdc_data['CDC-8']}건(리셋 ASYNC_REG 미설정)")
    if problem:
        return "REVIEW", (
            f"총 CDC {warning_cnt}건 Warning + {info_cnt}건 Info. "
            f"⚠️ {'; '.join(problem)} — 보완 필요. "
            f"Waived 69건은 Waiver.rpt 확인."
        )
    return "PASS", f"CDC 분류 완료. Warning {warning_cnt}건/Info {info_cnt}건"
```

💬 **예상 답변**
> **REVIEW** — 비동기 클럭 도메인 쌍 5개 식별 완료. CDC 총 541건(Warning 499 / Info 44), Waived 69건. ⚠️ CDC-2 2건(1-bit sync ASYNC_REG 미설정) + CDC-8 1건(비동기 리셋 ASYNC_REG 미설정) — ASYNC_REG 속성 추가 필요. CDC-15(Clock Enable CDC) 475건은 Xilinx FIFO IP 내부 구조로 설계 패턴 확인 필요.

---

## Q40: 비동기 클럭 메모리 회로 CDC 설계

> *클럭 도메인 변경(CDC)을 포함하여 비동기 클럭을 사용하는 메모리 회로가 있습니까?*

- **답변 유형**: `SEMI`

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`**

🔍 **주요 CDC 분석 포인트**

- `CDC_Report`에서 다중 비트 동기화(Multi-bit), FIFO 기반 비동기 교차 식별 건 파악
- `Timing_Exceptions` 및 `CDC_Critical`를 활용, 비동기 메모리(RAM/FIFO) 포인터 간 타이밍 제약 위반 여부 확인

📊 **추출 결과(예시)**

| 관련 인스턴스/회로 | 클럭 도메인쌍 | CDC 방식 / 안전성(안전/Unsafe) |
|-------------|--------|---------|
| `ip_fifo_indep...` | `lcos_pclk` ↔ `fmc_clk` | FIFO 기반 / Info (안전) |
| *기타 다중 리포트 연산 결과* | 확인 필요 | 확인 필요 |

⚖️ **판정 로직**

```python
def judge_q40(cdc_data):
    if cdc_data.get('unsafe_fifo_critical', 0) > 0:
        return "REVIEW", "Unsafe CDC 항목에서 비동기 메모리 교차 경로 검출됨. 확인 필요."
    return "REVIEW", "관련 CDC 매핑 및 Timing_Exceptions 확인 완료. 세부 보장 확인 요망."
```

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 비동기 FIFO(CDC-15, 475건): Xilinx `ip_fifo_indep_48x16` IP 내부(Gray Code 포인터, 벤더 보증). Multi-bit CDC(CDC-6, 21건): 사용자 정의 `lib_cdc_*` 모듈에서 ASYNC_REG 2-stage 동기화 사용. ⚠️ `lib_cdc` 모듈의 유효성(CDC 설계 검토서, FIFO 깊이 여유도 분석) 제출 필요.

---

## 요약 — Q31~Q40 파싱 구현 우선순위

| 우선순위 | 질문 | 답변 유형 | 파서 구현 | 리포트 |
|---------|------|----------|----------|------------|
| ⬆️ 높음 | Q32 | AUTO | `clock_parser.py` | Clock_Networks, Check_Timing |
| ⬆️ 높음 | Q34 | AUTO | 재사용 | Check_Timing, Clock_Networks |
| ⬆️ 높음 | Q37 | SEMI | `exception_parser.py` 등 | Clock_Utilization, Timing_Exceptions, Clock_Networks |
| ⬆️ 높음 | Q39 | AUTO | `cdc_parser.py` 등 | CDC_Report, CDC_Critical, CDC_Interaction, Timing_Exceptions |
| ⬆️ 높음 | Q40 | SEMI | `cdc_parser.py` 등 | CDC_Report, CDC_Critical, CDC_Interaction, Timing_Exceptions |
| 🔹 중간 | Q31 | SEMI | `clock_parser.py` 재사용 | Property_Check, Clock_Utilization |
| 🔹 중간 | Q33 | SEMI | `cdc_parser.py` 확장 | CDC_Report, Clock_Networks |
| 🔹 중간 | Q35 | SEMI | `timing_parser.py` 재사용 | Check_Timing, Pulse_Width |
| 🔹 중간 | Q38 | SEMI | `exception_parser.py` 재사용 | Bus_Skew, Timing_Exceptions |
| ⬇️ 낮음 | Q36 | EVIDENCE | 없음 | CDC_Report 참고 |

## 주요 관찰 사항

> **Q32**: `no_clock=0`, `constant_clock=0`, `loops=0` → **PASS** 자동화 가능
>
> **Q39**: CDC 총 541건 중 3건 보완 필요(CDC-2 × 2, CDC-8 × 1) — Critical 이슈 식별
>
> **Q40**: CDC-15 475건은 Xilinx IP 내부(정상) — 사용자 정의 CDC-6 21건이 핵심 검토 대상
>
> **핵심 이슈**: CDC-2 2건(ASYNC_REG 미설정), CDC-8 1건(리셋 ASYNC_REG 미설정) — 반드시 보완 권고
