from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Dict
from google.cloud import pubsub_v1
import os
import json
from dotenv import load_dotenv
from app.models.response import WhiteboardAction

load_dotenv()

router = APIRouter()

# GCP Pub/Sub 設定
project_id = os.getenv("GCP_PROJECT_ID")
topic_id = os.getenv("GCP_TOPIC_ID")  # 請放 topic 名稱，不是整個 topic_path
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


@router.get('/whiteboard')
def index():
    return {"message": "Welcome to the Whiteboard API"}

@router.post("/whiteboard/event")
async def post_whiteboard_event(payload: WhiteboardAction):
    try:
        message = {
            "type": "whiteboard",
            "sender": payload.sender_id,
            "content": payload.content,
            "action": payload.action
        }

        # 發布訊息
        future = publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
        message_id = future.result()
        return {"status": "ok", "message_id": message_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ 發布失敗: {str(e)}")
