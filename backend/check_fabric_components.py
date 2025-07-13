#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.hs_classification_service import HSClassificationService
from app.models.fabric_component import FabricComponent
from app.core.database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def check_fabric_components():
    # 데이터베이스 세션 생성
    db = SessionLocal()
    
    try:
        # 서비스 인스턴스 생성
        service = HSClassificationService(db)
        
        # 등록된 성분명들 확인
        print("=== 등록된 성분명들 ===")
        components = db.query(FabricComponent).all()
        
        print(f"총 {len(components)}개의 성분명이 등록되어 있습니다:\n")
        
        for i, comp in enumerate(components, 1):
            print(f"{i:2d}. {comp.component_name_en} ({comp.component_name_ko})")
        
        # 등록된 성분명 딕셔너리 생성
        registered_components = {comp.component_name_en.upper(): comp.component_name_en for comp in components}
        
        print("\n=== 대문자 변환된 성분명들 ===")
        for upper_name, original_name in registered_components.items():
            print(f"{original_name} -> {upper_name}")
        
        # 문제 케이스들 테스트
        print("\n=== 문제 케이스들 테스트 ===")
        
        test_cases = [
            "fabric silk (very soft)100LINEN26",
            "(SHELL) fabric silk (very soft) 98% POLYURETHANE 2% (LINING) COTTON 100%",
            "fabric cotton100LINEN26",
            "FABRIC COTTON 100%",
            "fabric silk (very soft) 100%",
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n테스트 케이스 {i}: {case}")
            
            try:
                result = service.parse_fabric_composition(case)
                print(f"결과: {result}")
                
                if result:
                    print("✓ 파싱 성공")
                    for component, percentage in result.items():
                        print(f"  - {component}: {percentage}%")
                else:
                    print("✗ 파싱 실패 (빈 결과 - 미등록 성분명 포함)")
                    
            except Exception as e:
                print(f"✗ 예외 발생: {e}")
                import traceback
                traceback.print_exc()
        
        # 특별히 문제가 되는 성분명들 확인
        print("\n=== 특정 성분명 등록 상태 확인 ===")
        
        check_components = [
            "FABRIC SILK (VERY SOFT)",
            "FABRIC SILK",
            "FABRIC COTTON",
            "LINEN",
            "POLYURETHANE",
            "COTTON",
        ]
        
        for component in check_components:
            is_registered = component in registered_components
            print(f"{component}: {'✓ 등록됨' if is_registered else '✗ 미등록'}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_fabric_components() 