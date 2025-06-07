from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    sender: str
    receiver: str
    message: str
    timestamp: datetime = datetime.now()
