import sys
import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, WebSocketDisconnect, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routers import books, users, transactions
from app import database
from app.sockets.websocket_handler import router as websocket_router  # ← 匯入 WebSocket router
import json


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
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System API"}
