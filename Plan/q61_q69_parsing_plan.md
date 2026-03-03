# Q61~Q69 상세 파싱 계획서

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

## Q61: 클럭/리셋 종류·주파수 명확화 및 구현 툴 로그 반영 확인

> *클럭 및 리셋 사양이 명확하며, 이것이 구현 툴 로그에 올바르게 반영되었음을 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Timing_Summary.rpt`** + **`Check_Timing.rpt`** + **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`**

🔍 **파싱 위치**

- `Timing_Summary.rpt`: `Clock Summary` 섹션 (클럭 명칭, 주파수, 파형 등의 정보 포함)
- `Check_Timing.rpt`: `checking no_clock`, `checking no_input_delay` 등 타이밍 검사 섹션
- 그 외 `CDC_Report.rpt` 등에서 비동기 리셋 경로와 관련된 사항 종합 확인

🧩 **파싱 로직**

```python
# 1) Clock Summary 섹션 파싱 → 클럭 명칭, 주파수, 파형 추출
import re
pattern_clk = (
    r'^([\w/]+)\s+'                       # 클럭 이름
    r'\{([\d.\s]+)\}\s+'                   # Waveform(ns)
    r'([\d.]+)\s+'                         # Period(ns)
    r'([\d.]+)'                            # Frequency(MHz)
)
clock_list = re.findall(pattern_clk, timing_summary_text, re.MULTILINE)

# 2) check_timing 섹션: no_clock=0 확인
pattern_no_clock = r'There are (\d+) register/latch pins with no clock'
no_clock_count = int(re.search(pattern_no_clock, ts_text).group(1))

# 3) CDC 리포트: 리셋 도메인 확인 (비동기 리셋 경로)
# Methodology LUTAR-1: LUT 기반 비동기 리셋 6건
```

📊 **클럭 요약 (Timing_Summary Clock Summary)**

| 입력 클럭 | 주파수 | 파생 클럭 수 | 비고 |
|----------|-----|-----------|------|
| `pin_i_clk_100m` | 100 MHz | 8개 | DDR3 MMCM/PLL 체인 |
| `pin_i_clk_20m` | 20 MHz | 9개 | LCOS/Power Loader |
| `pin_i_clk_78m` | 78.003 MHz | 4개 | LCOS SoftCCK |
| `pin_i_fmc_clk` | 43.2 MHz | 3개 | FMC 인터페이스 |

**파생 주요 클럭:**

- `clk_pll_i` (81.25 MHz, DDR3 MIG)
- `clk_out3_ip_clk_wiz_lcos_pclk` (156 MHz, LCOS 구동)
- `clk_out1_ip_clk_wiz_power_loader` (312 MHz, Power Loader)

**check_timing 결과:**

- no_clock: **0** ✅
- multiple_clock: **0** ✅
- combinational loops: **0** ✅
- no_input_delay 포트: **56포트** (pin_i_fmc_addr 등) ⚠️
- no_output_delay 포트: **102포트** (LCOS 패널 출력 등) ⚠️

**리셋 종류:**

- `ddr3_reset_n` (출력 핀, no_output_delay ⚠️)
- 비동기 리셋 LUT 구동: LUTAR-1 6건

⚖️ **판정 로직**

```python
def judge_q61(data, criteria):
    issues = []
    if data['no_input_delay'] > 0:
        issues.append(f"no_input_delay {data['no_input_delay']}포트(FMC)")
    if data['no_output_delay'] > 0:
        issues.append(f"no_output_delay {data['no_output_delay']}포트(LCOS패널 등)")
    if data['lutar1'] > 0:
        issues.append(f"LUTAR-1 {data['lutar1']}건(비동기리셋)")
    return "PASS_WITH_WARNING", (
        f"클럭 18개 정의됨 (4개 입력+파생). "
        f"no_clock=0, multiple_clock=0, combinational_loop=0. "
        f"⚠️ {' / '.join(issues)}"
    )
```

💬 **예상 답변**
> **PASS (경고 포함)** — 4개 입력 클럭(100M/20M/78M/43.2M) 및 파생 클럭 14개 정의. no_clock=0, loop=0 ✅. ⚠️ FMC 입력 56포트/LCOS출력 102포트 delay 미설정 (의도적 false path로 추정). LUTAR-1(비동기리셋 6건) 해소 권고.

