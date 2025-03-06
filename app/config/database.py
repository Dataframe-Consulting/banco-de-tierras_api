from .settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = settings.DATABASE_URL
if "postgresql" in DATABASE_URL:
    if settings.ENV == "production":
        DATABASE_URL += "?sslmode=require"
    else:
        DATABASE_URL += "?sslmode=disable"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
