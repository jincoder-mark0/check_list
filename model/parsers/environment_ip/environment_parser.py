"""
Environment.rpt 리포트 파서

이 모듈은 Environment.rpt 파일을 읽어서 Q01, Q05, Q08, Q09 등에 쓰이는
빌드 일시, 툴 버전, 디바이스 정보, 호스트 OS 정보 등을 추출합니다.

Attributes:
    없음

## WHY
* 프로젝트의 빌드 환경 및 타겟 디바이스 정보를 일괄적으로 파싱하기 위함

## WHAT
* 환경 리포트에서 Date, Tool Version, Device, Host 항목 추출

## HOW
* BaseParser의 정규식 매칭 및 파일 읽기 기능 활용
"""

from typing import Any, Dict
from core.base_parser import BaseParser

class EnvironmentParser(BaseParser):
    """ Environment.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Environment.rpt 파일 파싱 후 데이터 반환

        Logic:
            - 헤더 및 환경 변수 섹션에서 주요 메타데이터 추출

        Args:
            file_path: Environment.rpt 절대경로

        Returns:
            Dict[str, Any]: 추출된 환경 정보
        """
        result: Dict[str, Any] = {}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        pat_date = self.get_pattern('env_date', r'Date\s*:\s*(.*)')
        pat_tool = self.get_pattern('env_tool', r'Tool Version\s*:\s*Vivado\s+(v\.[\d.]+)\s+.*?Build\s+(\d+)')
        pat_device = self.get_pattern('env_device', r'Device\s*:\s*([\w-]+)')
        pat_speed = self.get_pattern('env_speed', r'Speed File\s*:\s*(.*)')
        pat_host = self.get_pattern('env_host', r'Host\s*:\s*\S+\s+running\s+(.*)')

        for line in lines:
            if date_val := self.extract_value_by_regex(line, pat_date):
                result['build_date'] = date_val.strip()
            elif match_tool := pat_tool.search(line):
                result['vendor'] = "Xilinx"
                result['tool_version'] = match_tool.group(1)
                result['tool_build'] = match_tool.group(2)
            elif dev_val := self.extract_value_by_regex(line, pat_device):
                result['device_part'] = dev_val
            elif speed_val := self.extract_value_by_regex(line, pat_speed):
                result['speed_file'] = speed_val.strip()
            elif host_val := self.extract_value_by_regex(line, pat_host):
                result['host_os'] = host_val.strip()

        return result
