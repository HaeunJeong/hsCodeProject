#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.hs_classification_service import HSClassificationService
from app.core.database import get_db
from app.core.config import settings
from sqlalchemy.orm import Session
import pandas as pd

# 데이터베이스 세션 없이 parse_fabric_composition 메서드만 테스트
class MockDB:
    pass

def test_problem_cases():
    # HSClassificationService 인스턴스 생성
    service = HSClassificationService(MockDB())
    
    # 문제 케이스들
    test_cases = [
        "fabric silk (very soft)100LINEN26",
        "(SHELL) fabric silk (very soft) 98% POLYURETHANE 2% (LINING) COTTON 100%",
        "fabric cotton100LINEN26",  # 이전에 작동했던 케이스
        "FABRIC COTTON 100%",  # 기본 케이스
        "fabric silk (very soft) 100%",  # 괄호 케이스
    ]
    
    print("=== 문제 케이스들 디버깅 ===\n")
    
    for i, case in enumerate(test_cases, 1):
        print(f"테스트 케이스 {i}: {case}")
        try:
            result = service.parse_fabric_composition(case)
            print(f"결과: {result}")
            
            # 결과 분석
            if result:
                print("✓ 파싱 성공")
                for component, percentage in result.items():
                    print(f"  - {component}: {percentage}%")
            else:
                print("✗ 파싱 실패 (빈 결과)")
                
        except Exception as e:
            print(f"✗ 예외 발생: {e}")
        
        print("-" * 60)
    
    print("\n=== 성분명 검증 ===")
    
    # 성분명 데이터베이스 확인 (임시로 하드코딩)
    # 실제 데이터베이스에서 가져오는 것은 나중에 확인
    test_components = [
        "FABRIC SILK (VERY SOFT)",
        "FABRIC COTTON",
        "LINEN",
        "POLYURETHANE",
        "COTTON",
        "FABRIC SILK"
    ]
    
    for component in test_components:
        print(f"성분명: {component}")
        # 여기서 실제로 데이터베이스에서 검증하는 로직 추가 필요
        print(f"  - 데이터베이스 검증 필요")
    
if __name__ == "__main__":
    test_problem_cases() 