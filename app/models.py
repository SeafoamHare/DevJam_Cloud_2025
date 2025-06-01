from pydantic import BaseModel
from typing import Optional
from datetime import date

class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_date: Optional[date] = None
    available_copies: int = 1

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: Optional[date] = None
    available_copies: int = 1

class UserCreate(BaseModel):
    username: str
    email: str

class BookBorrowRequest(BaseModel):
    user_id: int
    book_id: int

class BorrowRecord(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: date
    return_date: Optional[date] = None
