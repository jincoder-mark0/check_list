# FPGA 리포트 분석 도구 (FPGA Report Analysis Tool)

Vivado 설계 리포트(v.2019.2 등)를 자동으로 분석하여 전문적인 체크리스트 답변을 생성하고, 설계 자산(IP) 보호를 위해 리포트 내 민감정보를 안전하게 제거하는 **FPGA 설계 검증 보조 도구**입니다.

---

## 🚀 주요 기능 (Key Features)

### 1. 체크리스트 자동 판정 (`checklist`)

* **38종 이상의 리포트 분석**: `Timing_Summary`, `Utilization`, `CDC_Report`, `Power_Report` 등 Vivado에서 생성된 다양한 리포트를 통합 파싱합니다.
* **69개 문항 자동 답변**: 사전에 정의된 69개 체크리스트 항목에 대해 정밀한 판정(PASS, FAIL, REVIEW, INFO) 및 근거 요약을 생성합니다.
* **지능형 판정 로직**: 단순 수치 비교를 넘어 `QoR Assessment`, `Methodology`, `CDC Unsafe` 경로 등 복합적인 설계 품질 지표를 연동하여 분석합니다.

### 2. 민감정보 제거 및 마스킹 (`redact`)

* **설계 자산 보호**: 인스턴스 경로, 신호/핀 이름, 클럭 명칭, 파일 경로, 호스트 이름 등 설계 보안과 직결된 텍스트를 일관성 있게 마스킹합니다.
* **데이터 무결성 유지**: 설계 수치(ns, W, %, 개수 등)는 변경하지 않아, 보안 처리 후에도 분석 결과의 유효성이 그대로 유지됩니다.
* **대용량 처리**: `Power_Opt.rpt`와 같은 수만 행 규모의 대형 리포트도 빠르고 정확하게 처리합니다.

---

## 📂 프로젝트 구조 (Project Structure)

```text
fpga_check_list/
├── fpga_report_tool.py      # 메인 실행 파일 (CLI 진입점)
├── config/                  # 판정 임계값 및 설정 (criteria.json)
├── core/                    # 리포트 탐색 및 공통 베이스 파서
├── model/                   # 40여 종 리포트 전용 파서 및 데이터 모델
├── checklist/               # 비즈니스 판정 로직 (Answer Generator)
├── redactor/                # 민감정보 식별 패턴 및 치환 엔진
├── Plan/                    # 상세 파싱 계획서 및 문항 매핑 문서
├── resources/               # 리포트 파일 트리, checklist, report 생성 룰, ...
└── test/                    # 테스트 코드
```

---

## 🛠️ 설치 및 사용법 (Usage)

### 설치

본 도구는 Python 3.x 환경에서 동작하며, 표준 라이브러리 위주로 설계되어 별도의 복잡한 설치 과정이 필요하지 않습니다.

### 기본 실행 명령어

```bash
# 1. 체크리스트 자동 답변 생성 전담
python fpga_report_tool.py checklist --report-dir <리포트_폴더_경로>

# 2. 리포트 민감정보 제거 전담
python fpga_report_tool.py redact --report-dir <리포트_폴더_경로>

# 3. 전체 기능(체크리스트 생성 + 마스킹) 실행
python fpga_report_tool.py all --report-dir <리포트_폴더_경로>
```

---

## 💡 설계 철학 (Design Philosophy)

1. **리포트 중심 설계 (Report-Centric)**: 동일한 리포트를 반복해서 읽지 않도록 설계하여 대규모 프로젝트 분석 시에도 높은 성능을 유지합니다.
2. **동적 탐색 (Dynamic Discovery)**: 고정된 폴더 구조에 의존하지 않고, 하위 디렉토리를 재귀적으로 탐색하여 필요한 리포트를 자동으로 찾아 매핑합니다.
3. **외부 기준 관리 (Decoupled Logic)**: 판정 임계값(Threshold)을 코드가 아닌 `criteria.json`에서 관리하여, 프로젝트 성격에 따라 유연하게 기준을 변경할 수 있습니다.
4. **보안 우선 (Security First)**: 원본 리포트와 마스킹된 리포트의 일관성을 철저히 유지하여 외부 협업 시에도 안전하게 소통할 수 있도록 지원합니다.

---

## 📝 라이선스 및 문의

* 모든 권리는 본 프로젝트 개발 팀에 있습니다.
* 문의 사항은 Issue 또는 내부 채널을 통해 전달해 주시기 바랍니다.
