# Q51~Q60 상세 파싱 계획서

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

## Q51: 디버그용 레지스터 보호 기능 적용

> *디버그용 레지스터를 설계할 경우 보호 기능을 적용하십시오.*

- **답변 유형**: `AUTO` ✅

📄 **`Debug_Core.rpt`** + **`Methodology.rpt`**

🔍 **파싱 위치**

- `Debug_Core.rpt`: 디버그 관련 코어 존재 유무 파악 (존재 시 보호 기능 확인 대상)

🧩 **파싱 로직**

```python
# 1) 디버그 코어(ILA/VIO) 존재 여부
pattern_no_debug = r'No debug cores were found in this design'
has_no_debug = bool(re.search(pattern_no_debug, debug_core_text))

# 2) Methodology 리포트에서 디버그 관련 Warning 확인
pattern_dbg_method = r'TIMING-9|TIMING-10'  # Unknown CDC / Missing synchronizer
timing9 = re.findall(r'TIMING-9.*?Warning.*?(\d+)', method_text)
timing10 = re.findall(r'TIMING-10.*?Warning.*?(\d+)', method_text)
```

📊 **추출 결과**

| 항목 | 값 |
|-----|---|
| ILA/VIO 디버그 코어 | **없음** ✅ |
| TIMING-9 (Unknown CDC) | **1건** ⚠️ |
| TIMING-10 (Missing prop) | **1건** ⚠️ |

⚖️ **판정 로직**

```python
def judge_q51(data, criteria):
    if data['no_debug']:
        return "PASS", (
            "ILA/VIO 디버그 코어 없음 — 디버그 레지스터 미구현 확인. "
            "Q50에서 확인한 미정의 주소 접근 차단과 연계하여 "
            "운용 중 디버그 모드 진입 경로 없음. "
            "⚠️ TIMING-9(Unknown CDC 1건), TIMING-10(Missing property 1건) — "
            "Methodology 경고는 별도 해소 권고."
        )
    return "REVIEW", "디버그 코어 존재 — 보호 로직(패스워드 등) 구현 여부 별도 확인 필요."
```

💬 **예상 답변**
> **PASS** — ILA/VIO 디버그 코어 미구현. 디버그 레지스터 없음. 운용 중 디버그 모드 진입 경로 없음. ⚠️ TIMING-9/10 Methodology 경고 1건씩 해소 권고.

---

## Q52: 차동·고속(≥1GHz) 클럭 종단 회로 벤더 가이드라인 준수

> *차동 신호 및 1GHz 이상 고속 클럭의 종단 회로가 벤더 가이드라인에 부합합니까?*

- **답변 유형**: `AUTO` / `SEMI` 혼합

📄 **`SSN_Report.rpt`** + **`IO_Report.rpt`**

🔍 **파싱 위치**

- `SSN_Report.rpt`: IO 뱅크별 핀 정보가 표시된 종합 테이블 내의 `Signal Name`, `OFFCHIP_TERM`, `Result` 컬럼
- 차동 신호: `DIFF_SSTL135` (DDR3 DQS, CK) 등 식별, 종단 저항(FP_VTT 등) 적용 여부 확인

🧩 **파싱 로직**

```python
# SSN_Report CSV 파싱
# 컬럼: IO Bank, VCCO, Signal Name, Pin Number, IO Standard, Drive(mA),
#        Slew Rate, OFFCHIP_TERM, Remaining Margin(%), Result, Notes
import csv
ssn_rows = list(csv.DictReader(open('SSN_Report.rpt'), skipinitialspace=True))

# 1) 차동 신호 필터링 (DIFF_SSTL135, LVDS, LVPECL 등)
diff_signals = [r for r in ssn_rows if 'DIFF' in r.get('IO Standard', '')]

# 2) 고속 클럭 식별 (pin_i_clk_78m → 78MHz, pin_i_clk_100m → 100MHz)
# → 1GHz 미만이지만 차동 or FP_VTT 종단 적용 확인
pattern_clk_pin = r'pin[_io]*_[io]*clk|ddr3_ck'
clk_signals = [r for r in ssn_rows if re.search(pattern_clk_pin, r['Signal Name'])]

# 3) SSN FAIL 여부 확인
fail_signals = [r for r in ssn_rows if r.get('Result', '').strip() == 'FAIL']

# 4) OFFCHIP_TERM 설정 확인
# FP_VTT_50 = 종단 저항 설정됨
term_none = [r for r in diff_signals if r.get('OFFCHIP_TERM', '') == 'NONE']
```

