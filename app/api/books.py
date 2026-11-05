from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookOut])
def list_books(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Фильтр по id категории"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    """Список книг с фильтрацией по категории и цене"""
    return crud.get_all_books(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
    )


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по id"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    """Создать книгу. Проверяет, что категория существует."""
    # Бизнес-валидация: категория должна существовать
    category = crud.get_category(db, payload.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id={payload.category_id} does not exist",
        )

    return crud.create_book(
        db,
        title=payload.title,
        price=payload.price,
        category_id=payload.category_id,
        description=payload.description,
        url=payload.url or "",
    )


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу (частично)."""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if payload.category_id is not None:
        category = crud.get_category(db, payload.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id={payload.category_id} does not exist",
            )

    updated = crud.update_book(
        db,
        book_id=book_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        url=payload.url,
        category_id=payload.category_id,
    )
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None