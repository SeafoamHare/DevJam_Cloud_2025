import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import get_connection

class UserDAO:
    def __init__(self):
        self.conn = get_connection()

    def create_user(self, username, email, is_active=True):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, is_active)
                VALUES (%s, %s, %s)
                RETURNING id, username, email, is_active;
                """,
                (username, email, is_active)
            )
            self.conn.commit()
            return cur.fetchone()

    def get_user(self, user_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, username, email, is_active FROM users WHERE id = %s;",
                (user_id,)
            )
            return cur.fetchone()

    def get_users(self, skip=0, limit=10):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, username, email, is_active FROM users ORDER BY id OFFSET %s LIMIT %s;",
                (skip, limit)
            )
            return cur.fetchall()

    def update_user(self, user_id, username=None, email=None, is_active=None):
        fields = []
        values = []
        if username is not None:
            fields.append('username = %s')
            values.append(username)
        if email is not None:
            fields.append('email = %s')
            values.append(email)
        if is_active is not None:
            fields.append('is_active = %s')
            values.append(is_active)
        if not fields:
            return None
        values.append(user_id)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE id = %s RETURNING id, username, email, is_active;",
                tuple(values)
            )
            self.conn.commit()
            return cur.fetchone()

    def delete_user(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.conn.commit()

    def close(self):
        self.conn.close()