📊 **추출 결과**

| 항목 | 값 |
|-----|---|
| 분석 대상 신호 수 | 169개 |
| SSN FAIL | **0건** ✅ |
| SSN PASS | 169건 (100%) |
| 최소 Margin | 12.7% (pin_o_lcos_pow_analog_en) |
| 차동 신호 (DIFF_SSTL135) | DDR3 DQS±[0,1], CK±: `FP_VTT_50` 종단 |
| 고속 CLK 신호 (pin_o_clk_78m) | `OFFCHIP_TERM=FP_VTT_50`, `LVCMOS18`, Margin 14.0% |
| 입력 클럭 핀 (pin_i_clk_*) | IOB 위치 설정 (Clock_Utilization 확인) |

⚖️ **판정 로직**

```python
def judge_q52(ssn_data, diff_data, criteria):
    if not ssn_data['fail_signals']:
        return "PASS", (
            "SSN 전체 PASS (169/169). 차동 신호(DDR3 DQS, CK) DIFF_SSTL135 + "
            "FP_VTT_50 종단 적용. 최소 SSN Margin 12.7%. "
            "입력 클럭 핀(pin_i_clk_*) IOB 배치 확인. "
            "Xilinx 7-series 벤더 SelectIO 가이드라인(UG471) 준수."
        )
    return "REVIEW", f"SSN FAIL 항목: {ssn_data['fail_signals']}"
```

💬 **예상 답변**
> **PASS** — SSN 전체 169핀 PASS. DDR3 DQS/CK 차동 신호 `DIFF_SSTL135 + FP_VTT_50` 종단 적용. 최소 Margin 12.7%. Xilinx UG471 SelectIO 가이드라인 준수.

---

## Q53: 차동 클럭 AC 커플링 검토

> *차동 클럭의 AC 커플링 필요 여부를 확인했습니까? (미적용 시 PLL 오작동 사례 유의)*

- **답변 유형**: `SEMI`

📄 **`SSN_Report.rpt`** + **`Property_Check.rpt`**

🔍 **파싱 위치**

- `SSN_Report.rpt`: 차동 클럭 신호(예: `ddr3_ck_p/_n` 등)의 `IO Standard`가 `DIFF_SSTL135` 인지 식별
- `Property_Check.rpt`: MMCM/PLL 입력 클럭 소스(`pin_i_clk` 등) 품질 데이터(Jitter 등) 파악

🧩 **파싱 로직**

```python
# 1) 입력 클럭 핀별 IO Standard 확인 (AC 커플링 여부는 IBUFDS_GTE / LVDS 식별)
# pin_i_clk_100m → IOB_X0Y76 (Clock_Utilization 줄 773)
# pin_i_clk_20m  → IOB_X0Y174
# pin_i_clk_78m  → IOB_X0Y26

# 2) DDR3 CK는 DIFF_SSTL135 (DC 커플링, 종단 저항으로 보호)
pattern_diff_ck = r'ddr3_ck_[np],[\w\d]+,DIFF_SSTL135'

# 3) AC 커플링 = 입력 LVDS + 외부 커플링 캡 (PCB 레벨)
# Property_Check에서 입력 클럭 Jitter 값 확인
pattern_input_jitter = r'Input Jitter.*?(\d+\.?\d*)\s*ps'
jitter_values = re.findall(pattern_input_jitter, prop_text)

# 4) VCCO 기반 DC 레벨 확인 (DIFF_SSTL135 = 1.35V VCCO → 자동 common-mode)
pattern_vcco = r'34,1\.4,ddr3_ck_[np]'
```

📊 **추출 결과**

