# Q11~Q20 상세 파싱 계획서

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

## Q11: 자원 사용률 (FF, LUT, RAM, 클럭, IO, SerDes)

> *자원 사용률이 과거 사례 대비 예측 가능한 범위 내에 있습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Clock_Utilization.rpt`** + **`Utilization.rpt`** + **`Control_Sets.rpt`** + **`IO_Report.rpt`** + **`PR_PBLOCK_Utilization.rpt`** + **`QoR_Assessment.rpt`**

🔍 **Clock_Utilization.rpt 파싱 위치**

- `Clock Primitive Utilization` 센션 하위 테이블
- `Global Clock Resources` 센션 하위 테이블

🔍 **Utilization.rpt 파싱 위치**

- 메인 요약 테이블 또는 `1. Slice Logic` 하위 구조에서 `(top)` 모듈을 나타내는 최상위 행
- 컬럼: Instance, Module, Total LUTs, Logic LUTs, LUTRAMs, SRLs, FFs, RAMB36, RAMB18, DSP48

🔍 **IO_Report.rpt 파싱 위치**

- `1. Summary` 섹션 내 `Total User IO` 수치

🔍 **QoR_Assessment.rpt 파싱 위치**

- `QoR Assessment Details` 섹션 내부 요약 테이블 구조 (Threshold vs Actual)

🔍 **주요 파싱 위치 (추가 리포트)**

- `Control_Sets.rpt`: 컨트롤 셋 자원 및 라우팅 효율 평가 요약표
- `PR_PBLOCK_Utilization.rpt`: 존재 시 Pblock 기반 자원 사용률 테이블

🧩 **파싱 로직**

```python
# 1) Utilization.rpt — top-level 행 (첫 번째 데이터 행)
pattern_util_top = r'\|\s*top_with_ddr3\s*\|.*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|'
# 캡처: total_luts, logic_luts, lutrams, srls, ffs, ramb36, ramb18, dsp48

# 2) Clock_Utilization.rpt — Primitive 테이블
pattern_clk_prim = r'\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|'
# 캡처: type(BUFGCTRL/MMCM/PLL), used, available

# 3) IO_Report.rpt — Total User IO
pattern_io_total = r'\|\s*(\d+)\s*\|'  # Summary 섹션

# 4) QoR_Assessment.rpt — 리소스별 Threshold vs Actual
pattern_qor_row = r'\|\s+([\w\s]+?)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|'
# 캡처: name, threshold, actual%, used, available, status

# 5) 디바이스 총량 (xc7a100t 기준)
DEVICE_RESOURCES = {
    'LUT': 63400, 'FF': 126800, 'BRAM36': 135,
    'DSP48': 240, 'IO': 300, 'BUFG': 32, 'MMCM': 6, 'PLL': 6
}

# 6) Control_Sets.rpt — Control Sets 사용 개수 추출
pattern_ctrl_set = r'\|\s*Total control sets\s*\|\s*(\d+)\s*\|'

# 7) PR_PBLOCK_Utilization.rpt — Pblock별 사용률
pattern_pblock_util = r'\|\s*(pblock_\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|'

📊 **추출 결과**

| 리소스 | Used | Available | 사용률(%) | QoR Status |
|--------|------|-----------|-----------|------------|
| LUT (Logic) | 34,634 | 63,400 | 54.6% | OK |
| LUT (Total) | 37,174 | 63,400 | 58.6% | OK |
| LUT Combined | 8,528 | 37,174 | 22.9% | **REVIEW** (>20%) |
| FF (Register) | 37,601 | 126,800 | 29.7% | OK |
| BRAM (36+18) | 52+110=107 | 135 | 79.3% | OK (임계 80%) |
| DSP48 | 133 | 240 | 55.4% | OK |
| BUFGCTRL | 17 | 32 | 53.1% | — |
| MMCM | 5 | 6 | 83.3% | — |
| PLL | 2 | 6 | 33.3% | — |
| IO | 184 | 300 | 61.3% | — |
| Control Sets | 1,042 | 15,850 | 6.6% | OK |

