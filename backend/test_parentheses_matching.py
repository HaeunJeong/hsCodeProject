#!/usr/bin/env python3
"""
괄호가 포함된 성분명 매칭 테스트
"""

import sys
import os
from unittest.mock import Mock

# backend 경로를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.hs_classification_service import HSClassificationService
from app.models.fabric_component import FabricComponent

def create_test_components():
    """테스트용 성분 데이터 생성"""
    components = []
    
    # 기존 성분들
    component1 = FabricComponent()
    component1.component_name_en = "COTTON"
    component1.major_category_code = "COTTON"
    component1.minor_category_code = "COTTON"
    components.append(component1)
    
    component2 = FabricComponent()
    component2.component_name_en = "POLYESTER"
    component2.major_category_code = "MAN_MADE"
    component2.minor_category_code = "SYNTHETIC"
    components.append(component2)
    
    # 괄호가 포함된 성분들
    component3 = FabricComponent()
    component3.component_name_en = "FABRIC SILK (VERY SOFT)"
    component3.major_category_code = "ANIMAL"
    component3.minor_category_code = "SILK"
    components.append(component3)
    
    component4 = FabricComponent()
    component4.component_name_en = "COTTON (ORGANIC)"
    component4.major_category_code = "COTTON"
    component4.minor_category_code = "COTTON"
    components.append(component4)
    
    return components

def create_mock_db_session(components):
    """Mock DB 세션 생성"""
    mock_db = Mock()
    
    def mock_query(model_class):
        mock_query_obj = Mock()
        if model_class == FabricComponent:
            mock_query_obj.all.return_value = components
        return mock_query_obj
    
    mock_db.query.side_effect = mock_query
    return mock_db

def test_parentheses_matching():
    """괄호가 포함된 성분명 매칭 테스트"""
    print("=== 괄호가 포함된 성분명 매칭 테스트 ===")
    
    # 테스트 데이터 생성
    components = create_test_components()
    mock_db = create_mock_db_session(components)
    
    # 서비스 인스턴스 생성
    service = HSClassificationService(mock_db)
    
    # 테스트 케이스들
    test_cases = [
        {
            "name": "기존 성분 (괄호 없음)",
            "composition": "COTTON 100%",
            "expected_success": True,
            "expected_components": ["COTTON"]
        },
        {
            "name": "괄호 포함 성분 - 패턴 2",
            "composition": "FABRIC SILK (VERY SOFT) 100%",
            "expected_success": True,
            "expected_components": ["FABRIC SILK (VERY SOFT)"]
        },
        {
            "name": "괄호 포함 성분 - 패턴 1",
            "composition": "100% FABRIC SILK (VERY SOFT)",
            "expected_success": True,
            "expected_components": ["FABRIC SILK (VERY SOFT)"]
        },
        {
            "name": "괄호 포함 성분 - 소문자",
            "composition": "fabric silk (very soft) 100%",
            "expected_success": True,
            "expected_components": ["FABRIC SILK (VERY SOFT)"]
        },
        {
            "name": "괄호 포함 성분 - 혼합",
            "composition": "COTTON (ORGANIC) 50% POLYESTER 50%",
            "expected_success": True,
            "expected_components": ["COTTON (ORGANIC)", "POLYESTER"]
        },
        {
            "name": "괄호 포함 미등록 성분",
            "composition": "UNKNOWN FABRIC (SOFT) 100%",
            "expected_success": False,
            "expected_components": []
        }
    ]
    
    # 테스트 실행
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        print(f"\n🧪 테스트: {test_case['name']}")
        print(f"입력: {test_case['composition']}")
        
        try:
            result = service.parse_fabric_composition(test_case['composition'])
            print(f"파싱 결과: {result}")
            
            success = len(result) > 0
            
            if success == test_case['expected_success']:
                if success:
                    # 성공한 경우, 예상 성분명들이 포함되어 있는지 확인
                    result_components = list(result.keys())
                    expected_components = test_case['expected_components']
                    
                    if all(comp in result_components for comp in expected_components):
                        print("✅ 통과 - 예상 성분명 모두 포함")
                        passed += 1
                    else:
                        print(f"❌ 실패 - 예상 성분명 불일치")
                        print(f"   기대: {expected_components}")
                        print(f"   실제: {result_components}")
                        failed += 1
                else:
                    # 실패한 경우
                    print("✅ 통과 - 예상대로 실패")
                    passed += 1
            else:
                print(f"❌ 실패 - 예상과 다른 결과")
                print(f"   기대 성공: {test_case['expected_success']}")
                print(f"   실제 성공: {success}")
                failed += 1
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            failed += 1
    
    print(f"\n=== 테스트 결과 ===")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")
    print(f"성공률: {passed / (passed + failed) * 100:.1f}%")
    
    # 등록된 성분명 목록 출력
    print(f"\n=== 등록된 성분명 목록 ===")
    for comp in components:
        print(f"- {comp.component_name_en}")

if __name__ == "__main__":
    test_parentheses_matching() 