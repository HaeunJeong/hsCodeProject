#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re
from app.constants.fabric_parsing_constants import (
    get_secondary_parts_pattern,
    get_bracket_labels_pattern,
    get_main_labels_pattern
)

def debug_fabric_composition_parsing():
    # 디버깅할 텍스트
    composition_text = "플록 OUTSHELL: 100% NYLON 지조직 BASE: 100% WOOL LINING: 57% POLYESTER 43% BEMBERG CUPRO"
    
    print(f"=== 원본 텍스트 ===")
    print(f"'{composition_text}'")
    print()
    
    # 1단계: 부수적인 파트 제거
    print(f"=== 1단계: 부수적인 파트 제거 ===")
    secondary_pattern = get_secondary_parts_pattern()
    print(f"Secondary pattern: {secondary_pattern}")
    
    parts = re.split(rf'\b({secondary_pattern})\b', composition_text, flags=re.IGNORECASE)
    print(f"Split 결과: {parts}")
    composition_text = parts[0]
    print(f"1단계 후: '{composition_text}'")
    print()
    
    # 2단계: 괄호 안의 라벨 제거
    print(f"=== 2단계: 괄호 안의 라벨 제거 ===")
    bracket_pattern = get_bracket_labels_pattern()
    print(f"Bracket pattern: {bracket_pattern[:50]}...")
    
    before_bracket = composition_text
    composition_text = re.sub(rf'\b\((?:{bracket_pattern})\d*\)', '', composition_text, flags=re.IGNORECASE)
    print(f"변경 전: '{before_bracket}'")
    print(f"2단계 후: '{composition_text}'")
    print()
    
    # 3단계: 단순 라벨 제거
    print(f"=== 3단계: 단순 라벨 제거 ===")
    main_pattern = get_main_labels_pattern()
    print(f"Main pattern: {main_pattern}")
    
    before_main = composition_text
    composition_text = re.sub(rf'\b({main_pattern})\d*\b', '', composition_text, flags=re.IGNORECASE)
    print(f"변경 전: '{before_main}'")
    print(f"3단계 후: '{composition_text}'")
    print()
    
    # 4단계: 공백 정리
    print(f"=== 4단계: 공백 정리 ===")
    before_space = composition_text
    composition_text = re.sub(r'\s+', ' ', composition_text).strip()
    print(f"변경 전: '{before_space}'")
    print(f"4단계 후: '{composition_text}'")
    print()
    
    # 5단계: 구간 분리 방식
    print(f"=== 5단계: 구간 분리 방식 ===")
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
                print(f"  추출된 성분: '{component}' = {percentage}%")
            
            i += 2
        else:
            i += 1
    
    print(f"구간 분리 결과: {segment_components}")
    print()
    
    # 6단계: 정규식 패턴들 테스트
    print(f"=== 6단계: 정규식 패턴들 테스트 ===")
    
    # 패턴 1: "숫자% 성분명"
    pattern1 = r'(\d+(?:\.\d+)?)\s*%\s+([A-Za-z][A-Za-z0-9_\-\(\)\s]+?)(?=\s*\d|$|\s*[A-Z]+\s*\d)'
    matches1 = list(re.finditer(pattern1, composition_text, re.IGNORECASE))
    print(f"패턴 1 매칭: {[(m.group(), m.group(1), m.group(2)) for m in matches1]}")
    
    # 패턴 2: "성분명 숫자%"
    pattern2 = r'\b([A-Za-z][A-Za-z0-9_\-\(\)\s]+?)\s+(\d+(?:\.\d+)?)\s*%'
    matches2 = list(re.finditer(pattern2, composition_text, re.IGNORECASE))
    print(f"패턴 2 매칭: {[(m.group(), m.group(1), m.group(2)) for m in matches2]}")
    
    # 패턴 3: "성분명숫자" (공백 없이)
    pattern3 = r'\b([A-Za-z][A-Za-z0-9_\-\(\)\s]+?)(\d+(?:\.\d+)?)\b'
    matches3 = list(re.finditer(pattern3, composition_text, re.IGNORECASE))
    print(f"패턴 3 매칭: {[(m.group(), m.group(1), m.group(2)) for m in matches3]}")
    print()
    
    original_text = "플록 OUTSHELL: 100% NYLON 지조직 BASE: 100% WOOL LINING: 57% POLYESTER 43% BEMBERG CUPRO"
    print(f"=== 최종 분석 ===")
    print(f"원본: '{original_text}'")
    print(f"최종 처리된 텍스트: '{composition_text}'")
    print(f"구간 분리로 추출된 성분: {segment_components}")

if __name__ == "__main__":
    debug_fabric_composition_parsing() 