⚖️ **판정 로직**

```python
# THRESHOLDS는 config/criteria.json에서 로드됨
# 예: THRESHOLDS = criteria['utilization']['thresholds']

def judge_q11(util_data, criteria):
    thresholds = criteria['utilization']['thresholds']
    warnings = []
    for res, pct in util_data.items():
        limit = thresholds.get(res, 90)
        if pct >= limit:
            warnings.append(f"{res}: {pct:.1f}% (임계 {limit}%)")
    if warnings:
        return "REVIEW", f"임계 초과 자원: {', '.join(warnings)}"
    return "PASS", "모든 자원 사용률 임계값 이내"
```

💬 **예상 답변**
> **REVIEW** — 대부분 자원 적정 범위. ⚠️ **BRAM 79.3%** (임계 80% 근접), **MMCM 83.3%** (5/6), **LUT Combined 22.9%** (QoR REVIEW). LUT 58.6%, FF 29.7%, DSP 55.4%, IO 61.3%는 양호. Pblock 분할/PR 사용 시 각 Pblock 내부 자원 효율 점검, 전체 Control Sets는 1,042/15,850(6.6%)으로 여유.

---

## Q12: 스피드 그레이드 적정성 (타이밍 성능)

> *FPGA/PLD 스피드 그레이드가 요구 타이밍 성능에 적절함을 확인했습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Timing_Summary.rpt`** + **`Setup_Critical.rpt`** + **`Hold_Critical.rpt`** + **`QoR_Assessment.rpt`** + **`Datasheet.rpt`** + **`Check_Timing**

🔍 **Timing_Summary.rpt 파싱 위치**

- 상단 헤더 섹션: `Device` 및 `Speed File` 정보 추출
- `check_timing` 섹션: `register/latch pins with no clock` 등의 제약 부족 카운팅
- 상단 Summary 섹션의 Unconstrained Paths 목록

🔍 **QoR_Assessment.rpt 파싱 위치**

- `QoR Assessment Details` 섹션 내부의 `WNS`, `TNS`, `WHS`, `THS` 요약 행

🔍 **Datasheet.rpt 파싱 위치**

- `Setup between Clocks` 섹션 (클럭 도메인 간 최악 경로)

🔍 **비고 (세부 분석 리포트)**

- `Setup_Critical.rpt`: Setup 타이밍 (WNS) 관련 Critical Path 세부 분석
- `Hold_Critical.rpt`: Hold 타이밍 (WHS) 관련 Critical Path 세부 분석

🧩 **파싱 로직**

```python
# 1) 스피드 그레이드
pattern_speed = r'Speed File\s*:\s*(-\d+)\s+(\w+)\s+([\d.]+)'
# 캡처: grade(-2), status(PRODUCTION), version(1.23)

# 2) QoR 타이밍 값
pattern_wns = r'\|\s+WNS\s+\|\s+[\d.]+\s+\|\s+([-\d.]+)\s+\|'
pattern_tns = r'\|\s+TNS\s+\|\s+[\d.]+\s+\|\s+([-\d.]+)\s+\|'
pattern_whs = r'\|\s+WHS\s+\|\s+[\d.]+\s+\|\s+([-\d.]+)\s+\|'
pattern_ths = r'\|\s+THS\s+\|\s+[\d.]+\s+\|\s+([-\d.]+)\s+\|'

# 3) no_input_delay / no_output_delay 경고 수
pattern_no_input = r'There are (\d+) input ports with no input delay'
pattern_no_output = r'There are (\d+) output ports with no output delay'

# 4) check_timing 항목별 0/비0 체크
pattern_check = r'There are (\d+) register/latch pins with (no clock|constant_clock|multiple clocks)'

# 5) Setup/Hold_Critical.rpt — 최악 경로 세부 검사
pattern_crit_path = r'Slack\s*:\s*([-\d.]+)\s*ns.*?Source\s*:\s*(\S+).*?Destination\s*:\s*(\S+)'
# 캡처: slack_ns, source_cell, dest_cell
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `speed_grade` | -2 |
| `speed_status` | PRODUCTION |
| `WNS` (Setup) | +0.09 ns ✅ |
| `TNS` | 0.00 ns ✅ |
| `WHS` (Hold) | +0.01 ns ✅ |
| `THS` | 0.00 ns ✅ |
| `no_clock_pins` | 0 ✅ |
| `no_input_delay_ports` | 56 ⚠️ (HIGH) |
| `no_output_delay_ports` | 0 ✅ |
| `combinational_loops` | 0 ✅ |
| `clock_domains` | 5개 (pin_i_clk_100m, pin_i_clk_20m, pin_i_clk_78m, pin_i_fmc_clk) |

⚖️ **판정 로직**

```python
def judge_q12(timing, criteria):
    wns_warn_th = criteria['timing']['wns_warning_threshold'] # 예: 0.5
    if timing['WNS'] < 0 or timing['WHS'] < 0:
        return "FAIL", f"타이밍 위반: WNS={timing['WNS']}ns, WHS={timing['WHS']}ns"
    warnings = []
    if timing['WNS'] < wns_warn_th:
        warnings.append(f"Setup 마진 미소: WNS={timing['WNS']}ns")
    if timing['no_input_delay'] > 0:
        warnings.append(f"Input delay 미지정 포트 {timing['no_input_delay']}개")
    if warnings:
        return "REVIEW", "; ".join(warnings)
    return "PASS", "타이밍 충족, 충분한 마진"
