# FPGA 리포트 분석 도구 (`fpga_report_tool.py`)

## Phase 0: 문서/리포트 분석 및 파싱 계획 수립 (완료)

- [x] 3개 핵심 문서 분석
- [x] 전체 리포트 현황 파악 (38개 파일, 7개 그룹)
- [x] Q1~Q69 ↔ 리포트 매핑 (AUTO/SEMI/EVIDENCE 분류)
- [x] 민감정보 6개 카테고리 분류 및 밀도 평가
- [x] 구현 계획서 작성 (v2) 및 리뷰 요청
- [x] Q1~Q10 상세 파싱 계획서 작성 (`q01_q10_parsing_plan.md`)
- [x] Q11~Q20 상세 파싱 계획서 작성 (`q11_q20_parsing_plan.md`)
- [x] Q21~Q30 상세 파싱 계획서 작성 (`q21_q30_parsing_plan.md`)
- [x] Q31~Q40 상세 파싱 계획서 작성 (`q31_q40_parsing_plan.md`)
- [x] Q41~Q50 상세 파싱 계획서 작성 (`q41_q50_parsing_plan.md`)
- [x] Q51~Q60 상세 파싱 계획서 작성 (`q51_q60_parsing_plan.md`)
- [x] Q61~Q69 상세 파싱 계획서 작성 (`q61_q69_parsing_plan.md`)

## Phase 1: 파서 및 데이터 파이프라인 구현 (완료)

*참고 문서: 총 7개의 상세 파싱 계획서 및 `code_style_guide.md`, `comment_guide.md` 엄격 준수*

### 1-1. 프로젝트 구조 및 설정 기반 마련 (Core & Config)

- [x] 디렉토리 구조 설정 (`core/`, `model/`, `config/` 등 명명 규칙 준수)
- [x] 판정 기준 설정 관리 모듈 (`config/criteria.json` 및 로더 파일)
  - `code_style_guide`: 상수명은 UPPER_CASE, 모듈명은 snake_case 규칙 준수
- [x] 동적 리포트 탐색기 (`core/report_finder.py`) 구현
  - `comment_guide`: 파일 상단 모듈 Docstring(WHY/WHAT/HOW) 및 타입 힌트 철저 적용

### 1-2. 데이터 모델 및 공통 파서 설계 (Model)

- [x] 파싱 데이터 및 판정 결과 응답용 모델 설계 (`model/report_models.py`)
  - `code_style_guide`: 클래스는 PascalCase, 인스턴스/메서드는 snake_case 사용
- [x] 질문-리포트 매핑 체계 모델화 (`model/question_map.py`)
  - `comment_guide`: 비즈니스 분기문이나 매핑 규칙에 상세한 블록/인라인 주석 선언
- [x] 복잡한 정규식을 처리하는 베이스 파서 (`core/base_parser.py`) 설계
  - `comment_guide`: 정규식 상수값 및 복잡한 표현식에 출처와 의미 인라인 주석 처리

### 1-3. 상세 모듈별 파서 구현 (`model/parsers/`)

- **개발 가이드**:
  - **리포트 중심 설계**: 개별 질문(Q) 단위가 아닌 **리포트 원본(데이터) 중심**으로 모듈을 설계함. 중복 파일 읽기를 방지하기 위해 단일 리포트(예: `Timing_Summary.rpt`)를 한 번만 읽어 해당 리포트를 참조하는 여러 질문(Q12, Q61, Q63 등)에 필요한 데이터 꾸러미(Dict/Object)를 추출하는 방식을 취할 것.
  - **문서화 의무**: 각 파서 모듈(`.py`) 최상단 Docstring에 "이 모듈은 OO_Report.rpt 등 N종을 읽어 QXX, QYY 등에 쓰이는 데이터를 추출합니다"와 같이 역할과 참조 리포트/문항을 필수로 명시하고 코딩을 시작할 것.
- `comment_guide`: 파서 모든 함수에 `Args`, `Returns`, `Raises`, `Logic` 섹션(Google Style Docstring) 구비
- [x] Q01~Q10 영역별 파서 함수 구현 + Q01~Q10 영역별 criteria.json 업데이트
- [x] Q11~Q20 영역별 파서 함수 구현 + Q11~Q20 영역별 criteria.json 업데이트
- [x] Q21~Q30 영역별 파서 함수 구현 + Q21~Q30 영역별 criteria.json 업데이트
- [x] Q31~Q40 영역별 파서 함수 구현 + Q31~Q40 영역별 criteria.json 업데이트
- [x] Q41~Q50 영역별 파서 함수 구현 + Q41~Q50 영역별 criteria.json 업데이트
- [x] Q51~Q60 영역별 파서 함수 구현 + Q51~Q60 영역별 criteria.json 업데이트
- [x] Q61~Q69 영역별 파서 함수 구현 + Q61~Q69 영역별 criteria.json 업데이트

### [x] 1-4. 비즈니스 로직 연동 및 검증 로직 (Integration)

- [x] 각 파싱 결과를 엮어주는 통합 모듈 구현 (`model/parsers/__init__.py` 등)
- [x] 파싱 결과 기반 판정 및 응답 생성기 (`checklist/answer_generator.py`)
  - `comment_guide`: 50~100줄 이상 로직시 논리적 단위 블록 주석(1., 2. ...) 구성
- [x] `fpga_report_tool.py` (CLI 통합 및 결과 생성)
- [x] 비즈니스 로직(Q1~Q69) 최종 정합성 검토 및 파싱 계획서 100% 동기화 (Task Matrix 완료)

## [x] Phase 2: 민감정보 제거기 (Redactor) 구현 (완료)

- [x] 패턴 등록 (`redactor/pattern_registry.py`)
- [x] 매핑 테이블 (`redactor/name_mapper.py`)
- [x] 치환 엔진 (`redactor/report_redactor.py`)

## [x] Phase 3: 도구 통합 및 검증 (완료)

- [x] `fpga_report_tool.py` CLI
- [x] 실제 리포트로 테스트 (38개 파일)
- [x] Power_Opt.rpt (22K+줄) 대용량 처리 확인
