# FPGA_Checklist_2_Vivado_Automated_Reports_Guide.md

**Vivado Automated Reports (Group 01 - 07)**

- 프로젝트명: LCoS 기반 WSS 제어 시스템
- Tool: Xilinx Vivado 2019.2
- Device: Artix-7
- 문서 버전: v0.1
- 작성일: 2026-02-26
- 작성자: K.J Lee
- 검토자: (TBD)
- 승인자: (TBD)

---

## 0. 머릿말

본 문서는 FPGA Checklist 전체 중 **Vivado Automated Report Guide**로서 다음 역할을 수행한다.

- Group 01~07 자동 생성 리포트의 **생성 기준, 제출 규칙, PASS 조건** 정의
- Checklist(1~69) 항목 중 Vivado 리포트 기반으로 검증 가능한 항목에 대한 **구체적 대응 기준** 제공
- Run Snapshot, Naming 규칙, 자동 생성 Tcl 구조 등 **재현성(Reproducibility)** 보장

본 문서는 **FPGA_Checklist_1_Main_Documentation_Index.md** 의 스타일을 따른다.

---

## 1. 문서 세트 구성

아래와 같은 3개의 문서로 구성된다.

| 번호 | 문서명 | 목적 |
|------|--------|------|
| 1 | FPGA_Checklist_1_Main_Documentation_Index.md | 전체 패키지의 인덱스/구조 정의 |
| **2** | **FPGA_Checklist_2_Vivado_Automated_Reports_Guide.md** *(본 문서)* | Group 01~07 자동 리포트 생성/검증 가이드 |
| 3 | FPGA_Checklist_3_System_Evidence_Guide.md | Group 08 실측, 정책 기반 증빙 가이드 |

---

## 2. 증빙 자료 패키지 구성 (Folder Structure)

### **폴더 구조 및 체크리스트 대응**

- **파일명은 단순 BaseName만 사용하며,**
- **STAGE/REV/DATETIME은 상위 ‘Run Snapshot 폴더명’에 적용합니다.**

| 폴더명 | 포함 리포트 (파일명) | 체크리스트 대응 핵심 항목 |
| :--- | :--- | :--- |
| **01_Timing_CDC** | `Timing_Summary.rpt`, `Setup_Critical.rpt`, `Hold_Critical.rpt`, `CDC_Report.rpt`, `CDC_Critical.rpt`, `CDC_Unsafe.rpt`, `Timing_Exceptions.rpt`, `CDC_Interaction.rpt`, `Check_Timing.rpt`, `Bus_Skew.rpt`, `Pulse_Width.rpt`, `Clock_Utilization.rpt`, `Clock_Networks.rpt` | 12, 32~45, 59, 61~65 |
| **02_Power_Thermal** | `Power_Data.xpe`, `Power_Report.rpt`, `Power_Opt.rpt`, `Switching_Activity.rpt`, `SSN_Report.rpt`, `Operating_Cond.rpt` | 13, 14, 25, 52, 53 |
| **03_Resources_DRC** | `Utilization.rpt`, `RAM_Utilization.rpt`, `Methodology.rpt`, `DRC_Report.rpt`, `Waiver.rpt`, `Control_Sets.rpt`, `IO_Report.rpt` | 11, 22, 30, 47, 48, 66, 67, 68 |
| **04_Design_Analysis** | `Design_Analysis.rpt`, `QoR_Assessment.rpt`, `QoR_Suggestions.rpt`, `Pipeline_Analysis.rpt`, `High_Fanout.rpt`, `Debug_Core.rpt` | 15, 16~18, 50, 51, 57 |
| **05_Environment_IP** | `IP_Status.rpt`, `Environment.rpt`, `Datasheet.rpt`, `Compile_Order.rpt`, `Property_Check.rpt`, `Clocks_Summary.rpt`, `Config_Impl.rpt` | 1~10, 19, 27, 28, 69 |
| **06_Verification** | `Coverage_Report.html`, `Coverage_Report.txt`, `Sim_Log.log`, `Testbench_Arch.pdf`, `Testcase_Index.xlsx`, `Req_Test_Traceability.xlsx`, `Assertions_Report.rpt`, `Regression_Summary.csv`, `Waveforms/`, `Sim_Config.txt` | 55, 56, 58, 59, 60 |
| **07_PR_Evidence** | `PR_DFX_Detection.txt`, `PR_NA_Evidence.txt`, `PR_Verify_Report.rpt`, `PR_DRC_Report.rpt`, `PR_PBLOCK_Utilization.rpt`, `Partial_Bit_Config_Summary.rpt` | 11, 15, 18, 26~28 |

### **공통 생성 타이밍 (기본 원칙)**

- **Timing/CDC/DRC/Utilization/Clock** -> *route_design 완료 후 post_route 기준*
- **Power/SSN/Operating Conditions** -> *최종 환경 설정 후 post_route (SAIF/VCD 반영 권장)*
- **Environment/IP/Compile Order** -> *제출 직전 최신 환경 스냅샷*
- **Verification Coverage** -> *검증 캠페인 종료 시점 종합본(HTML + 텍스트 동시 제출)*

### **그룹별 목적 / 생성 타이밍 / PASS 기준 요약**

- **설명:**
  - 아래 요약은 01~08 모든 제출 폴더의 *역할(목적)*, *생성 타이밍 또는 준비 기준*, *PASS 판단 기준 또는 충족 조건*, *체크리스트 대응 항목*을 정리한 것입니다.

- **01_Timing_CDC** - *Checklist: 12, 32~45, 59, 61~65*
  - **목적:** 타이밍 수렴(Setup/Hold), CDC 안정성, Clock/Pulse/Skew/네트워크 분석
  - **생성 타이밍:** post_route (`route_design` 완료 후)
  - **PASS 기준:**
    - WNS/WHS >= 0
    - Unconstrained = 0
    - CDC Unsafe/Critical = 0 *(Critical/Unsafe/전체 3분할 리포트 제출)*
    - Pulse Width Violation = 0
    - Bus Skew <= 인터페이스 스펙
    - Clock Duty/Phase 정상

- **02_Power_Thermal** - *Checklist: 13, 14, 25, 52, 53*
  - **목적:** 소비전력/열/SSN(동시 스위칭 노이즈)/Operating Condition 분석
  - **생성 타이밍:** post_route + 활동률(SAIF/VCD/정적 SAIF) 적용 후
  - **PASS 기준:**
    - Total Power <= PSU 설계 한계
    - Rail Current <= 전압 레일 공급 스펙
    - Junction Temperature 목표 이내
    - SSN Noise <= Vendor 가이드라인
    - AC Coupling 필요 신호 정상 처리
  - **생성 지침:** XPE 데이터는 `write_xpe`(우선) 사용 + `catch` 가드

- **03_Resources_DRC** - *Checklist: 11, 22, 30, 47, 48, 66, 67, 68*
  - **목적:** 자원 사용률, RAM/DPRAM 구성, DRC/Methodology, Control-set/IO 검증
  - **생성 타이밍:** post_route
  - **PASS 기준:**
    - FF/LUT/BRAM/DSP 사용률 < 85% (권장)
    - DRC Critical = 0
    - Methodology High Severity = 0
    - Control-set 분화 과다 없음
    - DPRAM Conflict 고려 설계 혹은 검증됨
    - PCB 종단(IOSTANDARD/TERM/VREF) 보드와 일치

- **04_Design_Analysis** - *Checklist: 15, 16~18, 50, 51, 57*
  - **목적:** QoR 예측, 혼잡(Congestion), Fanout, Pipeline, Debug Core 분석
  - **생성 타이밍:** post_place 및 post_route 비교(필요 시)
  - **PASS 기준:**
    - QoR Assessment -> “Likely to meet timing” 이상
    - 혼잡 hotspot 해결 또는 경로 분산
    - Debug Core가 양산 비트스트림에 영향을 주지 않음
    - 디버그 전용 레지스터 보호 적용

- **05_Environment_IP** - *Checklist: 1~10, 19, 27, 28, 69*
  - **목적:** 개발 환경 재현성, 사용된 IP 상태/파라미터/컴파일 순서/생성 규칙 추적
  - **생성 타이밍:** 제출 직전 최신 환경 기준
  - **PASS 기준:**
    - Vivado/OS/License/패치 버전 명확
    - IP Up-to-date 또는 Lock 사유 명확
    - Datasheet Report와 외부 인터페이스 요구 타이밍 정합
    - Config/Compile 설정이 문서와 일치

- **06_Verification** - *Checklist: 55, 56, 58, 59, 60*
  - **목적:** 요구사항 기반 기능 검증 / 커버리지 / 대체 검증(Ansync/실측 포함)
  - **생성 타이밍:** 검증 캠페인 완료 후
  - **PASS 기준:**
    - Code Coverage >= 95% (Line/Cond/Toggle/FSM 등)
    - Functional Coverage >= 90%
    - Assertion Fail = 0
    - Regression PASS 100% (Known Issue 제외 문서화)
    - Simulation 불가 항목은 System Evidence로 대체 검증
    - **HTML + 텍스트 커버리지 리포트 동시 제출(HTML 미지원 환경 대비)**

- **07_PR_Evidence** - *Checklist: 11, 15, 18, 26~28*
  - **목적:** In-service Upgrade(Partial Reconfiguration) 중 Static/RM 정상 동작 증명
  - **생성 타이밍:** PR Static/RM Implementation 완료 후
  - **PASS 기준:**
    - `pr_verify` All PASS
    - PR DRC High Severity = 0
    - Pblock 경계/자원/Isolation 조건 준수
    - Partial Bitstream Checksum/Offset/ID 정상
    - **PR 미사용 설계 시:** `PR_DFX_Detection.txt` + `PR_NA_Evidence.txt`(BUFGMUX/HD.RECONFIGURABLE=1 카운트 0)로 N/A 증빙
      *(참고: BUFG* MUX류 존재는 **PR 사용을 직접 의미하지 않음**. PR 사용 판정은 **HD.RECONFIGURABLE/Pblock 설정**을 최우선으로 함.)*

---

## 3. Vivado 리포트 추출 및 검토 상세 가이드

### **기본 설정**

- **설명**
  - 본 단계는 프로젝트 실행 후 **모든 리포트 생성 전에 단 1회 실행되는 초기화 절차**입니다.
  - 공통 경로/네이밍 규칙을 설정하여 **리포트 파일명과 출력 디렉터리가 일관되게 생성**되도록 합니다.
  - **동작 조건(set_operating_conditions)** 을 Worst-case(산업 등급/최대 공정/고온)로 설정하고,
    Simulation SAIF/VCD가 없을 경우를 대비하여 **IN/OUT/INOUT 포트 기반의 최소 활동률(Rough Switching Activity)** 을 지정합니다.
  - 이를 통해 이후 생성되는 `report_power`, `report_switching_activity` 및 기타 구현 리포트가
    **동일한 환경 조건(boundary 조건)** 하에서 분석되도록 보장하며,
    전력 분석의 초기 정확도와 재현성을 확보합니다.
  - **PR/DFX 사용 여부 자동 검출** 및 **사용 시 DCP 자동 저장** 유틸을 포함.
  - **Vivado 2019.2 호환성**을 위해 일부 명령은 `catch`로 감쌉니다.

- **체크리스트 대응**
  - **1:** 프로세스/산출물 절차 가시화
  - **8:** 툴/환경 명시
  - **13:** Worst-case 전력/열
  - **14:** 활동률 근거
  - **69:** 재현 환경 자동화
  - **26~28:** PR/DFX 사용 시 증빙 자동 보조 *(옵션)*