```

💬 **예상 답변**
> **REVIEW** — Speed Grade **-2** (PRODUCTION). 타이밍 충족: WNS=+0.09ns, WHS=+0.01ns, TNS/THS=0. ⚠️ Setup 마진 미소(0.09ns), Input delay 미지정 포트 56개(HIGH). 4개 클럭 도메인 간 교차 경로 존재 확인. Critical Path 확인(Setup_Critical.rpt) 결과 `u_ddr_ctrl` 내 경로가 병목 요소임.

---

## Q13: 최대 소비전력 요구 사양 초과 여부

> *FPGA/PLD 최대 소비전력이 요구 사양을 초과하지 않음을 확인했습니까?*

- **답변 유형**: `SEMI` — 전력 값 추출 가능, 요구 사양은 외부 문서

📄 **`Power_Data.rpt`** + **`Power_Report.rpt`** + **`Power_Opt.rpt`** + **`Operating_Cond.rpt`**

🔍 **주요 파싱 위치**

- `Power_Report.rpt` (혹은 `Power_Data.rpt`): Total Power, Junction Temp, Confidence Level
- `Power_Opt.rpt`: 전력 최적화 조치 확인
- `Operating_Cond.rpt`: 설정된 동작 조건(온도, 전압)과 환경 일치성

🧩 **파싱 로직**

```python
# 1) Summary
pattern_total_power = r'Total On-Chip Power \(W\)\s*\|\s*([\d.]+)'
pattern_dynamic = r'Dynamic \(W\)\s*\|\s*([\d.]+)'
pattern_static = r'Device Static \(W\)\s*\|\s*([\d.]+)'
pattern_junction = r'Junction Temperature \(C\)\s*\|\s*([\d.]+)'
pattern_max_ambient = r'Max Ambient \(C\)\s*\|\s*([\d.]+)'
pattern_confidence = r'Confidence Level\s*\|\s*(\w+)'
pattern_budget = r'Design Power Budget \(W\)\s*\|\s*(.*)'

# 2) On-Chip Components 테이블
pattern_component = r'\|\s+([\w/ ]+?)\s+\|\s+([\d.<]+)\s+\|\s+(\d*)\s+\|\s+(\d*)\s+\|\s+([\d.]*)\s+\|'
# 캡처: component, power_w, used, available, util%

# 3) Power_Opt.rpt — 전력 최적화 수행 여부 확인
pattern_power_opt = r'Power Optimization\s*\|\s*(.*)'

