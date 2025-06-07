import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import get_connection  # 假設你有 get_connection 方法
from app.models.response import WhiteboardAction

class WhiteboardDAO:
    def __init__(self):
        self.conn = get_connection()

    def create_whiteboard(self, whiteboard_action: WhiteboardAction):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO whiteboards (user_id, content)
                VALUES (%s, %s)
                RETURNING user_id, content;
                """,
                (whiteboard_action.sender_id, whiteboard_action.content)
            )
            self.conn.commit()
            return cur.fetchone()

    def get_whiteboard(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT user_id, content
                FROM whiteboards;
                """
            )
            return cur.fetchone()

    def update_whiteboard(self, user_id: int, new_content: str):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE whiteboards
                SET content = %s
                WHERE user_id = %s
                RETURNING user_id, content;
                """,
                (new_content, user_id)
            )
            self.conn.commit()
            return cur.fetchone()
