from pydantic import BaseModel, Field
from typing import Optional, Literal, Union
from datetime import datetime

class ChatMessage(BaseModel):
    from_id: int
    to_id: int
    content: str
    action: str


class WhiteboardAction(BaseModel):
    sender_id: int = Field(..., description="發送者 ID")
    content: str = Field(..., description="白板內容")
    action: Literal["draw", "erase"]


class WebSocketMessage(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Union[ChatMessage, WhiteboardAction]