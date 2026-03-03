# Q1~Q10 상세 파싱 계획서

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

## Q1: FPGA 개발 프로세스/일정 개요

> *선정한 FPGA 개발 프로세스 및 일정(스케줄) 개요를 제시해 주세요.*

- **답변 유형**: `SEMI` — 리포트에서 프로젝트 규모 근거(소스 파일 수, IP 수, 빌드 일시) 추출 가능하나, 실제 일정 문서는 외부 증빙 필요

📄 **`Compile_Order.rpt`** + **`Environment.rpt`** + **`IP_Status.rpt`**

🔍 **Compile_Order.rpt 파싱 위치** (프로세스 규모 식별)

- `Source compile order for 'synthesis'` 섹션 하위 테이블 (전체 소스 수 및 유형)
- `Source compile order for 'simulation'` 섹션 하위 테이블 (시뮬레이션 소스 수)

🔍 **Environment.rpt 파싱 위치** (빌드 일시 확인)

- 공통 헤더의 `Date` 필드 (예: `Date : Thu Feb 26 11:47:33 2026`)

🔍 **IP_Status.rpt 파싱 위치** (IP 사용 규모 파악)

- `1. Project IP Status` 섹션의 요약 문장 (`Your project uses XX IP.`)

🧩 **파싱 로직**

```python
# 1) Synthesis 소스 파일 수, 파일 유형별 분류
pattern_src_line = r'^\s*(\d+)\s+(\S+)\s+(Synth.*?|Sim)\s+(\w+)\s+'
# 추출: index, filename, used_in, file_type
# 파일 유형 카운트: DCP, Verilog, VHDL, VHeader, COE, PRJ

# 2) 모듈 구조 분석 (경로에서 모듈 그룹 추출)
# /new/ddr3/ → DDR3 모듈, /new/lcos/ → LCOS 모듈, /new/sys/ → System 모듈 등
pattern_module = r'/new/(\w+)/'

# 3) IP 개수 (ip_ 시작 파일 중 DCP 유형)
pattern_ip_dcp = r'^\s*\d+\s+(ip_\w+\.dcp)\s+'
```

📊 **추출 결과**

| 필드 | 값 (실제) |
|------|----------|
| `synth_source_count` | 160 (`Synthesis` 테이블 내역 수) |
| `sim_source_count` | 284건 (`Simulation` 섹션 테이블 내역 수) |
| `file_types` | `{DCP: 52, Verilog: 87, VHDL: 11, VHeader: 6, COE: 2, PRJ: 2}` |
| `module_groups` | `{ddr3: 10, lcos/lcos_driver: 5, lcos/lcos_pg: ~40, lcos/lcos_test_img: 8, phy: 3, sys: 12, util: 5, fmc: 1}` |
| `constraint_files` | 3 (XDC files: Constraints_with_ddr3, IO_Constraints, IO_Standard) |
| `build_date` | `Thu Feb 26 11:44:36 2026` (from Environment.rpt `Date`) |
| `ip_count` | 52 (from IP_Status.rpt 요약) |
| `testbench_count` | 5 (sim_1 섹션 `tb_*.v`) |

⚖️ **판정**: `INFO` — 프로세스 일정은 외부 문서이므로, 리포트에서 추출 가능한 프로젝트 규모 정보만 제공

💬 **예상 답변**
> **INFO** — 프로젝트 규모: Verilog 소스 87개, IP(DCP) 52개, 제약조건 3개. 주요 모듈: DDR3(10), LCOS PG(~40), PHY(3), System(12). 빌드 시점: 2026-02-26. ⚠️ 개발 일정 문서는 별도 제출 필요.

---

## Q2: 개발팀 내부 리뷰 계획

> *개발 프로세스와 연계하여 개발팀 내부에서 수행할 리뷰 계획을 제시해 주세요.*

- **답변 유형**: `EVIDENCE_NEEDED` — 리포트에 리뷰 계획 정보 없음

📄 **참조 리포트 없음**

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 리뷰 계획은 리포트에서 추출할 수 없습니다. 별도 리뷰 계획서/프로세스 문서를 제출해 주세요.

---

## Q3: 리뷰 결과 관계자 공유 여부

> *리뷰 결과는 모든 관계자에게 공유되고 있습니까?*

- **답변 유형**: `EVIDENCE_NEEDED` — 리포트에 리뷰 공유 정보 없음

📄 **참조 리포트 없음**

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 리뷰 결과 공유 내역은 리포트에 포함되지 않습니다. 리뷰 회의록 또는 공유 이력을 제출해 주세요.

