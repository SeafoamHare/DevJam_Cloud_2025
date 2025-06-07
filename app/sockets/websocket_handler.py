from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import json
from app.manager import manager
from app.models.response import ChatMessage

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    await websocket.send_text("✅ 登入成功，等待傳訊息")

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                # 將原始 JSON 轉成 ChatMessage 物件
                parsed = json.loads(raw)
                parsed["from_id"] = user_id  # 強制使用 path 中的 user_id，避免偽造
                chat_msg = ChatMessage(**parsed)

                if not chat_msg.content.strip():
                    raise ValueError("message 不可為空")

                await manager.send_to(chat_msg)

            except Exception as e:
                await websocket.send_text(f"⚠️ 傳送錯誤：{str(e)}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"🚪 使用者 {user_id} 離線")