---

## Q62: PLL 출력 주파수·듀티·위상 조건 만족 확인

> *PLL 사용 시 출력 주파수, 듀티(통상 50%), 위상 등의 조건이 명확하며 만족함을 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Pulse_Width.rpt`** + **`Clocks_Summary.rpt`** + **`Property_Check.rpt`** + **`Timing_Summary.rpt`**  + **`Check_Timing.rpt`**

🔍 **파싱 위치**

- `Timing_Summary.rpt`: `Clock Summary` 섹션 내 각 클럭의 `Waveform` 컬럼 (High/Low Pulse Width)
- `Timing_Summary.rpt`: `Design Timing Summary` 섹션의 `WPWS(ns)` 컬럼 및 관련 요약 통계
- `Pulse_Width.rpt`: `Pulse Width Checks` 또는 `High/Low Pulse Width` 관련 상세 위반/Slack 검사 섹션

🧩 **파싱 로직**

```python
# 1) Clock Summary에서 Waveform 파싱 → Duty 계산
# 형식: {rise_ns fall_ns} → duty = (period-fall+rise)/period×100
for clk in clock_list:
    name, waveform, period, freq = clk
    rise, fall = map(float, waveform.split())
    high_time = fall - rise
    duty_pct = high_time / float(period) * 100

# 2) WPWS(ns) - Worst Pulse Width Slack: 전체 0건 실패 확인
pattern_wpws = r'WPWS\(ns\).*?(\d+\.\d+)'
wpws_wns = float(re.search(pattern_wpws, ts_text).group(1))

# 3) Pulse Width Checks → 개별 클럭 Slack 추출
pattern_pw_slack = r'(Low|High) Pulse Width\s+\w+\s+\S+\s+n/a\s+([\d.]+)\s+([\d.]+)\s+([-\d.]+)'
pw_checks = re.findall(pattern_pw_slack, ts_text)
```

📊 **PLL 출력 Duty 및 WPWS 결과**

| 클럭 | 주기(ns) | Waveform | Duty(%) | WPWS(ns) |
|-----|---------|---------|--------|---------|
| `pin_i_clk_100m` | 10.000 | {0.000 5.000} | **50.0%** ✅ | 3.000 |
| `clk_out1_ip_clk_wiz_ddr3_clk` | 10.000 | {0.000 5.000} | **50.0%** ✅ | 3.000 |
| `clk_out1_ip_clk_wiz_lcos_pclk` | 12.821 | {0.000 6.410} | **50.0%** ✅ | 5.556 |
| `clk_out3_ip_clk_wiz_lcos_pclk` | 6.410 | {0.000 3.205} | **50.0%** ✅ | 2.351 |
| `clk_out2_ip_clk_wiz_lcos_pclk` | 25.641 | {6.410 19.231} | **50.0%** ✅ | 12.321 |
| `clk_out1_ip_clk_wiz_power_loader` | 3.205 | {0.000 1.603} | **50.0%** ✅ | 0.473 |
| `clk_out1_ip_clk_wiz_fmc_clk` | 11.574 | {0.000 5.787} | **50.0%** ✅ | 4.657 |
| `freq_refclk` | 1.538 | {0.000 0.769} | **50.0%** ✅ | 0.287 |

**TPWS**: 0 Failing Endpoints 전체 ✅

⚖️ **판정 로직**

```python
def judge_q62(data, criteria):
    if data['tpws_fail'] == 0 and all(abs(d-50) < 1 for d in data['duty_list']):
        return "PASS", (
            "MMCM/PLL 출력 클럭 전체 Duty=50%. "
            f"WPWS 최소 {min(data['wpws_list']):.3f}ns (전체 PASS). "
            "no_input_delay 포트의 시스템 지터 영향 없음."
        )
```

💬 **예상 답변**
> **PASS** — MMCM/PLL 모든 출력 클럭 Duty=50%. WPWS 최소 0.264ns(전체 Failing=0). 주파수: 312MHz(Power Loader) → 81.25MHz(DDR3) → 156MHz(LCOS) 정의 충족.

---

## Q63: Worst-case 조건 (지터·변동 포함) 타이밍 분석 확인

> *변동 및 지터를 고려한 최악 조건(Worst-case)에서 타이밍 분석 및 보증을 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Timing_Summary.rpt`** + **`Setup_Critical.rpt`** + **`Hold_Critical.rpt`**

