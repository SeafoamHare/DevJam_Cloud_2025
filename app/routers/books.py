from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.book import Book, BookCreate
from app.dao.books_dao import BookDAO

router = APIRouter()
book_dao = BookDAO()

@router.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    db_book = book_dao.create_book(title=book.title, author=book.author, description=book.description)
    return Book(**db_book)

@router.get("/books/", response_model=List[Book])
async def read_books(skip: int = 0, limit: int = 10):
    db_books = book_dao.get_books(skip=skip, limit=limit)
    return [Book(**b) for b in db_books]

@router.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int):
    db_book = book_dao.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**db_book)

@router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: BookCreate):
    db_book = book_dao.update_book(book_id, title=book_update.title, author=book_update.author, description=book_update.description)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**db_book)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    db_book = book_dao.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_dao.delete_book(book_id)
    return