```tcl
# === 기본 경로/디렉터리 설정 ===
set PROJ_DIR  [get_property DIRECTORY [current_project]]    ;# 프로젝트 디렉터리
set PROJ_NAME [get_property NAME [current_project]]         ;# 프로젝트 이름
set RPT_DIR   [file join $PROJ_DIR "$PROJ_NAME.reports"]    ;# 리포트 루트 폴더
if {![file exists $RPT_DIR]} {
  file mkdir $RPT_DIR
  puts "Created directory: $RPT_DIR"
}

# === 공통 태그 변수 (stage/rev/datetime) ===
if {![info exists STAGE]} { set STAGE "post_route" }        ;# post_synth/post_place/post_route
if {![info exists REV]}   { set REV   "revA" }              ;# 리비전 태그
set DATETIME [clock format [clock seconds] -format "%Y%m%d_%H%M%S"]

# === Run 스냅샷 폴더 생성 (STAGE_REV_DATETIME) ===
set RUN_TAG "${STAGE}_${REV}_${DATETIME}"                   ;# 예: post_route_revA_20260225_104516
set RUN_DIR [file join $RPT_DIR $RUN_TAG]
if {![file exists $RUN_DIR]} {
  file mkdir $RUN_DIR
  puts "Created run directory: $RUN_DIR"
}

# === 그룹 폴더 생성 유틸 ===
proc ensure_group_dir {group_id group_name} {
  global RUN_DIR
  set d [file join $RUN_DIR $group_id]
  if {![file exists $d]} { file mkdir $d }
  return $d
}

# === 리포트 파일명 유틸 (짧은 BaseName 유지) ===
proc outfile {group_id base ext} {
  set gdir [ensure_group_dir $group_id ""]
  set safe_base [string map {" " "_"} $base]
  return [file join $gdir "${safe_base}.${ext}"]
}

# === 동작 조건 설정 (Power/Timing Worst-case) ===
# 한글 주석: 산업 등급/최대 공정/고온으로 전력/타이밍 worst-case 가정
set_operating_conditions -grade industrial -process maximum -ambient_temp 80.0

# === 포트/Clock/활동률 수집/적용 유틸 (2019.2 호환 + 안전장치) ===

# Clock/DDR/DQS 등 clock-like 이름 패턴 (v0.2: '*ck*' 추가)
if {![info exists name_clk_pat]} {
  set name_clk_pat {NAME =~ *clk* || NAME =~ *clock* || NAME =~ *dqs* || NAME =~ *ck*}
}
# 비Clock 신호 오탐 제외 (ack/cke/clock_en/clken)
if {![info exists non_clk_ex_pat]} {
  set non_clk_ex_pat {NAME =~ *ack* || NAME =~ *cke* || NAME =~ *clock_en* || NAME =~ *clken*}
}

# Clock 소스 포트를 net 역추적으로 수집
set clk_nets      [get_nets  -quiet -of_objects [all_clocks]]
set clk_src_ports [get_ports -quiet -of_objects $clk_nets]

# 리스트 차집합 유틸
proc list_diff {A B} {
  set dictB {}
  foreach x $B { dict set dictB $x 1 }
  set out {}
  foreach x $A {
    if {![dict exists $dictB $x]} { lappend out $x }
  }
  return $out
}

# 패턴으로 포트 수집 (버스 패턴 포함)
proc _ports_from_patterns {patterns} {
  set out {}
  foreach p $patterns {
    set objs [get_ports -quiet $p]
    if {[llength $objs] > 0} { set out [concat $out $objs] }
  }
  return [lsort -unique $out]
}

# 공통 제외 필터: Clock/차동N/Clock소스/오탐 제외
proc _filter_io_targets {ports} {
  # clock-like 이름 제외
  set tmp [get_ports -quiet $ports -filter "!($::name_clk_pat)"]
  # 오탐(ack/cke/clken 등)도 제외
  set tmp [get_ports -quiet $tmp   -filter "!($::non_clk_ex_pat)"]
  # 차동 N 제외
  set tmp [get_ports -quiet $tmp   -filter {NAME !~ *_n && NAME !~ *_N}]
  # Vivado가 인지한 Clock 소스 포트 제외
  set tmp [list_diff $tmp $::clk_src_ports]
  return [lsort -unique $tmp]
}

# 방향별 수집: dir ∈ {IN|OUT|INOUT}
proc collect_ports {dir include_patterns exclude_patterns} {
  # 1) 방향 기본 후보 수집
  set base [get_ports -quiet -filter "DIRECTION == $dir"]

  # 2) include 패턴이 있으면 교집합 적용
  if {[llength $include_patterns] > 0} {
    set inc [_ports_from_patterns $include_patterns]
    set filtered {}
    foreach p $base {
      if {[lsearch -exact $inc $p] != -1} {
        lappend filtered $p
      }
    }
    set base $filtered
  }

  # 3) exclude 패턴 처리
  if {[llength $exclude_patterns] > 0} {
    set exc [_ports_from_patterns $exclude_patterns]
    set filtered {}
    foreach p $base {
      if {[lsearch -exact $exc $p] == -1} {
        lappend filtered $p
      }
    }
    set base $filtered
  }

  # 4) 공통 제외(Clock 패턴/오탐/차동 N/Clock소스 제외)
  return [_filter_io_targets $base]
}

# === 프로젝트별 활동률 대상 패턴 설정 ===
# 필요 시 include/exclude 패턴만 수정해 재사용
array set ACTIVITY_CONFIG {
  IN.include     { pin_i_fmc_addr[*] pin_i_fpga_parts_version[*] pin_i_wss_rst_n pin_i_fmc_adv_n pin_i_fmc_cs1_n pin_i_fmc_oe_n pin_i_fmc_we_n }
  IN.exclude     { pin_i_*clk* pin_i_*ck* }   ;# 입력 Clock명 안전 제외

  OUT.include    { ddr3_addr[*] ddr3_ba[*] ddr3_dm[*]
                   ddr3_cas_n ddr3_ck_n ddr3_ck_p ddr3_cke ddr3_cs_n ddr3_odt
                   ddr3_ras_n ddr3_reset_n ddr3_we_n
                   pin_o_lcos_dac_data_a[*] pin_o_lcos_dac_data_b[*]
                   pin_o_lcos_ito_ctl_m pin_o_lcos_ito_ctl_p
                   pin_o_lcos_panel_* pin_o_tp0 }
  OUT.exclude    { pin_o_*clk* pin_o_*ck* }   ;# 출력 Clock명 안전 제외

  INOUT.include  { pin_io_fmc_data[*] }
  INOUT.exclude  { }
}

# === 누락 키 보정 가드 (키가 없으면 {}로 초기화) ===
if {![info exists ACTIVITY_CONFIG]} { array set ACTIVITY_CONFIG {} }
foreach key {IN.include IN.exclude OUT.include OUT.exclude INOUT.include INOUT.exclude} {
  if {![info exists ACTIVITY_CONFIG($key)]} {
    set ACTIVITY_CONFIG($key) {}
  }
}

# === 방향별 자동 수집 실행 ===
set in_ports_targets     [collect_ports IN     $ACTIVITY_CONFIG(IN.include)    $ACTIVITY_CONFIG(IN.exclude)]
set out_ports_targets    [collect_ports OUT    $ACTIVITY_CONFIG(OUT.include)   $ACTIVITY_CONFIG(OUT.exclude)]
set inout_ports_targets  [collect_ports INOUT  $ACTIVITY_CONFIG(INOUT.include) $ACTIVITY_CONFIG(INOUT.exclude)]

# 미리보기
puts [format "Collected IN    : %6d ports" [llength $in_ports_targets]]
puts [format "Collected OUT   : %6d ports" [llength $out_ports_targets]]
puts [format "Collected INOUT : %6d ports" [llength $inout_ports_targets]]

# === check_timing 선실행하여 no_clock 탐지/활동률 보수 적용 플래그 ===
set timing_chk_file [outfile 01 Check_Timing rpt]
check_timing -verbose -file $timing_chk_file

# 파일 내 'no_clock' 문자열 탐지(간이)
set NO_CLOCK_GUARD 0
if {[file exists $timing_chk_file]} {
  set fp [open $timing_chk_file r]
  set txt [read $fp]; close $fp
  if {[string match *no_clock* $txt] || [string match *No clock* $txt]} {
    set NO_CLOCK_GUARD 1
    puts "WARN: check_timing indicates possible 'no_clock' issues. Default switching activity will be applied conservatively."
  }
}

# === Rough 활동률 적용 (경고 최소화, catch 가드)  ===
# NO_CLOCK_GUARD=1이면 더 낮은 값으로 보수 적용
proc _apply_activity {ports sp tr label} {
  if {[llength $ports] > 0} {
    set emsg ""
    catch { set_switching_activity -static_probability $sp -toggle_rate $tr $ports } emsg
    if {[info exists emsg] && $emsg ne ""} { puts "WARN(activity $label): $emsg" }
  }
}

if {$NO_CLOCK_GUARD} {
  _apply_activity $in_ports_targets    0.05  0.01  IN
  _apply_activity $out_ports_targets   0.05  0.01  OUT
  _apply_activity $inout_ports_targets 0.04  0.008 INOUT
} else {
  _apply_activity $in_ports_targets    0.10  0.02  IN
  _apply_activity $out_ports_targets   0.10  0.02  OUT
  _apply_activity $inout_ports_targets 0.08  0.015 INOUT
}

# === Clock Buffer/MMCM/PLL 비-Clock 출력넷 ===
# 데이터성 넷에 한정하여 batch 적용(안전)
set clk_bufs [get_cells -hier -filter {REF_NAME =~ BUFG* || REF_NAME =~ BUFR* || REF_NAME =~ MMCM* || REF_NAME =~ PLL*}]
set clk_out_pins {}
foreach c $clk_bufs {
  set pins [get_pins -of_objects $c -filter {DIRECTION == OUT}]
  # Vivado가 clock으로 인지하는 핀 제외
  set pins [lsort -unique [lsearch -inline -all -not -exact $pins [get_pins -quiet -of_objects [all_clocks]]]]
  set clk_out_pins [concat $clk_out_pins $pins]
}
set data_like_nets [lsort -unique [get_nets -quiet -of_objects $clk_out_pins]]
# 이름 패턴으로 Clock스러운 net 배제(+오탐 제외)
set data_like_nets [get_nets -quiet -of_objects $data_like_nets -filter {! (NAME =~ *clk* || NAME =~ *clock* || NAME =~ *dqs* || NAME =~ *ck* || NAME =~ *ack* || NAME =~ *cke* || NAME =~ *clock_en* || NAME =~ *clken*)}]

if {[llength $data_like_nets] > 0} {
  set batch_size 8000
  for {set i 0} {$i < [llength $data_like_nets]} {incr i $batch_size} {
    set chunk [lrange $data_like_nets $i [expr {$i + $batch_size - 1}]]
    if {[llength $chunk] > 0} {
      set emsg ""
      catch { set_switching_activity -static_probability 0.05 -toggle_rate 0.01 $chunk } emsg
      if {[info exists emsg] && $emsg ne ""} { puts "WARN(activity data-like): $emsg" }
    }
  }
}

# === 정적 SAIF 저장(선택) ===
catch {
  write_saif -file [file join $RUN_DIR "Estimated_Activity.saif"] -hierarchical
  puts "Estimated SAIF saved: [file join $RUN_DIR Estimated_Activity.saif]"
}

# === PR/DFX 자동 검출 + DCP 자동 저장(안전 가드) ===
# 기본 활성화(PR_DCP_ENABLE=1)
proc detect_pr_dfx_simple {} {
  set reconfig_cells   [get_cells   -hier -quiet -filter {HD.RECONFIGURABLE == 1}]
  set reconfig_pblocks {}
  catch { set reconfig_pblocks [get_pblocks -quiet -filter {HD.RECONFIGURABLE == 1 || RECONFIGURABLE == 1}] }

  set used [expr {[llength $reconfig_cells] > 0 || [llength $reconfig_pblocks] > 0}]

  set msg ""
  append msg "PR/DFX 자동 점검 결과\n"
  append msg "----------------------------------------\n"
  append msg [format "HD.RECONFIGURABLE 셀 존재: %s\n" [expr {[llength $reconfig_cells] > 0 ? "YES" : "NO"}]]
  if {[llength $reconfig_cells] > 0} {
    append msg "  - 예시(상위 8개):\n"
    set i 0
    foreach c $reconfig_cells {
      append msg "    * $c\n"
      incr i
      if {$i >= 8} { append msg "    ... (생략)\n"; break }
    }
  }
  append msg [format "재구성 Pblock 속성 탐지: %s\n" [expr {[llength $reconfig_pblocks] > 0 ? "YES" : "NO"}]]
  if {[llength $reconfig_pblocks] > 0} {
    append msg "  - Pblock 목록: [join $reconfig_pblocks ", "]\n"
  }
  append msg "----------------------------------------\n"
  append msg [format "결론: %s\n" [expr {$used ? "PR/DFX 사용" : "PR/DFX 미사용(추정)"}]]

  puts $msg
  if {[info commands outfile] ne ""} {
    set out [outfile 07 PR_DFX_Detection txt]
    set fp [open $out "w"]; puts $fp $msg; close $fp
    puts "Saved PR/DFX detection report: $out"
  }
  return $used
}

# Run 존재 여부 확인 유틸
proc _run_exists {name} { expr {[llength [get_runs -quiet $name]] > 0} }

# DCP 자동 저장 스위치/기본 Run명 (필요 시 사용자 프로젝트에 맞게 조정)
if {![info exists PR_DCP_ENABLE]} { set PR_DCP_ENABLE 1 }     ;# 0=비활성, 1=활성
if {![info exists PR_STATIC_RUN]} { set PR_STATIC_RUN "impl_static" }
if {![info exists PR_RM_RUNS]}   { set PR_RM_RUNS {} }

set PR_USED [detect_pr_dfx_simple]
if {!$PR_USED} {
  puts "INFO(PR/DFX): 설계 PR/DFX 미사용(추정) -> DCP 저장 생략."
} elseif {!$PR_DCP_ENABLE} {
  puts "INFO(PR/DFX): PR_DCP_ENABLE=0 -> DCP 자동 저장 비활성 유지."
} else {
  puts "INFO(PR/DFX): PR/DFX 사용 감지 -> DCP 저장 시도."

  # Static Run 결정(없으면 자동 후보)
  if {![_run_exists $PR_STATIC_RUN]} {
    foreach cand {impl_static static_impl impl_1} {
      if {[_run_exists $cand]} { set PR_STATIC_RUN $cand; break }
    }
  }

  # RM Run 결정(사용자 지정 없으면 이름 패턴으로 자동 수집)
  set rm_runs_exist {}
  foreach r $PR_RM_RUNS { if {[_run_exists $r]} { lappend rm_runs_exist $r } }
  if {[llength $rm_runs_exist] == 0} {
    foreach r [get_runs -quiet -filter {IS_IMPLEMENTATION}] {
      set rn [get_property NAME $r]
      if {[string match *rm* $rn] || [string match *reconfig* $rn]} { lappend rm_runs_exist $rn }
    }
  }

  # Static DCP 저장
  if {[_run_exists $PR_STATIC_RUN]} {
    if {[catch {open_run $PR_STATIC_RUN} emsg]} {
      puts "WARN(PR/DFX): open_run $PR_STATIC_RUN 실패: $emsg"
    } else {
      if {[catch {write_checkpoint -force [file join $RUN_DIR "static_routed.dcp"]} emsg]} {
        puts "WARN(PR/DFX): static_routed.dcp 저장 실패: $emsg"
      } else {
        puts "Saved: [file join $RUN_DIR static_routed.dcp]"
      }
    }
  } else {
    puts "WARN(PR/DFX): Static 구현 Run을 찾지 못함(PR_STATIC_RUN=$PR_STATIC_RUN). Static DCP 저장 생략."
  }

  # RM DCP 저장(존재하는 run만)
  if {[llength $rm_runs_exist] > 0} {
    foreach rr $rm_runs_exist {
      if {[catch {open_run $rr} emsg]} { puts "WARN(PR/DFX): open_run $rr 실패: $emsg"; continue }
      set rr_name [string map {" " "_" "/" "_" "\\" "_" ":" "_" "*" "_" "?" "_" "\"" "_" "<" "_" ">" "_" "|" "_"} $rr]
      set outname [format "rm_%s_routed.dcp" $rr_name]
      if {[catch {write_checkpoint -force [file join $RUN_DIR $outname]} emsg]} {
        puts "WARN(PR/DFX): $outname 저장 실패: $emsg"
      } else {
        puts "Saved: [file join $RUN_DIR $outname]"
      }
    }
  } else {
    puts "INFO(PR/DFX): RM 구현 Run을 찾지 못함 -> RM DCP 저장 생략."
  }

  puts "INFO(PR/DFX): DCP 자동 저장 절차 완료."
}

# === PR 미사용 N/A 추가 증빙: BUFGMUX/HD.RECONFIGURABLE 카운트 0 ===
# 항상 실행하되 파일로 저장하여 Group 07 N/A 근거로 활용
set mux_cells [get_cells -hier -quiet -filter {REF_NAME =~ BUFGMUX* || REF_NAME =~ BUFGCTRL* || REF_NAME =~ BUFGCE* || REF_NAME =~ BUFGCE_DIV*}]
set reconfig_cells [get_cells -hier -quiet -filter {HD.RECONFIGURABLE == 1}]
set out_na [outfile 07 PR_NA_Evidence txt]
set fp_na [open $out_na "w"]
puts $fp_na "PR N/A 증빙 스냅샷"
puts $fp_na "----------------------------------------"
puts $fp_na [format "Clock MUX primitives (BUFGMUX/BUFGCTRL/BUFGCE*): %d" [llength $mux_cells]]
puts $fp_na [format "HD.RECONFIGURABLE==1 cells:                   %d" [llength $reconfig_cells]]
if {[llength $mux_cells] == 0 && [llength $reconfig_cells] == 0} {
  puts $fp_na "결론: Clock 스위칭/PR 관련 구조 미사용(추정) -> Group 07 = N/A"
  puts $fp_na "참고: BUFG* MUX류 존재만으로 PR 사용을 의미하지 않으며, HD.RECONFIGURABLE/Pblock 속성이 최우선 판단 기준입니다."
} else {
  puts $fp_na "결론: 관련 구조 일부 존재 -> Group 07 증빙(Verify/DRC) 필요"
}
close $fp_na
puts "Saved PR N/A evidence: $out_na"

puts "Report base directory: $RPT_DIR"
puts "Current run snapshot:  $RUN_DIR"
```