---

## Q4: FPGA 기인 결함 시 조사 결과 제출

> *FPGA 기인 결함 발생 시, 조사 결과 및 전체 리뷰 결과 제출을 요청받을 수 있습니다.*

- **답변 유형**: `EVIDENCE_NEEDED` — 고지 사항이므로 정보 문항

📄 **참조 리포트 없음**

⚖️ **판정**: `N/A` (고지 / acknowledgement 문항)

💬 **예상 답변**
> **N/A** — 이 항목은 고지 사항입니다. FPGA 기인 결함 발생 시 조사 결과 및 리뷰 이력 제출이 필요함을 인지합니다.

---

## Q5: FPGA/PLD 벤더 및 모델명

> *선정한 FPGA/PLD의 벤더와 모델명을 명시해 주세요.*

- **답변 유형**: `AUTO` ✅

📄 **`Environment.rpt`**

🔍 **Environment.rpt 파싱 위치**

- 공통 헤더의 `Tool Version` 필드: 사용 툴을 통해 벤더 확인 (예: Vivado = Xilinx)
- 공통 헤더의 `Device` 필드: 전체 디바이스 모델명 (Full Part Name) 추출
- (참조) `Environment.rpt` 외 모든 `.rpt` 공통 헤더에 Device 정보가 포함됨

🧩 **파싱 로직**

```python
# Environment.rpt 공통 헤더에서 추출
pattern_tool = r'Tool Version\s*:\s*Vivado'
# → 매칭 시 벤더 = "Xilinx"

pattern_device = r'Device\s*:\s*([\w-]+)'
# 캡처: xc7a100tfgg676-2
# 파트명(xc7a100t), 패키지(fgg676), 스피드그레이드(-2) 분리 추출 로직 적용
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `vendor` | Xilinx |
| `device_part` | xc7a100tfgg676-2 |
| `device_family` | Artix-7 |
| `package` | fgg676 |
| `speed_grade` | -2 |

⚖️ **판정**: `INFO` — 사실 정보 제공

💬 **예상 답변**
> **INFO** — Vendor: **Xilinx**, Part: **xc7a100tfgg676-2** (Artix-7, Package: FGG676, Speed Grade: -2)

---

## Q6: FPGA/PLD 선정 근거 리뷰

> *FPGA/PLD 선정 근거에 대한 리뷰를 수행했습니까?*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **참조 리포트 없음** (선정 근거는 설계 문서에 존재)

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 디바이스 선정 근거 리뷰 이력은 리포트에 포함되지 않습니다. 선정 검토 보고서를 제출해 주세요.

---

## Q7: 디바이스 선정 참고 문서

> *디바이스 선정 시 참고한 문서 및 자료 정보를 알려주세요.*

- **답변 유형**: `EVIDENCE_NEEDED`

📄 **참조 리포트 없음**

⚖️ **판정**: `EVIDENCE_NEEDED`

💬 **예상 답변**
> **EVIDENCE_NEEDED** — 디바이스 선정 참고 문서는 리포트에 포함되지 않습니다. 데이터시트, 선정 비교표 등을 제출해 주세요.

---

## Q8: 사용 툴 버전

> *사용 툴 버전을 알려주세요. 최신 버전입니까? 안정성이 검증된 버전입니까?*

- **답변 유형**: `AUTO` ✅

📄 **`Environment.rpt`** + **`Config_Impl.rpt`**

🔍 **Environment.rpt 파싱 위치** (기본 툴 버전 및 환경 확인)

- 공통 헤더의 `Tool Version` 필드: Vivado 버전, 빌드 번호, 빌드 일자
- 공통 헤더의 `Host` 필드: OS 및 플랫폼 정보
- `Environment Variables` 섹션 하위의 `XILINX_VIVADO` 설정 경로를 통해 버전 교차 검증

🔍 **Config_Impl.rpt 파싱 위치** (구현 설정 및 안정성 확인)

- `Strategy`, `Place Directive`, `Route Directive` 필드 파싱
- 하위 `Vivado Version` 필드를 통한 실제 구현 툴 버전 교차 검증

🧩 **파싱 로직**

```python
# 1) 툴 버전 추출
pattern_version = r'Vivado\s+(v\.\d+\.\d+)\s*\((\w+)\)\s*Build\s+(\d+)\s+(.*?\d{4})'
# 캡처: version, platform, build_number, build_date

