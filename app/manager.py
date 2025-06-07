from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import json
from app.rag.main import ask

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"使用者 {user_id} 已連接")

    def disconnect(self, websocket: WebSocket):
        # 找到并移除对应的连接
        for user_id, conn in list(self.active_connections.items()):
            if conn == websocket:
                del self.active_connections[user_id]
                print(f"使用者 {user_id} 已斷開連接")
                break

    async def send_to(self, from_id: int, to_id: int, message: str):
        if to_id == 1:  # AI 用户
            await self.answer_by_ai(from_id, message)
            return

        if to_id in self.active_connections:
            await self.active_connections[to_id].send_text(f"來自使用者 {from_id}: {message}")
        else:
            if from_id in self.active_connections:
                await self.active_connections[from_id].send_text(f"⚠️ 使用者 {to_id} 不在線")

    async def answer_by_ai(self, sender_id: int, message: str):
        try:
            print(f"收到來自使用者 {sender_id} 的問題：{message}")
            # 获取AI回答
            answer = ask(message)
            print(f"AI回答：{answer}")
            
            # 发送AI回答
            if sender_id in self.active_connections:
                await self.active_connections[sender_id].send_text(f"AI回答：{answer}")
            else:
                print(f"⚠️ 使用者 {sender_id} 已斷開連接，無法發送回答")
        except Exception as e:
            error_msg = f"⚠️ AI回答出錯：{str(e)}"
            print(error_msg)
            if sender_id in self.active_connections:
                await self.active_connections[sender_id].send_text(error_msg)

    async def broadcast(self, message: str):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(f"使用者 {user_id}: {message}")
            except WebSocketDisconnect:
                self.disconnect(connection)

# 创建全局实例
manager = ConnectionManager()
