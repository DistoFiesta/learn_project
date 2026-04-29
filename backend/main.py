from fastapi import FastAPI, HTTPException, Body
from typing import List
from backend.schemas import ProductCreate, ProductResponse
import backend.crud as crud

app = FastAPI(title="API Интернет-магазина")

@app.get("/products", response_model=List[ProductResponse])
def read_products(): return crud.get_all_products()

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate): return crud.create_product(product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if not crud.delete_product(product_id): raise HTTPException(404)
    return {"status": "ok"}

# _____НОВЫЙ ЭНДПОИНТ ДЛЯ МАССОВОГО УДАЛЕНИЯ_____
@app.post("/products/bulk-delete")
def bulk_delete(ids: List[int] = Body(...)):
    crud.delete_multiple_products(ids)
    return {"status": "deleted"}

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int):
    p = crud.get_product(product_id)
    if not p: raise HTTPException(404)
    return p

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate):
    return crud.update_product(product_id, product)