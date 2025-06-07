import os
import sys
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 取得 DB 連線

# 主搜尋功能
def search_similar_contents(query: str, top_k: int = 3):
    # 1. 載入模型
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embedding = model.encode(query)

    # 2. 查詢最相近內容
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT content, embedding <-> %s::vector AS distance
            FROM embeddings
            ORDER BY embedding <-> %s::vector
            LIMIT %s
            """,
            (embedding.tolist(), embedding.tolist(), top_k)
        )
        results = cur.fetchall()
        return results
    except Exception as e:
        print(f"❌ 查詢時錯誤: {str(e)}")
        return []
    finally:
        cur.close()
        conn.close()

# # 測試執行
# if __name__ == "__main__":
#     query = input("請輸入問題：")
#     results = search_similar_contents(query)
#     print("🔍 搜尋結果：")
#     for i, row in enumerate(results, 1):
#         print(f"{i}. 相似度距離: {row['distance']:.4f}")
#         print(f"   內容：{row['content'][:100]}...\n")
