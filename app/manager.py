from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

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

    async def send_to(self, sender_id: int, receiver_id: int, message: str):
        receiver_ws = self.active_connections.get(receiver_id)
        if receiver_ws:
            try:
                await receiver_ws.send_text(f"來自 {sender_id} 的訊息：{message}")
            except Exception as e:
                print(f"無法傳送訊息給 {receiver_id}：{e}")
        else:
            print(f"使用者 {receiver_id} 不在線上")

    async def broadcast(self, message: str):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(f"使用者 {user_id}: {message}")
            except WebSocketDisconnect:
                self.disconnect(connection)

# 全域 manager 實例
manager = ConnectionManager()