# 4) Operating_Cond.rpt — 온도/전압 보드 환경 설정 확인
pattern_ambient = r'Ambient Temp \(C\)\s*\|\s*([\d.]+)'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `total_power` | 2.236 W |
| `dynamic_power` | 1.799 W |
| `static_power` | 0.437 W |
| `junction_temp` | 85.8°C |
| `max_ambient` | 94.2°C |
| `confidence` | **Low** ⚠️ |
| `design_budget` | Unspecified ⚠️ |
| 주요 소비원 | Clocks 0.214W, Slice Logic 0.128W, MMCM **0.515W**, PLL 0.221W, I/O 0.289W, BRAM 0.117W |

⚖️ **판정 로직**

```python
def judge_q13(power, criteria):
    max_junction_temp = criteria['power']['max_junction_temp'] # 예: 100

    issues = []
    if power['junction_temp'] > max_junction_temp:
        issues.append(f"접합 온도 초과: {power['junction_temp']}°C")
    if power['confidence'] == 'Low':
        issues.append("전력 추정 신뢰도 Low — 시뮬레이션 Activity 미반영")
    if power['design_budget'] == 'Unspecified':
        issues.append("Design Power Budget 미설정")
    if issues:
        return "REVIEW", "; ".join(issues)
    return "PASS", "전력 요구 사양 이내"
```

💬 **예상 답변**
> **REVIEW** — 총 소비전력 **2.236W** (Dynamic 1.799W + Static 0.437W). 접합 온도 85.8°C (Industrial Grade, Ambient Temp 25°C 셋업 기준). ⚠️ 신뢰도 **Low** (I/O Activity 75%+ 미지정, Internal nodes 25% 미만). Design Power Budget **미설정** — 요구 사양 대비 비교 불가. 전력 최적화(Power_Opt.rpt) 미적용 확인.

---

## Q14: 전압 레일별 소비전류 적정성

> *각 전압 레일별 소비전류가 전원 공급 사양 이하임을 확인했습니까?*

- **답변 유형**: `SEMI` — 전류 값 추출 가능, 공급 사양은 외부 문서

📄 **`Power_Data.rpt`** + **`Power_Report.rpt`** + **`Switching_Activity.rpt`**

🔍 **주요 파싱 위치**

- `Power_Report.rpt` (혹은 `Power_Data.rpt`): Power Supply Summary 테이블 (Vccint, Vccaux 등 각 레일별 전류)
- `Switching_Activity.rpt`: 동적 전력 계산의 근거가 되는 스위칭 액티비티 리뷰

🧩 **파싱 로직**

```python
# Power Supply Summary (Power_Report.rpt)
pattern_supply = r'\|\s+(\w+)\s+\|\s+([\d.]+)\s+\|\s+([\d.*]+)\s+\|\s+([\d.]+)\s+\|\s+([\d.]+)\s+\|'
# 캡처: source, voltage_v, total_a, dynamic_a, static_a

# 스위칭 액티비티 글로벌 기본값 (Switching_Activity.rpt)
pattern_default_toggle = r'Default Toggle Rate\s*:\s*([\d.]+)%'
pattern_default_static = r'Default Static Probability\s*:\s*([\d.]+)'
```

📊 **추출 결과**

| 전원 레일 | 전압(V) | 총 전류(A) | Dynamic(A) | Static(A) | 비고 |
|-----------|---------|-----------|------------|-----------|------|
| Vccint | 1.000 | 0.957 | 0.652 | 0.305 | 코어 전원 |
| Vccaux | 1.800 | 0.587 | 0.521 | 0.066 | 보조 전원 |
| Vcco33 | 3.300 | 0.043* | 0.020 | 0.023 | Bank 16 (FMC) |
| Vcco18 | 1.800 | 0.043* | 0.037 | 0.006 | Bank 13 (LCOS) |
| Vcco135 | 1.350 | 0.052 | 0.049 | 0.003 | Bank 34/35 (DDR3) |
| Vccbram | 1.000 | 0.062* | 0.010 | 0.052 | BRAM 전원 |
| Vccadc | 1.800 | 0.031 | 0.001 | 0.030 | XADC |

