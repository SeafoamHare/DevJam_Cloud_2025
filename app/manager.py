from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
from app.main import ask

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"使用者 {user_id} 已連接")

    def disconnect(self, websocket: WebSocket):
        for user_id, conn in list(self.active_connections.items()):
            if conn == websocket:
                del self.active_connections[user_id]
                print(f"使用者 {user_id} 已斷開連接")
                break

    async def send_to(self, from_id: int, to_id: int, message: str):
        if to_id in self.active_connections:
            await self.active_connections[to_id].send_text(f"來自使用者 {from_id}: {message}")
        else:
            if from_id in self.active_connections:
                await self.active_connections[from_id].send_text(f"⚠️ 使用者 {to_id} 不在線")

    async def answer_by_ai(self, sender_id: int, message: str):
        sender_ws = self.active_connections.get(sender_id)
        try:
            return await ask(message)
        except Exception as e:
            print(f"無法傳送訊息給 ai：{e}")

    async def broadcast(self, message: str):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(f"使用者 {user_id}: {message}")
            except WebSocketDisconnect:
                self.disconnect(connection)

# 全域 manager 實例
manager = ConnectionManager()
