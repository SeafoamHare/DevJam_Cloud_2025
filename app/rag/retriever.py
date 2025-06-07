import os
import sys
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 設定路徑與環境
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

# DB 連線參數
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
sslmode = os.getenv("DB_SSLMODE", "allow")
conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"

# 取得 DB 連線
def get_connection():
    return psycopg2.connect(conn_string, cursor_factory=RealDictCursor)

def search_similar_contents(query: str, top_k: int = 3):
    from psycopg2.extensions import register_adapter, AsIs
    import numpy as np
# 讓 psycopg2 支援 numpy float 自動轉換
    def addapt_numpy_float32(numpy_float32):
        return AsIs(numpy_float32)

    register_adapter(np.float32, addapt_numpy_float32)
    register_adapter(np.float64, addapt_numpy_float32)

    # 1. 載入模型
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embedding = model.encode(query)

    # 將 numpy array 轉成 PostgreSQL 支援格式
    embedding_list = embedding.tolist()
    embedding_str = "[" + ",".join([str(x) for x in embedding_list]) + "]"

    # 2. 查詢最相近內容
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # 讓結果是 dict
    try:
        cur.execute(
            """
            SELECT content, embedding <-> %s::vector AS distance
            FROM embeddings
            ORDER BY embedding <-> %s::vector
            LIMIT %s
            """,
            (embedding_str, embedding_str, top_k)
        )
        results = cur.fetchall()
        # results = 'blabla'
        return results
    except Exception as e:
        print(f"❌ 查詢時錯誤: {str(e)}")
        return []
    finally:
        cur.close()
        conn.close()  