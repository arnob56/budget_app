import sqlite3
import logging

DB_NAME = "budget.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT CHECK(type IN ('income','expense')) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
    """)

    conn.commit()
    conn.close()

def add_category(name, type_):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO categories (name, type) VALUES (?, ?)",
            (name, type_),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def get_categories(type_=None):
    conn = get_connection()
    cursor = conn.cursor()

    if type_:
        cursor.execute("SELECT * FROM categories WHERE type=?", (type_,))
    else:
        cursor.execute("SELECT * FROM categories")

    data = cursor.fetchall()
    conn.close()
    return data

def add_transaction(date, amount, category_id, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, amount, category_id, description)
        VALUES (?, ?, ?, ?)
    """, (date, amount, category_id, description))

    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.date, t.amount, c.name, c.type, t.description
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.date ASC
    """)

    data = cursor.fetchall()
    conn.close()
    return data