| 클럭 신호 | IO Standard | OFFCHIP_TERM | AC커플링 방식 |
|---------|----------|-------------|------------|
| `pin_i_clk_100m` | (IOB) LVCMOS (추정) | - | PCB 설계 확인 필요 |
| `pin_i_clk_78m` | LVCMOS18 → 출력 | FP_VTT_50 | 해당 없음 (출력) |
| `ddr3_ck_p/n` | DIFF_SSTL135 | FP_VTT_50 | DC 커플링 (SSTL: 벤더 권장) |
| `pin_i_fmc_clk` | (IOB_X0Y126) | - | PCB 설계 확인 필요 |

⚖️ **판정 로직**

```python
def judge_q53(data, criteria):
    return "REVIEW", (
        "DDR3 CK 차동 신호: DIFF_SSTL135 DC 커플링 (Xilinx MIG 설계 가이드 준수). "
        "입력 클럭 핀(pin_i_clk_100m, pin_i_fmc_clk): PCB 설계 문서에서 "
        "AC 커플링 캐패시터 적용 여부 확인 필요. "
        "Property_Check에서 입력 Jitter 확인 가능 (PLL 정상 동작 기준)."
    )
```

💬 **예상 답변**
> **REVIEW** — DDR3 CK: DIFF_SSTL135 DC 커플링(MIG 가이드 준수). MMCM 입력 클럭(pin_i_clk_100m, pin_i_fmc_clk): PCB 설계도에서 AC 커플링 캐패시터 적용 여부 확인 필요. (Property_Check에서 Jitter 입력값 정상 범위 확인 완료).

---

## Q54: 시뮬레이션 사양 검토 시 벤더 자료 참고

> *시뮬레이션 사양 검토 시 벤더 자료를 참고했습니까? 참고 문헌을 명시해 주세요.*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 직접 파싱 대상 리포트 없음 — 설계/시뮬레이션 문서 필요

🔍 **참고 가능 리포트**

- `IP_Status.rpt` (05/): 사용 IP 목록 및 벤더 버전 → 벤더 자료 참고 리스트 구성 힌트

🧩 **파싱 로직**

```python
# IP_Status에서 사용 IP Xilinx 버전 추출 → 각 IP의 벤더 PG 문서 참고 근거
pattern_ip_name = r'(ip_[a-z_]+)\s*\|\s*([\d.]+)'
ip_list = re.findall(pattern_ip_name, ip_status_text)
# → 예: ip_mig_ddr3 → Xilinx PG150 UltraScale+ Memory IP Guide
#         ip_fifo_indep → Xilinx PG057 FIFO Generator
#         ip_clk_wiz   → Xilinx PG065 Clocking Wizard

# 이를 기반으로 벤더 자료 참고 목록 자동 생성
```

📊 **예상 벤더 자료 목록**

| IP / 기능 | 벤더 참고 자료 |
|----------|------------|
| `ip_mig_ddr3` | Xilinx PG150 / UG586 MIG 7-Series |
| `ip_fifo_indep_48x16` | Xilinx PG057 FIFO Generator |
| `ip_clk_wiz_*` | Xilinx PG065 Clocking Wizard |
| `ip_blk_mem_gen` | Xilinx PG058 Block Memory Generator |
| SelectIO 종단 | Xilinx UG471 7-Series SelectIO |
| CDC설계 | Xilinx WP272 Clock Domain Crossing |

⚖️ **판정**: `EVIDENCE_NEEDED` — IP_Status에서 자동 목록 생성 가능하나, 실제 참고 여부는 설계 문서 확인 필요.

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 사용 IP 기반 벤더 자료 목록 자동 생성 가능(MIG PG150, FIFO PG057, Clocking Wizard PG065, BRAM PG058, SelectIO UG471). 실제 설계 시 참고 여부는 시뮬레이션 사양서/설계 문서에서 확인 필요.

---

## Q55: 시뮬레이션 커버리지 계획 수립

> *기능 요구사양을 기반으로 시뮬레이션 커버리지(범위)를 정의했습니까?*

- **답변 유형**: `SEMI` / `EVIDENCE_NEEDED`

📄 **`Coverage_Report.html / .txt`** + **`Design_Analysis.rpt`** + **`DRC_Report.rpt`** + **`Methodology.rpt`**

🔍 **파싱 위치**

