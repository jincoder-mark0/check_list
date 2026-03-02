"""
리포트 민감정보 제거 실행 엔진

개별 파일을 읽어 정의된 패턴을 찾아 치환하고,
결과를 별도 폴더에 저장합니다.
"""

import os
import re
from typing import List, Dict
from .pattern_registry import MASKING_PATTERNS
from .name_mapper import NameMapper

class ReportRedactor:
    """리포트 파일 치환 엔진"""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.mapper = NameMapper()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def redact_file(self, input_path: str, output_path: str) -> bool:
        """단일 파일에 대해 민감정보 치환 수행"""
        try:
            with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # 패턴별 치환 수행
            # 1. 계층 구조 (가장 긴 패턴이므로 먼저 수행)
            content = self._apply_masking(content, "hierarchy")

            # 2. 나머지 패턴들
            for category in ["path", "ip", "signal", "design", "mac"]:
                content = self._apply_masking(content, category)

            # 결과 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error redacting {input_path}: {e}")
            return False

    def _apply_masking(self, content: str, category: str) -> str:
        """특정 카테고리의 패턴을 찾아 치환"""
        pattern = MASKING_PATTERNS.get(category)
        if not pattern:
            return content

        def replace_func(match):
            original = match.group(0)
            return self.mapper.get_dummy_name(original, category)

        return pattern.sub(replace_func, content)

    def batch_redact(self, reports: Dict[str, str]):
        """여러 리포트 파일들에 대해 일괄 치환 실행"""
        print(f"[*] Starting redaction of {len(reports)} files...")
        success_count = 0

        for name, path in reports.items():
            # 출력 경로 결정 (원본 폴더 구조는 무시하고 평면적으로 저장하거나, 구조 유지 가능)
            # 여기서는 파일명 그대로 사용
            filename = os.path.basename(path)
            out_path = os.path.join(self.output_dir, filename)

            if self.redact_file(path, out_path):
                success_count += 1

        print(f"[*] Redaction complete. ({success_count}/{len(reports)} files processed)")
