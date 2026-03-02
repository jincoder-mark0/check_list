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

## Phase 1: 리포트 파서 및 체크리스트 생성기 구현 (진행 예정)

*참고 문서: `q01_q10_parsing_plan.md`를 포함한 총 7개의 상세 파싱 계획서를 기반으로 구현*

- [ ] 코어 인프라: 동적 리포트 탐색기 (`report_finder.py`)
- [ ] 코어 인프라: 판정 기준 외부 관리기 (`config/criteria.json` 및 로더)
- [ ] 공통 헤더 파서 (`base_parser.py`)
- [ ] 파싱 상세 계획서(`q01_q10_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 파싱 상세 계획서(`q11_q20_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 파싱 상세 계획서(`q21_q30_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 파싱 상세 계획서(`q31_q40_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 파싱 상세 계획서(`q41_q50_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 파싱 상세 계획서(`q51_q60_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 파싱 상세 계획서(`q61_q69_parsing_plan.md`) 기반 파서 함수 구현
- [ ] 13종 통합 파서 모듈 구현 (`parsers/*.py`)
- [ ] 질문-리포트 매핑 (`question_map.py`)
- [ ] 파싱 결과 + 판정 기준(`criteria`) 결합 처리 (`answer_generator.py`)

## Phase 2: 민감정보 제거기 (Redactor) 구현

- [ ] 패턴 등록 (`pattern_registry.py`)
- [ ] 매핑 테이블 (`name_mapper.py`)
- [ ] 치환 엔진 (`report_redactor.py`)

## Phase 3: 도구 통합 및 검증

- [ ] `fpga_report_tool.py` CLI
- [ ] 실제 리포트로 테스트 (38개 파일)
- [ ] Power_Opt.rpt (22K+줄) 대용량 처리 확인