- `Design_Analysis.rpt`: `Complexity Characteristics` 등 모듈별 복잡도 테이블 (Rent 지수, 인스턴스 수 추출)
- `DRC_Report.rpt`: `Design Rule Check` (DRC) 위반 요약 구간 (검증 필요 항목 식별)
- `Methodology.rpt`: `Methodology Summary` 요약 구간
- (커버리지 리포트가 제공될 경우) 시뮬레이션 환경 및 검증 조건/커버리지 지표 파싱
- 미제공 시 외부 문서로 EVIDENCE_NEEDED 처리

🧩 **파싱 로직**

```python
# 1) 설계 복잡도 기반 커버리지 필요 규모 추정
pattern_complexity = r'\|\s*(top|u_\w+)\s*\|\s*\S+\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*(\d+)'
# → Rent 지수(복잡도), Total Instances 수

# 2) DRC Warning 목록 → 시뮬레이션 대상 항목 자동 분류
drc_warnings = {
    'DPIP-1': 128,  # DSP48 입력 비파이프라인 → DSP 경로 시뮬 필요
    'DPOP-1': 64,   # DSP48 출력 비파이프라인
    'DPOP-2': 66,   # DSP48 MREG 비파이프라인
    'REQP-1839': 3, # RAMB async control → 비동기 RAM reset 시뮬 필요
    'REQP-1709': 1, # Clock output buffering
}

# 3) Methodology Warning → 추가 커버리지 항목
method_warnings = {
    'LUTAR-1': 6,   # LUT→비동기리셋 → 리셋 경로 시뮬 필요
    'PDRC-190': 14, # 최적화 안 된 동기화 체인 → CDC 시뮬
    'TIMING-9': 1,  # Unknown CDC → CDC 시뮬
    'TIMING-10': 1, # Missing synchronizer → 동기화 시뮬
    'TIMING-47': 2, # False path 비동기 클럭 → CDC 경계 시뮬
}
```

📊 **설계 복잡도 요약**

| 모듈 | Rent 지수 | 인스턴스 수 | 복잡도 등급 |
|-----|---------|---------|---------|
| `top_with_ddr3` | 0.28 | 83,310 | **Very Low** ✅ |
| `u_ddr3_top` | 0.43 | 12,835 | **Low** |
| `u_lcos_top` | 0.47 | 27,488 | **Low** |
| `u_sys_top_with_ddr3` | N/A | 42,437 | - |

**주요 시뮬레이션 대상 항목 (DRC/Methodology 기반):**

| 카테고리 | 항목 | 건수 | 시뮬 필요 이유 |
|---------|------|-----|------------|
| DSP 비파이프라인 | DPIP/DPOP | 258건 | 지연 타이밍 영향 확인 |
| 비동기 RAMB제어 | REQP-1839 | 3건 | reset 시 데이터 무결성 |
| LUT→비동기리셋 | LUTAR-1 | 6건 | 글리치 리셋 가능성 |
| CDC 동기화 | TIMING-9/10 | 2건 | 메타스태빌리티 |

⚖️ **판정 로직**

```python
def judge_q55(data, criteria):
    return "REVIEW", (
        f"설계 복잡도: Rent=0.28 (Very Low), 총 {data['total_inst']:,}개 인스턴스. "
        f"DRC/Methodology 기반 필요 시뮬 항목 식별 가능: "
        f"DSP 비파이프라인 {data['dsp_warn']}건, "
        f"비동기 제어 {data['async_warn']}건, "
        f"CDC {data['cdc_warn']}건. "
        "⚠️ 공식 시뮬레이션 커버리지 계획 문서 제출 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — DRC/Methodology 위반 목록 기반 필요 시뮬 대상 자동 추출: DSP 비파이프라인(258건), RAMB 비동기 제어(3건), LUTAR(6건), CDC(2건). ⚠️ 공식 시뮬레이션 커버리지 계획서 제출 필요.

---

## Q56: 시뮬레이션 사양 — 요구사양 기반 검증

> *시뮬레이션 사양서가 요구 사양을 기반으로 작성되었습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **`Coverage_Report.html / .txt`**

🔍 **참고 사항**

- 해당 문서/리포트에서 요구사항 명세 대비 검증 항목 표기 여부 확인.
- 파싱으로는 상세 검증이 어려우므로 증빙 문서 제출 검토.

```python
# 간접 확인: DRC_Report, Methodology의 Warning을 요구사양 매핑
# 예: REQP-1709(Clock buffer) → 요구사항 clk_78m 출력 지원 여부
# 예: LUTAR-1(비동기리셋) → 요구사항의 "리셋 후 정상 동작 보장"
# → 자동 연결은 불가 (요구사양 문서 없음)

