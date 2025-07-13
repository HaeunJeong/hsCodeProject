#!/usr/bin/env python3
"""
복잡한 연결 패턴 디버깅
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
    component1.component_name_en = "FABRIC COTTON"
    component1.major_category_code = "COTTON"
    component1.minor_category_code = "COTTON"
    components.append(component1)
    
    component2 = FabricComponent()
    component2.component_name_en = "LINEN"
    component2.major_category_code = "OTHER"
    component2.minor_category_code = "OTHER"
    components.append(component2)
    
    component3 = FabricComponent()
    component3.component_name_en = "FABRIC SILK"
    component3.major_category_code = "ANIMAL"
    component3.minor_category_code = "SILK"
    components.append(component3)
    
    component4 = FabricComponent()
    component4.component_name_en = "FABRIC SILK (VERY SOFT)"
    component4.major_category_code = "ANIMAL"
    component4.minor_category_code = "SILK"
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

def test_complex_patterns():
    """복잡한 연결 패턴 테스트"""
    print("=== 복잡한 연결 패턴 디버깅 ===")
    
    # 테스트 데이터 생성
    components = create_test_components()
    mock_db = create_mock_db_session(components)
    
    # 서비스 인스턴스 생성
    service = HSClassificationService(mock_db)
    
    # 문제가 되는 테스트 케이스들
    test_cases = [
        "fabric cotton100LINEN26",
        "fabric silk100LINEN26", 
        "fabric silk (very soft)100LINEN26"
    ]
    
    for composition_text in test_cases:
        print(f"\n🔍 디버깅: {composition_text}")
        
        try:
            result = service.parse_fabric_composition(composition_text)
            print(f"최종 파싱 결과: {result}")
            
            if not result:
                print("❌ 빈 결과 - 등록되지 않은 성분명으로 처리됨")
            else:
                print("✅ 파싱 성공")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    
    # 등록된 성분명 목록 출력
    print(f"\n=== 등록된 성분명 목록 ===")
    for comp in components:
        print(f"- {comp.component_name_en}")

if __name__ == "__main__":
    test_complex_patterns() 