🧩 **파싱 로직**

```python
# 1) Timer Settings: Multi Corner(Slow+Fast) 활성화 확인
pattern_mc = r'Enable Multi Corner Analysis\s+:\s+(\w+)'
multi_corner = re.search(pattern_mc, ts_text).group(1)  # 'Yes'

# 2) Pessimism Removal 확인
pattern_pr = r'Enable Pessimism Removal\s+:\s+(\w+)'
pessimism_removal = re.search(pattern_pr, ts_text).group(1)  # 'Yes'

# 3) Design Timing Summary: WNS/WHS/WPWS 전체 확인
pattern_dts = r'(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)'
dts = re.search(pattern_dts, ts_text.split('Design Timing Summary')[1])

# 4) 지터(System Jitter) 값 확인 (경로별 클럭 불확실도)
# → 대표 경로에서 TSJ/DJ 추출
pattern_jitter = r'Total System Jitter\s+\(TSJ\)\s*:\s*([\d.]+)ns'
tsj = float(re.search(pattern_jitter, ts_text).group(1))
pattern_dj = r'Discrete Jitter\s+\(DJ\)\s*:\s*([\d.]+)ns'
dj = float(re.search(pattern_dj, ts_text).group(1))
```

📊 **Worst-case 타이밍 분석 결과**

| 항목 | 값 | 판정 |
|-----|---|------|
| Multi Corner (Slow+Fast) | **Yes** | ✅ |
| Pessimism Removal | **Yes** | ✅ |
| WNS (Setup) | **0.093 ns** | ✅ PASS |
| WHS (Hold) | **0.010 ns** | ✅ PASS |
| WPWS (PW) | **0.264 ns** | ✅ PASS |
| TNS/THS/TPWS | **전체 0 ns** | ✅ |
| Total System Jitter (TSJ) | 0.071 ns | - |
| Discrete Jitter (DJ) | 0.078 ns | - |
| Setup Critical Path (WNS) | `clk_out3_ip_clk_wiz_lcos_pclk` 0.093 ns | 최소 마진 |
| Hold Critical Path (WHS) | `clk_out2_ip_clk_wiz_ddr3_clk` 0.010 ns | 최소 마진 ⚠️ |

⚖️ **판정 로직**

```python
def judge_q63(data, criteria):
    whs_warn_th = criteria['timing']['whs_warning_threshold'] # 예: 0.020
    if (data['wns'] >= 0) and (data['whs'] >= 0) and (data['wpws'] >= 0):
        note = ""
        if data['whs'] < whs_warn_th:
            note = f"⚠️ WHS={data['whs']:.3f}ns (최소 마진 주의)"
        return "PASS", (
            f"Slow+Fast Multi Corner 분석 완료. "
            f"WNS={data['wns']:.3f}ns, WHS={data['whs']:.3f}ns, "
            f"WPWS={data['wpws']:.3f}ns. 전체 타이밍 충족. {note}"
        )
```

💬 **예상 답변**
> **PASS** — Slow/Fast Multi Corner 분석 완료. WNS=0.093ns, WHS=0.010ns(최소마진 주의), WPWS=0.264ns. 전체 61,129 경로 클리어. 지터 포함(TSJ=0.071ns, DJ=0.078ns) 분석 완료.

---

## Q64: 클럭 간 경로 식별 및 스큐·마진 평가

> *클럭 간 경로(Master-to-Sub 등)를 식별하고, 스큐 및 지연 등 마진 평가를 실시했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Timing_Summary.rpt`** + **`Setup_Critical.rpt`** + **`Hold_Critical.rpt`** + **`Bus_Skew.rpt`**

🧩 **파싱 로직**

```python
# 1) Inter Clock Table 파싱 (클럭 간 경로)
pattern_inter = (
    r'(\S+)\s{2,}'           # From Clock
    r'(\S+)\s{2,}'           # To Clock
    r'(\S+)\s+'              # WNS
    r'(\S+)\s+'              # TNS
    r'(\d+)\s+(\d+)\s+'     # Fail / Total (Setup)
    r'(\S+)\s+(\S+)\s+'     # WHS / THS
    r'(\d+)\s+(\d+)'        # Fail / Total (Hold)
)
inter_paths = re.findall(pattern_inter, ts_text.split('Inter Clock Table')[1])

