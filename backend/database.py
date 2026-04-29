import sqlite3

DB_NAME = "shop.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # _____ПОЛЕ image_urls ТЕПЕРЬ ХРАНИТ МАССИВ В ФОРМАТЕ JSON-СТРОКИ_____
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS products
                   (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        price REAL NOT NULL,
                        old_price REAL,
                        image_urls TEXT DEFAULT '[]', 
                        quantity INTEGER NOT NULL DEFAULT 0
                   )
                   ''')
    conn.commit()
    conn.close()


init_db()