import os
import sys
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import vertexai
from vertexai.generative_models import GenerativeModel
PROJECT_ID = "devjam-cloud-2025"
LOCATION = "us-central1"
# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

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
        
def ask(query: str):
    docs = search_similar_contents(query)
    print(docs)
    if docs and docs[0]['distance'] < 4:  # 距離小代表相似
        context = "\n".join([doc['content'] for doc in docs])
        print('context', context)
        return call_openai(f"根據以下內容回答問題：\n{context}\n\n問題：{query}")
    else:        
        return call_openai(f"請回答下列問題：{query}")
    
def call_openai(prompt: str):
    try:
        model = GenerativeModel("gemini-2.0-flash-001")  # 使用 gemini-2.0-flash-001 模型
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ 呼叫 OpenAI 時錯誤: {str(e)}")
        return "抱歉，無法回答您的問題。請稍後再試。"
    # client = OpenAI(api_key=OPENAI_API_KEY)
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.choices[0].message.content
    # return "This is answer by ai"