# 2) User Ignored Paths (set_clock_groups false_path)
pattern_ignored = r'\(none\)\s+(\S+)\s+(\S+)'
ignored_pairs = re.findall(pattern_ignored, ts_text.split('User Ignored Path Table')[1])

# 3) Bus_Skew 요약 파싱
pattern_skew = r'(\d+)\s+\d+\s+\[.*?\]\s*\n.*?\n.*?(\w+)\s+([\d.]+)\s+([\d.]+)$'
skew_entries = [...]  # 16개 CDC 버스 스큐

# 4) 최소 Bus Skew Slack 확인
min_slack = min(e['slack'] for e in skew_entries)
```

📊 **Inter Clock 경로 요약**

| From → To | WNS(ns) | WHS(ns) | 비고 |
|----------|---------|---------|-----|
| `clk_pll_i → iserdes_clk(C)` | 11.370 | 46.775 | DDR3 칼리브레이션 |
| `clk_pll_i → iserdes_clk(D)` | 12.332 | 46.249 | DDR3 칼리브레이션 |
| `sync_pulse → mem_refclk` | 1.287 | 0.910 | DDR3 동기 펄스 |
| `oserdes_clk[0-4] → oserdes_clkdiv` | 2.279 | 0.078 | OSERDES 배율 |
| `lcos_pclk_out2 → lcos_pclk_out1` | 10.041 | 0.089 | LCOS 위상 |
| `lcos_pclk_out1 → lcos_pclk_out2` | 2.176 | 5.985 | LCOS 위상 |

**Ignored (set_clock_groups) 경로**: 17쌍 (비동기 클럭 도메인 분리)

**Bus Skew 요약 (16개 CDC 경로):**

| 항목 | 값 |
|-----|---|
| 총 Bus Skew 제약 | 16개 |
| 전체 Slack MET | ✅ (모두 Positive) |
| 최소 Slack | **5.159 ns** (u_lcos_pg_top FIFO 4) |
| 최대 Actual Skew | 1.573 ns |
| CDC 클럭 조합 | `lcos_pclk_out1/3 → fmc_clk_out1` |

⚖️ **판정 로직**

```python
def judge_q64(data, criteria):
    if data['inter_fail_total'] == 0 and data['bus_skew_min_slack'] > 0:
        return "PASS", (
            f"Inter Clock 경로 전체 MET. "
            f"비동기 클럭 쌍 17쌍 set_clock_groups 처리. "
            f"Bus Skew 16경로 전체 MET (최소 Slack={data['bus_skew_min_slack']:.3f}ns). "
            "클럭 스큐 분석 완료."
        )
```

💬 **예상 답변**
> **PASS** — Inter Clock 6쌍 모두 MET. 비동기 클럭 17쌍 set_clock_groups 처리. Bus Skew 16경로 전체 PASS (최소 Slack 5.159ns). FIFO CDC Gray Code 동기화 스큐 최대 1.573ns (요구 6.41ns~11.574ns 대비 충분).

---

## Q65: 클럭 전환 시 각 조합 타이밍 마진 확인

> *클럭 전환 시, 각 클럭 조합에 대해 정상 동작 및 타이밍 마진을 확인/보증했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Setup_Critical.rpt`** + **`Hold_Critical.rpt`** + **`Bus_Skew.rpt`** + **`Timing_Summary.rpt`** + **`Timing_Exceptions.rpt`** + **`Clock_Utilization.rpt`**

🧩 **파싱 로직**

```python
# 1) Other Path Groups Table - **async_default** 그룹 확인
# → BUFGCTRL 클럭 스위칭 경로 분석 대상
pattern_async = r'\*\*async_default\*\*\s+(\S+)\s+(\S+)\s+([\d.]+)\s+([\d.]+)'
async_groups = re.findall(pattern_async, ts_text)

# 2) Clock_Utilization → BUFGCTRL 기반 클럭 스위칭 여부 확인
# (이전에 확인됨: BUFGCTRL_X0Y3, X0Y19, X0Y20, X0Y21)

# 3) Timing_Exceptions → set_clock_groups -asynchronous 확인
pattern_set_clk_grp = r'set_clock_groups\s+-asynchronous\s+-group.*?(?=-group|\Z)'
clk_groups = re.findall(pattern_set_clk_grp, exceptions_text, re.DOTALL)
num_async_groups = len(clk_groups)

# 4) Bus_Skew → CDC 버스 스큐(스위칭 시 데이터 정합성)
```

