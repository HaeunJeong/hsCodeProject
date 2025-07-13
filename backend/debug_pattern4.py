#!/usr/bin/env python3
import re

test_strings = [
    "fabric cotton100LINEN26",
    "fabric silk100LINEN26", 
    "fabric silk (very soft)100LINEN26"
]

# 현재 패턴
pattern4 = r'([A-Za-z]+(?:\s+[A-Za-z]+)*(?:\s*\([^)]*\))?)(\d+)([A-Za-z]+(?:\s+[A-Za-z]+)*)(\d+)'

print("=== 패턴 4 디버깅 ===")
print(f"패턴: {pattern4}")

for test_string in test_strings:
    print(f"\n테스트 문자열: {test_string}")
    
    matches = re.finditer(pattern4, test_string)
    match_found = False
    
    for match in matches:
        match_found = True
        print(f"✅ 매칭 발견: {match.group(0)}")
        print(f"  그룹 1 (첫 번째 성분): '{match.group(1)}'")
        print(f"  그룹 2 (첫 번째 비율): '{match.group(2)}'")
        print(f"  그룹 3 (두 번째 성분): '{match.group(3)}'")
        print(f"  그룹 4 (두 번째 비율): '{match.group(4)}'")
    
    if not match_found:
        print("❌ 매칭되지 않음")
        
        # 단계별 디버깅
        print("  단계별 테스트:")
        
        # 1. 첫 번째 성분명만
        pattern1 = r'([A-Za-z]+(?:\s+[A-Za-z]+)*(?:\s*\([^)]*\))?)'
        match1 = re.search(pattern1, test_string)
        if match1:
            print(f"    1단계 (첫 번째 성분): '{match1.group(1)}'")
        else:
            print("    1단계: 매칭 실패")
        
        # 2. 성분명 + 숫자
        pattern2 = r'([A-Za-z]+(?:\s+[A-Za-z]+)*(?:\s*\([^)]*\))?)(\d+)'
        match2 = re.search(pattern2, test_string)
        if match2:
            print(f"    2단계 (첫 번째 성분+비율): '{match2.group(1)}' + '{match2.group(2)}'")
        else:
            print("    2단계: 매칭 실패")
        
        # 3. 전체 패턴을 non-greedy로
        pattern3 = r'([A-Za-z]+(?:\s+[A-Za-z]+)*?(?:\s*\([^)]*\))?)(\d+)([A-Za-z]+(?:\s+[A-Za-z]+)*)(\d+)'
        match3 = re.search(pattern3, test_string)
        if match3:
            print(f"    3단계 (non-greedy): 성공")
            print(f"      그룹 1: '{match3.group(1)}'")
            print(f"      그룹 2: '{match3.group(2)}'")
            print(f"      그룹 3: '{match3.group(3)}'")
            print(f"      그룹 4: '{match3.group(4)}'")
        else:
            print("    3단계: 매칭 실패")
        
        # 4. 더 간단한 패턴
        pattern4_simple = r'([A-Za-z\s\(\)]+?)(\d+)([A-Za-z]+)(\d+)'
        match4 = re.search(pattern4_simple, test_string)
        if match4:
            print(f"    4단계 (간단): 성공")
            print(f"      그룹 1: '{match4.group(1)}'")
            print(f"      그룹 2: '{match4.group(2)}'")
            print(f"      그룹 3: '{match4.group(3)}'")
            print(f"      그룹 4: '{match4.group(4)}'")
        else:
            print("    4단계: 매칭 실패") 