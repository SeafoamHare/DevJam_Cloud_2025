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
        # 找到并移除对应的连接
        for user_id, conn in list(self.active_connections.items()):
            if conn == websocket:
                del self.active_connections[user_id]
                print(f"使用者 {user_id} 已斷開連接")
                break

    async def broadcast(self, message: str):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(f"使用者 {user_id}: {message}")
            except WebSocketDisconnect:
                self.disconnect(connection)

# 全域 manager 實例
manager = ConnectionManager()
