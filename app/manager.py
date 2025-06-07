from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import json
from app.rag import ask
from app.models.response import ChatMessage, WhiteboardAction, WebSocketMessage

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

    async def send_to(self, message: ChatMessage):
        sender_id = message.from_id
        receiver_id = message.to_id

        # AI 處理路徑（假設 sender_id == 1 是 AI）
        if receiver_id == '1':
            await self.answer_by_ai(sender_id, message.content)
            return

        if receiver_id in self.active_connections:
            await self.active_connections[receiver_id].send_text(
                f"來自使用者 {sender_id}: {message.content}"
            )
        else:
            # 回傳通知 sender：對方不在線
            if sender_id in self.active_connections:
                await self.active_connections[sender_id].send_text(
                    f"⚠️ 使用者 {receiver_id} 不在線"
                )

    async def answer_by_ai(self, sender_id: int, message: str):
        try:
            print(f"收到來自使用者 {sender_id} 的問題：{message}")
            answer = ask(message)  # 這裡假設你已經有定義好的 AI 回答函數
            print(f"AI 回答：{answer}")

            if sender_id in self.active_connections:
                await self.active_connections[sender_id].send_text(f"🤖 AI 回答：{answer}")
            else:
                print(f"⚠️ 使用者 {sender_id} 已斷開連接")
        except Exception as e:
            error_msg = f"⚠️ AI 回答出錯：{str(e)}"
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