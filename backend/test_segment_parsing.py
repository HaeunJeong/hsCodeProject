#!/usr/bin/env python3
"""
구간 분리 방식 테스트
"""

def parse_text_number_segments(text):
    """텍스트를 문자 구간과 숫자 구간으로 순차 분리"""
    segments = []
    i = 0
    
    while i < len(text):
        # 문자 구간 찾기 (영문자, 공백, 괄호 포함)
        if text[i].isalpha():
            start = i
            while i < len(text) and (text[i].isalpha() or text[i].isspace() or text[i] in '()'):
                i += 1
            component = text[start:i].strip()
            if component:
                segments.append(('text', component))
        
        # 숫자 구간 찾기
        elif text[i].isdigit():
            start = i
            while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                i += 1
            number = text[start:i]
            if number:
                segments.append(('number', float(number)))
        
        else:
            i += 1  # 다른 문자는 건너뛰기
    
    return segments

def extract_components(text):
    """(문자, 숫자) 쌍으로 구성된 성분들 추출"""
    segments = parse_text_number_segments(text)
    components = []
    
    i = 0
    while i < len(segments) - 1:
        if segments[i][0] == 'text' and segments[i+1][0] == 'number':
            component = segments[i][1].strip().upper()
            percentage = segments[i+1][1]
            
            # 성분명이 유효한 경우만 추가
            if len(component.replace(' ', '').replace('(', '').replace(')', '')) >= 3:
                components.append((component, percentage))
            
            i += 2  # 다음 (문자, 숫자) 쌍으로
        else:
            i += 1
    
    return components

# 테스트 케이스
test_cases = [
    "fabric cotton100LINEN26",
    "fabric silk100LINEN26", 
    "fabric silk (very soft)100LINEN26",
    "COTTON 50% POLYESTER 50%",  # 기존 케이스도 테스트
    "100% COTTON"  # 기존 케이스도 테스트
]

print("=== 구간 분리 방식 테스트 ===")

for test_case in test_cases:
    print(f"\n📝 테스트: {test_case}")
    
    # 1. 구간 분리 결과
    segments = parse_text_number_segments(test_case)
    print(f"구간 분리: {segments}")
    
    # 2. 성분 추출 결과
    components = extract_components(test_case)
    print(f"성분 추출: {components}")
    
    # 3. 결과를 딕셔너리로 변환
    result_dict = {comp: perc for comp, perc in components}
    print(f"최종 결과: {result_dict}") 