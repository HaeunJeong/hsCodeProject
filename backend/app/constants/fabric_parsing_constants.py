"""
패브릭 성분 파싱에 사용되는 상수들
"""

# 겉감정보
MAIN_LABELS = [
    "SHELL",
    "MAIN",
    "EXTERIOR",
    "TOP", 
    "BOTTOM",
    "OUTSHELL",
    "FACE",
    "BACK"
]

# 부수적인 파트 제거에 사용되는 키워드들
SECONDARY_PARTS = [
    "RIB",
    "LINING", 
    "ATTACHED",
    "INTERIOR",
    "COMPONENT",
    "TRIM",
    "FILL",
    "FILLING",
    "FILLER",
    "DETACHABLE COLLAR",
    "COLLAR",
    "DETACHABLE COLLAR LINING",
    "MESH",
    "CONTRAST",
    "BASE",
    "MEFFLER",
    "YARN"
]

# 정규식 패턴용 문자열 생성 함수들
def get_bracket_labels_pattern():
    """괄호 라벨 제거용 패턴 반환 (MAIN_LABELS + SECONDARY_PARTS)"""
    all_labels = MAIN_LABELS + SECONDARY_PARTS
    return "|".join(all_labels)

def get_main_labels_pattern():
    """단순 라벨 제거용 패턴 반환"""
    return "|".join(MAIN_LABELS) 

def get_secondary_parts_pattern():
    """부수적인 파트 제거용 패턴 반환"""
    return "|".join(SECONDARY_PARTS)