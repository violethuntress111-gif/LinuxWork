from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import models
from app.db.models import Book, Category

# ========== CRUD для Category ==========

def create_category(db: Session, title: str) -> Category:
    """Создание новой категории"""
    db_category = Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int) -> Optional[Category]:
    """Получение категории по ID"""
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_title(db: Session, title: str) -> Optional[Category]:
    """Получение категории по названию"""
    return db.query(Category).filter(Category.title == title).first()

def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    """Получение всех категорий с пагинацией"""
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, title: str) -> Optional[Category]:
    """Обновление категории"""
    db_category = get_category(db, category_id)
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    """Удаление категории"""
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# ========== CRUD для Book ==========

def create_book(
    db: Session,
    title: str,
    price: float,
    category_id: int,
    description: Optional[str] = None,
    url: Optional[str] = ""
) -> Book:
    """Создание новой книги"""
    db_book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Получение книги по ID"""
    return db.query(Book).filter(Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
    """Получение всех книг в категории"""
    return db.query(Book).filter(Book.category_id == category_id).offset(skip).limit(limit).all()

def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    category_id: Optional[int] = None
) -> List[Book]:
    """Получение всех книг с фильтрацией и пагинацией"""
    query = db.query(Book)
    
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()

def search_books_by_title(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Book]:
    """Поиск книг по названию (частичное совпадение)"""
    return db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).offset(skip).limit(limit).all()

def update_book(
    db: Session,
    book_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    url: Optional[str] = None,
    category_id: Optional[int] = None
) -> Optional[Book]:
    """Обновление книги"""
    db_book = get_book(db, book_id)
    if db_book:
        if title is not None:
            db_book.title = title
        if description is not None:
            db_book.description = description
        if price is not None:
            db_book.price = price
        if url is not None:
            db_book.url = url
        if category_id is not None:
            db_book.category_id = category_id
        
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    """Удаление книги"""
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def get_books_count(db: Session, category_id: Optional[int] = None) -> int:
    """Получение количества книг"""
    query = db.query(Book)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    return query.count()