---

### **[Group 01] 타이밍 및 CDC 분석**
- **그룹 핵심:** 최악 조건 타이밍 보장/Ansync clock 처리 안전성.
- **체크리스트 대응:** *12, 32~45, 59, 61~65*

#### **① 타이밍 요약 (report_timing_summary)**
- **핵심:** 전 설계 타이밍 상태(Setup/Hold/Unconstrained)를 한 번에 점검.
- **체크리스트 대응:** *12(속도 등급 타당성), 61(clock/Reset 정의 반영), 63(최악 조건 분석), 64(서브clock 경로 마진)*
- **Tcl 명령:**
```tcl
# 타이밍 요약 (setup/hold, unconstrained, check_timing 포함)
report_timing_summary \
  -delay_type min_max -report_unconstrained -check_timing \
  -max_paths 10 -input_pins -routable_nets \
  -name final_timing_report \
  -file [outfile 01 Timing_Summary rpt]
```
- **주요 확인 사항:** WNS/WHS >= 0, Unconstrained=0, IO 포함 분석, 경로 그룹별 Fmax 대비 마진.
- **대응(조치):** 경로 재구조화(파이프라인), 제약 보강(clock/IO delay), floorplan/phys_opt 적용.

#### **② 상세 타이밍 (report_timing)**
- **핵심:** 크리티컬 경로의 Logic/Route 지연 구조 원인 파악.
- **체크리스트 대응:** *12(타이밍), 63(최악 경로 분석), 64~65(clock/스위칭 조합 마진)*
- **Tcl 명령:**
```tcl
# Setup worst path 상세
report_timing -delay_type max -path_type full_clock -max_paths 10 \
  -slack_lesser_than 0.2 -nworst 2 -name setup_critical \
  -file [outfile 01 Setup_Critical rpt]

# Hold worst path 상세
report_timing -delay_type min -path_type full_clock -max_paths 10 \
  -slack_lesser_than 0.1 -name hold_critical \
  -file [outfile 01 Hold_Critical rpt]
```
- **주요 확인 사항:** Logic/Route 비중, 반복 경로 패턴, placement 거리/혼잡, 예외와 일치성.
- **대응(조치):** 레지스터 슬라이싱/Replication, Pblock 재배치, Net weight 조정, 예외 정정.

#### **③ CDC/예외/clock 상호작용 (report_cdc / report_exceptions / report_clock_interaction)**
- **핵심:** Ansync 경로의 안전성, 예외 타당성, 도메인 간 상호작용 확인.
- **체크리스트 대응:** *39~44(Ansync/스위칭/타이밍), 47(DPRAM 충돌 대비), 59(Simulation 불가 항목 명확화), 61(정의 반영)*
- **Tcl 명령:**
```tcl
# CDC 상세 분석 (전체/세부 분리 저장: Critical/Unsafe/All)
report_cdc -details                              -name cdc_all      -file [outfile 01 CDC_Report    rpt]
catch { report_cdc -details -severity critical   -name cdc_critical -file [outfile 01 CDC_Critical rpt] }
catch { report_cdc -details -severity unsafe     -name cdc_unsafe   -file [outfile 01 CDC_Unsafe   rpt] }

# 타이밍 예외 상세 (MCP/FP 등 확인)
report_exceptions -verbose -file [outfile 01 Timing_Exceptions rpt]

# clock 도메인 상호작용 (async 경로 가시화, 노이즈 저감 옵션)
catch { report_clock_interaction -delay_type max -significant -file [outfile 01 CDC_Interaction rpt] }
```
- **주요 확인 사항:** Critical/Unsafe/Unknown=0, 멀티비트 handshake/Gray/FIFO, async 경로 <-> 예외 일치.
- **대응(조치):** 2/3-FF Sync 삽입, handshake/Gray/FIFO 적용, 잘못된 False/MCP 수정.

#### **④ 타이밍 체크 (check_timing)**
- **핵심:** 제약 누락/충돌 탐지로 타이밍 분석 신뢰성 확보.
- **체크리스트 대응:** *61(clock/Reset/IO 딜레이 정의), 66~68(메시지 처리/Waiver)*
- **Tcl 명령:**
```tcl
# 제약 누락/불일치 점검 (generated clock, I/O delay 등)
check_timing -verbose -file [outfile 01 Check_Timing rpt]
```
- **주요 확인 사항:** No_clock/Generated clock 누락 0, IO delay 누락 0, 예외 충돌 없음.
- **대응(조치):** clock/Generated clock 정의 추가, set_input/output_delay 보강, 예외 재설계.

#### **⑤ 버스 Skew (report_bus_skew)**
- **핵심:** DDR/병렬 버스의 비트 간 도착 시간 편차 관리.
- **체크리스트 대응:** *64(서브clock/CLK-Data skew), 65(스위칭 조합 정상성)*
- **Tcl 명령:**
```tcl
# Bus Skew Report (required when set_bus_skew constraints exist)
report_bus_skew -file [outfile 01 Bus_Skew rpt]
```
- **주요 확인 사항:** DQS-DQ skew spec 만족, worst/best skew 및 마진.
- **대응(조치):** 라우팅 길이 매칭, IDELAY/ODELAY 튜닝, 제약 개선.

#### **⑥ Pulse 폭 (report_pulse_width)**
- **핵심:** clock/게이트 신호의 min/max Pulse Width 위반 방지.
- **체크리스트 대응:** *45(PLL/SERDES duty), 62(PLL 출력 스펙 충족)*
- **Tcl 명령:**
```tcl
# 최소/최대 Pulse Width 위반 및 duty 준수 확인
report_pulse_width -file [outfile 01 Pulse_Width rpt]
```
- **주요 확인 사항:** min/max pulse 위반 0, duty 50%±허용오차.
- **대응(조치):** MMCM/PLL 파라미터 재설정, clock 분주/게이팅 수정.

#### **⑦ clock 리소스 (report_clock_utilization)**
- **핵심:** BUFG/MMCM/PLL 사용률/배치 적정성 점검.
- **체크리스트 대응:** *11(리소스 사용률), 37(clock 스위칭 미사용 기대)*
- **Tcl 명령:**
```tcl
# BUFG/MMCM/PLL 등 clock 자원 사용 현황
report_clock_utilization -file [outfile 01 Clock_Utilization rpt]
```
- **주요 확인 사항:** 사용률 < 85%, 중복 buffer 제거, clock 루트 균형.
- **대응(조치):** clock 통합/분리 재설계, buffer 삭감/재배치.

#### **⑧ clock 네트워크 (report_clock_networks)**
- **핵심:** clock 트리/분배 경로에서 비의도 게이팅/스위칭 차단.
- **체크리스트 대응:** *37(스위칭), 41(글리치/해저드 방지)*
- **Tcl 명령:**
```tcl
# clock 트리/분배 네트워크 구조 확인
report_clock_networks -file [outfile 01 Clock_Networks rpt]
```
- **주요 확인 사항:** clock gating/switch 의도 일치, root/BUF 계층 정상.
- **대응(조치):** clock 라우팅 재설계, glitch-free mux 적용 또는 제거.

---

### **[Group 02] 전력 및 동작 환경 분석**
- **그룹 핵심:** 레일별 전류/열/SSN 영향 평가.
- **체크리스트 대응:** *13, 14, 25, 52, 53*

#### **① 전력 리포트 (report_power / write_xpe)**
- **핵심:** worst-case 전력/열 예측으로 PSU/열설계 검증.
- **체크리스트 대응:** *13(최대 전력), 14(전압별 전류), 25(초기화 환경 일치)*
- **Tcl 명령:**
```tcl
# XPE 형식 요약 (2019.2 호환: write_xpe 우선, catch 가드)
catch { write_xpe -force [outfile 02 Power_Data xpe] }

# 상세 전력/열 리포트 (advisory 포함)
report_power -advisory -file [outfile 02 Power_Report rpt]
```
- **주요 확인 사항:** Total Power/rail current/Tj 목표 내, hotspot 블록, PSU 마진.
- **대응(조치):** clock gating/활동률 최적화, IO drive/slew 조정, 방열 강화.

#### **② 전력 최적화 (report_power_opt)**
- **핵심:** 자동 권고 기반 전력 절감 기회 도출.
- **체크리스트 대응:** *13(전력 절감 조치 검토)*
- **Tcl 명령:**
```tcl
# 전력 최적화 결과 보고 (버전/라이선스 조건에 따라 지원 상이)
catch { report_power_opt -file [outfile 02 Power_Opt rpt] }
```
- **주요 확인 사항:** 권고 적용->절감 효과, 미지원/미적용 사유.
- **대응(조치):** 권고 반영 또는 설계 변경 계획 수립/추적.

- **Vivado 버전 주의:** 일부 에디션/디바이스에서 `report_power_opt` 미출력 가능.
- **대체 증빙:** QoR/Design Analysis 제안(`report_qor_suggestions`), Clock게이팅/활동률 변경에 따른 `report_power` 전/후 비교를 Mapping.xlsx에 링크.