def build_req_mapping(drc_data, methodology_data):
    return {
        'CLOCK_OUTPUT': drc_data.get('REQP-1709', 0),
        'ASYNC_RESET': methodology_data.get('LUTAR-1', 0),
        'CDC_PROTECTION': methodology_data.get('TIMING-9', 0) + methodology_data.get('TIMING-10', 0),
    }
```

📊 **관련 데이터**

| 항목 | 값 | 관련 리포트 |
|-----|---|-----------|
| DRC Violation 요약 | 335건 (Warning + Advisory) | DRC_Report |
| Methodology Violation | 378건 | Methodology |
| 요구사양 매핑 문서 | EVIDENCE_NEEDED | 외부 문서 |

⚖️ **판정**: `EVIDENCE_NEEDED` — 리포트 기반 위반 목록 자동 추출 가능하나, 요구사양 문서와의 실제 매핑은 외부 확인 필요.

💬 **예상 답변**
> **EVIDENCE_NEEDED** — DRC(335건)/Methodology(378건) 위반 목록은 자동 추출 완료. 시뮬레이션 사양이 요구사양을 기반으로 작성되었음을 증명하는 사양서/검증 계획서 제출 필요.

---

## Q57: 설계 변경 시 영향 범위 재검증

> *설계 변경(ECO 등) 시 영향 범위를 분석하고 재검증을 수행했습니까?*

- **답변 유형**: `SEMI` — Design Analysis 분석 필요

📄 **`Design_Analysis.rpt`** + **`Methodology.rpt`**

🔍 **파싱 위치**

- `Design_Analysis.rpt`: `Congestion` 분석 관련 섹션에서 Level 5 이상 혼잡도 발생 여부 검출 (`No congestion windows` 등)
- `Methodology.rpt`: `SYNTH-10 Wide multiplier` 등 병목 의심 사례 수량 검출 (설계 변경 후 재배치 영향 확인)

🧩 **파싱 로직**

```python
# 1) Congestion 없음 확인 → 설계 변경 여유도 확인
pattern_no_congestion = r'No congestion windows are found above level 5'
no_congestion = bool(re.search(pattern_no_congestion, design_analysis_text))

# 2) 설계 변경 이력은 리포트에서 직접 확인 불가
# → Date 필드로 빌드 날짜/리비전 추출
pattern_date = r'Date\s+:\s+(\S+\s+\S+\s+\d+\s+[\d:]+\s+\d+)'
build_date = re.search(pattern_date, text).group(1)

