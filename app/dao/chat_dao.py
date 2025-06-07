from app.database import get_connection
from app.models.response import ChatMessage
from datetime import datetime

def save_message(chat_message: ChatMessage) -> bool:
    conn = None
    cursor = None
    print(f"📥 儲存訊息：{chat_message.from_id} -> {chat_message.to_id} : {chat_message.content}")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO chat_messages (sender, receiver, message, timestamp)
            VALUES (%s, %s, %s, %s);
            """,
            (chat_message.from_id, chat_message.to_id, chat_message.content, datetime.now())
        )
        conn.commit()
        return True
    except Exception as e:
        # Optionally log the error e
        print(f"❌ 儲存訊息失敗：{e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_messages_by_sender_receiver(sender: str, receiver: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT sender, receiver, message, timestamp
        FROM chat_messages
        WHERE sender = %s AND receiver = %s OR sender = %s AND receiver = %s
        ORDER BY timestamp ASC;
        """,
        (sender, receiver, receiver, sender) 
    )
    messages_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    messages = []
    for row in messages_data:
        messages.append(ChatMessage(
            sender=row[0],
            receiver=row[1],
            message=row[2],
            timestamp=row[3]
        ))
    return messages