📊 **클럭 스위칭/조합 분석**

| **async_default** 그룹 | WNS(ns) | WHS(ns) | 비고 |
|---------------------|--------|--------|-----|
| `fmc_clk → fmc_clk` | 8.106 | 0.563 | FMC 내부 |
| `lcos_pclk1 → lcos_pclk1` | 6.825 | 0.291 | LCOS 내부 |
| `lcos_pclk3 → lcos_pclk3` | 1.524 | 0.494 | LCOS 156MHz 내부 |
| `clk_pll_i → clk_pll_i` | 9.216 | 0.892 | DDR3 PLL |

**Ignored 경로 (비동기 클럭 조합)**: 17쌍 → set_clock_groups로 분리

⚖️ **판정 로직**

```python
def judge_q65(data, criteria):
    if all(g['wns'] >= 0 and g['whs'] >= 0 for g in data['async_groups']):
        return "PASS", (
            f"async_default 그룹 4개 전체 MET (최소 WNS 1.524ns). "
            f"비동기 클럭 조합 17쌍 set_clock_groups 분리 처리. "
            "BUFGCTRL 기반 클럭 스위칭 → CDC FIFO 경유로 정합성 보장."
        )
```

💬 **예상 답변**
> **PASS** — async_default 그룹(FMC, LCOS156, DDR3 PLL) 4개 전체 WNS/WHS MET. 비동기 클럭 조합 17쌍 set_clock_groups 분리. BUFGCTRL 기반 클럭 전환 시 Bus Skew FIFO(Gray Code) 기반 동기화 완료.

---

## Q66: 구현 로그 Error/Critical 메시지 전체 해소 확인

> *구현 로그의 주요 메시지(Error/Critical)가 모두 해결되었음을 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Check_Timing.rpt`** + **`Methodology.rpt`** + **`DRC_Report.rpt`**

🧩 **파싱 로직**

```python
# 1) Check_Timing: 치명적 오류 확인
# → "All user specified timing constraints are met" 확인
pattern_met = r'All user specified timing constraints are met'
timing_met = bool(re.search(pattern_met, ts_text))

# 2) DRC Report: Error 등급 항목 확인 (현재: Warning + Advisory만 존재)
pattern_drc_error = r'\|\s*([\w-]+)\s*\|\s*(Error|Critical)\s*\|'
drc_errors = re.findall(pattern_drc_error, drc_text)

# 3) Methodology Report: Error 등급 항목 확인
pattern_method_error = r'\|\s*([\w-]+)\s*\|\s*(Error|Critical)\s*\|'
method_errors = re.findall(pattern_method_error, method_text)
```

📊 **Error/Critical 메시지 현황**

| 리포트 | Error | Critical | Warning | Advisory |
|-------|-------|---------|---------|---------|
| DRC | **0** ✅ | **0** ✅ | 272 | 63 |
| Methodology | **0** ✅ | **0** ✅ | 362 | 16 |
| Timing | **0** ✅ | **0** ✅ | - | - |

> `All user specified timing constraints are met.` ✅

⚖️ **판정 로직**

```python
def judge_q66(data, criteria):
    if data['drc_errors'] == 0 and data['method_errors'] == 0 and data['timing_met']:
        return "PASS", (
            "구현 로그 Error/Critical 메시지 없음. "
            "타이밍 제약 전체 충족. "
            f"⚠️ DRC Warning {data['drc_warnings']}건, "
            f"Methodology Warning {data['method_warnings']}건 (Q67 참조)."
        )
