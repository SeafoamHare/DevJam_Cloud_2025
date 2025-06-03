import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
sslmode = os.getenv("DB_SSLMODE", "allow")

conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"


def get_connection():
    return psycopg2.connect(conn_string)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id serial PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(100) NOT NULL,
            description TEXT,
            available_copies INTEGER DEFAULT 1
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_records (
            id serial PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            book_id INTEGER NOT NULL REFERENCES books(id),
            borrow_date DATE NOT NULL,
            return_date DATE
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# 若要初始化資料庫，請在主程式或啟動時呼叫 initialize_database()
