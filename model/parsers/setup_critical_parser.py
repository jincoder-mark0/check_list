"""
Setup_Critical.rpt 리포트 파서

이 모듈은 Setup_Critical.rpt 파일을 읽어서 Q12 분석에 쓰이는
Setup 타이밍 최악 경로(Critical Path)의 Slack 및 시점/종점 데이터를 추출합니다.

Attributes:
    없음

## WHY
* Setup 타이밍 위반의 근원적인 경로를 식별하여 코드 수정 가이드 제공

## WHAT
* 최악 경로의 Slack(ns), 소스(Source), 데스티네이션(Destination) 정보 추출

## HOW
* BaseParser를 통해 텍스트 기반 경로 상세 정보 파싱
"""

from typing import Any, Dict, List
from core.base_parser import BaseParser

class SetupCriticalParser(BaseParser):
    """ Setup_Critical.rpt 파일 파싱 클래스 """

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Setup_Critical.rpt 파일 파싱 후 최악 경로 데이터 반환

        Args:
            file_path: Setup_Critical.rpt 절대경로

        Returns:
            Dict[str, Any]: Critical Path 상세 정보 (최대 10개 등 수집 가능)
        """
        result: Dict[str, List[Dict[str, Any]]] = {'critical_paths': []}
        lines = self.read_file_lines(file_path)
        if not lines:
            return result

        # 여러 경로 정보를 순차적으로 수집하기 위한 패턴
        pat_crit_path = self.get_pattern('setup_crit', r'Slack\s*:\s*([-\d.]+)\s*ns.*?Source\s*:\s*(\S+).*?Destination\s*:\s*(\S+)')

        # 파일 전체에서 매칭 수행 (멀티라인 고려 필요 시 보강)
        content = "".join(lines)
        for match in pat_crit_path.finditer(content):
            result['critical_paths'].append({
                'slack': float(match.group(1)),
                'source': match.group(2),
                'destination': match.group(3)
            })

        return result
