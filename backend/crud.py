from backend.database import get_db_connection
from backend.schemas import ProductCreate


# ==========================================
# READ: Получение данных (Вывод товаров)
# ==========================================

def get_all_products():
    """Забирает все товары из базы. Это для главной страницы магазина."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL: Выбери всё (*) из таблицы products
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()  # Забираем все найденные строки
    conn.close()

    # Превращаем строки из SQLite в обычные питоновские словари (JSON)
    return [dict(row) for row in rows]


def get_product(product_id: int):
    """Ищет один конкретный товар по его ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL: Выбери всё, где колонка id равна нашему числу
    # Запятая (product_id,) обязательна, так SQLite защищается от взлома (SQL-иньекций)
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()  # Забираем только одну строчку
    conn.close()

    if row:
        return dict(row)
    return None


# ==========================================
# CREATE: Создание данных (Добавление товара)
# ==========================================

def create_product(product: ProductCreate):
    """Добавляет новый товар в базу."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL: Вставь в таблицу products в такие-то колонки вот такие-то значения
    cursor.execute('''
                   INSERT INTO products (name, description, price, quantity)
                   VALUES (?, ?, ?, ?)
                   ''', (product.name, product.description, product.price, product.quantity))

    conn.commit()  # Тот самый "Сейв" - сохраняем изменения на диск
    new_id = cursor.lastrowid  # Узнаем, какой ID база присвоила новому товару
    conn.close()

    # Возвращаем только что созданный товар, чтобы показать его пользователю
    return get_product(new_id)


# ==========================================
# UPDATE: Обновление данных (Редактирование)
# ==========================================

def update_product(product_id: int, product: ProductCreate):
    """Перезаписывает данные существующего товара."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL: Обнови таблицу products, установи новые значения туда, где id совпадает
    cursor.execute('''
                   UPDATE products
                   SET name        = ?,
                       description = ?,
                       price       = ?,
                       quantity    = ?
                   WHERE id = ?
                   ''', (product.name, product.description, product.price, product.quantity, product_id))

    conn.commit()  # Сохраняем изменения
    conn.close()

    return get_product(product_id)


# ==========================================
# DELETE: Удаление данных
# ==========================================

def delete_product(product_id: int):
    """Удаляет товар по ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL: Удали из таблицы products строку с таким-то id
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))

    conn.commit()  # Сохраняем (фиксируем удаление)
    # cursor.rowcount показывает, сколько строк было удалено. Если > 0, значит удаление прошло успешно
    success = cursor.rowcount > 0
    conn.close()

    return success