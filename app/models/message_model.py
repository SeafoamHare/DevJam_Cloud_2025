from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageSchema(BaseModel):
    sender_id: int = Field(..., description="發布者 ID")
    content: str = Field(..., description="留言或操作內容")
    action: str = Field(..., description="動作類型，例如 comment、draw、erase")
    