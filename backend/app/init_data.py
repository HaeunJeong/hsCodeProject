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
            {
                "category_code": "CAT001",
                "category_name_en": "accessories",
                "category_name_ko": "부속품",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT002",
                "category_name_en": "active_outer",
                "category_name_ko": "기능성 아우터",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT003",
                "category_name_en": "classic_outer",
                "category_name_ko": "클래식 아우터",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT004",
                "category_name_en": "babies_accessories",
                "category_name_ko": "유아용 부속품",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT005",
                "category_name_en": "babies_garments",
                "category_name_ko": "유아용 의류",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT006",
                "category_name_en": "underwear_accessory",
                "category_name_ko": "속옷 부속품",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT007",
                "category_name_en": "brassieres",
                "category_name_ko": "브레지어",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT008",
                "category_name_en": "underpants",
                "category_name_ko": "속옷 하의",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT009",
                "category_name_en": "compression_hosiery",
                "category_name_ko": "압박 스타킹",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT010",
                "category_name_en": "corselette",
                "category_name_ko": "코르슬렛",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT011",
                "category_name_en": "dresses",
                "category_name_ko": "드레스",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT012",
                "category_name_en": "ensembles",
                "category_name_ko": "앙상블",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT013",
                "category_name_en": "girdles",
                "category_name_ko": "거들",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT014",
                "category_name_en": "gloves",
                "category_name_ko": "장갑",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT015",
                "category_name_en": "handkerchiefs",
                "category_name_ko": "손수건",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT016",
                "category_name_en": "jackets",
                "category_name_ko": "재킷",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT017",
                "category_name_en": "knit_layer",
                "category_name_ko": "니트 레이어류",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT018",
                "category_name_en": "robe",
                "category_name_ko": "실내용 가운",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT019",
                "category_name_en": "sleepwear",
                "category_name_ko": "잠옷",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT020",
                "category_name_en": "pantyhose",
                "category_name_ko": "팬티스타킹",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT021",
                "category_name_en": "parts",
                "category_name_ko": "부분품",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT022",
                "category_name_en": "wrap_accessory",
                "category_name_ko": "스카프/숄",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT023",
                "category_name_en": "shirt_top",
                "category_name_ko": "셔츠/블라우스",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT024",
                "category_name_en": "singlet",
                "category_name_ko": "민소매 이너",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT025",
                "category_name_en": "ski_suits",
                "category_name_ko": "스키슈트",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT026",
                "category_name_en": "skirts",
                "category_name_ko": "스커트",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT027",
                "category_name_en": "slipwear",
                "category_name_ko": "슬립/속치마",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT028",
                "category_name_en": "sports_uniforms",
                "category_name_ko": "무술복",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT029",
                "category_name_en": "legwear",
                "category_name_ko": "양말류",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT030",
                "category_name_en": "suits",
                "category_name_ko": "슈트",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT031",
                "category_name_en": "swimwear",
                "category_name_ko": "수영복",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT032",
                "category_name_en": "ties",
                "category_name_ko": "넥타이",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT033",
                "category_name_en": "hosiery",
                "category_name_ko": "스타킹류",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT034",
                "category_name_en": "track_suits",
                "category_name_ko": "트랙슈트",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT035",
                "category_name_en": "bottoms",
                "category_name_ko": "하의",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT036",
                "category_name_en": "tshirts",
                "category_name_ko": "티셔츠",
                "description": "",
                "keywords": ""
            },
            {
                "category_code": "CAT037",
                "category_name_en": "working_gloves",
                "category_name_ko": "작업용 장갑",
                "description": "",
                "keywords": ""
            }
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