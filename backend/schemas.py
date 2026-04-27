from pydantic import BaseModel
from typing import Optional

# Базовая схема, содержит общие поля для товара
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    quantity: int

# Схема для создания товара (использует те же поля, что и базовая)
class ProductCreate(ProductBase):
    pass

# Схема для ответа API (возвращаем всё то же самое + ID товара из базы)
class ProductResponse(ProductBase):
    id: int

    class Config:
        # Позволяет Pydantic читать данные из объектов SQLite
        from_attributes = True