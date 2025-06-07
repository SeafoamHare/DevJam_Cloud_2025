from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import json
from app.manager import manager  # 假設你把 ConnectionManager 寫在這

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # 登入階段
    await manager.connect(websocket, user_id)
    await websocket.send_text("✅ 登入成功，等待傳訊息")

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                to = int(data.get("to"))
                msg = data.get("message")
                if not msg:
                    raise ValueError("message 不可為空")
                    
                await manager.send_to(user_id, to, msg)
            except Exception as e:
                await websocket.send_text(f"⚠️ 傳送錯誤：{str(e)}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"🚪 使用者 {user_id} 離線")
