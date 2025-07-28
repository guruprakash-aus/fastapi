from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://fastapi_db:fastapi_db_password@localhost:5472/fastapi_postgres_db"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5472",
            database="fastapi_postgres_db",
            user="fastapi_db",
            password="fastapi_db_password",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Database connection failed")
        print(f"Error: {e}")
        time.sleep(2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()