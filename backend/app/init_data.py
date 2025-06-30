from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.material_classification import MaterialClassification
from app.models.standard_category import StandardCategory
from app.models.hs_code_rule import HsCodeRule

def init_material_classifications(db: Session):
    """소재 분류 초기 데이터"""
    materials = [
        # 인조섬유 - 합성섬유
        {"material_name": "POLYESTER", "major_category": "인조섬유", "minor_category": "합성섬유"},
        {"material_name": "NYLON", "major_category": "인조섬유", "minor_category": "합성섬유"},
        {"material_name": "ACRYLIC", "major_category": "인조섬유", "minor_category": "합성섬유"},
        {"material_name": "POLYURETHANE", "major_category": "인조섬유", "minor_category": "합성섬유"},
        {"material_name": "SPANDEX", "major_category": "인조섬유", "minor_category": "합성섬유"},
        {"material_name": "ELASTANE", "major_category": "인조섬유", "minor_category": "합성섬유"},
        
        # 인조섬유 - 재생섬유
        {"material_name": "RAYON", "major_category": "인조섬유", "minor_category": "재생섬유"},
        {"material_name": "VISCOSE", "major_category": "인조섬유", "minor_category": "재생섬유"},
        {"material_name": "MODAL", "major_category": "인조섬유", "minor_category": "재생섬유"},
        {"material_name": "LYOCELL", "major_category": "인조섬유", "minor_category": "재생섬유"},
        {"material_name": "TENCEL", "major_category": "인조섬유", "minor_category": "재생섬유"},
        
        # 천연섬유 - 면
        {"material_name": "COTTON", "major_category": "천연섬유", "minor_category": "면"},
        {"material_name": "ORGANIC COTTON", "major_category": "천연섬유", "minor_category": "면"},
        
        # 천연섬유 - 울
        {"material_name": "WOOL", "major_category": "천연섬유", "minor_category": "울"},
        {"material_name": "MERINO WOOL", "major_category": "천연섬유", "minor_category": "울"},
        {"material_name": "CASHMERE", "major_category": "천연섬유", "minor_category": "울"},
        {"material_name": "ALPACA", "major_category": "천연섬유", "minor_category": "울"},
        
        # 천연섬유 - 실크
        {"material_name": "SILK", "major_category": "천연섬유", "minor_category": "실크"},
        
        # 천연섬유 - 마
        {"material_name": "LINEN", "major_category": "천연섬유", "minor_category": "마"},
        {"material_name": "HEMP", "major_category": "천연섬유", "minor_category": "마"},
    ]
    
    for material_data in materials:
        existing = db.query(MaterialClassification).filter(
            MaterialClassification.material_name == material_data["material_name"]
        ).first()
        
        if not existing:
            material = MaterialClassification(**material_data)
            db.add(material)
    
    db.commit()

