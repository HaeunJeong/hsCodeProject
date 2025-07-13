#!/usr/bin/env python3
"""
단계별 디버깅
"""

import sys
import os
import re
from unittest.mock import Mock

# backend 경로를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.fabric_component import FabricComponent

def create_test_components():
    """테스트용 성분 데이터 생성"""
    components = []
    
    component1 = FabricComponent()
    component1.component_name_en = "FABRIC COTTON"
    components.append(component1)
    
    component2 = FabricComponent()
    component2.component_name_en = "LINEN"
    components.append(component2)
    
    component3 = FabricComponent()
    component3.component_name_en = "FABRIC SILK"
    components.append(component3)
    
    component4 = FabricComponent()
    component4.component_name_en = "FABRIC SILK (VERY SOFT)"
    components.append(component4)
    
    return components

def debug_parse_fabric_composition(composition_text: str, components):
    """parse_fabric_composition 함수의 단계별 디버깅"""
    print(f"\n=== 디버깅: {composition_text} ===")
    
    if not composition_text:
        print("❌ 빈 텍스트")
        return {}
    
    # 전처리 과정
    print(f"1. 원본 텍스트: '{composition_text}'")
    
    # 부수적인 파트 제거
    parts = re.split(r'\b(RIB|LINING|ATTACHED)\b', composition_text, flags=re.IGNORECASE)
    composition_text = parts[0]
    print(f"2. RIB/LINING/ATTACHED 제거 후: '{composition_text}'")
    
    # 괄호 안의 라벨 제거
    composition_text = re.sub(r'\b\((?:SHELL|MAIN|RIB|LINING|ATTACHED)\d*\)', '', composition_text, flags=re.IGNORECASE)
    print(f"3. 괄호 라벨 제거 후: '{composition_text}'")
    
    # SHELL1, SHELL2, MAIN1 등의 라벨 제거
    composition_text = re.sub(r'\b(SHELL|MAIN)\d*\b', '', composition_text, flags=re.IGNORECASE)
    print(f"4. SHELL/MAIN 라벨 제거 후: '{composition_text}'")
    
    # 불필요한 공백 및 개행 정리
    composition_text = re.sub(r'\s+', ' ', composition_text).strip()
    print(f"5. 공백 정리 후: '{composition_text}'")
    
    # 구간 분리 테스트
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
    print(f"6. 구간 분리 결과: {segments}")
    
    # 성분 추출
    all_matches = []
    i = 0
    segment_start_pos = 0
    while i < len(segments) - 1:
        if segments[i][0] == 'text' and segments[i+1][0] == 'number':
            component = segments[i][1].strip().upper()
            percentage = segments[i+1][1]
            
            if len(component.replace(' ', '').replace('(', '').replace(')', '')) >= 3:
                all_matches.append({
                    'start': segment_start_pos,
                    'end': segment_start_pos + len(component) + len(str(int(percentage))),
                    'component': component,
                    'percentage': percentage,
                    'pattern': 'segment'
                })
                segment_start_pos += len(component) + len(str(int(percentage)))
            
            i += 2
        else:
            i += 1
    
    print(f"7. 추출된 매칭들: {all_matches}")
    
    # 위치별 정렬 (생략하고 바로 성분 추출)
    final_components = {}
    for match in all_matches:
        if match['component'] not in final_components:
            final_components[match['component']] = match['percentage']
    
    print(f"8. 중복 제거 후: {final_components}")
    
    # 등록된 성분명과 매칭
    registered_components_map = {comp.component_name_en.upper(): comp.component_name_en for comp in components}
    registered_component_names = list(registered_components_map.keys())
    print(f"9. 등록된 성분명들: {registered_component_names}")
    
    fabric_components = {}
    for component_name, percentage in final_components.items():
        matched = False
        matched_original_name = None
        
        print(f"10. '{component_name}' 매칭 시도 중...")
        
        if component_name in registered_component_names:
            matched = True
            matched_original_name = registered_components_map[component_name]
            print(f"    ✅ 정확 매칭: '{matched_original_name}'")
        else:
            for registered_name in registered_component_names:
                if registered_name == component_name:
                    matched = True
                    matched_original_name = registered_components_map[registered_name]
                    print(f"    ✅ 매칭 성공: '{matched_original_name}'")
                    break
            
            if not matched:
                print(f"    ❌ 매칭 실패")
        
        if not matched:
            print(f"11. 미등록 성분 발견: '{component_name}' - 분류 중단")
            return {}
        
        fabric_components[matched_original_name] = percentage
    
    print(f"12. 최종 결과: {fabric_components}")
    return fabric_components

# 테스트 실행
components = create_test_components()
test_cases = [
    "fabric cotton100LINEN26",
    "fabric silk100LINEN26", 
    "fabric silk (very soft)100LINEN26"
]

for test_case in test_cases:
    result = debug_parse_fabric_composition(test_case, components)
    print(f"\n🏁 최종 결과: {result}")
    print("=" * 50) 