> `*` = Power-up current

⚖️ **판정 로직**

```python
def judge_q14(supply_data, spec_limits=None):
    if spec_limits is None:
        return "REVIEW", "전원 공급 사양(Spec) 미제공 — 각 레일 전류값만 제시"
    violations = []
    for rail in supply_data:
        if rail['total_a'] > spec_limits.get(rail['source'], float('inf')):
            violations.append(f"{rail['source']}: {rail['total_a']}A > Spec {spec_limits[rail['source']]}A")
    if violations:
        return "FAIL", f"전류 초과: {', '.join(violations)}"
    return "PASS", "모든 레일 사양 이내"
```

💬 **예상 답변**
> **REVIEW** — 전압별 전류: Vccint=0.957A, Vccaux=0.587A, Vcco33=0.043A, Vcco18=0.043A, Vcco135=0.052A. 기본 스위칭 토글률 12.5%, Static Prob 0.5 적용됨. ⚠️ 전원 공급 사양(Supply Capacity)은 리포트에 미포함 — PCB 회로도 대비 별도 검토 필요. 신뢰도 Low 유의.

---

## Q15: 기능 요구 사양 충족 리뷰

> *FPGA로 구현되는 기능이 요구 사양을 만족함을 리뷰로 확인했습니까?*

- **답변 유형**: `SEMI` — QoR 점수 제공 가능, 기능 리뷰는 외부 문서

📄 **`QoR_Assessment.rpt`** + **`QoR_Suggestions.rpt`** + **`Pipeline_Analysis.rpt`** + **`High_Fanout.rpt`** + **`PR_PBLOCK_Utilization.rpt`**

🔍 **주요 파싱 위치**

- `QoR_Assessment.rpt`, `QoR_Suggestions.rpt`: 전반적인 설계 품질 점수 및 제안
- `Pipeline_Analysis.rpt`: 경로 성능 최적화(파이프라이닝) 분석
- `High_Fanout.rpt`: 타이밍 병목이 되는 High Fanout 넷 조치 분석
- `PR_PBLOCK_Utilization.rpt`: 블록별 자원 균형 (QoR 기여도)

🧩 **파싱 로직**

```python
# 1) QoR Score
pattern_score = r'QoR Assessment Score\s*\|\s*(\d+)\s*-\s*(.*?)\s*\|'
# 캡처: score(5), description("Design runs will meet timing")

# 2) Methodology Status
pattern_method = r'Methodology Status\s*\|\s*(.*?)\s*\|'

# 3) Methodology violations
pattern_violation = r'\|\s+(\w+-\d+)\s+\|\s+(.*?)\s+\|\s+(\w+)\s+\|\s+(\d+)\s+\|'
# 캡처: id, description, criticality, count

# 4) DONT_TOUCH count
pattern_dont_touch = r'DONT_TOUCH \(cells/nets\)\s*\|\s*\d+\s*\|\s*(\d+)'

# 5) High_Fanout.rpt — 팬아웃 10000 이상 넷 개수 파악
pattern_high_fanout = r'Fanout\s*>\s*10000\s*(:)?\s*(\d+) nets'

# 6) Pipeline_Analysis.rpt — 파이프라이닝 제안 카운트 파악
pattern_pipeline_sugg = r'Number of paths suggested for pipelining\s*\|\s*(\d+)'

```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `qor_score` | 5 — "Design runs will meet timing" |
| `methodology_status` | Failed with warnings |
| `ml_compatible` | Yes |
| `incremental_compatible` | Yes |
| `dont_touch_count` | 36,870 (REVIEW) |
| `dont_touch_mark_debug` | 0 (OK) |
| `congestion` | OK (Level 5 미만) |
| `high_fanout_10k` | 0 (OK) |

⚖️ **판정 로직**