#### **③ 스위칭 활동 (report_switching_activity)**
- **핵심:** 전력 분석의 활동률 근거 확보.
- **체크리스트 대응:** *14(전압별 전류 산정 근거)*
- **Tcl 명령:**
```tcl
# 스위칭 활동률 요약, 계층 전체 셀 목록을 대상 오브젝트로 명시 후 리포트
report_switching_activity [get_cells -hierarchical *] -file [outfile 02 Switching_Activity rpt]
```
- **주요 확인 사항:** 활동률 소스/시나리오 일치, default 최소화(Unknown/Default 비중 확인).
- **대응(조치):** Simulation 시나리오 확장, SAIF/VCD 정확도 향상(Idle/Max/Use-case 2~3종 권장).

#### **④ SSN 분석 (report_ssn)**
- **핵심:** 동시 스위칭 노이즈에 대한 I/O bank 리스크 저감.
- **체크리스트 대응:** *52(차동/고속 종단), 53(AC coupling 필요성)*
- **Tcl 명령:**
```tcl
# 동시 스위칭 노이즈(SSN) 분석
catch { report_ssn -file [outfile 02 SSN_Report rpt] }
```
- **주요 확인 사항:**
  - bank별 simultaneous switching 제한, IO 설정/PCB 종단 일치.
  - bank별 Noise Margin 확보 및 AC Coupling 미적용 시의 기술적 근거 확인.
- **대응(조치):** Slew/Drive/IOSTANDARD 조정, 핀 재배치, AC coupling 도입 검토.
- **Vivado 버전 주의:** 일부 에디션/디바이스에서 `report_ssn` 미출력 가능.
- **대체 증빙:**System Evidence 08A**(리플/노이즈 실측)로 대체 증빙.

#### **⑤ 동작 조건 (report_operating_conditions)**
- **핵심:** 분석/설계에 사용된 온도/전압/코너의 일관성 보장.
- **체크리스트 대응:** *13(조건 일치성)*
- **Tcl 명령:**
```tcl
# 동작 전압/온도/프로세스 코너 확인
report_operating_conditions -file [outfile 02 Operating_Cond rpt]
```
- **주요 확인 사항:** 전력 리포트와 동일 조건, 디바이스 grade/전압 사양.
- **대응(조치):** 조건 재설정 후 전력/타이밍 재평가.

---

### **[Group 03] 리소스 및 규칙 준수**
- **그룹 핵심:** 자원/DRC/Methodology/IO/Control-set 규정 준수.
- **체크리스트 대응:** *11, 22, 30, 47, 48, 66, 67, 68*

#### **① 리소스 사용량 (report_utilization)**
- **핵심:** 계층별 자원 집중도와 혼잡 유발 가능성 확인.
- **체크리스트 대응:** *11(자원 사용률 적정성)*
- **Tcl 명령:**
```tcl
# 계층별 자원 사용률 (FF/LUT/BRAM/DSP 등)
report_utilization -hierarchical -file [outfile 03 Utilization rpt]
```
- **주요 확인 사항:** 사용률 < 85%, hotspot 계층, congestion 위험.
- **대응(조치):** 리팩터링/파티션/플로어플랜 조정.

#### **② RAM 사용량 (report_ram_utilization)**
- **핵심:** BRAM/URAM 구성과 W/R 충돌 위험 파악.
- **체크리스트 대응:** *22(DPRAM W/R 충돌 방지), 47(경합 보장 범위), 48(벤더 가이드 준수)*
- **Tcl 명령:**
```tcl
# RAM 블록 상세 사용률 (버전별 지원 여부에 따라 catch)
catch { report_ram_utilization -file [outfile 03 RAM_Utilization rpt] }
```
- **주요 확인 사항:** True/SDP/TDP, read-first/write-first, collision 조건.
- **대응(조치):** arbitration 삽입, 파이프 스테이지 추가, access 분리.

#### **③ 방법론 (report_methodology)**
- **핵심:** 권장 설계 가이드 준수 여부와 리스크 식별.
- **체크리스트 대응:** *66(에러 처리), 67(Warning 조치), 68(내부 합의)*
- **Tcl 명령:**
```tcl
# Xilinx 권장 설계 방법론 점검
report_methodology -name methodology_1 -file [outfile 03 Methodology rpt]
```
- **주요 확인 사항:** High severity=0, 경고 항목 처리/waiver.
- **대응(조치):** 설계 수정 또는 create_waiver + 사유서.

#### **④ DRC (report_drc)**
- **핵심:** 물리/전기적 규칙 위반 제거.
- **체크리스트 대응:** *66(필수 메시지 해결), 67(Warning 검토)*
- **Tcl 명령:**
```tcl
# 하드웨어 설계 규칙(DRC) 위반 점검
report_drc -ruledecks {default} -file [outfile 03 DRC_Report rpt]
```
- **주요 확인 사항:** ERROR/Critical 0, Waiver 대상 최소화.
- **대응(조치):** 배치/배선/전원/IO 수정, 규칙 준수.

#### **⑤ Waiver (report_waivers)**
- **핵심:** 승인된 예외의 공식 기록/추적.
- **체크리스트 대응:** *68(내부 합의/기록)*
- **Tcl 명령:**
```tcl
# 승인된 waiver 목록 출력
report_waivers -file [outfile 03 Waiver rpt]
```
- **주요 확인 사항:** 승인 근거/영향/대안, 반복 여부.
- **대응(조치):** 재검토 스케줄, 대체 증빙 강화.

#### **⑥ Control Sets (report_control_sets)**
- **핵심:** reset/enable 분화 과도 방지로 라우팅 효율 확보.
- **체크리스트 대응:** *11(자원/라우팅 효율)*
- **Tcl 명령:**
```tcl
# reset/enable/clock 제어 세트 분석
report_control_sets -verbose -file [outfile 03 Control_Sets rpt]
```
- **주요 확인 사항:** control-set 수, 분화 원인, QoR 영향.
- **대응(조치):** reset synchronization /합치, enable 공유화.

#### **⑦ IO (report_io)**
- **핵심:** 핀/IOSTANDARD/TERM/전압/VREF의 보드 정합성 확인.
- **체크리스트 대응:** *11(핀 사용률), 19(외부 메모리 IO), 30(PCB 종단), 52(고속 종단)*
- **Tcl 명령:**
```tcl
# I/O 핀/표준/전압/종단 정보 출력
report_io -file [outfile 03 IO_Report rpt]
```
- **주요 확인 사항:**
  - IOSTANDARD/DRIVE/SLEW/TERM/VREF/Bank 전압, PCB 일치.
  - 리포트의 **'Pull Type'** 설정을 전수 조사하여, FPGA 구성 전 상태가 보드 설계(Pull-up/down)와 충돌하지 않는지 확인.
- **대응(조치):** 핀 재배치, 종단/전압 조정, SI 재검토.

---

### **[Group 04] 디자인 분석 (QoR)**
- **그룹 핵심:** 성능 최적화(QoR) 및 디버그 로직의 보안성 통제.
- **체크리스트 대응:** *15, 16~18, 50, 51, 57*

#### **① Design Analysis (report_design_analysis)**
- **핵심:** 혼잡/복잡도/로직 레벨로 병목 구간 식별.
- **체크리스트 대응:** *57(변경 영향 지역 식별)*
- **Tcl 명령:**
```tcl
# 혼잡/복잡도/로직 레벨 분포 분석
report_design_analysis -congestion -complexity -logic_level_distribution \
  -file [outfile 04 Design_Analysis rpt]
```
- **주요 확인 사항:** hotspot vs critical path, 논리 레벨 깊이, placer/router 현황.
- **대응(조치):** 파이프라인 삽입, floorplan/region 재설계.

#### **② QoR Assessment/Suggestions (report_qor_assessment / report_qor_suggestions)**
- **핵심:** 타이밍 달성 가능성 평가 및 개선 제안 수립.
- **체크리스트 대응:** *15(사양 충족 가능성 평가)*
- **Tcl 명령:**
```tcl
# QoR 평가 및 개선 제안
report_qor_assessment  -file [outfile 04 QoR_Assessment  rpt]
report_qor_suggestions -file [outfile 04 QoR_Suggestions rpt]
```
- **주요 확인 사항:** meet likelihood, actionable 제안.
- **대응(조치):** 제안 반영/미반영 사유 기록, 다음 run 계획.

#### **③ Pipeline Analysis (report_pipeline_analysis)**
- **핵심:** 데이터 경로 지연 분포와 레지스터 삽입 후보 도출.
- **체크리스트 대응:** *15(경로 성능 최적화)*
- **Tcl 명령:**
```tcl
# 파이프라인 효율성/후보 경로 분석 (버전별 지원 여부에 따라 catch)
catch { report_pipeline_analysis -file [outfile 04 Pipeline_Analysis rpt] }
```
- **주요 확인 사항:** latency 영향, throughput trade-off.
- **대응(조치):** pipeline stage 배치, 프로토콜 영향 검토.

#### **④ High Fanout (report_high_fanout_nets)**
- **핵심:** 팬아웃 초과 신호에 대한 replication/buffer 전략.
- **체크리스트 대응:** *15(병목 신호 조치)*
- **Tcl 명령:**
```tcl
# 팬아웃 상위 신호 식별
report_high_fanout_nets -max_nets 50 -file [outfile 04 High_Fanout rpt]
```
- **주요 확인 사항:** fanout 임계 초과 신호, reset/enable 구조.
- **대응(조치):** buffer/replication, tree 분기 재설계.

#### **⑤ Debug Core (report_debug_core)**
- **핵심:** ILA/VIO 등 디버그 로직의 무단 접근 방지 및 양산 시 비활성화 확인.
- **체크리스트 대응:** *18(디버그 보호), 50(비규격 접근 금지), 51(디버그 레지스터 보호)*
- **Tcl 명령:**
```tcl
# ILA/VIO 등 디버그 코어 구성 확인
report_debug_core -file [outfile 04 Debug_Core rpt]
```
- **주요 확인 사항:** 양산 비트스트림 비활성, 접근 통제, QoR 영향.
- **대응(조치):** 디버그 신호 축소/제거, JTAG 보안, access policy 문서화.

---

### **[Group 05] 환경 및 IP 정보**
- **그룹 핵심:** 툴 버전, IP 에라타 및 하드 매크로 속성 검증.
- **체크리스트 대응:** *1~10, 19, 27, 28, 69*

#### **① IP Status (report_ip_status)**
- **핵심:** 사용 IP 버전 관리와 재생성 영향 추적.
- **체크리스트 대응:** *9(결함/이슈 확인), 10(IP 재생성 영향)*
- **Tcl 명령:**
```tcl
# IP 버전/업데이트/에라타 상황 점검
report_ip_status -file [outfile 05 IP_Status rpt]
```
- **주요 확인 사항:** out-of-date/locked/black-box, upgrade 영향/계획.
- **대응(조치):** 재생성/locking 결정, 변경 영향 보고.

#### **② Environment (report_environment)**
- **핵심:** Vivado/OS/License 등 환경 스냅샷으로 재현성 보장.
- **체크리스트 대응:** *8(버전), 69(실사용 툴 결함 확인)*
- **Tcl 명령:**
```tcl
# Vivado/OS/License 등 환경 스냅샷
report_environment -file [outfile 05 Environment rpt]
```
- **주요 확인 사항:** Vivado 2019.2/패치/OS, 라이선스.
- **대응(조치):** 환경 버전 고정, 변경 시 영향 보고.

#### **③ Datasheet (report_datasheet)**
- **핵심:** 외부 인터페이스 IO 타이밍 참고값 추출.
- **체크리스트 대응:** *19(외부 메모리), 24(초기화 후 동작), 25(파워/초기화 시퀀스)*
- **Tcl 명령:**
```tcl
# 외부 인터페이스용 IO 타이밍 데이터시트
report_datasheet -file [outfile 05 Datasheet rpt]
```
- **주요 확인 사항:** IO setup/hold 값, 시스템 타이밍 예산 정합.
- **대응(조치):** 타이밍 여유 부족 시 PCB/FPGA 제약 조정.

#### **④ Compile Order (report_compile_order)**
- **핵심:** 소스/제약 우선순위 충돌 예방.
- **체크리스트 대응:** *1(프로세스 가시화)*
- **Tcl 명령:**
```tcl
# 소스/제약 컴파일 순서 목록
report_compile_order -file [outfile 05 Compile_Order rpt]
```
- **주요 확인 사항:** precedence 충돌 없음, XDC 적용 순서 일치.
- **대응(조치):** 파일 의존성 정리, out-of-context 관리.

#### **⑤ Property Check (report_property / report_clocks)**
- **핵심:** 모든 clock 객체의 Frequency/Phase/Duty/Generated Clock 파라미터를 점검하여 설정 일관성을 검증.
- **체크리스트 대응:** *27 (하드매크로 활성 조건 검토), 62 (PLL 출력 Frequency/Phase/Duty 검증)*
- **Tcl 명령 (요약 + 상세 리포트 생성):**
```tcl
# Clock 요약 리포트 (추천: 사람이 읽기 쉬운 표 형태)
report_clocks -file [outfile 05 Clocks_Summary rpt]

# Clock별 속성 상세 (report_property는 단일 객체만 허용하므로 loop 사용)
set rpt_file [outfile 05 Property_Check rpt]
set first 1
foreach clk [all_clocks] {
  if ($first) {
    report_property $clk -file $rpt_file         ;# 첫 Clock -> 파일 생성
    set first 0
  } else {
    report_property $clk -append -file $rpt_file ;# 이후 Clock -> append
  }
}
```
- **주요 확인 사항:** Frequency/Phase/Duty, 생성clock 파라미터.
- **대응(조치):** clock 파라미터 수정, 제약 업데이트.

