from fastapi import FastAPI, HTTPException
from typing import List
from backend.schemas import ProductCreate, ProductResponse
import backend.crud as crud

app = FastAPI(title="API Интернет-магазина")

@app.get("/products", response_model=List[ProductResponse])
def read_products():
    return crud.get_all_products()

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int):
    product = crud.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    return crud.create_product(product)

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate):
    existing_product = crud.get_product(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return crud.update_product(product_id, product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    success = crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message": "Товар успешно удален"}