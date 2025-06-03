from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    available_copies: Optional[int] = 1

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    available_copies: Optional[int] = 1
