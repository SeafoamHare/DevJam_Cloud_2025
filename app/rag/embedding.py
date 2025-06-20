import os
import sys
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

# 数据库连接配置
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
sslmode = os.getenv("DB_SSLMODE", "allow")

conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"

def get_connection():
    return psycopg2.connect(conn_string)

def create_embeddings_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(384),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ 資料表創建成功")
    except Exception as e:
        print(f"❌ 創建資料表時發生錯誤: {str(e)}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_embedding(content: str, embedding: np.ndarray):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO embeddings (content, embedding)
            VALUES (%s, %s)
            """,
            (content, embedding.tolist())
        )
        conn.commit()
        print("✅ 嵌入向量插入成功")
    except Exception as e:
        print(f"❌ 插入嵌入向量時發生錯誤: {str(e)}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def main():
    # 创建数据库表
    create_embeddings_table()
    
    print("正在加載文本嵌入模型...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    file_path = os.path.join(root_dir, 'app', 'docs', 'symptom.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("✅ 成功讀取文本文件")
            
            # 生成文本嵌入
            print("正在生成文本嵌入...")
            embedding = model.encode(content)
            
            # 插入数据库
            insert_embedding(content, embedding)
            
    except FileNotFoundError:
        print(f"❌ 找不到文件: {file_path}")
    except Exception as e:
        print(f"❌ 處理文件時發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()
