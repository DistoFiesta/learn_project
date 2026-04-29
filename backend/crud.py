import json
from backend.database import get_db_connection
from backend.schemas import ProductCreate

# _____ВЫВОД ВСЕХ ТОВАРОВ_____
def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()
    return [_format_row(row) for row in rows]

def _format_row(row):
    if not row: return None
    d = dict(row)
    try:
        d['image_urls'] = json.loads(d['image_urls'])
    except:
        d['image_urls'] = []
    return d

# _____ЛОГИКА СОЗДАНИЯ_____
def create_product(product: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    urls_json = json.dumps(product.image_urls)
    cursor.execute('''
        INSERT INTO products (name, description, price, old_price, image_urls, quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product.name, product.description, product.price, product.old_price, urls_json, product.quantity))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_product(new_id)

# _____ЛОГИКА УДАЛЕНИЯ (ОДИНОЧНОЕ И МАССОВОЕ)_____
def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success

def delete_multiple_products(product_ids: list):
    """Массовое удаление через SQL IN"""
    if not product_ids: return False
    conn = get_db_connection()
    cursor = conn.cursor()
    # Создаем строку из знаков вопроса (?, ?, ?)
    placeholders = ', '.join(['?' for _ in product_ids])
    cursor.execute(f'DELETE FROM products WHERE id IN ({placeholders})', product_ids)
    conn.commit()
    conn.close()
    return True

# ... функции get_product и update_product остаются как в прошлом шаге ...
def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    return _format_row(row)

def update_product(product_id: int, product: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    urls_json = json.dumps(product.image_urls)
    cursor.execute('''
        UPDATE products SET name=?, description=?, price=?, old_price=?, image_urls=?, quantity=?
        WHERE id=?
    ''', (product.name, product.description, product.price, product.old_price, urls_json, product.quantity, product_id))
    conn.commit()
    conn.close()
    return get_product(product_id)