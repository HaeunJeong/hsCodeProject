from typing import List, Dict, Any
import pandas as pd
from fastapi import UploadFile
from ..models import Product, Dictionary

class ExcelService:
    @staticmethod
    async def process_excel_file(file: UploadFile) -> List[Dict[str, Any]]:
        """엑셀 파일을 처리하고 데이터를 파싱합니다."""
        df = pd.read_excel(file.file)
        return df.to_dict('records')

    @staticmethod
    async def map_hs_codes(products: List[Dict[str, Any]], db) -> List[Dict[str, Any]]:
        """제품 데이터에 HS 코드를 매핑합니다."""
        # 여기에 HS 코드 매핑 로직 구현
        return products

    @staticmethod
    async def save_products(products: List[Dict[str, Any]], db) -> List[Product]:
        """처리된 제품 데이터를 데이터베이스에 저장합니다."""
        db_products = []
        for product_data in products:
            db_product = Product(**product_data)
            db.add(db_product)
            db_products.append(db_product)
        
        await db.commit()
        for product in db_products:
            await db.refresh(product)
        
        return db_products 