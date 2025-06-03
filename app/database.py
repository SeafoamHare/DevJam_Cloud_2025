import psycopg2

host = "34.135.182.134"
dbname = "postgres"
user = "postgres"
password = "admin"
sslmode = "allow"
DATABASE_URL = "postgresql://postgres:admin@34.135.182.134/postgres"

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
