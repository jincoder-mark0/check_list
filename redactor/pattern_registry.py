"""
민감정보 제거를 위한 정규표현식 패턴 레지스트리

계층 구조, 인스턴스명, 신호명, IP 이름, 호스트명 등
리포트 내에서 마스킹이 필요한 6가지 카테고리의 패턴을 정의합니다.
"""

import re
from typing import Dict, List, Pattern

# 계층 인스턴스 경로 (depth 가 2 이상인 경우 우선 타겟)
# 예: inst_top/inst_sub/target_inst
HIERARCHY_PATTERN = re.compile(r'(?:[a-zA-Z_]\w*(?:\[\d+\])?/){2,}[a-zA-Z_]\w*(?:\[\d+\])?')

# 개별 신호 및 핀 이름 (DDR, Pin_IO 등 관용적 패턴 포함)
# 예: ddr3_dq[0], pin_io_data
SIGNAL_PATTERN = re.compile(r'\b(?:pin_[io]_\w+|ddr\d?_\w+|sig_\w+)(?:\[\d+\])?\b', re.IGNORECASE)

# IP 인스턴스명 (blk, fifo, mig, clk_wiz 등)
# 예: ip_blk_mem_gen_0
IP_NAME_PATTERN = re.compile(r'\bip_(?:blk|fifo|mig|clk_wiz|pcie|dsp)\w*\b', re.IGNORECASE)

# 호스트명 및 절대 경로 패턴
# 예: C:/Users/..., /home/user/...
PATH_PATTERN = re.compile(r'(?:[a-zA-Z]:[\\/]|[\\/])[/\w\.-]+[\\/][\w\.-]+')

# 프로젝트/디자인/MAC 주소 패턴
DESIGN_PATTERN = re.compile(r'\btop_\w+\b|\bdesign_\w+\b', re.IGNORECASE)
MAC_PATTERN = re.compile(r'(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}')

# 카테고리별 패턴 묶음
MASKING_PATTERNS: Dict[str, Pattern] = {
    "hierarchy": HIERARCHY_PATTERN,
    "signal": SIGNAL_PATTERN,
    "ip": IP_NAME_PATTERN,
    "path": PATH_PATTERN,
    "design": DESIGN_PATTERN,
    "mac": MAC_PATTERN
}