# 3) Methodology TIMING-24 (Overridden Max delay) 16건 → 변경 후 예외 재검토 필요
timing24 = methodology_data.get('TIMING-24', 0)
```

📊 **추출 결과**

| 항목 | 값 |
|-----|---|
| Placer Congestion >Level5 | **없음** ✅ |
| Router Congestion >Level5 | **없음** ✅ |
| 빌드 날짜 | 2026-02-26 |
| TIMING-24 (Max delay override) | **16건** ⚠️ |
| SYNTH-10 (Wide multiplier) | 64건 (Power_Loader) |
| 설계 변경 이력 문서 | EVIDENCE_NEEDED |

⚖️ **판정 로직**

```python
def judge_q57(data, criteria):
    return "REVIEW", (
        f"빌드: {data['build_date']}, Congestion 없음 — 설계 여유도 충분. "
        f"TIMING-24(Max delay override) {data['timing24']}건: "
        "변경 시 영향 범위 재검토 필요 항목. "
        "⚠️ 설계 변경 이력(ECO, Git Log 등) 및 재검증 결과 문서 제출 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — 빌드 2026-02-26, Congestion 없음(설계 여유도 양호). TIMING-24 16건(타이밍 예외 오버라이드): 설계 변경 시 재검토 필요. ⚠️ 공식 ECO/변경 이력 및 재검증 보고서 제출 필요.

---

## Q58: 검증 커버리지 100% 달성 확인

> *시뮬레이션 커버리지가 요구 사양 기반으로 100% 달성됨을 확인했습니까?*

- **답변 유형**: `SEMI` / `EVIDENCE_NEEDED`

📄 **`Coverage_Report.html / .txt`** + **`DRC_Report.rpt`** + **`Methodology.rpt`** + **`Waiver.rpt`**

🔍 **파싱 위치**

- 검증 커버리지 수치 (Coverage %)
- 확인 불가 시 방법에 대한 설명(EVIDENCE) 요구

- `DRC_Report.rpt`: 메시지/요약 구간 내 전체 `Violations found` 수치 파악
- `Methodology.rpt`: 메시지/요약 구간 내 전체 `Violations found` 수치 파악
- `Waiver.rpt`: 파일 내 면제/Waived 처리된 전체 건수 파악

🧩 **파싱 로직**

```python
# 1) DRC 위반 요약 (심각도별 분류)
pattern_drc_summary = r'\|\s*([\w-]+)\s*\|\s*(Warning|Advisory)\s*\|\s*[\w\s]+\|\s*(\d+)\s*\|'
drc_items = re.findall(pattern_drc_summary, drc_text)
drc_warnings = [(r, s, int(c)) for r, s, c in drc_items if s == 'Warning']

# 2) Methodology Warning 요약
method_items = re.findall(pattern_drc_summary, method_text)
method_warnings = [(r, s, int(c)) for r, s, c in method_items if s == 'Warning']

# 3) CDC Waiver 건수
pattern_cdc_waiver = r'CDC\s*\|.*?waived.*?(\d+)'
cdc_waived = int(re.search(pattern_cdc_waiver, waiver_text).group(1))

# 4) 커버리지% 계산 불가 (외부 TB 커버리지 데이터 필요)
```

📊 **검증 상태 요약**

| 리포트 | 총 위반 | Warning | Advisory |
|-------|--------|---------|---------|
| DRC | 335 | 266 (DPIP/DPOP) | 72 |
| Methodology | 378 | 378 | 16 |
| CDC Waiver | 69건 면제 | - | - |

**미해소 주요 경고:**

| 규칙 | 건수 | 우선순위 |
|-----|-----|---------|
| LUTAR-1 (LUT→비동기리셋) | 6 | 높음 |
| TIMING-9 (Unknown CDC) | 1 | 높음 |
| TIMING-10 (Missing property) | 1 | 높음 |
| REQP-1839 (RAMB async) | 3 | 중간 |
| DPIP/DPOP (DSP 비파이프라인) | 258 | 낮음 |

⚖️ **판정 로직**

```python
def judge_q58(data, criteria):
    unresolved_high = (data['lutar1'] + data['timing9'] +
                       data['timing10'] + data['reqp1839'])
    return "REVIEW", (
        "DRC 335건 / Methodology 378건 위반 확인. "
        "고우선 미해소 항목: "
        f"LUTAR-1({data['lutar1']}건), "
        f"TIMING-9({data['timing9']}건), "
        f"TIMING-10({data['timing10']}건), "
        f"REQP-1839({data['reqp1839']}건). "
        "⚠️ 시뮬레이션 커버리지 보고서(Coverage Report) 별도 제출 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — DRC 335건 / Methodology 378건 위반 확인. 고우선 미해소: LUTAR-1(6건), TIMING-9/10(각 1건), REQP-1839(3건). DSP 비파이프라인 258건은 성능 최적화 권고. ⚠️ 공식 커버리지 보고서 제출 필요.

---

## Q59: 시뮬레이션 불가 항목 식별

> *시뮬레이션으로 검증할 수 없는 항목을 식별하고 목록화했습니까?*

- **답변 유형**: `AUTO` ⚙️

📄 **`CDC_Report.rpt`** + **`CDC_Critical.rpt`** + **`CDC_Unsafe.rpt`** + **`CDC_Interaction.rpt`** + **`Timing_Exceptions.rpt`** + **`Coverage_Report.html / .txt`** + **`Methodology.rpt`** + **`Waiver.rpt`** + **`SSN_Report.rpt`**

🧩 **파싱 로직**

```python
# 시뮬레이션 불가 항목 자동 분류 기준:
# 1) 비동기 CDC 경로 (set_clock_groups) → STA에서 제외, 시뮬 검증 어려움
# 2) 메타스태빌리티 (TIMING-9/10) → 확률적 특성, 시뮬 재현 어려움
# 3) SSN (동시 스위칭 노이즈) → HW 측정 필요
# 4) LUT 비동기 리셋 (LUTAR-1) → 타이밍 의존, 시뮬 어려움
# 5) CDC Waiver (69건) → 면제된 CDC = 위험 허용, 시뮬 커버리지 밖

pattern_cdc_async = r'set_clock_groups'
num_async_pairs = len(re.findall(pattern_cdc_async, exceptions_text))

simulation_impossible = [
    {'category': '비동기 CDC 경로', 'count': num_async_pairs, 'source': 'Timing_Exceptions'},
    {'category': '메타스태빌리티 (TIMING-9)', 'count': 1, 'source': 'Methodology'},
    {'category': '동기화 속성 미설정 (TIMING-10)', 'count': 1, 'source': 'Methodology'},
    {'category': 'LUT→비동기리셋 (LUTAR-1)', 'count': 6, 'source': 'Methodology'},
    {'category': 'CDC Waived 항목', 'count': 69, 'source': 'Waiver'},
    {'category': 'SSN (동시 스위칭 노이즈)', 'count': 169, 'source': 'SSN_Report'},
]
```

📊 **시뮬레이션 불가 항목 목록**

| 카테고리 | 건수 | 출처 리포트 | 대체 검증 |
|---------|-----|-----------|---------|
| 비동기 CDC 쌍 (set_clock_groups) | 49쌍 | Timing_Exceptions | CDC 검사 도구 |
| 메타스태빌리티 (TIMING-9) | 1건 | Methodology | MTBF 계산 |
| 동기화 속성 미설정 (TIMING-10) | 1건 | Methodology | RTL 수정 |
| LUT→비동기리셋 (LUTAR-1) | 6건 | Methodology | 정적 분석 |
| CDC Waived 항목 | 69건 | Waiver | 설계 근거 문서 |
| SSN (동시 스위칭) | 169핀 | SSN_Report | SSN 자동 검사 |

💬 **예상 답변**
> **AUTO** — 시뮬레이션 불가 항목 자동 추출: 비동기 CDC 쌍(49쌍), 메타스태빌리티(TIMING-9 1건), LUT비동기리셋(LUTAR-1 6건), CDC Waived(69건), SSN(169핀). 각 항목별 대체 검증 방법(CDC 도구, MTBF 계산, SSN 시뮬레이터) 필요.

---

## Q60: 시뮬레이션 불가 항목 대체 검증 방법 확인

> *시뮬레이션으로 검증할 수 없는 항목에 대해 대체 검증 방법을 정의하고 수행했습니까?*

- **답변 유형**: `SEMI` / `EVIDENCE_NEEDED`

📄 **`Coverage_Report.html / .txt`** + **`CDC_Report.rpt`** + **`Waiver.rpt`** + **`SSN_Report.rpt`**

🧩 **파싱 로직**

```python
# Q59의 시뮬 불가 항목별 대체 검증 결과를 리포트에서 확인
# 1) CDC → CDC_Report.rpt 존재 = CDC 도구 검증 수행됨
cdc_report_verified = os.path.exists('CDC_Report.rpt')

# 2) SSN → SSN_Report.rpt 전체 PASS = SSN 자동 검사 수행됨
ssn_all_pass = all(r['Result'] == 'PASS' for r in ssn_rows)

# 3) CDC Waiver → 69건 면제 근거 존재 여부 (Waiver 리포트)
cdc_waiver_count = 69  # Waiver.rpt 확인됨

# 4) LUTAR-1 / TIMING-9/10 → 현재 해소 안 됨 (미수행)
unresolved_method_warnings = ['LUTAR-1', 'TIMING-9', 'TIMING-10']
```

📊 **대체 검증 수행 현황**

| 항목 | 대체 검증 방법 | 수행 여부 |
|-----|------------|--------|
| 비동기 CDC | Vivado CDC 분석 도구 | ✅ 수행 (CDC_Report 존재) |
| SSN | SSN 자동 분석 | ✅ 수행 (전체 PASS) |
| CDC Waived 69건 | Waiver 등록 | ✅ 등록됨 |
| 메타스태빌리티 (TIMING-9) | MTBF 계산 / RTL 수정 | ⚠️ 미수행 |
| LUT→비동기리셋 (LUTAR-1) | RTL 동기 리셋 변경 | ⚠️ 6건 미해소 |
| TIMING-10 | ASYNC_REG property 추가 | ⚠️ 미수행 |

⚖️ **판정 로직**

```python
def judge_q60(data, criteria):
    performed = data['cdc_verified'] + data['ssn_pass'] + data['cdc_waived']
    unresolved = data['lutar1'] + data['timing9'] + data['timing10']
    return "REVIEW", (
        "대체 검증 수행 항목: "
        "CDC 도구 분석(✅), SSN 자동 분석(✅ PASS), CDC Waiver(✅ 69건). "
        f"미수행/미해소: "
        f"LUTAR-1 {data['lutar1']}건(LUT비동기리셋), "
        f"TIMING-9/10 각 1건(메타스태빌리티/동기화속성). "
        "⚠️ 미해소 항목 RTL 수정 또는 MTBF 계산 결과 제출 필요."
    )
```

💬 **예상 답변**
> **REVIEW** — 대체 검증 수행: CDC 도구(✅), SSN 자동 분석(✅ 전체 PASS), CDC Waiver 69건 등록(✅). ⚠️ 미해소: LUTAR-1(LUT비동기리셋 6건), TIMING-9/10(메타스태빌리티/동기화속성 각 1건) → RTL 수정 또는 대체 검증 결과 제출 필요.

---

## 요약 — Q51~Q60 파싱 구현 우선순위

| 우선순위 | 문항 | 답변 유형 | 파서 모듈 | 다중/단일 리포트 목록 |
|---------|------|----------|----------|------------|
| ⬆️ 높음 | Q51 | AUTO | `debug_parser.py` 등 | Debug_Core, Methodology |
| ⬆️ 높음 | Q52 | AUTO | `io_parser.py` 등 | SSN_Report, IO_Report |
| ⬆️ 높음 | Q59 | AUTO | `cdc_parser.py` 등 | CDC_Report 외 4종, Methodology, Waiver, SSN_Report |
| 🔹 중간 | Q53 | SEMI | `io_parser.py` 등 | SSN_Report, Property_Check |
| 🔹 중간 | Q54 | EVIDENCE | 없음 (IP_Status 참고) | IP_Status |
| 🔹 중간 | Q55 | SEMI | `coverage_parser.py` 등 | Coverage_Report.html / .txt, Design_Analysis, DRC_Report, Methodology |
| 🔹 중간 | Q56 | EVIDENCE | 없음 (공통 참조) | Coverage_Report.html / .txt, DRC_Report, Methodology |
| 🔹 중간 | Q57 | SEMI | `analysis_parser.py` | Design_Analysis, Methodology |
| 🔹 중간 | Q58 | SEMI | `coverage_parser.py`| Coverage_Report.html / .txt, DRC_Report, Methodology, Waiver |
| 🔹 중간 | Q60 | SEMI | `coverage_parser.py`| Coverage_Report.html / .txt, CDC_Report, Waiver, SSN_Report |

## 주요 발견 사항

> **Q51 PASS**: 디버그 코어(ILA/VIO) 없음 → 디버그 레지스터 미구현
>
> **Q52 PASS**: SSN 169핀 전체 PASS, DDR3 CK `DIFF_SSTL135 + FP_VTT_50` 종단 적용
>
> **Q59 AUTO**: 시뮬 불가 항목 자동 추출 — CDC 49쌍, LUTAR-1 6건, TIMING-9/10 2건, CDC Waived 69건, SSN 169핀
>
> **주요 미해소 항목 (Q58/Q60 REVIEW):**
>
> - `LUTAR-1` 6건: LUT가 비동기 리셋 핀 구동 (u_lcos_driver, u_ddr3_infrastructure)
> - `TIMING-9` 1건: Unknown CDC 로직
> - `TIMING-10` 1건: 동기화 속성 미설정 (ASYNC_REG 추가 필요)
> - `REQP-1839` 3건: RAMB36 비동기 제어 신호
