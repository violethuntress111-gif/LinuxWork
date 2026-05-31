#!/usr/bin/env python3
"""
Основной модуль для чтения данных из базы данных и их вывода на экран
Запуск: python app/main.py
"""

import sys
import os

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud

def print_separator(char="=", length=80):
    """Вывод разделительной линии"""
    print(char * length)

def print_header(text):
    """Вывод заголовка"""
    print_separator()
    print(f"📚 {text}")
    print_separator()

def print_category_info(category, book_count):
    """Вывод информации о категории"""
    print(f"\n📖 {category.title.upper()} (ID: {category.id})")
    print(f"   Количество книг: {book_count}")

def print_book_info(book, index=None):
    """Вывод информации о книге"""
    prefix = f"   {index}. " if index else "   • "
    print(f"{prefix}📕 {book.title}")
    print(f"      💰 Цена: ${book.price:.2f}")
    if book.description:
        # Ограничиваем длину описания для красиво
        description = book.description[:100] + "..." if len(book.description) > 100 else book.description
        print(f"      📝 Описание: {description}")
    if book.url:
        print(f"      🔗 Ссылка: {book.url}")

def main():
    """Основная функция для чтения и вывода данных из БД"""
    
    print_header("КНИЖНЫЙ МАГАЗИН - КАТАЛОГ КНИГ")
    
    db = SessionLocal()
    
    try:
        # Получаем все категории
        categories = crud.get_all_categories(db)
        
        if not categories:
            print("\n❌ В базе данных нет категорий.")
            print("   Запустите сначала 'python app/init_db.py' для инициализации данных.")
            return
        
        print(f"\n📊 Общее количество категорий: {len(categories)}")
        
        # Счетчик общего количества книг
        total_books = 0
        total_cost = 0.0
        
        # Перебираем все категории
        for category in categories:
            # Получаем книги в категории
            books = crud.get_books_by_category(db, category.id)
            book_count = len(books)
            total_books += book_count
            
            # Выводим информацию о категории
            print_category_info(category, book_count)
            
            # Выводим книги в категории
            if books:
                category_cost = 0
                for i, book in enumerate(books, 1):
                    print_book_info(book, i)
                    category_cost += book.price
                
                total_cost += category_cost
                print(f"   💵 Общая стоимость книг в категории: ${category_cost:.2f}")
                print(f"   📊 Средняя цена книги в категории: ${(category_cost / book_count):.2f}")
            else:
                print("   ⚠ Нет книг в этой категории")
        
        # Выводим общую статистику
        print_separator()
        print("\n📊 ОБЩАЯ СТАТИСТИКА:")
        print(f"   • Всего категорий: {len(categories)}")
        print(f"   • Всего книг: {total_books}")
        print(f"   • Общая стоимость всех книг: ${total_cost:.2f}")
        print(f"   • Средняя цена книги: ${(total_cost / total_books):.2f}" if total_books > 0 else "")
        
        # Дополнительный поиск по названию (пример дополнительной функциональности)
        print_separator()
        print("\n🔍 ДОПОЛНИТЕЛЬНЫЙ ПОИСК:")
        
        search_term = input("\nВведите слово для поиска книг (или нажмите Enter для пропуска): ").strip()
        if search_term:
            found_books = crud.search_books_by_title(db, search_term)
            if found_books:
                print(f"\n✓ Найдено книг по запросу '{search_term}': {len(found_books)}")
                for book in found_books[:5]:  # Показываем только первые 5
                    category = crud.get_category(db, book.category_id)
                    print(f"   • {book.title} (Категория: {category.title if category else 'Неизвестно'}) - ${book.price:.2f}")
                if len(found_books) > 5:
                    print(f"   ... и еще {len(found_books) - 5} книг")
            else:
                print(f"\n❌ Книг по запросу '{search_term}' не найдено")
        
        print_separator()
        print("\n✅ Программа успешно завершила работу!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при чтении данных из базы данных: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
