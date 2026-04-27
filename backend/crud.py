from backend.database import get_db_connection
from backend.schemas import ProductCreate

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def create_product(product: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, old_price, quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', (product.name, product.description, product.price, product.old_price, product.quantity))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_product(new_id)

def update_product(product_id: int, product: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE products 
        SET name = ?, description = ?, price = ?, old_price = ?, quantity = ?
        WHERE id = ?
    ''', (product.name, product.description, product.price, product.old_price, product.quantity, product_id))
    conn.commit()
    conn.close()
    return get_product(product_id)

def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    success = cursor.rowcount > 0
    conn.close()
    return success