```python
def judge_q15(qor):
    if qor['score'] >= 4:
        status = "PASS" if qor['methodology'] == "Passed" else "REVIEW"
        msg = f"QoR Score {qor['score']}/5. Methodology: {qor['methodology']}"
        if qor['dont_touch'] > 0:
            msg += f". DONT_TOUCH {qor['dont_touch']}개 — IP 자동 생성으로 추정"
        if qor['high_fanout'] > 0:
            msg += f". High Fanout 넷 {qor['high_fanout']}개 (최적화 불리)"
        return status, msg
    return "FAIL", f"QoR Score {qor['score']}/5 — 타이밍 미충족 위험"
```

💬 **예상 답변**
> **REVIEW** — QoR Score **5/5** (타이밍 충족). ⚠️ Methodology "Failed with warnings": DONT_TOUCH 36,870개 (IP 자동 생성 기인, MARK_DEBUG 0개). Congestion/Fanout 양호. 기능 사양 충족 여부는 별도 설계 리뷰 문서 필요.

---

## Q16: 요구 사양 외 독자 기능 추가 여부

> *요구 사양에 없는 독자적 기능을 추가하지 않았습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **참조 리포트 없음** — 설계 사양 비교 문서 필요

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 요구 사양 외 기능 추가 여부는 리포트에서 확인할 수 없습니다. 설계 사양서 대비 기능 비교표를 제출해 주세요.

---

## Q17: 16번 추가 기능이 디버그 목적인지

> *16번 항목의 구현 기능은 디버그 목적입니까?*

- **답변 유형**: `EVIDENCE_NEEDED` (Q16 종속)

📄 **참조 리포트 없음**

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — Q16 종속 문항. 추가 기능 존재 시, 디버그 목적 여부를 명시해 주세요.

---

## Q18: 디버그/테스트 기능 보호 (패스워드 등)

> *디버그 기능이 정상 운용 중 오작동하지 않도록 보호되어 있습니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Debug_Core.rpt`** + **`Partial_Bit_Config_Summary.rpt`**

🔍 **주요 파싱 위치**

- `Debug_Core.rpt`: 디버그 코어 유무 확인
- `Partial_Bit_Config_Summary.rpt`: 재설정(리셋 루프 등) 방지/보안 관련 확인

🧩 **파싱 로직**

```python
# Debug Core 존재 여부
pattern_no_debug = r'No debug cores were found in this design'
pattern_debug_core = r'\|\s+(\S+)\s+\|\s+(\S+)\s+\|\s+(\d+)\s+\|'
# 캡처: core_name, type, probe_count (코어 존재 시)
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `debug_cores_found` | 0 |
| `ila_cores` | 0 |
| `vio_cores` | 0 |
| `mark_debug_nets` | 0 (QoR에서 확인) |

⚖️ **판정 로직**

```python
def judge_q18(debug_data):
    if debug_data['debug_cores'] == 0 and debug_data['mark_debug'] == 0:
        return "PASS", "디버그 코어 없음 — 보호 불필요 (프로덕션 빌드)"
    elif debug_data['debug_cores'] > 0:
        return "REVIEW", f"디버그 코어 {debug_data['debug_cores']}개 발견 — 보호 조치 확인 필요"
    return "PASS", "해당 없음"
```

💬 **예상 답변**
> **PASS** — 디버그 코어 **없음** (ILA/VIO 0개, MARK_DEBUG 0개). 프로덕션 빌드로 확인됨 — 디버그 기능 보호 조치 불필요.

---

## Q19: 외부 메모리 인터페이스 검증

> *외부 메모리(DDR, SSRAM, Flash, FMC) 인터페이스의 기동, 초기화, 캘리브레이션을 검증했습니까?*

- **답변 유형**: `SEMI` — DDR3 인터페이스 존재 확인 + IO 정보 제공 가능

📄 **`IO_Report.rpt`** + **`Datasheet.rpt`** + **`Utilization.rpt`**

🔍 **IO_Report.rpt 파싱 위치**

- 패드/핀 매핑 테이블에서 신호명 기준 매칭 (예: `ddr3_*` 신호, I/O Standard가 SSTL135, DIFF_SSTL135 등인지 파악)

🔍 **Datasheet.rpt 파싱 위치**

