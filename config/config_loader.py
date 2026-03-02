"""
JSON 형식의 판정 기준(Criteria) 설정을 로드하고 관리

FPGA 리포트 분석에 필요한 각 평가 항목의 임계값, 허용 범위 등
설정 데이터를 `criteria.json` 파일에서 로드하여 제공

Attributes:
    DEFAULT_CONFIG_PATH: 기본 설정 파일 경로

## WHY
* 판정 기준값(임계치, 퍼센트, 조건 등)의 하드코딩 방지
* 사용자가 기준값을 쉽게 변경하고 관리할 수 있도록 지원

## WHAT
* `criteria.json` 파싱 후 파이썬 딕셔너리로 제공
* 파일 미존재 및 JSON 포맷 오류에 대한 예외 처리

## HOW
* 내장 `json` 모듈을 통한 파일 읽기 수행
* 타입 힌팅을 활용해 설정 데이터 구조 명확화
"""

import json
import os
from typing import Any, Dict

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "criteria.json")

def load_criteria(config_path: str = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    JSON 형식의 평가 기준 설정 파일 로드

    지정된 경로의 JSON 파일을 파싱하여 파이썬 딕셔너리로 반환.
    파일 누락이나 JSON 파싱 실패 시 빈 딕셔너리 부분 반환.

    Logic:
        - 파일 존재 여부 확인 후 읽기 시도
        - JSON 파싱 예외 처리 (FileNotFoundError, json.JSONDecodeError)

    Args:
        config_path: 설정 파일의 경로. 기본값은 DEFAULT_CONFIG_PATH

    Returns:
        Dict[str, Any]: 로드된 설정 데이터 딕셔너리. 오류 발생 시 빈 딕셔너리(`{}`) 반환.

    Examples:
        >>> criteria = load_criteria("custom_criteria.json")
        >>> print(criteria.get("tool", {}).get("known_stable_versions", []))
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file not found at {config_path}. Using empty criteria.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from {config_path}. {e}")
        return {}
