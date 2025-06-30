import re
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.material_classification import MaterialClassification
from app.models.standard_category import StandardCategory
from app.models.hs_code_rule import HsCodeRule

class HsCodeService:
    def __init__(self, db: Session):
        self.db = db

    def parse_material_detail(self, material_detail: str) -> Dict[str, float]:
        """
        소재 상세 정보를 파싱하여 소재별 함량을 추출
        예: "30% POLYESTER, 20% COTTON, 20% POLYURETHANE, 30% RAYON"
        """
        if not material_detail:
            return {}
        
        materials = {}
        # 정규식으로 "숫자% 소재명" 패턴 추출
        pattern = r'(\d+(?:\.\d+)?)%\s*([A-Za-z\s]+)'
        matches = re.findall(pattern, material_detail.upper())
        
        for percentage, material in matches:
            material = material.strip()
            if material:
                materials[material] = float(percentage)
        
        return materials

    def get_material_classifications(self, materials: Dict[str, float]) -> Tuple[str, str]:
        """
        소재별 함량을 기반으로 주요 소재 대분류와 중분류를 계산
        """
        if not materials:
            return "unknown", "unknown"
        
        # 대분류별, 중분류별 함량 합산
        major_category_sum = {}
        minor_category_sum = {}
        
        for material_name, percentage in materials.items():
            # DB에서 소재 분류 정보 조회
            classification = self.db.query(MaterialClassification).filter(
                MaterialClassification.material_name.ilike(f"%{material_name}%")
            ).first()
            
            if classification:
                # 대분류 합산
                if classification.major_category in major_category_sum:
                    major_category_sum[classification.major_category] += percentage
                else:
                    major_category_sum[classification.major_category] = percentage
                
                # 중분류 합산
                if classification.minor_category in minor_category_sum:
                    minor_category_sum[classification.minor_category] += percentage
                else:
                    minor_category_sum[classification.minor_category] = percentage
        
        # 가장 높은 함량의 대분류, 중분류 선택
        major_category = max(major_category_sum.items(), key=lambda x: x[1])[0] if major_category_sum else "other"
        minor_category = max(minor_category_sum.items(), key=lambda x: x[1])[0] if minor_category_sum else "other"
        
        return major_category, minor_category

    def get_standard_category(self, category: str) -> str:
        """
        카테고리명을 기반으로 표준 카테고리 조회
        """
        if not category:
            return "other"
        
        standard_cat = self.db.query(StandardCategory).filter(
            StandardCategory.item_name.ilike(f"%{category}%")
        ).first()
        
        return standard_cat.standard_category if standard_cat else "other"

    def find_hs_code(self, fabric_type: str, standard_category: str, gender: str, 
                     major_material: str, minor_material: str) -> str:
        """
        조건에 맞는 HS코드 규칙을 찾아 HS코드 반환
        """
        # 성별이 없으면 기본값 women으로 설정
        if not gender or gender.lower() not in ['men', 'women']:
            gender = 'women'
        
        # 직조 방식 검증
        if not fabric_type or fabric_type.lower() not in ['knit', 'woven']:
            return "unknown"
        
        # 우선순위 순으로 규칙 조회
        rules = self.db.query(HsCodeRule).order_by(HsCodeRule.priority.desc()).all()
        
        for rule in rules:
            if self._match_rule(rule, fabric_type.lower(), standard_category, gender.lower(), 
                              major_material, minor_material):
                return rule.hs_code
        
        return "unknown"

    def _match_rule(self, rule: HsCodeRule, fabric_type: str, standard_category: str, 
                    gender: str, major_material: str, minor_material: str) -> bool:
        """
        규칙과 조건이 일치하는지 확인
        """
        # 직조 방식 매칭
        if rule.fabric_type.lower() != fabric_type:
            return False
        
        # 표준 카테고리 매칭
        if rule.standard_category != "any" and rule.standard_category != standard_category:
            return False
        
        # 성별 매칭
        if rule.gender != "any" and rule.gender.lower() != gender:
            return False
        
        # 주요소재 대분류 매칭
        if rule.major_material != "any" and rule.major_material != major_material:
            return False
        
        # 주요소재 중분류 매칭
        if rule.minor_material != "any" and rule.minor_material != minor_material:
            return False
        
        return True

    def map_to_hs_code(self, fabric_type: str, category: str, gender: str, material_detail: str) -> str:
        """
        메인 매핑 함수: 모든 조건을 종합하여 HS코드 반환
        """
        try:
            # 1. 소재 상세 파싱
            materials = self.parse_material_detail(material_detail)
            
            # 2. 주요 소재 대분류, 중분류 계산
            major_material, minor_material = self.get_material_classifications(materials)
            
            # 3. 표준 카테고리 조회
            standard_category = self.get_standard_category(category)
            
            # 4. HS코드 규칙 매칭
            hs_code = self.find_hs_code(fabric_type, standard_category, gender, 
                                      major_material, minor_material)
            
            return hs_code
            
        except Exception as e:
            print(f"HS코드 매핑 중 오류 발생: {e}")
            return "unknown" 