- `Input Ports Setup/Hold` 섹션 내부의 특정 외부 메모리 DQ/DQS 포트 타이밍 마진
- `Output Ports Clock-to-out` 섹션
- `Setup between Clocks` 섹션

🔍 **Utilization.rpt 파싱 위치**

- 계층형 리소스 사용 테이블 (`Hierarchy` 기준) 내의 MIG 생성 컨트롤러(예: `u_ddr3_top` 또는 `.ip_mig_ddr3`) 행 탐색

🧩 **파싱 로직**

```python
# 1) DDR3 신호 존재 확인 (IO_Report)
pattern_ddr3_io = r'\|\s+(ddr3_\w+)\s+\|.*?\|\s+(\w+)\s+\|\s+([\w]+)\s+\|.*?\|\s+(\d+)\s+\|'
# 캡처: signal_name, direction, io_standard, bank

# 2) DDR3 DQ Setup/Hold (Datasheet)
pattern_ddr3_timing = r'pin_i_clk_100m\s+\|\s+(ddr3_dq\[\d+\])\s+\|.*?\|\s+([-\d.]+)\s+\((\w)\)\s+\|.*?\|\s+([-\d.]+)\s+\((\w)\)\s+\|'
# 캡처: signal, setup_ns, edge, hold_ns, edge

# 3) MIG IP 존재 확인 (Utilization)
pattern_mig = r'\|\s*(u_ddr3_top.*?ip_mig_ddr3)\s*\|'

# 4) DDR3 신호 분류
DDR3_SIGNALS = {
    'addr': r'ddr3_addr\[\d+\]',
    'ba': r'ddr3_ba\[\d+\]',
    'dq': r'ddr3_dq\[\d+\]',
    'dqs': r'ddr3_dqs_[np]\[\d+\]',
    'dm': r'ddr3_dm\[\d+\]',
    'ctrl': r'ddr3_(ck_[np]|cke|cs_n|ras_n|cas_n|we_n|odt|reset_n)'
}
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `ddr3_present` | ✅ (MIG 4.2) |
| `ddr3_data_width` | 16-bit (dq[15:0]) |
| `ddr3_addr_width` | 14-bit (addr[13:0]) |
| `ddr3_bank_width` | 3-bit (ba[2:0]) |
| `ddr3_io_standard` | SSTL135 / DIFF_SSTL135 |
| `ddr3_io_bank` | Bank 34/35 (Vcco=1.35V) |
| `ddr3_dq_setup` | -0.419ns ~ -0.655ns (negative = MIG internal) |
| `ddr3_dq_hold` | +1.322ns ~ +1.399ns |
| `ddr3_module_lut` | 5,312 |
| `ddr3_module_ff` | 6,457 |

⚖️ **판정 로직**

```python
def judge_q19(ddr3_data):
    if not ddr3_data['present']:
        return "N/A", "외부 메모리 인터페이스 없음"
    info = f"DDR3 존재: {ddr3_data['data_width']}-bit, MIG IP, Bank {ddr3_data['bank']}"
    return "REVIEW", f"{info}. 캘리브레이션/초기화 시퀀스 검증은 시뮬레이션/보드 테스트 결과 필요"
```

💬 **예상 답변**
> **REVIEW** — DDR3 인터페이스 확인: **16-bit DQ**, 14-bit Addr, MIG 4.2 IP 사용, Bank 34/35 (SSTL135). PHASER 기반 자동 캘리브레이션 적용 (18 PHASER 블록). ⚠️ 기동/리셋/캘리브레이션 시퀀스 검증 결과(시뮬레이션/보드 테스트)는 별도 제출 필요.

---

## Q20: 내부 메모리 Parity/ECC 및 소프트에러 대응

> *내부 메모리 블록에 Parity/ECC 등 오류 검출 및 소프트에러 대응을 적용했습니까?*

- **답변 유형**: `SEMI` — BRAM 사용 현황 제공 가능, ECC 적용 여부는 설계 문서

📄 **`Utilization.rpt`** + **`Power_Report.rpt`**

🔍 **파싱 위치**

- `Utilization.rpt`: 메모리/BRAM 자원 요약 섹션(`Block RAM Tile` 등의 테이블)을 통해 `RAMB36`, `RAMB18` 총 수량 확인
- `Power_Report.rpt` (혹은 Power Data): On-Chip Power 테이블 내부 `Block RAM`의 전력 사용 및 Utilization % 정보

🧩 **파싱 로직**

```python
# 1) BRAM 사용량
pattern_bram = r'\|\s+Block RAM\s+\|\s+([\d.]+)\s+\|\s+(\d+)\s+\|\s+(\d+)\s+\|\s+([\d.]+)\s+\|'
# 캡처: power_w, used, available, util%