#### **⑥ Config Implementation (report_config_implementation)**
- **핵심:** 구현 Run 전략/옵션 투명성 확보.
- **체크리스트 대응:** *28(전원/설정 절차 일관)*
- **Tcl 명령:**
```tcl
# 출력 파일 경로
set _cfg_out [outfile 05 Config_Impl rpt]

# 1) 우선: report_config_implementation 시도
set _rc_msg ""
if {[catch { report_config_implementation -file $_cfg_out } _rc_msg]} {
  puts "INFO: report_config_implementation not available or failed: $_rc_msg"
  puts "INFO: Falling back to manual Config/Impl summary."

  # 2) 대체 요약(Fallback) – 구현 Run 자동 탐색 + 주요 속성 덤프

  # (a) 구현 Run 자동 탐색: 사용자가 impl_1, impl_static 등 여러 이름을 쓸 수 있으므로
  set _impl_candidates {impl_1 impl_static static_impl}
  # 구현 Run 중에서 가장 최근(마지막) 것을 후순위로도 고려
  set _all_impl_runs [get_runs -quiet -filter {IS_IMPLEMENTATION}]
  foreach r $_all_impl_runs {
    # 사용자 정의 후보보다 실제 존재하는 구현 run을 우선 리스트 맨 앞에 넣음 (중복 방지)
    set rn [get_property NAME $r]
    if {[lsearch -exact $_impl_candidates $rn] < 0} {
      set _impl_candidates [linsert $_impl_candidates 0 $rn]
    }
  }

  # (b) 첫 번째 존재하는 구현 Run 선택
  set _impl_run ""
  foreach cand $_impl_candidates {
    if {[llength [get_runs -quiet $cand]] > 0} { set _impl_run $cand ; break }
  }

  # (c) 출력 파일 오픈
  set _fp [open $_cfg_out "w"]

  # (d) 예쁘게 출력하는 포맷터
  proc _pp {name val} { return [format "%-30s : %s\n" $name $val] }

  if {$_impl_run ne ""} {
    set _run_obj [get_runs -quiet $_impl_run]

    # (e) 기본 정보
    puts $_fp [_pp "Run Name"             [get_property NAME $_run_obj]]
    puts $_fp [_pp "Strategy"             [get_property STRATEGY $_run_obj]]

    # (f) 단계별 디렉티브/시드 (버전/전략에 따라 속성이 없을 수 있으므로 catch)
    set _pdir ""; catch { set _pdir [get_property STEPS.PLACE_DESIGN.ARGS.DIRECTIVE $_run_obj] }
    set _rdir ""; catch { set _rdir [get_property STEPS.ROUTE_DESIGN.ARGS.DIRECTIVE $_run_obj] }
    set _phyd ""; catch { set _phyd [get_property STEPS.PHYS_OPT_DESIGN.ARGS.DIRECTIVE $_run_obj] }
    set _psee ""; catch { set _psee [get_property STEPS.PLACE_DESIGN.ARGS.PLACE_SEED $_run_obj] }
    set _rsee ""; catch { set _rsee [get_property STEPS.ROUTE_DESIGN.ARGS.ROUTE_SEED $_run_obj] }
    set _more ""; catch { set _more [get_property STRATEGY.MORE_OPTIONS $_run_obj] }

    puts $_fp [_pp "Place Directive"      $_pdir]
    puts $_fp [_pp "Route Directive"      $_rdir]
    puts $_fp [_pp "phys_opt Directive"   $_phyd]
    puts $_fp [_pp "Placer Seed"          $_psee]
    puts $_fp [_pp "Router Seed"          $_rsee]
    puts $_fp [_pp "More Options"         $_more]

    # (g) 멀티스레드/성능 관련 전역 파라미터(있다면)
    set _jobs "";  catch { set _jobs  [get_param general.maxThreads] }
    set _ultra ""; catch { set _ultra [get_property STEPS.PLACE_DESIGN.ARGS.ULTRAFAST $_run_obj] }
    if {$_jobs ne ""}  { puts $_fp [_pp "Max Threads" $_jobs] }
    if {$_ultra ne ""} { puts $_fp [_pp "UltraFast Place" $_ultra] }

    # (h) 실행 상태/결과 스냅샷
    set _sts ""; catch { set _sts [get_property STATUS $_run_obj] }
    set _strt ""; catch { set _strt [get_property START_TIME $_run_obj] }
    set _endt ""; catch { set _endt [get_property END_TIME   $_run_obj] }
    if {$_sts ne ""}  { puts $_fp [_pp "Run Status"  $_sts] }
    if {$_strt ne ""} { puts $_fp [_pp "Start Time"  $_strt] }
    if {$_endt ne ""} { puts $_fp [_pp "End Time"    $_endt] }

    # (i) 핵심 툴 버전/환경(요약)
    set _vivado_ver [version -short]
    puts $_fp [_pp "Vivado Version" $_vivado_ver]
    # 필요 시 OS/License 등은 report_environment에 포괄되므로 여기서는 요약만
  } else {
    puts $_fp "No implementation run found. Please ensure at least one implementation run exists (e.g., impl_1)."
  }

  close $_fp
  puts "Saved Config/Impl summary (fallback): $_cfg_out"
} else {
  puts "Saved Config/Impl summary (native): $_cfg_out"
}
```
- **주요 확인 사항:** strategy/phys_opt/seed, reproducibility.
- **대응(조치):** 전략 고정/변경 이력 관리.

---

### **[Group 06] 검증 커버리지 (Verification)**
- **그룹 핵심:** 요구사항 기반 Simulation 충실도 및 대체 검증 수단 확보.
- **체크리스트 대응:** *55, 56, 58, 59, 60*

#### **① Simulation Coverage (xsim/xcrg 또는 대안)**
- **핵심:** Code/Functional/Assertion 커버리지로 검증 충실도 입증.
- **체크리스트 대응:** *55~56(Simulation 스펙/환경/조건), 58(커버리지 확인법), 59(Ansync 등 Simulation 불가 항목 명시), 60(대체 검증)*

- **Tcl/Bash 명령:**
```tcl
# (Vivado) 커버리지 DB 생성/리포트
# 환경에 따라 xcrg가 없을 수 있으므로 HTML + 텍스트를 병행
xsim <tb_name> -cov_db_name_dir ./cov_data -tclbatch run.tcl

# 1) HTML 리포트(가능한 경우)
catch { xcrg -report_format html -dir ./cov_data -report_dir [ensure_group_dir 06 "Verification"]/Coverage_Report_html }

# 2) 텍스트 리포트(항상 제출 권장)
catch { xcrg -report_format text -dir ./cov_data -report_dir [ensure_group_dir 06 "Verification"]/Coverage_Report_txt }
```
```bash
# (대안) xelab/xsim 경로: 텍스트 리포트 확보
xelab -prj tb.prj -debug typical --incr --relax --mt 8 --timescale 1ns/1ps --coverage all -s tb_cov
xsim tb_cov -t xsim_run.tcl -runall
# 환경에 따라 HTML 변환이 불가할 수 있으므로, 텍스트 요약을 병행 제출
# 결과 파일 예시:
#   06_Verification/Coverage_Report.html
#   06_Verification/Coverage_Report.txt
```
- **주요 확인 사항:** CodeCov(Line/Cond/Toggle/FSM/Branch)/FuncCov 목표 충족, Assertion Fail=0, Regression=100%(예외 문서화), Req<->TC trace 완결.
- **대응(조치):** 미달 항목 TC 추가/Stimulus 강화, Assertion 보강, 실측/에뮬로 대체 검증.
- **Coverage Exclusion/Waiver 권고:** 벤더 IP/DFX/검증 불가 영역은 08S(Warning_Disposition_Minutes)에 **제외 기준/사유/승인**을 기록하고, Coverage 리포트에 Exclusion 마스크를 링크하십시오.
- **Simulation이 불가능한 항목:** 비동기 로직 등 Simulation이 불가능한 항목은, **System Evidence**와 매칭하여 추적성 확보.

---

### **[Group 07] Partial Reconfiguration Evidence Package (PR/DFX)**

- **그룹 핵심:** 서비스 중 재구성 시 정적 영역(Static)에 미치는 영향 차단.
- **체크리스트 대응:** *26, 27, 28*
- **핵심 사항:** 미사용 시 N/A 근거 서류(`PR_NA_Evidence.txt`) 제출 필수.

#### **PR/DFX 미사용 설계:**
- 본 설계는 Partial Reconfiguration(DFX)을 사용하지 않는 **정적(Static) 구성 FPGA 설계**
- 따라서 본 그룹은 **N/A 처리**되며,
  - 기본 설정 단계에서 자동 생성된 `PR_DFX_Detection.txt` (PR 사용 여부 추정 결과)
  - **추가 N/A 근거**: `PR_NA_Evidence.txt` *(BUFGMUX/BUFGCTRL/BUFGCE* 카운트, HD.RECONFIGURABLE=1 카운트 = 0)*
  를 함께 제출한다.
- 아래는 체크리스트 26/27/28에 대한 공식 답변 예

| 항목 | 답변 | 이유 |
|:---:|:----:|:-----|
| **26** | **N/A** | PR/DFX 없음 -> 재구성 중 동작 변화 없음 |
| **27** | **YES** | 하드매크로 조건은 정적 설계 규칙만 적용 |
| **28** | **YES** | 정적 full-config만 사용, partial-config 없음 |

> **주의:** BUFG* Clock MUX류 **존재만으로 PR 사용을 의미하지 않음**.
> PR 사용 판정은 **HD.RECONFIGURABLE 속성/Pblock 설정/DFX Flow 구성**으로 판단.

#### **① PR Verify (Static <-> RM 호환성 체크)**
- **핵심:** Static <-> RM 인터페이스 호환성/일관성 검증.
- **체크리스트 대응:** *26(서비스 중 무영향 보장)*
- **Tcl 명령:**
```tcl
# Static <-> RM 인터페이스 호환성/일관성 점검
# PR/DFX 사용 설계인 경우에만 실행됨
if {$PR_USED} {
  # 입력 DCP 자동 유도
  if {![info exists PR_STATIC_DCP]} { set PR_STATIC_DCP [file join $RUN_DIR "static_routed.dcp"] }
  if {![info exists PR_RM_DCPS]}    { set PR_RM_DCPS    [glob -nocomplain [file join $RUN_DIR "rm_*_routed.dcp"]] }
  if {[file exists $PR_STATIC_DCP] && [llength $PR_RM_DCPS] > 0} {
    set emsg ""
    catch {
      pr_verify -full_check \
        -initial   $PR_STATIC_DCP \
        -additional $PR_RM_DCPS \
        -file [outfile 07 PR_Verify_Report rpt]
    } emsg
    if {$emsg ne ""} { puts "WARN(pr_verify): $emsg" }
  } else {
    puts "INFO: pr_verify 입력 DCP가 충분하지 않아 스킵합니다."
  }
}
```
- **주요 확인 사항:** 모든 체크 PASS, RM 변형 간 cross-compatibility, mismatch 0.
- **대응(조치):** 인터페이스 정의/속성 재정렬, 버전 호환 매트릭스 재검증.

#### **② PR 전용 DRC (HDPR-* 규칙)**
- **핵심:** PR 경계 규칙(fence/blocker/containment) 준수 확인.
- **체크리스트 대응:** *27(활성 조건/제한 준수)*
- **Tcl 명령:**
```tcl
# PR 전용 HDPR 규칙 기반 DRC
if {$PR_USED} {
  set pr_checks [get_drc_checks -quiet -regexp {^HDPR-}]
  report_drc -checks $pr_checks \
    -file [outfile 07 PR_DRC_Report rpt]
}
```
- **주요 확인 사항:** High severity=0, overlap/out-of-range 0, containment 위반 0.
- **대응(조치):** Pblock 경계 수정, route containment 보강.

#### **③ Pblock Floorplan Evidence (RP 영역)**
- **핵심:** RP 영역 자원 여유/인터페이스 근접 배치/혼잡 억제.
- **체크리스트 대응:** *11(자원), 15(QoR)*
- **Tcl 명령:**
```tcl
# RP Pblock 자원/경계/혼잡 확인
if {$PR_USED && [llength $PR_PBLOCKS] > 0} {
  report_pblock -pblocks $PR_PBLOCKS \
    -file [outfile 07 PR_PBLOCK_Utilization rpt]
}
```
- **주요 확인 사항:** RP 자원 여유, 인터페이스 최소 경로, 혼잡 확산 방지.
- **대응(조치):** RP 크기/형상 조정, 인터페이스 경계 재배치.