# 2) OS 정보
pattern_os = r'Host\s*:\s*\S+\s+running\s+(.*)'
# → "64-bit Ubuntu 24.04.3 LTS"

# 3) Config Strategy
# Config_Impl.rpt에서:
pattern_strategy = r'Strategy\s*:\s*(.*)'
pattern_place = r'Place Directive\s*:\s*(.*)'
pattern_route = r'Route Directive\s*:\s*(.*)'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `tool_name` | Vivado |
| `tool_version` | v.2019.2 |
| `platform` | lin64 |
| `build_number` | 2708876 |
| `build_date` | Wed Nov 6 21:39:14 MST 2019 |
| `host_os` | 64-bit Ubuntu 24.04.3 LTS |
| `strategy` | Vivado Implementation Defaults |
| `place_directive` | Default |
| `route_directive` | Default |
| `is_latest` | ❌ (2019.2 — 최신은 2024.x 이상) |

⚖️ **판정 로직**

```python
def judge_q8(version_str, criteria):
    # criteria.json에서 로드된 안정 버전 목록 사용
    # 예: known_stable = criteria['tool']['known_stable_versions']
    known_stable = criteria['tool']['known_stable_versions']
    major, minor = parse_version(version_str)  # (2019, 2)
    if major >= 2023:
        return "PASS", "최신 버전 사용"
    elif version_str in known_stable:
        return "REVIEW", "구버전이나 안정성 검증된 버전. 최신 Errata 확인 권장"
    else:
        return "FAIL", "권장하지 않는 구버전"
```

💬 **예상 답변**
> **REVIEW** — Tool: **Vivado v.2019.2** (lin64, Build 2708876). 최신 버전은 아니나 (2019 릴리스), 널리 사용된 안정 버전입니다. 최신 Errata 확인을 권장합니다. Strategy: Implementation Defaults, Directive: Default.

---

## Q9: 디바이스/툴 결함 정보 (Errata) 확인

> *사용 디바이스 및 툴 각각의 결함 정보(Errata, Issue 등)를 확인했습니까?*

- **답변 유형**: `SEMI` — IP 상태에서 부분적 확인 가능

📄 **`IP_Status.rpt`** + **`Environment.rpt`**

🔍 **IP_Status.rpt 파싱 위치** (IP 결함 및 업데이트 검토)

- `1. Project IP Status` 섹션의 IP 개체 수 요약 (`Your project uses XX IP.`)
- `Project IP Instances` 테이블 전체 행 파싱: 각 인스턴스별 `Status` 및 `Recommendation` 열 검사

🔍 **Environment.rpt 파싱 위치** (라이선스 결함 여부)

- `6. License Information` 하위 라이선스 목록 테이블: 각 IP/기능의 라이선스 상태(`Okay` 등) 확인

🧩 **파싱 로직**

```python
# 1) IP 전체 개수
pattern_ip_count = r'Your project uses (\d+) IP'

# 2) IP 상태 테이블 파싱
# 멀티라인 테이블: | Instance Name | Status | Recommendation | ...
# Status 값: "Up-to-date" / "Major Update Available" / "Deprecated" 등
pattern_ip_row = r'\|\s*(\S+)\s*\|\s*([\w-]+)\s*\|\s*(.*?)\s*\|'
# 캡처: instance_name, status, recommendation

# 3) 상태별 카운트
# up_to_date_count, update_available_count, deprecated_count

# 4) 라이선스 유효성 확인 (Environment.rpt `6. License Information` 테이블)
pattern_license = r'\|\s*(\S+)\s*\|.*?\|\s*(Okay|Expired|Invalid)\s*\|'
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `total_ip_count` | 52 |
| `status_up_to_date` | 52 (100%) |
| `status_update_available` | 0 |
| `status_deprecated` | 0 |
| `ip_types` | Block Memory Gen 8.4: 33개, Clocking Wizard 6.0: 5개, FIFO Gen 13.2: 2개, Adder/Sub 12.0: 7개, Divider 5.1: 2개, Multiplier 12.0: 1개, MIG 4.2: 1개, XADC 3.3: 1개 |
| `target_device` | xc7a100tfgg676-2 (모든 IP 동일) |
| `license_status` | 모든 라이선스 "Okay" |

⚖️ **판정 로직**

```python
def judge_q9(ip_data, criteria):
    if ip_data['status_deprecated'] > 0:
        return "FAIL", f"Deprecated IP {ip_data['status_deprecated']}개 발견"
    elif ip_data['status_update_available'] > 0:
        return "REVIEW", f"업데이트 가능 IP {ip_data['status_update_available']}개 — 변경 로그 확인 필요"
    else:
        return "PASS", "모든 IP Up-to-date, 라이선스 유효"
