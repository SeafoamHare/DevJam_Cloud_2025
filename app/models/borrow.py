from pydantic import BaseModel
from typing import Optional
from datetime import date

class BorrowRecord(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: date
    return_date: Optional[date] = None

class BookBorrowRequest(BaseModel):
    user_id: int
    book_id: int