#### **④ Partial Bitstream / 구성 무결성 Evidence**
- **핵심:** PR Configuration Summary(Checksum/Offset/Partition ID)로 무결성/절차 확인.
- **체크리스트 대응:** *26(동작 영향), 28(설정 절차), 18(보안/무결성)*
- **Tcl 명령:**
```tcl
# Partial Bitstream 생성 (RM 대상 인스턴스 경로가 있을 경우)
if {$PR_USED && [info exists PR_RM_INSTANCE]} {
    # 1. 비트스트림 생성 (바이너리)
    catch {
        write_bitstream -cell $PR_RM_INSTANCE -partial -force \
            [file join $RUN_DIR "07_partial_rm0.bit"]
    }

    # 2. 구성 요약(Configuration Summary) Evidence 추출
    # Checksum, Offset, Partition ID 등 무결성 확인용 텍스트 리포트 생성
    set pr_summary_file [outfile 07 Partial_Bit_Config_Summary rpt]
    catch {
        report_pr_configuration_summary -cell $PR_RM_INSTANCE -file $pr_summary_file
    }
}
```
- **주요 확인 사항:** Static/RM checksum/offset/ID 기록, 암호화/CRC 옵션, 실패 시 롤백 절차.
- **대응(조치):** 비트스트림 재생성/검증, PR 절차서 업데이트, 보안 정책 반영.

---

### **전문가의 마지막 팁**
- **체크리스트 대응:** *66~68 (에러/경고 처리/합의)*
`report_methodology`/`report_drc` 경고 중 설계상 불가피 항목은 `create_waiver`로 프로젝트에 공식 기록하고, `report_waivers`를 제출 패키지에 포함하세요. 경고 해소/무시 사유는 체크리스트 비고란에 간단히 문서화하고, 로그에는 “협의 완료/영향 없음” 코멘트를 남기면 감사 대응이 수월합니다.
또한 **README**에는 다음을 명시하세요:
- Implement Strategy/Seed **잠금 정책**(placer/router/phys_opt directive/seed)
- **Git Tag/Commit + Bitstream SHA256** 매핑(릴리스/양산용)
- **XDC 적용 순서/우선순위 정책**(중복/충돌 방지, `check_timing` Zero-no_clock 목표)
- **Coverage 리포트 HTML + 텍스트** 동시 제출 지침
- **PR 미사용 N/A 증빙 파일 경로**(`PR_DFX_Detection.txt`, `PR_NA_Evidence.txt`)
- **Vivado 2019.2 지원 매트릭스/대체 증빙 표**(본 문서 3. 하단 표 참조)

---

## 4. Vivado 2019.2 지원 매트릭스 / 대체 증빙 표 (권장 부록)

| 명령/리포트 | 2019.2 지원성 | 비고/대체 증빙 |
|---|---|---|
| `report_power_opt` | 환경/에디션 의존 (미출력 가능) | QoR Suggestions, `report_power` 전/후 비교 증빙 |
| `report_ssn` | 디바이스/흐름 의존 | 08A 리플/SSN 실측으로 대체 |
| `report_pipeline_analysis` | 옵션 차이/에디션 의존 | `report_high_fanout_nets`, `report_design_analysis` 보조 |
| `report_ram_utilization` | 디바이스/버전 의존 | Utilization 계층 분석 + RTL RAM 인스턴스 표 추가 |
| `report_config_implementation` | 버전 의존 | **대체 스니펫(3.⑥ 하단)** 사용 |

> 본 표는 README에 그대로 포함하여 리뷰어가 *미출력=오류*로 오인하지 않도록 안내하십시오.

---

## 5. 문서 버전

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| v0.1 | 2026-02-26 | K.J Lee | 최초 작성 |

---

## 6. 변경 이력(Change Log)

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| v0.1 | 2026-02-26 | K.J Lee | 최초 작성 |

---

## Note

- 본 문서는 Vivado 자동 리포트 기반 Group 01~07의 **공식 기준 문서**이다.
- Group 08(System Evidence)은 본 문서의 대상이 아니며 별도의 문서에서 관리된다.
- 모든 리포트는 Run Snapshot 단위로 제출하며,
  동일 조건의 재현성(Reproducibility)을 보장해야 한다.

---

## [부록] PASS/FAIL 기준 표준 템플릿
- **체크리스트 대응:** *11~15, 57~68* - 각 기준 달성/미달성 시 조치 명문화.

| 그룹 | 항목 | PASS 기준 | FAIL 시 조치 |
|---|---|---|---|
| 01_Timing_CDC | WNS/WHS | >= 0.000 ns | 경로 분석, 파이프라인/제약/플로어플랜 개선 |
| 01_Timing_CDC | Unconstrained | 0 | Clock/Generated clock/IO constraints 보완 |
| 01_Timing_CDC | CDC Critical/Unsafe | 0 | Sync 삽입, Handshake/Gray/FIFO 적용, 예외 재검토 |
| 02_Power_Thermal | Total Power | PSU 용량-마진 내 | Clock gating, 전력 최적화, 활동률 개선 |
| 02_Power_Thermal | Rail Current | 사양 내 | IO Drive/Slew 조정, IP 파워 옵션 |
| 02_Power_Thermal | Tj | 목표 Tj 이내 | 히트싱크/에어플로우/Clock 다운 등 |
| 03_Resources_DRC | DRC Critical | 0 | 설계 수정 또는 Waiver + 사유서 |
| 03_Resources_DRC | Control Sets | 과도 증가 금지 | Reset/Enable 도메인 통합/정리 |
| 04_Design_Analysis | QoR 예상 | Meet 가능 | QoR suggestions 적용 |
| 05_Environment_IP | IP Status | Up-to-date | Regenerate/Lock + 문서화 |
| 06_Verification | Code/Func Cov | 합의 목표 달성 | TC 추가/Stimulus 개선 |
| 07_PR_Evidence | pr_verify | All PASS | 인터페이스 정의/속성 재점검 |
| 07_PR_Evidence | PR DRC | High Sev 0 | Pblock/Fence/Isolation 수정 |

---

## [부록] 일괄 리포트 자동화 스크립트 (경로/변수/outfile 재사용)
- **체크리스트 대응:** *1 (프로세스 가시화), 8 (툴 일관성), 69 (재현성)*

