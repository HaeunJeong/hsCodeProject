from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.standard_category import StandardCategory
from app.models.fabric_component import FabricComponent



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



def init_fabric_components(db: Session):
    """의류 성분 사전 초기 데이터"""
    # 기본 카테고리 데이터
    base_categories = [
        {"major_code": "COTTON", "major_name": "면(cotton)", "minor_code": "COTTON", "minor_name": "면(cotton)"},
        {"major_code": "COTTON", "major_name": "면(cotton)", "minor_code": "DENIM", "minor_name": "데님(denim)"},
        {"major_code": "SILK", "major_name": "견(silk)", "minor_code": "SILK", "minor_name": "견(silk)"},
        {"major_code": "ANIMAL", "major_name": "동물성 섬유(animal)", "minor_code": "WOOL", "minor_name": "양모(wool)"},
        {"major_code": "ANIMAL", "major_name": "동물성 섬유(animal)", "minor_code": "CASHMERE", "minor_name": "캐시미어(cashmere)"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "SYNTHETIC", "minor_name": "합성 섬유(synthetic)"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)"},
        {"major_code": "OTHER", "major_name": "기타 섬유(other)", "minor_code": "OTHER", "minor_name": "기타 섬유(other)"},
    ]
    
    # 상세 성분 데이터 (이미지 기반)
    components_data = [
        # 면(cotton)
        {"major_code": "COTTON", "major_name": "면(cotton)", "minor_code": "COTTON", "minor_name": "면(cotton)", "en": "cotton", "ko": "면"},
        {"major_code": "COTTON", "major_name": "면(cotton)", "minor_code": "DENIM", "minor_name": "데님(denim)", "en": "denim", "ko": "데님"},
        
        # 견(silk)  
        {"major_code": "SILK", "major_name": "견(silk)", "minor_code": "SILK", "minor_name": "견(silk)", "en": "silk", "ko": "견"},
        
        # 동물성 섬유
        {"major_code": "ANIMAL", "major_name": "동물성 섬유(animal)", "minor_code": "WOOL", "minor_name": "양모(wool)", "en": "wool", "ko": "양모"},
        {"major_code": "ANIMAL", "major_name": "동물성 섬유(animal)", "minor_code": "CASHMERE", "minor_name": "캐시미어(cashmere)", "en": "cashmere", "ko": "캐시미어"},
        
        # 인조 섬유 - 합성 섬유
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "SYNTHETIC", "minor_name": "합성 섬유(synthetic)", "en": "polyamide", "ko": "폴리아마이드"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "SYNTHETIC", "minor_name": "합성 섬유(synthetic)", "en": "acrylic", "ko": "아크릴"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "SYNTHETIC", "minor_name": "합성 섬유(synthetic)", "en": "polyester", "ko": "폴리에스터"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "SYNTHETIC", "minor_name": "합성 섬유(synthetic)", "en": "polyurethane", "ko": "폴리우레탄"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "SYNTHETIC", "minor_name": "합성 섬유(synthetic)", "en": "nylon", "ko": "나일론"},
        
        # 인조 섬유 - 재생 섬유
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "acetate", "ko": "아세테이트"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "viscose", "ko": "비스코스"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "rayon", "ko": "레이온"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "tencel", "ko": "텐셀"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "cupro", "ko": "큐프로"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "cupra", "ko": "큐프라"},
        {"major_code": "MAN_MADE", "major_name": "인조 섬유(man_made)", "minor_code": "ARTIFICIAL", "minor_name": "재생 섬유(artificial)", "en": "modal", "ko": "모달"},
        
        # 기타 섬유
        {"major_code": "OTHER", "major_name": "기타 섬유(other)", "minor_code": "OTHER", "minor_name": "기타 섬유(other)", "en": "linen", "ko": "리넨"},
        {"major_code": "OTHER", "major_name": "기타 섬유(other)", "minor_code": "OTHER", "minor_name": "기타 섬유(other)", "en": "spandex", "ko": "스판덱스"},
        {"major_code": "OTHER", "major_name": "기타 섬유(other)", "minor_code": "OTHER", "minor_name": "기타 섬유(other)", "en": "elite", "ko": "엘리트"},
    ]
    
    for component_data in components_data:
        existing = db.query(FabricComponent).filter(
            FabricComponent.major_category_code == component_data["major_code"],
            FabricComponent.minor_category_code == component_data["minor_code"],
            FabricComponent.component_name_en == component_data["en"]
        ).first()
        
        if not existing:
            component = FabricComponent(
                major_category_code=component_data["major_code"],
                major_category_name=component_data["major_name"],
                minor_category_code=component_data["minor_code"],
                minor_category_name=component_data["minor_name"],
                component_name_en=component_data["en"],
                component_name_ko=component_data["ko"]
            )
            db.add(component)
    
    db.commit()

def initialize_database():
    """데이터베이스 초기화"""
    # 테이블 생성
    print("데이터베이스 테이블 생성...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("표준 카테고리 데이터 초기화...")
        init_standard_categories(db)
        
        print("의류 성분 사전 데이터 초기화...")
        init_fabric_components(db)
        
        print("데이터베이스 초기화 완료!")
        
    except Exception as e:
        print(f"데이터베이스 초기화 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database() 