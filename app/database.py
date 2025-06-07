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
            username VARCHAR(50) PRIMARY KEY,
            email VARCHAR(100) NOT NULL,
            password TEXT NOT NULL,
            organization VARCHAR(100),
            role VARCHAR(50),
            referrer TEXT,
            points INTEGER DEFAULT 0,
            survey TEXT
        );
    """)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS counselors (
    #         id INTEGER PRIMARY KEY REFERENCES users(id),
    #         organization VARCHAR(100),
    #         role VARCHAR(50) CHECK (role IN ('student', 'teacher')),
    #         referrer TEXT,
    #         points INTEGER DEFAULT 0
    #     );
    # """)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS Questioner (
    #         id INTEGER PRIMARY KEY REFERENCES users(id),
    #         survey TEXT
    #     );
    # """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            sender VARCHAR(50) REFERENCES users(username) NOT NULL,
            receiver VARCHAR(50) REFERENCES users(username) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# 若要初始化資料庫，請在主程式或啟動時呼叫 initialize_database()
