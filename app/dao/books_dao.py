import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import get_connection

class BookDAO:
    def __init__(self):
        self.conn = get_connection()

    def create_book(self, title, author, description=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO books (title, author, description)
                VALUES (%s, %s, %s)
                RETURNING id, title, author, description;
                """,
                (title, author, description)
            )
            self.conn.commit()
            return cur.fetchone()

    def get_book(self, book_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, title, author, description FROM books WHERE id = %s;",
                (book_id,)
            )
            return cur.fetchone()

    def get_books(self, skip=0, limit=10):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, title, author, description FROM books ORDER BY id OFFSET %s LIMIT %s;",
                (skip, limit)
            )
            return cur.fetchall()

    def update_book(self, book_id, title=None, author=None, description=None):
        fields = []
        values = []
        if title is not None:
            fields.append('title = %s')
            values.append(title)
        if author is not None:
            fields.append('author = %s')
            values.append(author)
        if description is not None:
            fields.append('description = %s')
            values.append(description)
        if not fields:
            return None
        values.append(book_id)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f"UPDATE books SET {', '.join(fields)} WHERE id = %s RETURNING id, title, author, description;",
                tuple(values)
            )
            self.conn.commit()
            return cur.fetchone()

    def delete_book(self, book_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM books WHERE id = %s;", (book_id,))
            self.conn.commit()

    def close(self):
        self.conn.close()
