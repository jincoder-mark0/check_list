"""
RAM_Utilization.rpt 리포트 파서

이 모듈은 RAM_Utilization.rpt 파일을 읽어서 Q21(ECC), Q22(W/R 충돌) 분석에 쓰이는
Memory Utilization 및 ECC 활성화 여부 데이터를 추출합니다.

Attributes:
    없음

## WHY
* BRAM의 세부 설정(ECC, 포트 구성)을 파악하여 데이터 무결성 및 충돌 위험 평가

## WHAT
* Memory Utilization 테이블의 ECC Enabled 컬럼 및 Port 구성 정보 추출

## HOW
* BaseParser를 상속받아 테이블 헤더 위치 기반 컬럼 데이터 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class RAMUtilizationParser(BaseParser):
    """ RAM_Utilization.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        RAM_Utilization.rpt 파일 파싱 후 데이터 반환

        Logic:
            - 테이블 행에서 ECC Enabled 상태 및 메모리 타입(SP, SDP, TDP 등) 추출

        Args:
            file_path: RAM_Utilization.rpt 절대경로

        Returns:
            Dict[str, Any]: RAM 사용 상세 및 ECC 정보
        """
        result: Dict[str, Any] = {'memories': [], 'ecc_enabled': False, 'total_bram': 0, 'ram_types': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 메모리 타입 및 ECC 정보 추출 패턴
        # | Instance | Module | Type | ... | ECC Enabled |
        pat_ram_row = self.get_pattern('ram_row', r'\|\s*(\S+)\s*\|\s+(\S+)\s*\|\s+([^\|]+?)\s*\|.*?\|\s*(True|False|Yes|No|\s*)\s+\|$')

        for line in lines:
            match = pat_ram_row.search(line)
            if match:
                is_ecc = match.group(4).strip() in ['True', 'Yes']
                ram_type = match.group(3).strip()

                result['memories'].append({
                    'instance': match.group(1),
                    'module': match.group(2),
                    'type': ram_type,
                    'ecc_enabled': is_ecc
                })

                if is_ecc:
                    result['ecc_enabled'] = True
                if 'Block RAM' in ram_type or 'RAMB' in ram_type:
                    result['total_bram'] += 1
                if ram_type not in result['ram_types']:
                    result['ram_types'].append(ram_type)

        return result
