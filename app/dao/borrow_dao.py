import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import get_connection

class BorrowDAO:
    def __init__(self):
        self.conn = get_connection()

    def create_borrow_record(self, user_id, book_id, borrow_date):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO borrow_records (user_id, book_id, borrow_date)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, book_id, borrow_date, return_date;
                """,
                (user_id, book_id, borrow_date)
            )
            self.conn.commit()
            return cur.fetchone()

    def return_book(self, borrow_id, return_date):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE borrow_records
                SET return_date = %s
                WHERE id = %s AND return_date IS NULL
                RETURNING id, user_id, book_id, borrow_date, return_date;
                """,
                (return_date, borrow_id)
            )
            self.conn.commit()
            return cur.fetchone()

    def get_borrow_record(self, borrow_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, user_id, book_id, borrow_date, return_date FROM borrow_records WHERE id = %s;",
                (borrow_id,)
            )
            return cur.fetchone()

    def get_borrow_records(self, skip=0, limit=100):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, user_id, book_id, borrow_date, return_date FROM borrow_records ORDER BY id OFFSET %s LIMIT %s;",
                (skip, limit)
            )
            return cur.fetchall()

    def get_user_borrow_records(self, user_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, user_id, book_id, borrow_date, return_date FROM borrow_records WHERE user_id = %s ORDER BY id;",
                (user_id,)
            )
            return cur.fetchall()

    def close(self):
        self.conn.close()
