from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    url: Optional[str] = ""
    category_id: int

class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    """Все поля опциональны — частичное обновление"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    url: Optional[str] = None
    category_id: Optional[int] = None


class BookOut(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)