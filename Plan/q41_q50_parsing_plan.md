# Q41~Q50 상세 파싱 계획서

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

## Q41: 클럭 전환 회로 글리치·해저드·듀티 불균형 방지

> *클럭 전환 회로가 글리치, 해저드, 듀티 불균형 등을 방지하도록 구성되어 있습니까?*

- **답변 유형**: `SEMI` — Clock_Networks 및 CDC 관련 내용 확인

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Unsafe.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`** + **`Clock_Networks.rpt`** + **`Clock_Utilization.rpt`**

🔍 **파싱 위치**

- `Clock_Utilization.rpt`: `Clock Primitive Utilization` 섹션 (BUFGMUX 등 사용 여부 파악)
- `Clock_Utilization.rpt`: `Global Clock Resources` 섹션의 `Driver Type` 컬럼 확인
- `Clock_Networks.rpt`: 클럭 경로 상의 글리치/해저드 발생 가능 지점 (BUFGMUX 등) 식별
- `CDC_Report`, `CDC_Critical`, `CDC_Unsafe`, `CDC_Interaction`: 클럭 도메인 간 비동기/스위칭 전환 시 안전성
- `Timing_Exceptions.rpt`: 스위칭/타이밍 예외 설정 여부

🧩 **파싱 로직**

```python
# 1) BUFGMUX (클럭 전환 MUX) 사용 여부 확인 — 핵심 지표
# Clock Primitive Utilization 테이블 파싱
pattern_prim_table = r'\|\s*(BUFGCTRL|BUFGMUX|BUFGMUX_CTRL)\s*\|\s*(\d+)\s*\|'
clk_primitives = dict(re.findall(pattern_prim_table, clock_util_text))

# 2) Global Clock Resources에서 BUFGMUX 드라이버 타입 확인
pattern_mux_driver = r'BUFGMUX|CLK_SWITCH|CLKMUX'
bufgmux_count = len(re.findall(pattern_mux_driver, clock_util_text))

# 3) Waveform에서 Duty 확인 (50% = High/Low 동일)
pattern_waveform = r'Waveform\(ns\):\s+\{ ([\d.]+) ([\d.]+) \}'
pattern_period   = r'Period\(ns\):\s+([\d.]+)'
# Duty = (Rising2 - Rising1) / Period × 100%
def duty(wave_low, wave_high, period):
    return round((float(wave_high) - float(wave_low)) / float(period) * 100, 1)

# 4) Pulse Width 위반 확인 (Slack >= 0이면 정상)
pattern_pw_slack = r'(Low|High) Pulse Width\s+\S+\s+\S+\s+n/a\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)'
```

📊 **추출 결과**

| Clock Primitive | 사용 수 | 최대 수 |
|----------------|--------|--------|
| `BUFGCTRL` | 17 | 32 |
| `BUFH` | 1 | 96 |
| `BUFGMUX (전환)` | **0** ✅ | - |
| `BUFMR/BUFIO/BUFR` | 0 | - |
| `MMCM` | 5 | 6 |
| `PLL` | 2 | 6 |

**Duty Cycle 검증 (주요 클럭):**

| 클럭 | Period | Waveform | Duty(%) |
|------|-------|---------|--------|
| `clk_out1_ip_clk_wiz_power_loader` | 3.205ns | {0 1.603} | 50.0% ✅ |
| `clk_out1_ip_clk_wiz_lcos_pclk` | 12.821ns | {0 6.410} | 50.0% ✅ |
| `clk_out1_ip_clk_wiz_fmc_clk` | 11.574ns | {0 5.787} | 50.0% ✅ |
| `clk_out1_ip_clk_wiz_ddr3_clk` | 10.000ns | {0 5.000} | 50.0% ✅ |
| `clk_out2_ip_clk_wiz_lcos_pclk` | 25.641ns | {6.410 19.231} | 50.0% ✅ |
| `clk_out2_ip_clk_wiz_ddr3_clk` | 5.000ns | {0 2.500} | 50.0% ✅ |

**Pulse Width 위반:**

- 전체 18개 클럭 기준 모든 `Slack(ns)` > 0 → **위반 없음** ✅

⚖️ **판정 로직**

```python
def judge_q41(data, criteria):
    duty_tol = criteria['clocking']['duty_tolerance_pct'] # 예: 2.0 (%)
    bufgmux = data.get('BUFGMUX', 0) + data.get('CLK_SWITCH', 0)
    pw_violations = [c for c in data['clk_list'] if c['pw_slack'] < 0]
    duty_violations = [c for c in data['clk_list']
                       if abs(c['duty'] - 50.0) > duty_tol]

    if bufgmux > 0:
        return "REVIEW", f"BUFGMUX {bufgmux}개 사용 — 글리치 방지 설계 근거 필요"
    if pw_violations:
        return "REVIEW", f"Pulse Width 위반: {[c['name'] for c in pw_violations]}"
    if duty_violations:
        return "REVIEW", f"Duty != 50%: {[(c['name'], c['duty']) for c in duty_violations]}"
    return "PASS", (
        "BUFGMUX 사용 없음(순수 BUFGCTRL/MMCM/PLL 구조). "
        "모든 MMCM/PLL 출력 클럭 Duty = 50.0%. "
        "Pulse Width Slack 전체 양수 — 글리치/해저드/듀티 불균형 없음."
    )
