from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.db import Base

class Category(Base):
    """Модель категории книг"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True, index=True)
    
    # Связь с книгами
    books = relationship("Book", back_populates="category_rel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"

class Book(Base):
    """Модель книги"""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    url = Column(String(1000), nullable=True, default="")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    
    # Связь с категорией
    category_rel = relationship("Category", back_populates="books")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"
