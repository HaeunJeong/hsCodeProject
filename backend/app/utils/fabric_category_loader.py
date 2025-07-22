"""
패브릭 카테고리 데이터를 JSON 파일에서 로드하는 유틸리티
"""

import json
import os
from typing import Dict, List
from pathlib import Path


def get_fabric_categories_file_path() -> str:
    """패브릭 카테고리 JSON 파일 경로 반환"""
    current_dir = Path(__file__).parent.parent
    return os.path.join(current_dir, 'data', 'fabric_categories.json')


def load_fabric_categories() -> Dict:
    """JSON 파일에서 패브릭 카테고리 데이터 로드"""
    file_path = get_fabric_categories_file_path()
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"패브릭 카테고리 파일을 찾을 수 없습니다: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_major_categories_from_json() -> List[Dict[str, str]]:
    """JSON 파일에서 대분류 목록 반환"""
    try:
        categories_data = load_fabric_categories()
        
        return [
            {
                "major_category_code": code,
                "major_category_name": data["name"]
            }
            for code, data in categories_data.items()
        ]
    except Exception as e:
        print(f"대분류 로드 중 오류: {e}")
        return []


def get_minor_categories_from_json(major_category_code: str = None) -> List[Dict[str, str]]:
    """JSON 파일에서 중분류 목록 반환"""
    try:
        categories_data = load_fabric_categories()
        
        if major_category_code and major_category_code != "all":
            # 특정 대분류의 중분류만 반환
            if major_category_code in categories_data:
                minor_categories = categories_data[major_category_code].get('minor_categories', {})
                return [
                    {
                        "minor_category_code": code,
                        "minor_category_name": name
                    }
                    for code, name in minor_categories.items()
                ]
            else:
                return []
        else:
            # 모든 중분류 반환
            all_minor_categories = []
            for major_code, major_data in categories_data.items():
                minor_categories = major_data.get('minor_categories', {})
                for minor_code, minor_name in minor_categories.items():
                    all_minor_categories.append({
                        "minor_category_code": minor_code,
                        "minor_category_name": minor_name
                    })
            
            return all_minor_categories
    except Exception as e:
        print(f"중분류 로드 중 오류: {e}")
        return [] 