```

💬 **예상 답변**
> **PASS** — BUFGMUX(클럭 전환 MUX) 사용 없음. MMCM/PLL 출력 클럭 전체 Duty=50.0%. Pulse Width 위반 0건. 글리치·해저드·듀티 불균형 방지 설계 확인.

---

## Q42: 호스트-모듈 간 또는 모듈 내 CDC 회로 사용 여부

> *호스트-모듈 간 또는 모듈 내부에서 클럭 도메인 변경(CDC) 회로를 사용합니까?*

- **답변 유형**: `SEMI` — CDC 존재 확인 가능

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Unsafe.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`**

🔍 **파싱 위치**

- `CDC_Report.rpt`: `Severity` 요약 테이블 (CDC 유형별 건수 집계)
- `CDC_Report.rpt`: 각 CDC 세부 경로 상의 `Source Clock` 및 `Destination Clock` 도메인 명세 정보

🧩 **파싱 로직**

```python
# 1) CDC 전체 건수 확인 (존재 여부)
pattern_cdc_total = r'(CDC-\d+)\s+(Warning|Info)\s+(\d+)'
cdc_summary = re.findall(pattern_cdc_total, cdc_text)

# 2) 호스트-모듈 간 CDC 경로 식별
# FMC ↔ System 도메인, DDR3 ↔ System 도메인 경로
pattern_host_module = r'Source\s+Clock\s*:\s+(\S+).*?Destination\s+Clock\s*:\s+(\S+)'
clk_pairs = re.findall(pattern_host_module, cdc_text, re.DOTALL)

# 3) lib_cdc_* 모듈 구별 (사용자 정의 CDC vs Xilinx IP 내부)
pattern_lib_cdc = r'lib_cdc_(\w+)'
user_cdc_modules = re.findall(pattern_lib_cdc, cdc_text)
```

📊 **추출 결과**

| CDC 유형 | Severity | 건수 | 도메인 방향 |
|---------|---------|-----|----------|
| CDC-2 | Warning | 2 | lcos_pclk → fmc_clk (1-bit, ASYNC_REG 미설정) |
| CDC-3 | Info | 40 | 다수 도메인 (1-bit, ASYNC_REG 정상) |
| CDC-6 | Warning | 21 | lcos_pclk ↔ power_loader (Multi-bit lib_cdc) |
| CDC-8 | Warning | 1 | sys_clk → ddr3_ref_clk (비동기 리셋) |
| CDC-9 | Info | 2 | 비동기 리셋 정상 동기화 |
| CDC-15 | Warning | 475 | FIFO 내부 (Clock Enable CDC) |

**식별된 CDC 모듈:**

