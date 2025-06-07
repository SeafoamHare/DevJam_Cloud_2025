import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import get_connection

class UserDAO:
    def __init__(self):
        self.conn = get_connection()

    def create_user(self, username, email, password, organization=None, role=None, referrer=None, survey=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, password, organization, role, referrer, survey)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING username, email, password, organization, role, referrer, points, survey;
                """,
                (username, email, password, organization, role, referrer, survey)
            )
            self.conn.commit()
            return cur.fetchone()

    def get_user(self, username: str):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT username, email, password, organization, role, referrer, points, survey FROM users WHERE username = %s;",
                (username,)
            )
            return cur.fetchone()

    def get_user_by_username(self, username: str):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT username, email, password, organization, role, referrer, points, survey FROM users WHERE username = %s;",
                (username,)
            )
            return cur.fetchone()

    def get_users(self, skip=0, limit=10):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT username, email, password, organization, role, referrer, points, survey FROM users ORDER BY username OFFSET %s LIMIT %s;",
                (skip, limit)
            )
            return cur.fetchall()

    def update_user(self, username: str, email=None, password=None, organization=None, role=None, referrer=None, points=None, survey=None):
        fields = []
        values = []
        if email is not None:
            fields.append('email = %s')
            values.append(email)
        if password is not None:
            fields.append('password = %s')
            values.append(password)
        if organization is not None:
            fields.append('organization = %s')
            values.append(organization)
        if role is not None:
            fields.append('role = %s')
            values.append(role)
        if referrer is not None:
            fields.append('referrer = %s')
            values.append(referrer)
        if points is not None:
            fields.append('points = %s')
            values.append(points)
        if survey is not None:
            fields.append('survey = %s')
            values.append(survey)
        if not fields:
            return None
        values.append(username)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE username = %s RETURNING username, email, password, organization, role, referrer, points, survey;",
                tuple(values)
            )
            self.conn.commit()
            return cur.fetchone()

    def delete_user(self, username: str):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE username = %s;", (username,))
            self.conn.commit()

    def close(self):
        self.conn.close()
