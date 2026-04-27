import sqlite3

# Название файла базы данных, который создастся автоматически
DB_NAME = "shop.db"


def get_db_connection():
    """Открывает и возвращает соединение с базой данных."""
    conn = sqlite3.connect(DB_NAME)
    # Позволяет обращаться к колонкам по имени: row['name']
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создает таблицу товаров, если она еще не существует."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL-запрос на создание таблицы
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
        ''')
    conn.commit()
    conn.close()


# Сразу инициализируем базу при импорте этого файла
init_db()