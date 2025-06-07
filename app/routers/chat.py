from fastapi import APIRouter, HTTPException
from typing import List
from app.models.chat_model import ChatMessage
from app.dao import chat_dao

router = APIRouter()

@router.post("/chat/messages/", response_model=ChatMessage)
async def create_chat_message(message: ChatMessage):
    """
    Save a new chat message.
    """
    try:
        success = chat_dao.save_message(message)
        if success:
            return message
        else:
            raise HTTPException(status_code=500, detail="Failed to save message.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/chat/messages/{sender}/{receiver}", response_model=List[ChatMessage])
async def get_chat_messages(sender: str, receiver: str):
    """
    Retrieve chat history between a sender and a receiver.
    """
    try:
        messages = chat_dao.get_messages_by_sender_receiver(sender, receiver)
        if not messages:
            return []
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