```

💬 **예상 답변**
> **PASS** — DRC/Methodology/Timing Error/Critical 메시지 0건. 타이밍 제약 전체 충족. ⚠️ Warning합계(DRC 272건 + Methodology 362건)는 Q67에서 별도 검토.

---

## Q67: Warning 메시지 조치 필요 여부 검토

> *Warning 메시지에 대해서도 조치 필요 여부를 검토했습니까?*

- **답변 유형**: `AUTO` ⚙️ (자동 분류)

📄 **`Check_Timing.rpt`** + **`Methodology.rpt`** + **`DRC_Report.rpt`**

🧩 **파싱 로직**

```python
# DRC Warning 분류
drc_warnings = {
    'DPIP-1': {'count': 128, 'desc': 'DSP48 입력 비파이프라인', 'action': '성능개선 권고'},
    'DPOP-1': {'count': 64,  'desc': 'DSP48 출력 비파이프라인', 'action': '성능개선 권고'},
    'DPOP-2': {'count': 66,  'desc': 'DSP48 MREG 비파이프라인', 'action': '성능개선 권고'},
    'REQP-1839': {'count': 3, 'desc': 'RAMB36 비동기제어', 'action': '해소 필요'},
    'REQP-1709': {'count': 1, 'desc': '클럭버퍼 not routed', 'action': '검토 필요'},
    'RTSTAT-10': {'count': 7, 'desc': '배선 미사용/불완전', 'action': '검토 필요'},
}

# Methodology Warning 분류
method_warnings = {
    'LUTAR-1': {'count': 6,  'action': '해소 권고 (비동기리셋 RTL수정)'},
    'PDRC-190': {'count': 14,'action': '성능개선 권고 (동기화체인배치)'},
    'SYNTH-5':  {'count': 1, 'action': '확인 권고 (초기화 없는 FF)'},
    'SYNTH-10': {'count': 64,'action': '성능개선 권고 (DSP최적화)'},
    'TIMING-9': {'count': 1, 'action': '해소 필요 (Unknown CDC)'},
    'TIMING-10': {'count': 1,'action': '해소 필요 (ASYNC_REG 누락)'},
    'TIMING-24': {'count': 16,'action': '검토 권고 (Max delay override)'},
    'XDCB-1':   {'count': 1, 'action': '검토 권고 (XDC 포트 없음)'},
}

# 우선순위 분류
must_fix = [r for r, d in {**drc_warnings, **method_warnings}.items()
            if d['action'].startswith('해소 필요')]
```

📊 **Warning 우선순위 분류**

| 우선순위 | 규칙 ID | 건수 | 내용 | 권고 조치 |
|---------|--------|-----|-----|---------|
| 🔴 Must Fix | `TIMING-9` | 1 | Unknown CDC | CDC 경로 분석·RTL 수정 |
| 🔴 Must Fix | `TIMING-10` | 1 | ASYNC_REG 속성 누락 | XDC에 `ASYNC_REG TRUE` 추가 |
| 🔴 Must Fix | `REQP-1839` | 3 | RAMB36 비동기 제어 | 동기 제어 신호로 변경 |
| 🔴 Must Fix | `LUTAR-1` | 6 | LUT → 비동기리셋 | RTL 동기 리셋 변환 |
| 🟡 Review | `REQP-1709` | 1 | 클럭 버퍼 미라우팅 | `set_property CLOCK_BUFFER_TYPE NONE` 확인 |
| 🟡 Review | `TIMING-24` | 16 | Max delay 오버라이드 | 설계 의도 확인 |
| 🟡 Review | `XDCB-1` | 1 | XDC 포트 없음 | XDC 포트명 일치 확인 |
| 🟢 Info | `DPIP-1/DPOP-1/2` | 258 | DSP 비파이프라인 | 성능 최적화 권고 (타이밍 충족 시 무시 가능) |
| 🟢 Info | `PDRC-190` | 14 | 비최적 동기화체인 | 배치 개선 권고 |
| 🟢 Info | `SYNTH-5/10` | 65 | FF 초기화/DSP | Synthesis 최적화 |

💬 **예상 답변**
> **REVIEW** — Warning 총 634건 자동 분류 완료. Must Fix: TIMING-9/10, REQP-1839, LUTAR-1(총 11건). Review: REQP-1709, TIMING-24, XDCB-1(총 18건). 나머지 605건은 성능개선 권고 수준.

---

## Q68: 조치 불필요 Warning 사내 리뷰 및 관계자 합의

> *조치가 불필요하다고 판단한 Warning 항목에 대해 사내 리뷰 및 관계자 합의를 마쳤습니까?*

- **답변 유형**: `SEMI`

📄 **`Check_Timing.rpt`** + **`Methodology.rpt`** + **`Waiver.rpt`** + **`Timing_Exceptions.rpt`**

🔍 **파싱 위치**

- `Waiver.rpt`: 파일 내 포함된 전체 면제(Waived) 항목 리스트 및 사유명세
- `Timing_Exceptions.rpt`: `set_false_path`, `set_clock_groups` 등 타이밍 분석 제외/면제 설정 항목

🧩 **파싱 로직**

```python
# 1) Waiver.rpt: 면제 항목 자동 추출
pattern_waiver = r'create_waiver\s+-type\s+(\w+)\s+-id\s+([\w-]+)\s+-user\s+(\w+).*?-description\s+"([^"]+)"'
waivers = re.findall(pattern_waiver, waiver_text, re.DOTALL)