def init_standard_categories(db: Session):
    """표준 카테고리 초기 데이터 - 엑셀 파일 기반 37개 카테고리"""
    categories = [
        {"category_code": "CAT001", "category_name_en": "accessories", "category_name_ko": "액세서리", "description": "accessories", "keywords": "액세서리, ACC"},
        {"category_code": "CAT002", "category_name_en": "active_top", "category_name_ko": "활성 상의", "description": "active, top, sports, athletic, workout, exercise", "keywords": "활동적 상의"},
        {"category_code": "CAT003", "category_name_en": "active_wear", "category_name_ko": "활성복", "description": "activewear, sportswear, athletic_wear, workout_clothes", "keywords": "활동복"},
        {"category_code": "CAT004", "category_name_en": "babies_accessories", "category_name_ko": "유아 액세서리", "description": "babies_accessories", "keywords": "유아용 액세서리"},
        {"category_code": "CAT005", "category_name_en": "babies_garments", "category_name_ko": "유아복", "description": "babies_garments", "keywords": "유아용 의류"},
        {"category_code": "CAT006", "category_name_en": "underwear_accessory", "category_name_ko": "속옷 액세서리", "description": "bras, suspender, garter", "keywords": "속옷 관련 액세서리"},
        {"category_code": "CAT007", "category_name_en": "brasseries", "category_name_ko": "브래지어", "description": "brasseries", "keywords": "브래지어"},
        {"category_code": "CAT008", "category_name_en": "cardigans", "category_name_ko": "가디건", "description": "cardigan, knitwear, pullover", "keywords": "가디건, 카디건"},
        {"category_code": "CAT009", "category_name_en": "compression_hosiery", "category_name_ko": "압축 스타킹", "description": "compression_hosiery", "keywords": "압축 스타킹"},
        {"category_code": "CAT010", "category_name_en": "corsetrie", "category_name_ko": "코르셋", "description": "corsetrie", "keywords": "코르셋"},
        {"category_code": "CAT011", "category_name_en": "dresses", "category_name_ko": "드레스", "description": "dresses", "keywords": "드레스"},
        {"category_code": "CAT012", "category_name_en": "ensembles", "category_name_ko": "앙상블", "description": "ensembles", "keywords": "앙상블"},
        {"category_code": "CAT013", "category_name_en": "garments", "category_name_ko": "의류", "description": "garments, clothing, apparel", "keywords": "일반 의류"},
        {"category_code": "CAT014", "category_name_en": "gloves", "category_name_ko": "장갑", "description": "gloves", "keywords": "장갑"},
        {"category_code": "CAT015", "category_name_en": "handkerchiefs", "category_name_ko": "손수건", "description": "handkerchiefs", "keywords": "손수건"},
        {"category_code": "CAT016", "category_name_en": "jackets", "category_name_ko": "재킷", "description": "jackets, blazers", "keywords": "재킷"},
        {"category_code": "CAT017", "category_name_en": "knit_layer", "category_name_ko": "니트 레이어", "description": "jersey, pullover, cardigan, waistcoat", "keywords": "니트 레이어드 의류"},
        {"category_code": "CAT018", "category_name_en": "knitwear", "category_name_ko": "니트웨어", "description": "knitwear, knitted, sweater, jumper", "keywords": "니트웨어, 편직물"},
        {"category_code": "CAT019", "category_name_en": "sleepwear", "category_name_ko": "잠옷", "description": "nightdresses, nightshirts, pyjamas", "keywords": "잠옷"},
        {"category_code": "CAT020", "category_name_en": "pantyhose", "category_name_ko": "팬티스타킹", "description": "panty, hose, tights", "keywords": "팬티스타킹"},
        {"category_code": "CAT021", "category_name_en": "pants", "category_name_ko": "바지", "description": "pants", "keywords": "바지류"},
        {"category_code": "CAT022", "category_name_en": "wrap_accessory", "category_name_ko": "스카프 액세서리", "description": "shawl, scarves, mufflers, mantillas, veils", "keywords": "스카프 등 감싸는 액세서리"},
        {"category_code": "CAT023", "category_name_en": "shirt_top", "category_name_ko": "셔츠 상의", "description": "shirts, blouses", "keywords": "셔츠 상의"},
        {"category_code": "CAT024", "category_name_en": "shorts", "category_name_ko": "반바지", "description": "shorts, vest", "keywords": "반바지"},
        {"category_code": "CAT025", "category_name_en": "ski_suits", "category_name_ko": "스키복", "description": "ski_suits", "keywords": "스키복"},
        {"category_code": "CAT026", "category_name_en": "skirts", "category_name_ko": "스커트", "description": "skirts", "keywords": "스커트"},
        {"category_code": "CAT027", "category_name_en": "sleepwear", "category_name_ko": "잠옷", "description": "slips, petticoats", "keywords": "잠옷, 페티코트"},
        {"category_code": "CAT028", "category_name_en": "sports_uniforms", "category_name_ko": "스포츠 유니폼", "description": "sports_uniforms", "keywords": "스포츠 유니폼"}
    ]
    
    for category_data in categories:
        existing = db.query(StandardCategory).filter(
            StandardCategory.category_code == category_data["category_code"]
        ).first()
        
        if not existing:
            category = StandardCategory(**category_data)
            db.add(category)
    
    db.commit()

