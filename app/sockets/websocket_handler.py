from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import json
from app.manager import manager
from app.models.response import ChatMessage
from app.pubsub import listen_pubsub
import asyncio
from app.dao.chat_dao import save_message

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    await websocket.send_text("✅ 登入成功，等待傳訊息")
    asyncio.create_task(listen_pubsub(user_id, websocket))

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
                print(f"📩 收到來自 {chat_msg.from_id} 的訊息：{chat_msg.content}")
                save_message(chat_msg)  
                await manager.send_to(chat_msg)

            except Exception as e:
                await websocket.send_text(f"⚠️ 傳送錯誤：{str(e)}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"🚪 使用者 {user_id} 離線")
