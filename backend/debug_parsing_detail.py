#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.hs_classification_service import HSClassificationService
from app.models.fabric_component import FabricComponent
from app.core.database import SessionLocal
import re

def debug_parsing_detail():
    # 데이터베이스 세션 생성
    db = SessionLocal()
    
    try:
        # 서비스 인스턴스 생성
        service = HSClassificationService(db)
        
        # 등록된 성분명들 확인
        components = db.query(FabricComponent).all()
        registered_components = {comp.component_name_en.upper(): comp.component_name_en for comp in components}
        
        print("=== 등록된 성분명들 (대문자 변환) ===")
        for upper_name, original_name in registered_components.items():
            print(f"{original_name} -> {upper_name}")
        
        # 문제 케이스들에 대해 상세 디버깅
        test_cases = [
            "fabric silk (very soft)100LINEN26",
            "(SHELL) fabric silk (very soft) 98% POLYURETHANE 2% (LINING) COTTON 100%",
            "fabric silk (very soft) 100%",
        ]
        
        for case in test_cases:
            print(f"\n=== 테스트 케이스: {case} ===")
            
            # 파싱 함수의 일부를 복사하여 중간 결과 확인
            composition_text = case
            
            # 1. 전처리 과정
            parts = re.split(r'\b(RIB|LINING|ATTACHED)\b', composition_text, flags=re.IGNORECASE)
            composition_text = parts[0]
            print(f"1. 부수적 파트 제거 후: {composition_text}")
            
            # 괄호 안의 라벨 제거
            composition_text = re.sub(r'\b\((?:SHELL|MAIN|RIB|LINING|ATTACHED)\d*\)', '', composition_text, flags=re.IGNORECASE)
            print(f"2. 괄호 라벨 제거 후: {composition_text}")
            
            # SHELL1, SHELL2, MAIN1 등의 라벨 제거
            composition_text = re.sub(r'\b(SHELL|MAIN)\d*\b', '', composition_text, flags=re.IGNORECASE)
            print(f"3. SHELL/MAIN 라벨 제거 후: {composition_text}")
            
            # 불필요한 공백 및 개행 정리
            composition_text = re.sub(r'\s+', ' ', composition_text).strip()
            print(f"4. 공백 정리 후: {composition_text}")
            
            # 2. 구간 분리 방식 테스트
            print(f"\n--- 구간 분리 방식 ---")
            def parse_text_number_segments(text):
                segments = []
                i = 0
                
                while i < len(text):
                    if text[i].isalpha():
                        start = i
                        while i < len(text) and (text[i].isalpha() or text[i].isspace() or text[i] in '()'):
                            i += 1
                        component = text[start:i].strip()
                        if component:
                            segments.append(('text', component))
                    
                    elif text[i].isdigit():
                        start = i
                        while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                            i += 1
                        number = text[start:i]
                        if number:
                            segments.append(('number', float(number)))
                    
                    else:
                        i += 1
                
                return segments
            
            segments = parse_text_number_segments(composition_text)
            print(f"추출된 구간들: {segments}")
            
            # (문자, 숫자) 쌍으로 구성된 성분들 추출
            segment_components = {}
            i = 0
            while i < len(segments) - 1:
                if segments[i][0] == 'text' and segments[i+1][0] == 'number':
                    component = segments[i][1].strip().upper()
                    percentage = segments[i+1][1]
                    
                    if len(component.replace(' ', '').replace('(', '').replace(')', '')) >= 3:
                        segment_components[component] = percentage
                        print(f"  추출된 성분: {component} = {percentage}%")
                    
                    i += 2
                else:
                    i += 1
            
            print(f"구간 분리 결과: {segment_components}")
            
            # 3. 등록 여부 확인
            print(f"\n--- 등록 여부 확인 ---")
            for component in segment_components.keys():
                is_registered = component in registered_components
                print(f"{component}: {'✓ 등록됨' if is_registered else '✗ 미등록'}")
                
                if not is_registered:
                    # 유사한 등록된 성분명 찾기
                    similar = []
                    for reg_comp in registered_components.keys():
                        if component.replace(' ', '') == reg_comp.replace(' ', ''):
                            similar.append(reg_comp)
                    
                    if similar:
                        print(f"  유사한 등록된 성분명: {similar}")
            
            # 4. 최종 결과
            print(f"\n--- 최종 결과 ---")
            result = service.parse_fabric_composition(case)
            print(f"parse_fabric_composition 결과: {result}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_parsing_detail() 