import re
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from ..models.hs_code_rule import HSCodeRule
from ..models.standard_category import StandardCategory
from ..models.fabric_component import FabricComponent

class HSClassificationService:
    def __init__(self, db: Session):
        self.db = db
        
    def validate_template(self, df: pd.DataFrame, template_df: pd.DataFrame) -> Dict[str, Any]:
        """템플릿 양식 검증"""
        errors = []
        
        # 1. 헤더 검증 (첫 번째 행)
        required_headers = ["StyleNo", "제품명", "직조방식", "카테고리", "성별", "상세 성분", "HSCode", "Note"]
        if len(df.columns) < len(required_headers):
            errors.append("템플릿 컬럼 수가 부족합니다.")
        else:
            for i, header in enumerate(required_headers):
                if i < len(df.columns) and df.columns[i] != header:
                    errors.append(f"컬럼명이 일치하지 않습니다: 예상 '{header}', 실제 '{df.columns[i]}'")
        
        # 2. 필수값 검증 (설명 행 제외하고 실제 데이터부터)
        if len(df) <= 1:
            errors.append("데이터가 없습니다.")
        else:
            for idx, row in df.iterrows():
                row_errors = []

                if idx < 1:  # 0번째는 설명 행이므로 스킵
                    continue
                
                # StyleNo 필수
                if pd.isna(row.get('StyleNo')) or str(row.get('StyleNo')).strip() == '':
                    row_errors.append("StyleNo가 누락되었습니다.")
                
                # 직조방식 필수 및 값 검증
                weaving_type = str(row.get('직조방식', '')).strip().lower()
                if not weaving_type or weaving_type not in ['knit', 'woven']:
                    row_errors.append("직조방식은 knit 또는 woven이어야 합니다.")
                
                # 카테고리 필수
                if pd.isna(row.get('카테고리')) or str(row.get('카테고리')).strip() == '':
                    row_errors.append("카테고리가 누락되었습니다.")
                
                # 성별 값 검증 (선택사항이지만 값이 있으면 검증)
                gender = str(row.get('성별', '')).strip().lower()
                if gender and gender not in ['men', 'women', '']:
                    row_errors.append("성별은 men 또는 women이어야 합니다.")
                
                # 상세 성분 필수
                if pd.isna(row.get('상세 성분')) or str(row.get('상세 성분')).strip() == '':
                    row_errors.append("상세 성분이 누락되었습니다.")
                
                if row_errors:
                    errors.append(f"행 {idx + 2}: {', '.join(row_errors)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def find_standard_category(self, category_text: str) -> Optional[str]:
        """카테고리 텍스트에서 표준 카테고리 찾기"""
        if not category_text:
            return None
        
        category_text = category_text.lower().strip()
        
        # 표준 카테고리들과 매칭
        categories = self.db.query(StandardCategory).order_by(StandardCategory.id).all()
        
        for cat in categories:
            # 1. category_name_en과 직접 매칭 확인
            if cat.category_name_en and cat.category_name_en.lower() in category_text:
                return cat.category_name_en.lower()
            
            # 2. keywords와 매칭 확인
            if cat.keywords:
                keywords = cat.keywords.lower().split(',')
                for keyword in keywords:
                    keyword = keyword.strip()
                    if keyword and keyword in category_text:
                        return cat.category_name_en.lower()
        
        return None
    
    def parse_fabric_composition(self, composition_text: str) -> Dict[str, float]:
        """성분 텍스트 파싱하여 성분별 함량 계산"""
        if not composition_text:
            return {}
        
        # 부수적인 파트 제거 (RIB, LINING, ATTACHED 이후 텍스트 제거)
        parts = re.split(r'\b(RIB|LINING|ATTACHED)\b', composition_text, flags=re.IGNORECASE)
        composition_text = parts[0]
        
        # 괄호 안의 라벨 제거 (SHELL), (MAIN) 등
        composition_text = re.sub(r'\([^)]*\)', '', composition_text, flags=re.IGNORECASE)
        
        # SHELL1, SHELL2, MAIN1 등의 라벨 제거 (숫자가 붙은 경우도 포함)
        composition_text = re.sub(r'\b(SHELL|MAIN)\d*\b', '', composition_text, flags=re.IGNORECASE)
        
        # 불필요한 공백 및 개행 정리
        composition_text = re.sub(r'\s+', ' ', composition_text).strip()
        
        fabric_components = {}
        
        # 등록된 성분명들 가져오기
        components = self.db.query(FabricComponent).all()
        component_names = [comp.component_name_en.upper() for comp in components]
        
        # 모든 성분명을 하나의 패턴으로 결합
        if component_names:
            # 성분명들을 길이 순으로 정렬 (긴 것부터, 더 구체적인 매칭 우선)
            sorted_names = sorted(component_names, key=len, reverse=True)
            names_pattern = '|'.join([re.escape(name) for name in sorted_names])
            
            # "숫자% 성분명", "성분명 숫자%", "성분명숫자" 패턴으로 모든 쌍을 찾기
            pattern = rf'(?:(\d+(?:\.\d+)?)\s*%?\s*({names_pattern})|({names_pattern})\s*(\d+(?:\.\d+)?)\s*%?|({names_pattern})(\d+(?:\.\d+)?)\s*%?)'
            matches = re.findall(pattern, composition_text, re.IGNORECASE)
            
            for match in matches:
                # match = (percentage1, component1, component2, percentage2, component3, percentage3)
                if match[0] and match[1]:  # "숫자% 성분명" 형태
                    percentage = float(match[0])
                    component_name = match[1].upper()
                    fabric_components[component_name] = percentage
                elif match[2] and match[3]:  # "성분명 숫자%" 형태
                    percentage = float(match[3])
                    component_name = match[2].upper()
                    fabric_components[component_name] = percentage
                elif match[4] and match[5]:  # "성분명숫자" 형태 (Cotton60, Modal40 등)
                    percentage = float(match[5])
                    component_name = match[4].upper()
                    fabric_components[component_name] = percentage
        
        return fabric_components
    
    def calculate_major_minor_categories(self, fabric_composition: Dict[str, float]) -> Tuple[Optional[str], Optional[str]]:
        """성분 함량을 기반으로 대분류/중분류 계산"""
        if not fabric_composition:
            return None, None
        
        major_totals = {}
        minor_totals = {}
        
        # 등록된 성분들로부터 대분류/중분류 정보 가져오기
        for fabric_name, percentage in fabric_composition.items():
            component = self.db.query(FabricComponent).filter(
                FabricComponent.component_name_en.ilike(fabric_name)
            ).first()
            
            if component:
                # 코드에서 언더스코어 제거하고 소문자로 변환 (예: "MAN_MADE" → "manmade")
                major_cat = component.major_category_code.replace('_', '').lower()
                minor_cat = component.minor_category_code.replace('_', '').lower()
                
                if major_cat not in major_totals:
                    major_totals[major_cat] = 0
                if minor_cat not in minor_totals:
                    minor_totals[minor_cat] = 0
                
                major_totals[major_cat] += percentage
                minor_totals[minor_cat] += percentage
        
        # 가장 높은 함량의 대분류/중분류 선택
        major_category = max(major_totals.items(), key=lambda x: x[1])[0] if major_totals else None
        minor_category = max(minor_totals.items(), key=lambda x: x[1])[0] if minor_totals else None
        
        return major_category, minor_category
    
    def find_hs_code(self, weaving_type: str, standard_category: str, gender: str, 
                     major_category: str, minor_category: str) -> Optional[str]:
        """HS코드 룰에서 해당하는 HS코드 찾기"""
        
        # 성별이 없으면 women으로 기본값 설정
        if not gender:
            gender = "women"
        
        # 1단계: 정확한 매치 시도
        rule = self.db.query(HSCodeRule).filter(
            HSCodeRule.weaving_type == weaving_type.lower(),
            HSCodeRule.standard_category == standard_category.lower(),
            HSCodeRule.gender.in_([gender.lower(), "any"]),
            HSCodeRule.major_category == major_category.lower(),
            HSCodeRule.minor_category == minor_category.lower(),
            HSCodeRule.is_active == True
        ).first()
        
        if rule:
            return rule.hs_code
        
        # 2단계: minor_category를 other로 fallback (예: cotton/cotton → cotton/other)
        rule = self.db.query(HSCodeRule).filter(
            HSCodeRule.weaving_type == weaving_type.lower(),
            HSCodeRule.standard_category == standard_category.lower(),
            HSCodeRule.gender.in_([gender.lower(), "any"]),
            HSCodeRule.major_category == major_category.lower(),
            HSCodeRule.minor_category == "other",
            HSCodeRule.is_active == True
        ).first()
        
        if rule:
            return rule.hs_code
            
        # 3단계: major_category도 other로 fallback (예: cotton/other → other/other)
        rule = self.db.query(HSCodeRule).filter(
            HSCodeRule.weaving_type == weaving_type.lower(),
            HSCodeRule.standard_category == standard_category.lower(),
            HSCodeRule.gender.in_([gender.lower(), "any"]),
            HSCodeRule.major_category == "other",
            HSCodeRule.minor_category == "other",
            HSCodeRule.is_active == True
        ).first()
        
        return rule.hs_code if rule else None
    
    def classify_products(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """제품들의 HS코드 분류"""
        results = []
        
        # 설명 행을 제외하고 실제 데이터부터 처리
        for idx, row in df.iterrows():
            if idx < 1:  # 0번째는 설명 행이므로 스킵
                continue
                
            result = {
                "row_number": idx + 2,  # 실제 엑셀 행 번호 (헤더 1행 + 설명 1행 + 현재 인덱스)
                "style_no": str(row.get('StyleNo', '')),
                "product_name": str(row.get('제품명', '')),
                "weaving_type": str(row.get('직조방식', '')).strip(),
                "category": str(row.get('카테고리', '')),
                "gender": str(row.get('성별', '')).strip(),
                "composition": str(row.get('상세 성분', '')),
                "hs_code": "unknown",
                "note": ""
            }
            
            try:
                # 1. 필수값 검증
                if not result["style_no"]:
                    result["note"] = "필수 정보 누락 (StyleNo)"
                    results.append(result)
                    continue
                
                # 2. 직조방식 검증
                weaving_type = result["weaving_type"].lower()
                if weaving_type not in ['knit', 'woven']:
                    result["note"] = "지원하지 않는 직조 방식"
                    results.append(result)
                    continue
                
                # 3. 카테고리 검증 및 표준 카테고리 찾기
                if not result["category"]:
                    result["note"] = "필수 정보 누락 (카테고리)"
                    results.append(result)
                    continue
                
                standard_category = self.find_standard_category(result["category"])
                if not standard_category:
                    result["note"] = "등록되지 않은 카테고리"
                    results.append(result)
                    continue
                
                # 4. 성별 검증
                gender = result["gender"].lower()
                if gender and gender not in ['men', 'women']:
                    result["note"] = "성별 정보 오류"
                    results.append(result)
                    continue
                
                if not gender:
                    gender = "women"  # 기본값
                
                # 5. 성분 분석
                if not result["composition"]:
                    result["note"] = "필수 정보 누락 (성분)"
                    results.append(result)
                    continue
                
                fabric_composition = self.parse_fabric_composition(result["composition"])
                if not fabric_composition:
                    result["note"] = "등록되지 않은 성분명"
                    results.append(result)
                    continue
                
                major_category, minor_category = self.calculate_major_minor_categories(fabric_composition)
                if not major_category or not minor_category:
                    result["note"] = "등록되지 않은 성분명"
                    results.append(result)
                    continue
                
                # 6. HS코드 찾기
                hs_code = self.find_hs_code(weaving_type, standard_category, gender, 
                                          major_category, minor_category)
                
                if hs_code:
                    result["hs_code"] = hs_code
                    result["note"] = "분류 완료"
                else:
                    result["note"] = "분류 불가 (기타 사유)"
                
            except Exception as e:
                result["note"] = f"처리 중 오류: {str(e)}"
            
            results.append(result)
        
        return results 