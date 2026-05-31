import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# Получение параметров подключения из переменных окружения
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bookstore")

# Строка подключения к PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создание движка SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Для отладки - выводит SQL запросы
    pool_size=5,  # Размер пула соединений
    max_overflow=10
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db() -> Session:
    """Генератор для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создание всех таблиц в БД"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Удаление всех таблиц из БД (для тестирования)"""
    Base.metadata.drop_all(bind=engine)