```tcl
# run_all_reports.tcl (템플릿) - 모든 리포트를 일괄 생성

# === 기본 경로/디렉터리 설정 ===
set PROJ_DIR  [get_property DIRECTORY [current_project]]    ;# 프로젝트 디렉터리
set PROJ_NAME [get_property NAME [current_project]]         ;# 프로젝트 이름
set RPT_DIR   [file join $PROJ_DIR "$PROJ_NAME.reports"]    ;# 리포트 루트 폴더
if {![file exists $RPT_DIR]} {
  file mkdir $RPT_DIR
  puts "Created directory: $RPT_DIR"
}

# === 공통 태그 변수 (stage/rev/datetime) ===
if {![info exists STAGE]} { set STAGE "post_route" }        ;# post_synth/post_place/post_route
if {![info exists REV]}   { set REV   "revA" }              ;# 리비전 태그
set DATETIME [clock format [clock seconds] -format "%Y%m%d_%H%M%S"]

# === Run 스냅샷 폴더 생성 (STAGE_REV_DATETIME) ===
set RUN_TAG "${STAGE}_${REV}_${DATETIME}"                   ;# 예: post_route_revA_20260225_104516
set RUN_DIR [file join $RPT_DIR $RUN_TAG]
if {![file exists $RUN_DIR]} {
  file mkdir $RUN_DIR
  puts "Created run directory: $RUN_DIR"
}

# === 그룹 폴더 생성 유틸 ===
proc ensure_group_dir {group_id group_name} {
  global RUN_DIR
  set d [file join $RUN_DIR $group_id]
  if {![file exists $d]} { file mkdir $d }
  return $d
}

# === 리포트 파일명 유틸 (짧은 BaseName 유지) ===
proc outfile {group_id base ext} {
  set gdir [ensure_group_dir $group_id ""]
  set safe_base [string map {" " "_"} $base]
  return [file join $gdir "${safe_base}.${ext}"]
}

# === 동작 조건 설정 (Power/Timing Worst-case) ===
# 한글 주석: 산업 등급/최대 공정/고온으로 전력/타이밍 worst-case 가정
set_operating_conditions -grade industrial -process maximum -ambient_temp 80.0

# === 포트/Clock/활동률 수집/적용 유틸 (2019.2 호환 + 안전장치) ===

# Clock/DDR/DQS 등 clock-like 이름 패턴 (v0.2: '*ck*' 추가)
if {![info exists name_clk_pat]} {
  set name_clk_pat {NAME =~ *clk* || NAME =~ *clock* || NAME =~ *dqs* || NAME =~ *ck*}
}
# 비Clock 신호 오탐 제외 (ack/cke/clock_en/clken)
if {![info exists non_clk_ex_pat]} {
  set non_clk_ex_pat {NAME =~ *ack* || NAME =~ *cke* || NAME =~ *clock_en* || NAME =~ *clken*}
}

# Clock 소스 포트를 net 역추적으로 수집
set clk_nets      [get_nets  -quiet -of_objects [all_clocks]]
set clk_src_ports [get_ports -quiet -of_objects $clk_nets]

# 리스트 차집합 유틸
proc list_diff {A B} {
  set dictB {}
  foreach x $B { dict set dictB $x 1 }
  set out {}
  foreach x $A {
    if {![dict exists $dictB $x]} { lappend out $x }
  }
  return $out
}

# 패턴으로 포트 수집 (버스 패턴 포함)
proc _ports_from_patterns {patterns} {
  set out {}
  foreach p $patterns {
    set objs [get_ports -quiet $p]
    if {[llength $objs] > 0} { set out [concat $out $objs] }
  }
  return [lsort -unique $out]
}

# 공통 제외 필터: Clock/차동N/Clock소스/오탐 제외
proc _filter_io_targets {ports} {
  # clock-like 이름 제외
  set tmp [get_ports -quiet $ports -filter "!($::name_clk_pat)"]
  # 오탐(ack/cke/clken 등)도 제외
  set tmp [get_ports -quiet $tmp   -filter "!($::non_clk_ex_pat)"]
  # 차동 N 제외
  set tmp [get_ports -quiet $tmp   -filter {NAME !~ *_n && NAME !~ *_N}]
  # Vivado가 인지한 Clock 소스 포트 제외
  set tmp [list_diff $tmp $::clk_src_ports]
  return [lsort -unique $tmp]
}

# 방향별 수집: dir ∈ {IN|OUT|INOUT}
proc collect_ports {dir include_patterns exclude_patterns} {
  # 1) 방향 기본 후보 수집
  set base [get_ports -quiet -filter "DIRECTION == $dir"]

  # 2) include 패턴이 있으면 교집합 적용
  if {[llength $include_patterns] > 0} {
    set inc [_ports_from_patterns $include_patterns]
    set filtered {}
    foreach p $base {
      if {[lsearch -exact $inc $p] != -1} {
        lappend filtered $p
      }
    }
    set base $filtered
  }

  # 3) exclude 패턴 처리
  if {[llength $exclude_patterns] > 0} {
    set exc [_ports_from_patterns $exclude_patterns]
    set filtered {}
    foreach p $base {
      if {[lsearch -exact $exc $p] == -1} {
        lappend filtered $p
      }
    }
    set base $filtered
  }

  # 4) 공통 제외(Clock 패턴/오탐/차동 N/Clock소스 제외)
  return [_filter_io_targets $base]
}

# === 프로젝트별 활동률 대상 패턴 설정 ===
# 필요 시 include/exclude 패턴만 수정해 재사용
array set ACTIVITY_CONFIG {
  IN.include     { pin_i_fmc_addr[*] pin_i_fpga_parts_version[*] pin_i_wss_rst_n pin_i_fmc_adv_n pin_i_fmc_cs1_n pin_i_fmc_oe_n pin_i_fmc_we_n }
  IN.exclude     { pin_i_*clk* pin_i_*ck* }   ;# 입력 Clock명 안전 제외

  OUT.include    { ddr3_addr[*] ddr3_ba[*] ddr3_dm[*]
                   ddr3_cas_n ddr3_ck_n ddr3_ck_p ddr3_cke ddr3_cs_n ddr3_odt
                   ddr3_ras_n ddr3_reset_n ddr3_we_n
                   pin_o_lcos_dac_data_a[*] pin_o_lcos_dac_data_b[*]
                   pin_o_lcos_ito_ctl_m pin_o_lcos_ito_ctl_p
                   pin_o_lcos_panel_* pin_o_tp0 }
  OUT.exclude    { pin_o_*clk* pin_o_*ck* }   ;# 출력 Clock명 안전 제외

  INOUT.include  { pin_io_fmc_data[*] }
  INOUT.exclude  { }
}

# === 누락 키 보정 가드 (키가 없으면 {}로 초기화) ===
if {![info exists ACTIVITY_CONFIG]} { array set ACTIVITY_CONFIG {} }
foreach key {IN.include IN.exclude OUT.include OUT.exclude INOUT.include INOUT.exclude} {
  if {![info exists ACTIVITY_CONFIG($key)]} {
    set ACTIVITY_CONFIG($key) {}
  }
}

# === 방향별 자동 수집 실행 ===
set in_ports_targets     [collect_ports IN     $ACTIVITY_CONFIG(IN.include)    $ACTIVITY_CONFIG(IN.exclude)]
set out_ports_targets    [collect_ports OUT    $ACTIVITY_CONFIG(OUT.include)   $ACTIVITY_CONFIG(OUT.exclude)]
set inout_ports_targets  [collect_ports INOUT  $ACTIVITY_CONFIG(INOUT.include) $ACTIVITY_CONFIG(INOUT.exclude)]

# 미리보기
puts [format "Collected IN    : %6d ports" [llength $in_ports_targets]]
puts [format "Collected OUT   : %6d ports" [llength $out_ports_targets]]
puts [format "Collected INOUT : %6d ports" [llength $inout_ports_targets]]

# === check_timing 선실행하여 no_clock 탐지/활동률 보수 적용 플래그 ===
set timing_chk_file [outfile 01 Check_Timing rpt]
check_timing -verbose -file $timing_chk_file

# 파일 내 'no_clock' 문자열 탐지(간이)
set NO_CLOCK_GUARD 0
if {[file exists $timing_chk_file]} {
  set fp [open $timing_chk_file r]
  set txt [read $fp]; close $fp
  if {[string match *no_clock* $txt] || [string match *No clock* $txt]} {
    set NO_CLOCK_GUARD 1
    puts "WARN: check_timing indicates possible 'no_clock' issues. Default switching activity will be applied conservatively."
  }
}

# === Rough 활동률 적용 (경고 최소화, catch 가드)  ===
# NO_CLOCK_GUARD=1이면 더 낮은 값으로 보수 적용
proc _apply_activity {ports sp tr label} {
  if {[llength $ports] > 0} {
    set emsg ""
    catch { set_switching_activity -static_probability $sp -toggle_rate $tr $ports } emsg
    if {[info exists emsg] && $emsg ne ""} { puts "WARN(activity $label): $emsg" }
  }
}

if {$NO_CLOCK_GUARD} {
  _apply_activity $in_ports_targets    0.05  0.01  IN
  _apply_activity $out_ports_targets   0.05  0.01  OUT
  _apply_activity $inout_ports_targets 0.04  0.008 INOUT
} else {
  _apply_activity $in_ports_targets    0.10  0.02  IN
  _apply_activity $out_ports_targets   0.10  0.02  OUT
  _apply_activity $inout_ports_targets 0.08  0.015 INOUT
}

# === Clock Buffer/MMCM/PLL 비-Clock 출력넷 ===
# 데이터성 넷에 한정하여 batch 적용(안전)
set clk_bufs [get_cells -hier -filter {REF_NAME =~ BUFG* || REF_NAME =~ BUFR* || REF_NAME =~ MMCM* || REF_NAME =~ PLL*}]
set clk_out_pins {}
foreach c $clk_bufs {
  set pins [get_pins -of_objects $c -filter {DIRECTION == OUT}]
  # Vivado가 clock으로 인지하는 핀 제외
  set pins [lsort -unique [lsearch -inline -all -not -exact $pins [get_pins -quiet -of_objects [all_clocks]]]]
  set clk_out_pins [concat $clk_out_pins $pins]
}
set data_like_nets [lsort -unique [get_nets -quiet -of_objects $clk_out_pins]]
# 이름 패턴으로 Clock스러운 net 배제(+오탐 제외)
set data_like_nets [get_nets -quiet -of_objects $data_like_nets -filter {! (NAME =~ *clk* || NAME =~ *clock* || NAME =~ *dqs* || NAME =~ *ck* || NAME =~ *ack* || NAME =~ *cke* || NAME =~ *clock_en* || NAME =~ *clken*)}]

if {[llength $data_like_nets] > 0} {
  set batch_size 8000
  for {set i 0} {$i < [llength $data_like_nets]} {incr i $batch_size} {
    set chunk [lrange $data_like_nets $i [expr {$i + $batch_size - 1}]]
    if {[llength $chunk] > 0} {
      set emsg ""
      catch { set_switching_activity -static_probability 0.05 -toggle_rate 0.01 $chunk } emsg
      if {[info exists emsg] && $emsg ne ""} { puts "WARN(activity data-like): $emsg" }
    }
  }
}

# === 정적 SAIF 저장(선택) ===
catch {
  write_saif -file [file join $RUN_DIR "Estimated_Activity.saif"] -hierarchical
  puts "Estimated SAIF saved: [file join $RUN_DIR Estimated_Activity.saif]"
}

# === PR/DFX 자동 검출 + DCP 자동 저장(안전 가드) ===
# 기본 활성화(PR_DCP_ENABLE=1)
proc detect_pr_dfx_simple {} {
  set reconfig_cells   [get_cells   -hier -quiet -filter {HD.RECONFIGURABLE == 1}]
  set reconfig_pblocks {}
  catch { set reconfig_pblocks [get_pblocks -quiet -filter {HD.RECONFIGURABLE == 1 || RECONFIGURABLE == 1}] }

  set used [expr {[llength $reconfig_cells] > 0 || [llength $reconfig_pblocks] > 0}]

  set msg ""
  append msg "PR/DFX 자동 점검 결과\n"
  append msg "----------------------------------------\n"
  append msg [format "HD.RECONFIGURABLE 셀 존재: %s\n" [expr {[llength $reconfig_cells] > 0 ? "YES" : "NO"}]]
  if {[llength $reconfig_cells] > 0} {
    append msg "  - 예시(상위 8개):\n"
    set i 0
    foreach c $reconfig_cells {
      append msg "    * $c\n"
      incr i
      if {$i >= 8} { append msg "    ... (생략)\n"; break }
    }
  }
  append msg [format "재구성 Pblock 속성 탐지: %s\n" [expr {[llength $reconfig_pblocks] > 0 ? "YES" : "NO"}]]
  if {[llength $reconfig_pblocks] > 0} {
    append msg "  - Pblock 목록: [join $reconfig_pblocks ", "]\n"
  }
  append msg "----------------------------------------\n"
  append msg [format "결론: %s\n" [expr {$used ? "PR/DFX 사용" : "PR/DFX 미사용(추정)"}]]

  puts $msg
  if {[info commands outfile] ne ""} {
    set out [outfile 07 PR_DFX_Detection txt]
    set fp [open $out "w"]; puts $fp $msg; close $fp
    puts "Saved PR/DFX detection report: $out"
  }
  return $used
}

# Run 존재 여부 확인 유틸
proc _run_exists {name} { expr {[llength [get_runs -quiet $name]] > 0} }

# DCP 자동 저장 스위치/기본 Run명 (필요 시 사용자 프로젝트에 맞게 조정)
if {![info exists PR_DCP_ENABLE]} { set PR_DCP_ENABLE 1 }     ;# 0=비활성, 1=활성
if {![info exists PR_STATIC_RUN]} { set PR_STATIC_RUN "impl_static" }
if {![info exists PR_RM_RUNS]}   { set PR_RM_RUNS {} }

set PR_USED [detect_pr_dfx_simple]
if {!$PR_USED} {
  puts "INFO(PR/DFX): 설계 PR/DFX 미사용(추정) -> DCP 저장 생략."
} elseif {!$PR_DCP_ENABLE} {
  puts "INFO(PR/DFX): PR_DCP_ENABLE=0 -> DCP 자동 저장 비활성 유지."
} else {
  puts "INFO(PR/DFX): PR/DFX 사용 감지 -> DCP 저장 시도."

  # Static Run 결정(없으면 자동 후보)
  if {![_run_exists $PR_STATIC_RUN]} {
    foreach cand {impl_static static_impl impl_1} {
      if {[_run_exists $cand]} { set PR_STATIC_RUN $cand; break }
    }
  }

  # RM Run 결정(사용자 지정 없으면 이름 패턴으로 자동 수집)
  set rm_runs_exist {}
  foreach r $PR_RM_RUNS { if {[_run_exists $r]} { lappend rm_runs_exist $r } }
  if {[llength $rm_runs_exist] == 0} {
    foreach r [get_runs -quiet -filter {IS_IMPLEMENTATION}] {
      set rn [get_property NAME $r]
      if {[string match *rm* $rn] || [string match *reconfig* $rn]} { lappend rm_runs_exist $rn }
    }
  }

  # Static DCP 저장
  if {[_run_exists $PR_STATIC_RUN]} {
    if {[catch {open_run $PR_STATIC_RUN} emsg]} {
      puts "WARN(PR/DFX): open_run $PR_STATIC_RUN 실패: $emsg"
    } else {
      if {[catch {write_checkpoint -force [file join $RUN_DIR "static_routed.dcp"]} emsg]} {
        puts "WARN(PR/DFX): static_routed.dcp 저장 실패: $emsg"
      } else {
        puts "Saved: [file join $RUN_DIR static_routed.dcp]"
      }
    }
  } else {
    puts "WARN(PR/DFX): Static 구현 Run을 찾지 못함(PR_STATIC_RUN=$PR_STATIC_RUN). Static DCP 저장 생략."
  }

  # RM DCP 저장(존재하는 run만)
  if {[llength $rm_runs_exist] > 0} {
    foreach rr $rm_runs_exist {
      if {[catch {open_run $rr} emsg]} { puts "WARN(PR/DFX): open_run $rr 실패: $emsg"; continue }
      set rr_name [string map {" " "_" "/" "_" "\\" "_" ":" "_" "*" "_" "?" "_" "\"" "_" "<" "_" ">" "_" "|" "_"} $rr]
      set outname [format "rm_%s_routed.dcp" $rr_name]
      if {[catch {write_checkpoint -force [file join $RUN_DIR $outname]} emsg]} {
        puts "WARN(PR/DFX): $outname 저장 실패: $emsg"
      } else {
        puts "Saved: [file join $RUN_DIR $outname]"
      }
    }
  } else {
    puts "INFO(PR/DFX): RM 구현 Run을 찾지 못함 -> RM DCP 저장 생략."
  }

  puts "INFO(PR/DFX): DCP 자동 저장 절차 완료."
}

# === PR 미사용 N/A 추가 증빙: BUFGMUX/HD.RECONFIGURABLE 카운트 0 ===
# 항상 실행하되 파일로 저장하여 Group 07 N/A 근거로 활용
set mux_cells [get_cells -hier -quiet -filter {REF_NAME =~ BUFGMUX* || REF_NAME =~ BUFGCTRL* || REF_NAME =~ BUFGCE* || REF_NAME =~ BUFGCE_DIV*}]
set reconfig_cells [get_cells -hier -quiet -filter {HD.RECONFIGURABLE == 1}]
set out_na [outfile 07 PR_NA_Evidence txt]
set fp_na [open $out_na "w"]
puts $fp_na "PR N/A 증빙 스냅샷"
puts $fp_na "----------------------------------------"
puts $fp_na [format "Clock MUX primitives (BUFGMUX/BUFGCTRL/BUFGCE*): %d" [llength $mux_cells]]
puts $fp_na [format "HD.RECONFIGURABLE==1 cells:                   %d" [llength $reconfig_cells]]
if {[llength $mux_cells] == 0 && [llength $reconfig_cells] == 0} {
  puts $fp_na "결론: Clock 스위칭/PR 관련 구조 미사용(추정) -> Group 07 = N/A"
  puts $fp_na "참고: BUFG* MUX류 존재만으로 PR 사용을 의미하지 않으며, HD.RECONFIGURABLE/Pblock 속성이 최우선 판단 기준입니다."
} else {
  puts $fp_na "결론: 관련 구조 일부 존재 -> Group 07 증빙(Verify/DRC) 필요"
}
close $fp_na
puts "Saved PR N/A evidence: $out_na"

puts "Report base directory: $RPT_DIR"
puts "Current run snapshot:  $RUN_DIR"

### **[Group 01] 타이밍 및 CDC 분석**
# 타이밍 요약 (setup/hold, unconstrained, check_timing 포함)
report_timing_summary \
  -delay_type min_max -report_unconstrained -check_timing \
  -max_paths 10 -input_pins -routable_nets \
  -name final_timing_report \
  -file [outfile 01 Timing_Summary rpt]
# Setup worst path 상세
report_timing -delay_type max -path_type full_clock -max_paths 10 \
  -slack_lesser_than 0.2 -nworst 2 -name setup_critical \
  -file [outfile 01 Setup_Critical rpt]
# Hold worst path 상세
report_timing -delay_type min -path_type full_clock -max_paths 10 \
  -slack_lesser_than 0.1 -name hold_critical \
  -file [outfile 01 Hold_Critical rpt]
# CDC 상세 분석 (전체/세부 분리 저장: Critical/Unsafe/All)
report_cdc -details                              -name cdc_all     -file [outfile 01 CDC_Report    rpt]
catch { report_cdc -details -severity critical   -name cdc_critical -file [outfile 01 CDC_Critical rpt] }
catch { report_cdc -details -severity unsafe     -name cdc_unsafe   -file [outfile 01 CDC_Unsafe   rpt] }
# 타이밍 예외 상세 (MCP/FP 등 확인)
report_exceptions -verbose -file [outfile 01 Timing_Exceptions rpt]
# clock 도메인 상호작용 (async 경로 가시화, 노이즈 저감 옵션)
catch { report_clock_interaction -delay_type max -significant -file [outfile 01 CDC_Interaction rpt] }
# 제약 누락/불일치 점검 (generated clock, I/O delay 등)
check_timing -verbose -file [outfile 01 Check_Timing rpt]
# Bus Skew Report (required when set_bus_skew constraints exist)
report_bus_skew -file [outfile 01 Bus_Skew rpt]
# 최소/최대 Pulse Width 위반 및 duty 준수 확인
report_pulse_width -file [outfile 01 Pulse_Width rpt]
# BUFG/MMCM/PLL 등 clock 자원 사용 현황
report_clock_utilization -file [outfile 01 Clock_Utilization rpt]
# clock 트리/분배 네트워크 구조 확인
report_clock_networks -file [outfile 01 Clock_Networks rpt]

### **[Group 02] 전력 및 동작 환경 분석**
# XPE 형식 요약 (2019.2 호환: write_xpe 우선, catch 가드)
catch { write_xpe -force [outfile 02 Power_Data xpe] }
# 상세 전력/열 리포트 (advisory 포함)
report_power -advisory -file [outfile 02 Power_Report rpt]
# 전력 최적화 결과 보고 (버전/라이선스 조건에 따라 지원 상이)
catch { report_power_opt -file [outfile 02 Power_Opt rpt] }
# 스위칭 활동률 요약, 계층 전체 셀 목록을 대상 오브젝트로 명시 후 리포트
report_switching_activity [get_cells -hierarchical *] -file [outfile 02 Switching_Activity rpt]
# 동시 스위칭 노이즈(SSN) 분석
catch { report_ssn -file [outfile 02 SSN_Report rpt] }
# 동작 전압/온도/프로세스 코너 확인
report_operating_conditions -file [outfile 02 Operating_Cond rpt]

### **[Group 03] 리소스 및 규칙 준수**
# 계층별 자원 사용률 (FF/LUT/BRAM/DSP 등)
report_utilization -hierarchical -file [outfile 03 Utilization rpt]
# RAM 블록 상세 사용률 (버전별 지원 여부에 따라 catch)
catch { report_ram_utilization -file [outfile 03 RAM_Utilization rpt] }
# Xilinx 권장 설계 방법론 점검
report_methodology -name methodology_1 -file [outfile 03 Methodology rpt]
# 하드웨어 설계 규칙(DRC) 위반 점검
report_drc -ruledecks {default} -file [outfile 03 DRC_Report rpt]
# 승인된 waiver 목록 출력
report_waivers -file [outfile 03 Waiver rpt]
# reset/enable/clock 제어 세트 분석
report_control_sets -verbose -file [outfile 03 Control_Sets rpt]
# I/O 핀/표준/전압/종단 정보 출력
report_io -file [outfile 03 IO_Report rpt]

### **[Group 04] 디자인 분석 (QoR)**
# 혼잡/복잡도/로직 레벨 분포 분석
report_design_analysis -congestion -complexity -logic_level_distribution \
  -file [outfile 04 Design_Analysis rpt]
# QoR 평가 및 개선 제안
report_qor_assessment  -file [outfile 04 QoR_Assessment  rpt]
report_qor_suggestions -file [outfile 04 QoR_Suggestions rpt]
# 파이프라인 효율성/후보 경로 분석 (버전별 지원 여부에 따라 catch)
catch { report_pipeline_analysis -file [outfile 04 Pipeline_Analysis rpt] }
# 팬아웃 상위 신호 식별
report_high_fanout_nets -max_nets 50 -file [outfile 04 High_Fanout rpt]
# ILA/VIO 등 디버그 코어 구성 확인
report_debug_core -file [outfile 04 Debug_Core rpt]

### **[Group 05] 환경 및 IP 정보**
# IP 버전/업데이트/에라타 상황 점검
report_ip_status -file [outfile 05 IP_Status rpt]
# Vivado/OS/License 등 환경 스냅샷
report_environment -file [outfile 05 Environment rpt]
# 외부 인터페이스용 IO 타이밍 데이터시트
report_datasheet -file [outfile 05 Datasheet rpt]
# 소스/제약 컴파일 순서 목록
report_compile_order -file [outfile 05 Compile_Order rpt]
# Clock 요약 리포트 (추천: 사람이 읽기 쉬운 표 형태)
report_clocks -file [outfile 05 Clocks_Summary rpt]
# Clock별 속성 상세 (report_property는 단일 객체만 허용하므로 loop 사용)
set rpt_file [outfile 05 Property_Check rpt]
set first 1
foreach clk [all_clocks] {
  if ($first) {
    report_property $clk -file $rpt_file         ;# 첫 Clock -> 파일 생성
    set first 0
  } else {
    report_property $clk -append -file $rpt_file ;# 이후 Clock -> append
  }
}
# 출력 파일 경로
set _cfg_out [outfile 05 Config_Impl rpt]

# 1) 우선: report_config_implementation 시도
set _rc_msg ""
if {[catch { report_config_implementation -file $_cfg_out } _rc_msg]} {
  puts "INFO: report_config_implementation not available or failed: $_rc_msg"
  puts "INFO: Falling back to manual Config/Impl summary."

  # 2) 대체 요약(Fallback) – 구현 Run 자동 탐색 + 주요 속성 덤프

  # (a) 구현 Run 자동 탐색: 사용자가 impl_1, impl_static 등 여러 이름을 쓸 수 있으므로
  set _impl_candidates {impl_1 impl_static static_impl}
  # 구현 Run 중에서 가장 최근(마지막) 것을 후순위로도 고려
  set _all_impl_runs [get_runs -quiet -filter {IS_IMPLEMENTATION}]
  foreach r $_all_impl_runs {
    # 사용자 정의 후보보다 실제 존재하는 구현 run을 우선 리스트 맨 앞에 넣음 (중복 방지)
    set rn [get_property NAME $r]
    if {[lsearch -exact $_impl_candidates $rn] < 0} {
      set _impl_candidates [linsert $_impl_candidates 0 $rn]
    }
  }

  # (b) 첫 번째 존재하는 구현 Run 선택
  set _impl_run ""
  foreach cand $_impl_candidates {
    if {[llength [get_runs -quiet $cand]] > 0} { set _impl_run $cand ; break }
  }

  # (c) 출력 파일 오픈
  set _fp [open $_cfg_out "w"]

  # (d) 예쁘게 출력하는 포맷터
  proc _pp {name val} { return [format "%-30s : %s\n" $name $val] }

  if {$_impl_run ne ""} {
    set _run_obj [get_runs -quiet $_impl_run]

    # (e) 기본 정보
    puts $_fp [_pp "Run Name"             [get_property NAME $_run_obj]]
    puts $_fp [_pp "Strategy"             [get_property STRATEGY $_run_obj]]

    # (f) 단계별 디렉티브/시드 (버전/전략에 따라 속성이 없을 수 있으므로 catch)
    set _pdir ""; catch { set _pdir [get_property STEPS.PLACE_DESIGN.ARGS.DIRECTIVE $_run_obj] }
    set _rdir ""; catch { set _rdir [get_property STEPS.ROUTE_DESIGN.ARGS.DIRECTIVE $_run_obj] }
    set _phyd ""; catch { set _phyd [get_property STEPS.PHYS_OPT_DESIGN.ARGS.DIRECTIVE $_run_obj] }
    set _psee ""; catch { set _psee [get_property STEPS.PLACE_DESIGN.ARGS.PLACE_SEED $_run_obj] }
    set _rsee ""; catch { set _rsee [get_property STEPS.ROUTE_DESIGN.ARGS.ROUTE_SEED $_run_obj] }
    set _more ""; catch { set _more [get_property STRATEGY.MORE_OPTIONS $_run_obj] }

    puts $_fp [_pp "Place Directive"      $_pdir]
    puts $_fp [_pp "Route Directive"      $_rdir]
    puts $_fp [_pp "phys_opt Directive"   $_phyd]
    puts $_fp [_pp "Placer Seed"          $_psee]
    puts $_fp [_pp "Router Seed"          $_rsee]
    puts $_fp [_pp "More Options"         $_more]

    # (g) 멀티스레드/성능 관련 전역 파라미터(있다면)
    set _jobs "";  catch { set _jobs  [get_param general.maxThreads] }
    set _ultra ""; catch { set _ultra [get_property STEPS.PLACE_DESIGN.ARGS.ULTRAFAST $_run_obj] }
    if {$_jobs ne ""}  { puts $_fp [_pp "Max Threads" $_jobs] }
    if {$_ultra ne ""} { puts $_fp [_pp "UltraFast Place" $_ultra] }

    # (h) 실행 상태/결과 스냅샷
    set _sts ""; catch { set _sts [get_property STATUS $_run_obj] }
    set _strt ""; catch { set _strt [get_property START_TIME $_run_obj] }
    set _endt ""; catch { set _endt [get_property END_TIME   $_run_obj] }
    if {$_sts ne ""}  { puts $_fp [_pp "Run Status"  $_sts] }
    if {$_strt ne ""} { puts $_fp [_pp "Start Time"  $_strt] }
    if {$_endt ne ""} { puts $_fp [_pp "End Time"    $_endt] }

    # (i) 핵심 툴 버전/환경(요약)
    set _vivado_ver [version -short]
    puts $_fp [_pp "Vivado Version" $_vivado_ver]
    # 필요 시 OS/License 등은 report_environment에 포괄되므로 여기서는 요약만
  } else {
    puts $_fp "No implementation run found. Please ensure at least one implementation run exists (e.g., impl_1)."
  }

  close $_fp
  puts "Saved Config/Impl summary (fallback): $_cfg_out"
} else {
  puts "Saved Config/Impl summary (native): $_cfg_out"
}

### **[Group 06] 검증 커버리지 (Verification)**
## (Vivado) 커버리지 DB 생성/리포트
## 환경에 따라 xcrg가 없을 수 있으므로 HTML + 텍스트를 병행
#xsim <tb_name> -cov_db_name_dir ./cov_data -tclbatch run.tcl
#
## 1) HTML 리포트(가능한 경우)
#catch { xcrg -report_format html -dir ./cov_data -report_dir [ensure_group_dir 06 "Verification"]/Coverage_Report_html }
#
## 2) 텍스트 리포트(항상 제출 권장)
#catch { xcrg -report_format text -dir ./cov_data -report_dir [ensure_group_dir 06 "Verification"]/Coverage_Report_txt }
#
## [bash]
## (대안) xelab/xsim 경로: 텍스트 리포트 확보
## xelab -prj tb.prj -debug typical --incr --relax --mt 8 --timescale 1ns/1ps --coverage all -s tb_cov
## xsim tb_cov -t xsim_run.tcl -runall
## 환경에 따라 HTML 변환이 불가할 수 있으므로, 텍스트 요약을 병행 제출
## 결과 파일 예시:
##   06_Verification/Coverage_Report.html
##   06_Verification/Coverage_Report.txt

### **[Group 07] Partial Reconfiguration Evidence Package (PR/DFX)**
if {!$PR_USED} {
  # --- PR 미사용: N/A 처리 ---
  puts "INFO: PR/DFX 미사용 설계 -> Group 07 모든 PR Evidence는 N/A로 처리됩니다."
}
# Static <-> RM 인터페이스 호환성/일관성 점검
# PR/DFX 사용 설계인 경우에만 실행됨
if {$PR_USED} {
  # 입력 DCP 자동 유도
  if {![info exists PR_STATIC_DCP]} { set PR_STATIC_DCP [file join $RUN_DIR "static_routed.dcp"] }
  if {![info exists PR_RM_DCPS]}    { set PR_RM_DCPS    [glob -nocomplain [file join $RUN_DIR "rm_*_routed.dcp"]] }
  if {[file exists $PR_STATIC_DCP] && [llength $PR_RM_DCPS] > 0} {
    set emsg ""
    catch {
      pr_verify -full_check \
        -initial   $PR_STATIC_DCP \
        -additional $PR_RM_DCPS \
        -file [outfile 07 PR_Verify_Report rpt]
    } emsg
    if {$emsg ne ""} { puts "WARN(pr_verify): $emsg" }
  } else {
    puts "INFO: pr_verify 입력 DCP가 충분하지 않아 스킵합니다."
  }
}
# PR 전용 HDPR 규칙 기반 DRC
if {$PR_USED} {
  set pr_checks [get_drc_checks -quiet -regexp {^HDPR-}]
  report_drc -checks $pr_checks \
    -file [outfile 07 PR_DRC_Report rpt]
}
# RP Pblock 자원/경계/혼잡 확인
if {$PR_USED && [llength $PR_PBLOCKS] > 0} {
  report_pblock -pblocks $PR_PBLOCKS \
    -file [outfile 07 PR_PBLOCK_Utilization rpt]
}
# Partial Bitstream 생성 (RM 대상 인스턴스 경로가 있을 경우)
if {$PR_USED && [info exists PR_RM_INSTANCE]} {
    # 1. 비트스트림 생성 (바이너리)
    catch {
        write_bitstream -cell $PR_RM_INSTANCE -partial -force \
            [file join $RUN_DIR "07_partial_rm0.bit"]
    }

    # 2. 구성 요약(Configuration Summary) Evidence 추출
    # Checksum, Offset, Partition ID 등 무결성 확인용 텍스트 리포트 생성
    set pr_summary_file [outfile 07 Partial_Bit_Config_Summary rpt]
    catch {
        report_pr_configuration_summary -cell $PR_RM_INSTANCE -file $pr_summary_file
    }
}

puts "All reports generated in: $RPT_DIR"
```
