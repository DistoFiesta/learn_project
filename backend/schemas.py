from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    # _____ТЕПЕРЬ ЭТО ОФИЦИАЛЬНЫЙ СПИСОК СТРОК_____
    image_urls: List[str] = []
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True