def init_hs_code_rules(db: Session):
    """HS코드 규칙 초기 데이터"""
    rules = [
        # knit 상의 규칙
        {"fabric_type": "knit", "standard_category": "상의", "gender": "men", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6109.10.0000", "priority": 10},
        {"fabric_type": "knit", "standard_category": "상의", "gender": "women", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6109.90.0000", "priority": 10},
        {"fabric_type": "knit", "standard_category": "상의", "gender": "any", "major_material": "인조섬유", "minor_material": "합성섬유", "hs_code": "6110.20.0000", "priority": 8},
        {"fabric_type": "knit", "standard_category": "상의", "gender": "any", "major_material": "인조섬유", "minor_material": "재생섬유", "hs_code": "6110.30.0000", "priority": 8},
        {"fabric_type": "knit", "standard_category": "상의", "gender": "any", "major_material": "천연섬유", "minor_material": "울", "hs_code": "6110.11.0000", "priority": 9},
        
        # woven 상의 규칙
        {"fabric_type": "woven", "standard_category": "상의", "gender": "men", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6205.20.0000", "priority": 10},
        {"fabric_type": "woven", "standard_category": "상의", "gender": "women", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6206.30.0000", "priority": 10},
        {"fabric_type": "woven", "standard_category": "상의", "gender": "any", "major_material": "인조섬유", "minor_material": "합성섬유", "hs_code": "6205.30.0000", "priority": 8},
        {"fabric_type": "woven", "standard_category": "상의", "gender": "any", "major_material": "천연섬유", "minor_material": "울", "hs_code": "6205.10.0000", "priority": 9},
        
        # knit 하의 규칙
        {"fabric_type": "knit", "standard_category": "하의", "gender": "men", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6107.11.0000", "priority": 10},
        {"fabric_type": "knit", "standard_category": "하의", "gender": "women", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6108.21.0000", "priority": 10},
        {"fabric_type": "knit", "standard_category": "하의", "gender": "any", "major_material": "인조섬유", "minor_material": "합성섬유", "hs_code": "6107.12.0000", "priority": 8},
        
        # woven 하의 규칙
        {"fabric_type": "woven", "standard_category": "하의", "gender": "men", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6203.42.0000", "priority": 10},
        {"fabric_type": "woven", "standard_category": "하의", "gender": "women", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6204.62.0000", "priority": 10},
        {"fabric_type": "woven", "standard_category": "하의", "gender": "any", "major_material": "인조섬유", "minor_material": "합성섬유", "hs_code": "6203.43.0000", "priority": 8},
        
        # 원피스 규칙
        {"fabric_type": "knit", "standard_category": "원피스", "gender": "women", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6104.42.0000", "priority": 10},
        {"fabric_type": "woven", "standard_category": "원피스", "gender": "women", "major_material": "천연섬유", "minor_material": "면", "hs_code": "6204.42.0000", "priority": 10},
        
        # 기본 규칙 (우선순위 낮음)
        {"fabric_type": "knit", "standard_category": "other", "gender": "any", "major_material": "other", "minor_material": "other", "hs_code": "6117.90.0000", "priority": 1},
        {"fabric_type": "woven", "standard_category": "other", "gender": "any", "major_material": "other", "minor_material": "other", "hs_code": "6217.90.0000", "priority": 1},
    ]
    
    for rule_data in rules:
        existing = db.query(HsCodeRule).filter(
            HsCodeRule.fabric_type == rule_data["fabric_type"],
            HsCodeRule.standard_category == rule_data["standard_category"],
            HsCodeRule.gender == rule_data["gender"],
            HsCodeRule.major_material == rule_data["major_material"],
            HsCodeRule.minor_material == rule_data["minor_material"]
        ).first()
        
        if not existing:
            rule = HsCodeRule(**rule_data)
            db.add(rule)
    
    db.commit()

def initialize_database():
    """데이터베이스 초기화"""
    # 테이블 생성
    print("데이터베이스 테이블 생성...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("소재 분류 데이터 초기화...")
        init_material_classifications(db)
        
        print("표준 카테고리 데이터 초기화...")
        init_standard_categories(db)
        
        print("HS코드 규칙 데이터 초기화...")
        init_hs_code_rules(db)
        
        print("데이터베이스 초기화 완료!")
        
    except Exception as e:
        print(f"데이터베이스 초기화 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database() 