from pydantic import BaseModel, Field
from typing import Optional, Literal, Union
from datetime import datetime

class ChatMessage(BaseModel):
    from_id: str
    to_id: str
    content: str
    action: str


class WhiteboardAction(BaseModel):
    sender_id: str = Field(..., description="發送者 ID")
    content: str = Field(..., description="白板內容")
    action: Literal["draw", "erase"]


class WebSocketMessage(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Union[ChatMessage, WhiteboardAction]