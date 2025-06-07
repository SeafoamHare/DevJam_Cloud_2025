import sys
import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, WebSocketDisconnect, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routers import books, users, transactions
from app import database
from app.sockets.websocket_handler import manager

database.initialize_database()

app = FastAPI()

# 添加CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/api/v1", tags=["books"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System API"}


# 用户ID计数器
user_counter = 1

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global user_counter
    try:
        await manager.connect(websocket, user_counter)
        await websocket.send_text("✅ WebSocket 連線成功！")
        user_counter += 1  # 增加用户ID
        
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
            print(f"收到訊息：{data}")
            await websocket.send_text(f"你說：{data}")
    except WebSocketDisconnect:
        print("🚪 使用者離線")
        manager.disconnect(websocket)