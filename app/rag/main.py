from openai import OpenAI
from app.rag.retriever import search_similar_contents

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
    # client = OpenAI(api_key=OPENAI_API_KEY)
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.choices[0].message.content
    return "This is answer by ai"
