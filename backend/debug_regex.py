#!/usr/bin/env python3
import re

# 테스트 문자열
test_text = "FABRIC COTTON60"

# 패턴 3-2: "공백을 포함한 성분명숫자"
pattern3_2 = r'([A-Za-z][A-Za-z_\-]*(?:\s+[A-Za-z][A-Za-z_\-]*){1,2})(\d+(?:\.\d+)?)'

print(f"테스트 문자열: {test_text}")
print(f"패턴: {pattern3_2}")

matches = re.finditer(pattern3_2, test_text, re.IGNORECASE)
match_found = False

for match in matches:
    match_found = True
    print(f"매칭 발견: {match.group(0)}")
    print(f"그룹 1 (성분명): '{match.group(1)}'")
    print(f"그룹 2 (숫자): '{match.group(2)}'")
    print(f"시작 위치: {match.start()}")
    print(f"끝 위치: {match.end()}")

if not match_found:
    print("❌ 매칭되지 않음")
    
    # 단계별 디버깅
    print("\n=== 단계별 디버깅 ===")
    
    # 1. 첫 번째 단어만
    pattern1 = r'([A-Za-z][A-Za-z0-9_\-]*)'
    matches1 = re.finditer(pattern1, test_text, re.IGNORECASE)
    print(f"1. 첫 번째 단어만: {[m.group(0) for m in matches1]}")
    
    # 2. 공백 + 두 번째 단어
    pattern2 = r'([A-Za-z][A-Za-z0-9_\-]*\s+[A-Za-z][A-Za-z0-9_\-]*)'
    matches2 = re.finditer(pattern2, test_text, re.IGNORECASE)
    print(f"2. 두 단어: {[m.group(0) for m in matches2]}")
    
    # 3. 두 단어 + 숫자
    pattern3 = r'([A-Za-z][A-Za-z0-9_\-]*\s+[A-Za-z][A-Za-z0-9_\-]*)(\d+)'
    matches3 = re.finditer(pattern3, test_text, re.IGNORECASE)
    print(f"3. 두 단어 + 숫자: {[m.groups() for m in matches3]}")
    
    # 4. 원래 패턴을 간단화
    pattern4 = r'([A-Za-z][A-Za-z0-9_\-]*(?:\s+[A-Za-z][A-Za-z0-9_\-]*)+)(\d+)'
    matches4 = re.finditer(pattern4, test_text, re.IGNORECASE)
    print(f"4. 간단화된 패턴: {[m.groups() for m in matches4]}")
    
else:
    print("✅ 매칭 성공") 