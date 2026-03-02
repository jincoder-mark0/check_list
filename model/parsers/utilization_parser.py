"""
Utilization.rpt 리포트 파서

이 모듈은 Utilization.rpt 파일을 읽어서 리소스 사용량(Used, Available, Util%)을 추출합니다.
(report_utilization 명령 결과 분석)

Attributes:
    없음

## WHY
* FPGA 내부 자원 점유율을 파악하여 설계 안정성을 평가하기 위함

## WHAT
* Slice Logic, Memory, DSP 등 주요 자원별 Used, Available, Util% 추출

## HOW
* 테이블 형식(| Resource | Used | ... | Util% |) 파싱
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class UtilizationParser(BaseParser):
    """ Utilization.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Utilization.rpt 파일 파싱 후 데이터 반환

        Args:
            file_path: Utilization.rpt 절대경로

        Returns:
            Dict[str, Any]: 자원별 사용량 정보
        """
        result: Dict[str, Any] = {'details': {}}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 패턴 1: Summary 포맷용 (보통 한 행에 5~6개 컬럼)
        # | Resource | Used | Fixed | Available | Util% |
        pat_summary = self.get_pattern('util_row', r'\|\s+([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([<>\d.]+)\s*\|')

        for line in lines:
            # 1. Device 정보 추출
            if 'Device' in line and ':' in line and '|' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    result['device'] = parts[1].split('|')[0].strip()

            # 2. Hierarchical 포맷 유무 확인 및 처리 (컬럼 수가 많음)
            # | Instance | Module | Total LUTs | Logic LUTs | LUTRAMs | SRLs | FFs | RAMB36 | RAMB18 | DSP48 Blocks |
            if '|' in line and line.count('|') >= 10:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 11:
                    inst = parts[1]
                    # 헤더 및 구분선 제외
                    if inst.startswith('---') or inst.lower() == 'instance' or inst.startswith('+'):
                        continue

                    # 수치 데이터인지 확인 (Total LUTs가 숫자여야 함)
                    if parts[3].replace(',', '').isdigit():
                        if 'total_luts' not in result:
                            # 디자인 전체 합계 (첫 번째 데이터 행)
                            result['total_luts'] = int(parts[3].replace(',', ''))
                            result['ffs'] = int(parts[7].replace(',', ''))
                            result['bram_tiles'] = int(parts[8].replace(',', '')) + int(parts[9].replace(',', '')) * 0.5
                            result['dsps'] = int(parts[10].replace(',', ''))
                        continue # Hierarchical 행으로 처리했으므로 Summary 패턴 매칭 건너뜀

            # 3. Summary 포맷 파싱
            match = pat_summary.search(line)
            if match:
                name = match.group(1).strip()
                # Hierarchical 행의 중간 부분이 잘못 매칭되지 않도록 수동 필터링 (숫자만 있는 이름 제외)
                if name.replace(',', '').isdigit():
                    continue

                result['details'][name] = {
                    'used': int(match.group(2)),
                    'fixed': int(match.group(3)),
                    'available': int(match.group(4)),
                    'util_pct': float(match.group(5)) if match.group(5).replace('.', '', 1).isdigit() else 0.0
                }

                # 요약 정보 기반 전체 합계 설정 (Hierarchical이 없는 경우 대비)
                if "CLB LUTs" in name: result['total_luts'] = result['details'][name]['used']
                elif "CLB Registers" in name: result['ffs'] = result['details'][name]['used']
                elif "Block RAM Tile" in name: result['bram_tiles'] = result['details'][name]['used']
                elif "DSPs" in name: result['dsps'] = result['details'][name]['used']

        return result