```

💬 **예상 답변**
> **PASS** — 전체 52개 IP 모두 **Up-to-date** 상태, 변경 불필요. 모든 라이선스 유효(Okay). ⚠️ 단, 디바이스 자체 Errata(Xilinx AR# 문서)는 리포트에서 확인 불가 — 별도 확인 필요.

---

## Q10: 툴 버전 변경 시 IP 재생성 영향

> *구현 툴 버전을 변경할 경우, IP 재생성에 따른 포트 변경, 기능 확장/축소, Errata 영향을 확인했습니까?*

- **답변 유형**: `SEMI` — 현재 IP 상태 제공 가능, 버전 변경 영향은 추론

📄 **`IP_Status.rpt`**

🔍 **IP_Status.rpt 파싱 위치**

- `Project IP Instances` 테이블 내 `IP Version` 열과 `New Version` 열 비교
- 동일 리포트 파일 하단의 `Change Log` 참조 파일 경로 목록 (업데이트에 따른 포트/기능 변경 영향성 추론용)

🧩 **파싱 로직**

```python
# 1) IP 버전 비교 (현재 vs New)
# 이미 Q9에서 파싱한 데이터 재사용
# 실제 리포트에서: IP Version = "8.4 (Rev. 4)", New Version = "8.4 (Rev. 4)"
# → 동일하면 "변경 없음"

# 2) Change Log 경로 목록 파싱
pattern_changelog = r'\*\((\d+)\)\s+(.*?changelog\.txt)'
# 캡처: index, changelog_path
# IP 유형별 고유 changelog 경로 목록 추출

# 3) IP 유형별 재생성 리스크 평가
# MIG (DDR3) = 고위험 (포트 변경 가능성 높음)
# Clocking Wizard = 중위험 (출력 주파수 설정 변경 가능)
# Block Memory Gen = 저위험 (구조 안정적)
```

📊 **추출 결과**

| 필드 | 값 |
|------|---|
| `version_match_count` | 52/52 (현재 = 최신, 변경 불필요) |
| `version_mismatch_count` | 0 |
| `high_risk_ips` | `ip_mig_ddr3` (MIG 4.2) — DDR3 컨트롤러, 재생성 시 주의 |
| `changelog_types` | blk_mem_gen, clk_wiz, fifo_generator, c_addsub, div_gen, mult_gen, mig_7series, xadc_wiz (8종) |

⚖️ **판정 로직**

```python
def judge_q10(ip_data, criteria):
    if ip_data['version_mismatch_count'] > 0:
        return "FAIL", f"버전 불일치 IP {ip_data['version_mismatch_count']}개 — 재생성 필요, 포트 변경 검토 필수"
    else:
        # 현재 버전 일치 → 툴 버전 미변경 상태
        return "PASS", "현재 툴 버전에서 모든 IP 일치. 툴 변경 시 MIG IP 우선 검토 권장"
```

💬 **예상 답변**
> **PASS** — 현재 Vivado 2019.2에서 52개 IP 모두 버전 일치 (재생성 불필요). 향후 툴 버전 변경 시, **ip_mig_ddr3** (MIG 4.2, DDR3 컨트롤러)를 우선 검토해야 합니다. Change Log 8종 확인 대상.

---

## 요약 — Q1~Q10 파싱 구현 우선순위

| 우선순위 | 질문 | 답변 유형 | 파서 구현 | 리포트 |
|---------|------|----------|-------------|--------|
| ⬆️ 높음 | Q5 | AUTO | `base_parser.py` (공통 헤더) | Environment |
| ⬆️ 높음 | Q8 | AUTO | `environment_parser.py` → `parse_tool_version()` | Environment, Config_Impl |
| ⬆️ 높음 | Q9 | SEMI | `environment_parser.py` → `parse_ip_status()` | IP_Status, Environment |
| 🔹 중간 | Q10 | SEMI | Q9 파서 재사용 + changelog 파싱 | IP_Status |
| 🔹 중간 | Q1 | SEMI | `environment_parser.py` → `parse_compile_order()` | Compile_Order, Environment, IP_Status |
| ⬇️ 낮음 | Q2, Q3, Q4, Q6, Q7 | EVIDENCE_NEEDED | 파싱 불필요 | 없음 |
