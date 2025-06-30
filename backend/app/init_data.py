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
    """표준 카테고리 초기 데이터"""
    categories = [
        # 상의
        {"item_name": "티셔츠", "standard_category": "상의"},
        {"item_name": "셔츠", "standard_category": "상의"},
        {"item_name": "블라우스", "standard_category": "상의"},
        {"item_name": "탑", "standard_category": "상의"},
        {"item_name": "자켓", "standard_category": "상의"},
        {"item_name": "코트", "standard_category": "상의"},
        {"item_name": "가디건", "standard_category": "상의"},
        {"item_name": "스웨터", "standard_category": "상의"},
        {"item_name": "후드", "standard_category": "상의"},
        {"item_name": "후디", "standard_category": "상의"},
        
        # 하의
        {"item_name": "바지", "standard_category": "하의"},
        {"item_name": "팬츠", "standard_category": "하의"},
        {"item_name": "진", "standard_category": "하의"},
        {"item_name": "청바지", "standard_category": "하의"},
        {"item_name": "반바지", "standard_category": "하의"},
        {"item_name": "숏팬츠", "standard_category": "하의"},
        {"item_name": "스커트", "standard_category": "하의"},
        {"item_name": "치마", "standard_category": "하의"},
        {"item_name": "레깅스", "standard_category": "하의"},
        
        # 원피스
        {"item_name": "원피스", "standard_category": "원피스"},
        {"item_name": "드레스", "standard_category": "원피스"},
        {"item_name": "점프수트", "standard_category": "원피스"},
        {"item_name": "올인원", "standard_category": "원피스"},
        
        # 속옷
        {"item_name": "브라", "standard_category": "속옷"},
        {"item_name": "팬티", "standard_category": "속옷"},
        {"item_name": "런닝", "standard_category": "속옷"},
        {"item_name": "속바지", "standard_category": "속옷"},
        {"item_name": "언더웨어", "standard_category": "속옷"},
    ]
    
    for category_data in categories:
        existing = db.query(StandardCategory).filter(
            StandardCategory.item_name == category_data["item_name"]
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