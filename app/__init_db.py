#!/usr/bin/env python3
"""
Модуль для инициализации базы данных тестовыми данными
Запуск: python app/init_db.py
"""

import sys
import os

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, create_tables, engine
from app.db import crud
from app.db.models import Base

def init_database():
    """Инициализация базы данных с тестовыми данными"""
    
    print("=" * 50)
    print("Инициализация базы данных книжного магазина")
    print("=" * 50)
    
    # Создание таблиц (если они еще не созданы)
    print("\n1. Создание таблиц в базе данных...")
    create_tables()
    print("   ✓ Таблицы успешно созданы")
    
    # Получаем сессию базы данных
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные в таблице категорий
        existing_categories = crud.get_all_categories(db)
        if existing_categories:
            print("\n   ⚠ В базе данных уже есть категории. Очистка существующих данных...")
            # Очищаем существующие данные
            for category in existing_categories:
                crud.delete_category(db, category.id)
            print("   ✓ Существующие данные удалены")
        
        print("\n2. Добавление категорий товара...")
        
        # Создание категорий
        category_fiction = crud.create_category(db, "Художественная литература")
        print(f"   ✓ Создана категория: {category_fiction.title} (ID: {category_fiction.id})")
        
        category_science = crud.create_category(db, "Научная литература")
        print(f"   ✓ Создана категория: {category_science.title} (ID: {category_science.id})")
        
        category_children = crud.create_category(db, "Детская литература")
        print(f"   ✓ Создана категория: {category_children.title} (ID: {category_children.id})")
        
        print("\n3. Добавление книг в категории...")
        
        # Книги для категории "Художественная литература"
        print(f"\n   📚 Категория '{category_fiction.title}':")
        
        books_fiction = [
            {
                "title": "Война и мир",
                "description": "Роман-эпопея Льва Толстого о жизни русского общества в эпоху наполеоновских войн",
                "price": 15.99,
                "url": "https://example.com/war_and_peace"
            },
            {
                "title": "Преступление и наказание",
                "description": "Роман Федора Достоевского о moral dilemmas и психологии преступника",
                "price": 12.50,
                "url": "https://example.com/crime_and_punishment"
            },
            {
                "title": "Мастер и Маргарита",
                "description": "Мистический роман Михаила Булгакова о дьяволе, любви и творчестве",
                "price": 14.99,
                "url": "https://example.com/master_and_margarita"
            },
            {
                "title": "Анна Каренина",
                "description": "Трагическая история любви в высшем обществе России XIX века",
                "price": 13.99,
                "url": "https://example.com/anna_karenina"
            }
        ]
        
        for book_data in books_fiction:
            book = crud.create_book(
                db,
                title=book_data["title"],
                price=book_data["price"],
                category_id=category_fiction.id,
                description=book_data["description"],
                url=book_data["url"]
            )
            print(f"      - {book.title} (${book.price})")
        
        # Книги для категории "Научная литература"
        print(f"\n   📚 Категория '{category_science.title}':")
        
        books_science = [
            {
                "title": "Краткая история времени",
                "description": "Стивен Хокинг представляет сложные концепции космологии простым языком",
                "price": 24.99,
                "url": "https://example.com/brief_history_of_time"
            },
            {
                "title": "Искусство программирования",
                "description": "Фундаментальный труд Дональда Кнута по алгоритмам и структурам данных",
                "price": 89.99,
                "url": "https://example.com/art_of_programming"
            },
            {
                "title": "Sapiens. Краткая история человечества",
                "description": "Юваль Ной Харари о ключевых этапах развития человеческого вида",
                "price": 19.99,
                "url": "https://example.com/sapiens"
            }
        ]
        
        for book_data in books_science:
            book = crud.create_book(
                db,
                title=book_data["title"],
                price=book_data["price"],
                category_id=category_science.id,
                description=book_data["description"],
                url=book_data["url"]
            )
            print(f"      - {book.title} (${book.price})")
        
        # Книги для категории "Детская литература"
        print(f"\n   📚 Категория '{category_children.title}':")
        
        books_children = [
            {
                "title": "Маленький принц",
                "description": "Философская сказка Антуана де Сент-Экзюпери о дружбе и любви",
                "price": 11.99,
                "url": "https://example.com/little_prince"
            },
            {
                "title": "Гарри Поттер и философский камень",
                "description": "Первая книга Дж.К. Роулинг о юном волшебнике",
                "price": 18.99,
                "url": "https://example.com/harry_potter"
            },
            {
                "title": "Винни-Пух и все-все-все",
                "description": "Веселые приключения медвежонка Винни-Пуха и его друзей",
                "price": 9.99,
                "url": "https://example.com/winnie_the_pooh"
            },
            {
                "title": "Приключения Незнайки и его друзей",
                "description": "Николай Носов о забавных приключениях коротышек из Цветочного города",
                "price": 10.99,
                "url": "https://example.com/neznayka"
            }
        ]
        
        for book_data in books_children:
            book = crud.create_book(
                db,
                title=book_data["title"],
                price=book_data["price"],
                category_id=category_children.id,
                description=book_data["description"],
                url=book_data["url"]
            )
            print(f"      - {book.title} (${book.price})")
        
        # Вывод статистики
        print("\n" + "=" * 50)
        print("СТАТИСТИКА ИНИЦИАЛИЗАЦИИ:")
        print("=" * 50)
        
        all_categories = crud.get_all_categories(db)
        print(f"📑 Категории: {len(all_categories)}")
        
        all_books = crud.get_all_books(db)
        print(f"📚 Книги: {len(all_books)}")
        
        total_price = sum(book.price for book in all_books)
        print(f"💰 Общая стоимость всех книг: ${total_price:.2f}")
        print(f"💰 Средняя цена книги: ${(total_price / len(all_books)):.2f}")
        
        print("\n" + "=" * 50)
        print("✓ Инициализация базы данных успешно завершена!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Ошибка при инициализации базы данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
