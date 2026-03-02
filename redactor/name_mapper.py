"""
민감정보 치환을 위한 이름 매핑 관리 모듈

동일한 원본 이름은 서로 다른 리포트 파일에서도 항상 일관된 더미 이름으로
치환되도록 전역 매핑 테이블을 관리합니다.
"""

from typing import Dict

class NameMapper:
    """원본-더미 명칭 일관 매핑 관리자"""

    def __init__(self):
        # 원본 문자열 -> 치환된 문자열
        self.mapping: Dict[str, str] = {}
        # 카테고리별 카운터
        self.counters: Dict[str, int] = {
            "hierarchy": 1,
            "signal": 1,
            "ip": 1,
            "path": 1,
            "design": 1,
            "mac": 1
        }

    def get_dummy_name(self, original: str, category: str) -> str:
        """
        원본 문자열에 대응하는 더미 이름을 반환합니다.

        이미 매핑된 이력이 있다면 기존 더미 이름을,
        없다면 새로운 이름을 생성하여 저장 후 반환합니다.
        """
        if original in self.mapping:
            return self.mapping[original]

        # 새로운 더미 이름 생성
        prefix = category.upper()
        count = self.counters.get(category, 1)

        if category == "hierarchy":
            # 계층 구조는 깊이를 유지하기 위해 / 개수 파악
            depths = original.split('/')
            dummy = "/".join([f"inst_{chr(65+i % 26)}" for i in range(len(depths))])
        elif category == "path":
            dummy = f"[PATH_{count:03d}]"
        elif category == "ip":
            # IP 종류는 일부 보존
            if "blk" in original.lower(): dummy = f"[BlockMem_{count:02d}]"
            elif "fifo" in original.lower(): dummy = f"[FIFO_{count:02d}]"
            else: dummy = f"[IP_{count:02d}]"
        else:
            dummy = f"{prefix}_{count:03d}"

        self.mapping[original] = dummy
        self.counters[category] = count + 1
        return dummy

    def reset(self):
        """매핑 테이블 초기화"""
        self.mapping.clear()
        for k in self.counters:
            self.counters[k] = 1