- `lib_cdc_fmc_sys_rdata` (FMC → System)
- `lib_cdc_sys_fmc_addr` (System → FMC)
- `lib_cdc_power_loader_*` (Power Loader ↔ System)
- Xilinx IP 내부 FIFO CDC (ip_fifo_indep_48x16)

⚖️ **판정 로직**

```python
def judge_q42(cdc_data):
    total = sum(c['count'] for c in cdc_data)
    modules = list(set(user_cdc_modules))
    return "REVIEW", (
        f"호스트(FMC, DDR3, Power_Loader) ↔ 모듈(lcos_pclk) 간 "
        f"CDC 회로 사용 확인. 총 {total}건. "
        f"사용자 정의 CDC 모듈: {modules}. "
        "⚠️ CDC-2 2건(ASYNC_REG 미설정) 보완 필요. "
        "CDC-15 475건은 Xilinx IP 내부 FIFO(정상)."
    )
```

💬 **예상 답변**
> **YES (REVIEW)** — 호스트-모듈 간 CDC 회로 사용: FMC↔lcos_pclk, DDR3↔lcos_pclk, Power_Loader↔lcos_pclk. lib_cdc 사용자 정의 모듈로 1-bit ASYNC_REG 동기화 설계. ⚠️ CDC-2 2건(ASYNC_REG 미설정) 보완 권고.

---

## Q43: 비동기 클럭 메모리 W/R 위상 보장 (파워온/리셋 시)

> *비동기 클럭을 사용하는 메모리 회로에서 파워온/리셋 시에도 W/R 위상이 보장됩니까?*

- **답변 유형**: `SEMI` — FIFO 구조에서 부분 확인 가능

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Unsafe.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`**

🔍 **파싱 위치**

- `CDC_Report.rpt`: `CDC-15` 등 관련 경로에서 FIFO 포인터 보호 방식 식별
- `Timing_Exceptions.rpt`: MIG PHY 관련 `set_multicycle_path` 및 `set_false_path` 예외 설정 구간

🧩 **파싱 로직**

```python
# 1) FIFO 비동기 포인터 방식 확인 (Gray Code = 위상 보장)
# IP Xilinx FIFO는 Gray Code 포인터 사용 → 리셋 후 포인터 초기화
pattern_fifo_reset = r'gpr1.dout_i_reg|RDCOUNT|WRCOUNT'

# 2) False Path — 리셋 경로 타이밍 예외 확인
pattern_false_path = r'false_path.*?RESET|rst.*?false'

