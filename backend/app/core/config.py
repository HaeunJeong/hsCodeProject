from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Excel Data Management"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "11520"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:3000", "http://localhost:5173"]').strip('[]').replace('"', '').split(',')
    
    # 데이터베이스 설정 - SQLite 사용
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{Path(__file__).parent.parent.parent}/sql_app.db")
    
    # 임시 파일 저장 경로
    TEMP_DIR: str = os.path.join(Path(__file__).parent.parent.parent, "temp")
    
    class Config:
        case_sensitive = True


settings = Settings() 