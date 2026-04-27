from fastapi import FastAPI, HTTPException
from typing import List

# Импортируем наши схемы и функции работы с БД
from backend.schemas import ProductCreate, ProductResponse
import backend.crud as crud

# Создаем само приложение FastAPI
app = FastAPI(
    title="API Интернет-магазина",
    description="Лабораторная работа №3. Управление товарами.",
    version="1.0.0"
)


# ==========================================
# МАРШРУТЫ (Endpoints)
# ==========================================

# 1. Получить список всех товаров (Метод GET)
@app.get("/products", response_model=List[ProductResponse])
def read_products():
    """Возвращает список всех товаров из базы."""
    return crud.get_all_products()


# 2. Получить один товар по ID (Метод GET)
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int):
    """Возвращает информацию о конкретном товаре."""
    product = crud.get_product(product_id)
    if product is None:
        # Если CRUD вернул None, выбрасываем стандартную ошибку 404
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


# 3. Добавить новый товар (Метод POST)
@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    """Создает новый товар. Данные автоматически проверяются Pydantic-схемой."""
    return crud.create_product(product)


# 4. Обновить существующий товар (Метод PUT)
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate):
    """Полностью обновляет данные товара по его ID."""
    existing_product = crud.get_product(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")

    return crud.update_product(product_id, product)


# 5. Удалить товар (Метод DELETE)
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Удаляет товар из базы по ID."""
    success = crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")

    return {"message": "Товар успешно удален"}