# 3) Timing_Exceptions에서 FIFO 관련 Multicycle 설정
# MIG PHY Setup×6 / Hold×5 → DDR3 FIFO 포인터 마진
pattern_mig_mcp = r'set_multicycle_path.*?-setup\s+(\d+)'
```

📊 **추출 결과**

| FIFO 유형 | 위상 보장 방식 | 리셋 시 동작 |
|---------|------------|------------|
| `ip_fifo_indep_48x16` (Xilinx) | Gray Code 포인터 | 리셋 시 포인터 0 초기화 |
| DDR3 IN_FIFO/OUT_FIFO | PHY 내부 동기화 | MIG 캘리브레이션 후 안정화 |
| `lib_cdc_*` | ASYNC_REG 2-stage | 리셋 비동기, 동기화 후 전파 |

⚖️ **판정 로직**

```python
def judge_q43(data, criteria):
    return "REVIEW", (
        "Xilinx ip_fifo_indep_48x16: Gray Code 포인터 — 리셋 후 포인터 0초기화, "
        "파워온 시 최적 위상 보장(벤더 보증). "
        "DDR3 IN/OUT_FIFO: MIG 캘리브레이션 완료(init_calib_complete) 후 위상 정렬. "
        "⚠️ lib_cdc 모듈의 비동기 2-stage 동기화는 RESET 해제 후 최대 2 클럭 지연 허용 "
        "— RTL에서 reset 해제 시 data_valid 신호로 보호 여부 확인 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — Xilinx FIFO(Gray Code 포인터): 리셋 후 자동 초기화, 최적 위상 보장. DDR3: init_calib_complete 신호로 캘리브레이션 완료 후 사용. ⚠️ lib_cdc 사용자 모듈의 리셋 해제 후 data_valid 보호 로직 RTL 확인 필요.

---

## Q44: 비동기 CLK-Data 간 타이밍 보장

> *비동기 클럭 사용 시 CLK-Data 간의 타이밍이 보장됩니까?*

- **답변 유형**: `SEMI` — CDC 및 Timing_Exceptions 분석

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Unsafe.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`** + **`Bus_Skew.rpt`**

🔍 **파싱 위치**

- `Bus_Skew.rpt` (263KB): 클럭-데이터 Skew 결과
- `Timing_Exceptions.rpt`: `set_clock_groups` (타이밍 분석 제외 선언)
- `CDC_Report.rpt` CDC-6: Multi-bit lib_cdc 경로

🧩 **파싱 로직**

```python
# 1) Bus_Skew 요약 파싱 (상위 섹션만)
# → WBS(Worst Bus Skew), Slack 음수 여부
pattern_wbs = r'WBS\s*\|\s*([\d.-]+)'
pattern_bus_skew_heading = r'Bus Skew Check'

# 2) set_clock_groups (비동기 도메인 — CLK-Data 타이밍 분석 제외)
# → 제외 의미: 두 클럭 간 경로가 없거나 비동기 처리됨
pattern_clk_group_count = r'set_clock_groups'
num_clk_groups = len(re.findall(pattern_clk_group_count, exceptions_text))

# 3) CDC-6 Multi-bit 경로 세부 분석
pattern_cdc6 = r'CDC-6.*?Source Register : (\S+).*?Dest Register: (\S+)'
cdc6_paths = re.findall(pattern_cdc6, cdc_text, re.DOTALL)
```

📊 **추출 결과**

| 항목 | 값 |
|-----|---|
| `set_clock_groups` 예외 | 49쌍 (CLK-Data 타이밍 분석 제외) |
| Bus_Skew.rpt | 263KB — 별도 분석 필요 |
| CDC-6 (Multi-bit) | 21건 — lib_cdc_power_loader_* |
| MIG Multicycle | Setup×6 / Hold×5 (PHY 내부 타이밍 보장) |

⚖️ **판정 로직**

```python
def judge_q44(data, criteria):
    return "REVIEW", (
        "set_clock_groups 49쌍: 비동기 도메인 CLK-Data 경로 타이밍 분석 제외 선언. "
        "CDC-3(40건): ASYNC_REG 2-stage — CLK 에지 불확실성 허용. "
        "CDC-6(21건): Multi-bit lib_cdc — 동기화 후 CLK-Data 타이밍 확보. "
        "⚠️ Bus_Skew.rpt 세부 분석(비동기 도메인 간 Skew 측정값) 제출 권장."
    )
```

💬 **예상 답변**
> **REVIEW** — 비동기 도메인 간 CLK-Data 경로는 set_clock_groups 선언(49쌍)으로 STA에서 제외. ASYNC_REG 동기화 방식으로 메타스태빌리티 방지. ⚠️ Bus_Skew.rpt 상세 분석 및 CDC-6 Multi-bit 경로의 동기화 여유도 검토 결과 제출 필요.

---

## Q45: PLL/SERDES 출력 클럭 Duty Cycle 만족

> *PLL/SerDes 출력 클럭의 듀티비(통상 50%)가 사용 조건을 만족합니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Pulse_Width.rpt`** + **`Clock_Utilization.rpt`**

🧩 **파싱 로직**

```python
# 1) 각 클럭의 Waveform으로 Duty 계산
pattern_clk_block = r'''
    Clock\s+Name:\s+(\S+)\n
    Waveform\(ns\):\s+\{[\s]*([\d.]+)\s+([\d.]+)[\s]*\}\n
    Period\(ns\):\s+([\d.]+)
'''
clk_blocks = re.findall(pattern_clk_block, pw_text, re.VERBOSE)
for name, t_rise, t_fall, period in clk_blocks:
    duty = (float(t_fall) - float(t_rise)) / float(period) * 100

# 2) Pulse Width Slack 전체 확인
pattern_pw_check = r'(Low|High) Pulse Width\s+(\w+)\s+\S+\s+n/a\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)'
pw_results = re.findall(pattern_pw_check, pw_text)
violations = [(r[0], r[1], float(r[4])) for r in pw_results if float(r[4]) < 0]
```

📊 **주요 클럭 Duty 검증**

| 클럭 | Period(ns) | Waveform | Duty | Slack최소(ns) |
|------|----------|---------|------|-------------|
| clk_out1_clk_wiz_power_loader | 3.205 | {0, 1.603} | 50.0% ✅ | +0.473 |
| clk_out3_clk_wiz_lcos_pclk | 6.410 | {0, 3.205} | 50.0% ✅ | +2.351 |
| clk_out1_clk_wiz_lcos_pclk | 12.821 | {0, 6.410} | 50.0% ✅ | +5.556 |
| clk_out1_clk_wiz_fmc_clk | 11.574 | {0, 5.787} | 50.0% ✅ | +4.657 |
| clk_out1_clk_wiz_ddr3_clk | 10.000 | {0, 5.000} | 50.0% ✅ | +3.000 |
| clk_pll_i (DDR3 MMCM) | 12.308 | {0, 6.154} | 50.0% ✅ | +4.004 |
| clk_out2_clk_wiz_lcos_pclk | 25.641 | {6.410, 19.231} | 50.0% ✅ | +12.321 |
| freq_refclk (1.538ns) | 1.538 | {0, 0.769} | 50.0% ✅ | +0.287 (최소) |

⚖️ **판정 로직**

```python
def judge_q45(data, criteria):
    duty_tol = criteria['clocking']['duty_tolerance_pct'] # 예: 2.0 (%)
    duty_violations = [c for c in data if abs(c['duty'] - 50.0) > duty_tol]
    pw_violations = [c for c in data if c['pw_slack'] < 0]
    if duty_violations or pw_violations:
        return "REVIEW", f"Duty/PW 위반: ..."
    return "PASS", (
        f"전체 {len(data)}개 클럭 Duty = 50.0%. "
        "Pulse Width 위반 0건. 최소 Slack: freq_refclk 0.287ns (양수). "
        "Xilinx MMCM/PLL 50% 듀티 보장."
    )
```

💬 **예상 답변**
> **PASS** — 전체 18개 클럭 Duty = 50.0% (Waveform 기준). Pulse Width 위반 0건. 최소 Slack: freq_refclk 0.287ns(양수). MMCM/PLL 50% 듀티 설계 충족.

---

## Q46: 동기 RAM Address/Data 신호 동기 설계 확인

> *동기 RAM에서 주소(Address) 및 데이터(Data) 신호가 동기식으로 설계되었음을 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`RAM_Utilization.rpt`** (03/) + **`Check_Timing.rpt`** (01/)

🧩 **파싱 로직**

```python
# 1) RAM 유형 확인 (Single Port, Simple Dual Port → 단일 클럭 동기)
pattern_ram_type = r'(Single Port|Simple Dual Port|True Dual Port|FIFO)'
ram_types = re.findall(pattern_ram_type, ram_util_text)

# 2) True Dual Port 존재 여부 (비동기 가능성)
true_dp_count = ram_types.count('True Dual Port')

# 3) no_clock=0 확인 → 모든 FF에 클럭 정의됨
pattern_no_clock = r'There are (\d+) register/latch pins with no clock'

# 4) RAM 관련 Timing Check
# → SP/SDP는 단일 클럭 → 항상 동기
```

📊 **추출 결과**

| RAM 유형 | 인스턴스 수 | 비동기 가능성 |
|---------|-----------|------------|
| Single Port | 다수 | ❌ (단일 클럭, 동기) |
| Simple Dual Port | 다수 | ❌ (단일 클럭, 동기) |
| True Dual Port | **0** | 해당 없음 |
| Async FIFO (IP) | 다수 | Q40에서 별도 분석 |
| `no_clock` 핀 | **0** | ✅ 전체 동기 정의 |

⚖️ **판정 로직**

```python
def judge_q46(data, criteria):
    if data['true_dp_count'] == 0 and data['no_clock'] == 0:
        return "PASS", (
            "True Dual Port RAM 미사용. "
            "Single Port / Simple Dual Port만 사용 → 단일 클럭 동기 설계. "
            "no_clock=0 → 모든 FF 클럭 정의."
        )
    return "REVIEW", f"True Dual Port {data['true_dp_count']}개 — 비동기 접근 여부 확인 필요"
```

💬 **예상 답변**
> **PASS** — True Dual Port RAM 미사용. Single Port/Simple Dual Port만 사용(단일 클럭 동기 설계). no_clock=0. 동기 RAM Address/Data 신호 동기식 설계 확인.

---

## Q47: DPRAM W/R 충돌로 인한 데이터 부정 현상 방지

> *DPRAM 사용 시 W/R 충돌로 인한 데이터 부정 현상을 방지하거나 그 영향을 고려했습니까?*

- **답변 유형**: `SEMI` — RAM 구조 및 CDC 동기화에서 확인 가능

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Unsafe.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`** + **`RAM_Utilization.rpt`**

🔍 **파싱 위치**

- `RAM_Utilization.rpt`: DPRAM 충돌 보호 방식 및 경합 보장 범위 확인
- `CDC_Report` ~ `CDC_Interaction`: DPRAM 관련 비동기/동기화 충돌 대비 확인
- `Timing_Exceptions.rpt`: 예외 설정이 있는지 확인

🧩 **파싱 로직**

```python
# 1) SDP RAM 구조 — Xilinx SDP는 W/R 충돌 금지 (사용자 책임)
pattern_sdp = r'Simple Dual Port\s+\|\s+(\d+)'

# 2) FIFO async (독립 클럭) — Gray Code 포인터로 충돌 방지
pattern_fifo_indep = r'ip_fifo_indep|FIFO.*?independent'

# 3) CDC-6 28건: 비동기 다중 비트 CDC
# → lib_cdc_power_loader 경로에서 W/R 인터페이스 보호 확인
pattern_lib_cdc_addr = r'lib_cdc.*?addr|lib_cdc.*?data'

# 4) 동일 클럭 SDP: W/R 동시 발생 시 판정 — RTL에서 제어 신호 확인
```

📊 **추출 결과**

| DPRAM 유형 | 충돌 방지 방법 | 판정 |
|----------|------------|-----|
| Xilinx SDP (단일 클럭) | W/R 동시 제어 신호 필요 | SEMI (RTL 확인) |
| ip_fifo_indep_48x16 | Gray Code 포인터 | ✅ 자동 충돌 방지 |
| lib_cdc 멀티비트 | ASYNC_REG + handshake | SEMI (CDC-6 확인) |

⚖️ **판정 로직**

```python
def judge_q47(data, criteria):
    return "REVIEW", (
        "Xilinx ip_fifo_indep_48x16: Gray Code 포인터 — 충돌 자동 방지(벤더 보증). "
        "Xilinx SDP RAM: 단일 클럭 — 동시 W/R 금지 제어 신호는 RTL 구현 확인 필요. "
        "CDC-6(21건) lib_cdc 경로: 멀티비트 동기화로 W/R 인터페이스 보호. "
        "⚠️ SDP RAM W/R 동시 접근 보호 로직을 RTL 레벨에서 확인해 주세요."
    )
```

💬 **예상 답변**
> **REVIEW** — Xilinx Async FIFO(ip_fifo_indep_48x16): Gray Code 포인터로 충돌 자동 방지. Xilinx SDP: W/R 충돌 방지는 RTL 제어 신호로 보장해야 함(확인 필요). ⚠️ SDP RAM의 W/R 동시 접근 보호 로직 RTL 검토 결과 제출 필요.

---

## Q48: DPRAM 벤더 권장 설계 사례 및 주의사항 확인

> *DPRAM 사용 시 벤더의 권장 설계 사례 및 주의사항을 확인했습니까?*

- **답변 유형**: `SEMI`

📄 **`RAM_Utilization.rpt`** + **`IP_Status.rpt`**

🔍 **파싱 위치**

- `RAM_Utilization.rpt`: Xilinx Block RAM IP 사용 여부 및 벤더 가이드 준수 (메모리 파라미터 확인)
- `IP_Status.rpt`: IP 버전 및 상태

🧩 **파싱 로직**

```python
# 1) IP 기반 BRAM 사용 여부 (벤더 권장 IP = 가이드라인 준수 가정)
pattern_ip_bram = r'ip_blk_mem_gen|ip_fifo_indep|MIG.*RAM|BRAM'

# 2) RAM 파라미터 확인 (WRITE_MODE, READ_FIRST/WRITE_FIRST)
# → Vivado IP Catalog에서 충돌 정책 설정됨
pattern_write_mode = r'WRITE_MODE\s*=\s*(\w+)'

# 3) RAM_Utilization에서 IP 인스턴스 모듈명 추출
pattern_ip_instance = r'ip_(\w+)\s+\|.*?BlockRAM'
```

📊 **추출 결과**

| 항목 | 값 |
|-----|---|
| Xilinx BRAM IP 사용 | `ip_blk_mem_gen`, `ip_fifo_indep_48x16` |
| WRITE_MODE 설정 | Vivado IP Catalog에서 관리 |
| Single Port | 벤더 IP 기반(가이드라인 기본 적용) |
| DPRAM 주의사항 확인 | EVIDENCE_NEEDED (IP Catalog 사용 여부 근거 필요) |

⚖️ **판정 로직**

```python
def judge_q48(data, criteria):
    return "REVIEW", (
        "Xilinx BRAM IP(ip_blk_mem_gen, ip_fifo_indep_48x16) 사용: "
        "Vivado IP Catalog 기반 — 벤더 권장 설정 기본 적용. "
        "⚠️ WRITE_MODE(READ_FIRST/WRITE_FIRST/NO_CHANGE) 설정 캡처 "
        "및 충돌 시 동작 설계 결정서 제출 권장."
    )
```

💬 **예상 답변**
> **REVIEW** — Xilinx BRAM/FIFO IP(ip_blk_mem_gen, ip_fifo_indep_48x16) 사용 — Vivado IP Catalog 기반으로 벤더 권장 설정 적용. ⚠️ WRITE_MODE 설정(READ_FIRST/WRITE_FIRST/NO_CHANGE) 및 충돌 시 동작 명세 제출 권장.

---

## Q49: CPU-FPGA 인터페이스 엔디안 및 MSB/LSB 정의

> *CPU 내장 FPGA 또는 CPU 연결 시, 레지스터의 엔디안(Big/Little) 및 MSB/LSB 구성이 명확합니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **`Debug_Core.rpt`**

🔍 **파싱 위치**

- `Debug_Core.rpt`: 전체 메시지 상의 `INFO: No debug cores were found in this design` 검출
  → ILA/VIO 디버그 코어 없음 → 외부 CPU 인터페이스 레지스터 정의 확인 불가

📊 **관련 데이터**

| 항목 | 값 |
|-----|---|
| Debug Core (ILA/VIO) | 없음 |
| CPU 내장 (MicroBlaze 등) | 미식별 (RTL 확인 필요) |
| 엔디안 정의 문서 | EVIDENCE_NEEDED |
| MSB/LSB 정의 | EVIDENCE_NEEDED |

⚖️ **판정**: `EVIDENCE_NEEDED` — 디버그 코어 없음 → 외부 CPU 인터페이스 레지스터 존재 여부와 엔디안 정의를 설계 문서에서 확인해야 함.

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 본 디자인에 ILA/VIO 디버그 코어 없음(Debug_Core 확인). 외부 CPU 인터페이스(FMC, 시스템 버스) 사용 시 레지스터 엔디안(Big/Little Endian) 및 MSB/LSB 정의는 레지스터 명세서(Register Map) 및 CPU 설계 문서에서 확인 필요.

---

## Q50: 미정의 레지스터 주소에 대한 R/W 동작 차단

> *요구 사양에 없는 레지스터 주소에 대해 R/W 동작이 수행되지 않음을 확인했습니까? (디버그용 제외)*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **`Debug_Core.rpt`** + **`DRC_Report.rpt`**

🔍 **파싱 위치**

- `Debug_Core.rpt`: `No debug cores` 메시지 존재 유무 (디버그 코어 없음 → 관련 레지스터 없음 확인 용도)
- `DRC_Report.rpt`: 레지스터 접근 및 주소 할당 관련 DRC 위반 내역 유무

📊 **관련 데이터**

| 항목 | 값 |
|-----|---|
| Debug Core (ILA/VIO) | **없음** ✅ — 디버그 전용 레지스터 없음 |
| 미정의 주소 접근 차단 | RTL/소프트웨어 확인 필요 |
| 레지스터 맵 문서 | EVIDENCE_NEEDED |

⚖️ **판정**: `EVIDENCE_NEEDED`

```python
# 파싱 시 Debug Core 존재 여부 확인
pattern_no_debug = r'No debug cores were found'
has_no_debug = bool(re.search(pattern_no_debug, debug_core_text))
# → True이면 디버그 레지스터 없음 확인 (긍정 증거)
# → 미정의 주소 차단은 RTL 및 버스 설계에서 확인
```

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 디버그 코어(ILA/VIO) 없음으로 디버그 레지스터 미사용 확인. ⚠️ 요구 사양 레지스터 맵에 없는 주소 접근 시 응답 방식(Error Response, Tie-off 등)은 버스 IF 설계 문서 및 RTL 검토 필요.

---

## 요약 — Q41~Q50 파싱 구현 우선순위

| 우선순위 | 질문 | 답변 유형 | 파서 구현 | 리포트 |
|---------|------|----------|----------|------------|
| ⬆️ 높음 | Q41 | SEMI | `cdc_parser.py` 등 | CDC_Report 등 5종, Clock_Networks, Clock_Utilization |
| ⬆️ 높음 | Q42 | SEMI | `cdc_parser.py` 등 | CDC_Report 등 5종 |
| ⬆️ 높음 | Q43 | SEMI | `cdc_parser.py` 등 | CDC_Report 등 5종 |
| 🔹 중간 | Q44 | SEMI | `cdc_parser.py` 등 | CDC_Report 등 5종, Bus_Skew |
| 🔹 중간 | Q45 | AUTO | `timing_parser.py` | Pulse_Width, Clock_Utilization |
| 🔹 중간 | Q46 | AUTO | `ram_parser.py` 재사용 | RAM_Utilization, Check_Timing |
| 🔹 중간 | Q47 | SEMI | `cdc_parser.py` 등 | CDC_Report 등 5종, RAM_Utilization |
| 🔹 중간 | Q48 | SEMI | `ram_parser.py` | RAM_Utilization, IP_Status |
| ⬇️ 낮음 | Q49 | EVIDENCE | 없음 | (없음) |
| ⬇️ 낮음 | Q50 | EVIDENCE | 없음 | Debug_Core |

## 주요 관찰 사항

> **Q41 핵심**: `BUFGMUX=0` — 클럭 전환 MUX 미사용 → **PASS** 자동화 가능
>
> **Q45 핵심**: 전체 18개 클럭 Duty=50.0%, PW의 위반=0 → **PASS** 자동화
>
> **Q46 핵심**: True Dual Port RAM=0 → **PASS** 자동화 가능
>
> **Q47**: Xilinx Async FIFO(자동 충돌 방지) / SDP RAM(RTL 확인 필요)로 SEMI 분류
>
> **Q49/Q50**: Debug Core 없음은 긍정 증거이나, 레지스터 맵/버스 설계 문서 필요