# 2) ECC 키워드 검색 (Utilization hierarchy에서)
# blk_mem_gen 인스턴스 중 "ecc" 포함 여부
pattern_ecc = r'(?i)(ecc|parity|error.correction)'

# 3) BRAM 인스턴스별 분류 (Utilization hierarchy)
# ip_blk_*, ip_fifo_* 등의 BRAM 사용 모듈 목록
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `bram36_used` | 52 |
| `bram18_used` | 110 |
| `bram_total_equiv` | 107 (36Kb equiv.) |
| `bram_util` | 79.26% |
| `ecc_detected` | ❌ (hierarchy에서 ECC 키워드 미발견) |
| `bram_usage_by_module` | DDR3 Arbiter (1), DDR3 FMC RD/WR (8), LCOS Display (8), LCOS PG (~30+), etc. |

⚖️ **판정 로직**

```python
def judge_q20(bram_data):
    if bram_data['ecc_detected']:
        return "PASS", "ECC/Parity 적용 확인"
    elif bram_data['bram_total'] == 0:
        return "N/A", "내부 BRAM 미사용"
    else:
        return "REVIEW", f"BRAM {bram_data['bram_total']}블록 사용, ECC/Parity 미감지 — 미적용 사유 필요"
```

💬 **예상 답변**
> **REVIEW** — 내부 BRAM **107블록** (79.3%) 사용 중, ECC/Parity **미적용**. 주요 용도: DDR3 버퍼, LCOS Pattern Generator, FIFO 등. ⚠️ ECC 미적용 사유를 제시해 주세요 (예: 데이터 특성상 불필요, 또는 재전송 메커니즘 존재).

---

## 요약 — Q11~Q20 파싱 구현 우선순위

| 우선순위 | 질문 | 답변 유형 | 파서 구현 | 리포트 |
|---------|------|----------|----------|--------|
| ⬆️ 높음 | Q11 | AUTO | `resource_parser.py` 등 | Clock_Utilization, Utilization, Control_Sets, IO_Report, PR_PBLOCK_Utilization, QoR |
| ⬆️ 높음 | Q12 | AUTO | `timing_parser.py` 등 | Timing_Summary, Setup_Critical, Hold_Critical, QoR, Datasheet |
| ⬆️ 높음 | Q18 | AUTO | `design_parser.py` | Debug_Core, Partial_Bit_Config_Summary |
| 🔹 중간 | Q13 | SEMI | `power_parser.py` 등 | Power_Data, Power_Report, Power_Opt, Operating_Cond |
| 🔹 중간 | Q14 | SEMI | `power_parser.py` 등 | Power_Data, Power_Report, Switching_Activity |
| 🔹 중간 | Q15 | SEMI | `design_parser.py` 등 | QoR_Assessment, QoR_Suggestions, Pipeline_Analysis, High_Fanout, PR_PBLOCK_Utilization |
| 🔹 중간 | Q19 | SEMI | `io_parser.py` 등 | IO_Report, Datasheet, Utilization |
| 🔹 중간 | Q20 | SEMI | Q11 파서 재사용 + ECC 검색 | Utilization, Power_Report |
| ⬇️ 낮음 | Q16 | EVIDENCE_NEEDED | 없음 | 없음 |
| ⬇️ 낮음 | Q17 | EVIDENCE_NEEDED | 없음 | 없음 |
