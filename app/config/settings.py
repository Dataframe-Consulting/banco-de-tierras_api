import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ENV: str = os.getenv("ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mysecretkey")
    DEBUG: bool = ENV == "development"
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRATION", 30))

settings = Settings()

# TESTING ENV