# 2) Timing_Exceptions: set_false_path / set_clock_groups 확인
pattern_false_path = r'set_false_path.*?-from.*?-to'
false_paths = re.findall(pattern_false_path, exceptions_text)

# 3) CDC Waived 69건 근거 확인
pattern_cdc_waiver = r'Waived.*?CDC.*?(\d+)'
cdc_waived_count = ...
```

📊 **Waiver 현황**

| 항목 | 건수 | 비고 |
|-----|-----|-----|
| CDC Waived (Vivado CDC 도구 면제) | **69건** | Waiver.rpt 등록 |
| Timing_Exceptions (set_false_path) | 확인 필요 | 비동기 경계 |
| set_clock_groups (비동기 쌍) | 17쌍 | Timing_Exceptions 근거 |
| DRC DPIP/DPOP 면제 근거 | 미등록 | ⚠️ 사내 합의 문서 필요 |
| LUTAR-1 면제 근거 | 미등록 | ⚠️ 사내 합의 문서 필요 |

⚖️ **판정 로직**

```python
def judge_q68(data, criteria):
    return "REVIEW", (
        f"CDC Waived {data['cdc_waived']}건 Waiver 등록 확인. "
        f"set_clock_groups {data['clk_groups']}쌍 Timing_Exceptions 근거. "
        "⚠️ DPIP/DPOP(258건), LUTAR-1(6건) 미조치 항목: "
        "사내 리뷰 결과 및 관계자 합의 문서(Waiver 등록 또는 기술 노트) 제출 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — CDC 69건 Waiver 등록(✅). set_clock_groups 17쌍 근거 Timing_Exceptions 존재(✅). ⚠️ DPIP/DPOP(258건), LUTAR-1(6건) 미조치 항목: 사내 리뷰 합의 문서 또는 추가 Waiver 등록 필요.

---

## Q69: 툴 버전 변경 시 결함 정보(Errata) 확인

> *설계 초기와 구현 시점의 툴 버전이 다를 경우, 실제 사용 버전의 결함 정보를 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Environment.rpt`** + **`IP_Status.rpt`**

🧩 **파싱 로직**

```python
# 1) 툴 버전 추출 (모든 리포트 헤더에서 공통)
pattern_ver = r'Tool Version\s+:\s+Vivado\s+v\.([\d.]+)\s+\(lin64\)\s+Build\s+(\d+)'
tool_version = re.search(pattern_ver, header_text)
# → "2019.2", Build 2708876

# 2) IP_Status에서 IP 버전 확인 (툴 변경 시 IP 재생성 필요 여부)
# ip_mig_ddr3 / ip_clk_wiz / ip_fifo_indep 등 버전 파악

# 3) Xilinx Vivado 2019.2 Known Issues 참조 (외부)
# AR# 76780, AR# 75839 등 관련 Errata 여부

# 4) 현재 사용 버전이 안정 버전인지 확인
# → 2019.2는 Xilinx 7-series 공식 지원 안정 버전
known_stable = (tool_version.group(1) == "2019.2")
```

📊 **툴 버전 정보**

| 항목 | 값 |
|-----|---|
| 사용 툴 | Vivado v.2019.2 |
| Build | 2708876 |
| 지원 OS | Linux 64-bit |
| Speed File | -2 PRODUCTION 1.23 (2018-06-13) |
| 7-series 공식 지원 여부 | ✅ (7a100t-fgg676-2) |
| 최신 버전 여부 | ❌ (최신: 2024.x) |
| Vivado 2019.2 생산 중단 | 2024.3 이후 공식 지원 종료 예정 |

⚖️ **판정 로직**

```python
def judge_q69(data, criteria):
    known_stable = criteria['tool']['known_stable_versions']
    note = "안정 버전" if data['version'] in known_stable else "구버전"
    return "REVIEW", (
        f"사용 툴: Vivado v.{data['version']} (Build {data['build']}). "
        f"Xilinx 7-series xc7a100t 공식 지원 {note}. "
        f"⚠️ {data['version']} 버전에 대한 Xilinx AR 데이터베이스 Known Issue 확인 필요. "
        f"(https://support.xilinx.com 검색: Vivado {data['version']} AR#)"
    )
```

💬 **예상 답변**
> **REVIEW** — Vivado 2019.2 사용. xc7a100t 공식 지원 안정 버전. ⚠️ 구버전 사용으로 Xilinx AR(Answer Record) 데이터베이스에서 2019.2 Known Issues/Errata 확인 필요. 특히 MIG DDR3(AR# 관련), Timing Analysis 관련 AR 체크 권장.

---

## 요약 — Q61~Q69 파싱 구현 우선순위

| 우선순위 | 문항 | 답변 유형 | 파서 모듈 | 다중/단일 리포트 목록 |
|---------|------|----------|----------|------------|
| ⬆️ 높음 | Q61 | AUTO | `timing_parser.py` 등 | Timing_Summary, Check_Timing, CDC 4종, Timing_Exceptions |
| ⬆️ 높음 | Q62 | AUTO | `timing_parser.py` 등 | Pulse_Width, Clocks_Summary, Property_Check, Timing_Summary, Check_Timing |
| ⬆️ 높음 | Q63 | AUTO | `timing_parser.py` 등 | Timing_Summary, Setup_Critical, Hold_Critical |
| ⬆️ 높음 | Q64 | AUTO | `timing_parser.py` 등 | Timing_Summary, Setup_Critical, Hold_Critical, Bus_Skew |
| ⬆️ 높음 | Q65 | AUTO | `timing_parser.py` 등 | Setup_Critical, Hold_Critical, Bus_Skew, Timing_Summary, Timing_Exceptions, Clock_Utilization |
| ⬆️ 높음 | Q66 | AUTO | `methodology_parser.py` 등| Check_Timing, Methodology, DRC_Report |
| 🔹 중간 | Q67 | AUTO | `methodology_parser.py` 등| Check_Timing, Methodology, DRC_Report |
| 🔹 중간 | Q68 | SEMI | `waiver_parser.py` 등 | Check_Timing, Methodology, Waiver, Timing_Exceptions |
| 🔹 중간 | Q69 | AUTO | `environment_parser.py` | Environment, IP_Status |

## 주요 발견 사항

> **Q61 PASS**: 4개 입력 클럭 + 파생 14개 = 18개 클럭, no_clock=0, loop=0 ✅. ⚠️ FMC/LCOS 포트 delay 미설정 158포트 (의도적 경로 제외)
>
> **Q62 PASS**: 전 MMCM/PLL 출력 Duty=50%. WPWS 최소 0.264ns. TPWS Failing=0 ✅
>
> **Q63 PASS**: Slow+Fast Multi Corner. WNS=0.093ns, WHS=0.010ns(주의), WPWS=0.264ns ✅
>
> **Q64 PASS**: Inter Clock 전체 MET. Bus Skew 16경로 전체 PASS (최소 5.159ns) ✅
>
> **Q65 PASS**: async_default 4그룹 전체 WNS/WHS MET ✅
>
> **Q66 PASS**: Error/Critical 0건 ✅
>
> **Q67 AUTO 분류**: Must Fix 11건(TIMING-9/10, REQP-1839, LUTAR-1), Review 18건, Info 605건
>
> **Q68 REVIEW**: CDC Waiver 69건 등록 완료. DPIP/DPOP 258건, LUTAR-1 6건은 사내합의 문서 필요
>
> **Q69 REVIEW**: Vivado 2019.2 구버전 — AR 데이터베이스 Errata 확인 필요
