import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import  users, chat, whiteboard
from app import database
from app.sockets.websocket_handler import router as websocket_router


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

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(websocket_router)
app.include_router(whiteboard.router, prefix="/api/v1", tags=["whiteboard"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System API"}

@app.get('/health')
def health():
    return {"message": "ok"}
