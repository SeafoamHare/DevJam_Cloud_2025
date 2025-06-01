from fastapi import APIRouter, HTTPException, status
from typing import List
from .. import models

router = APIRouter()

fake_books_db = []
next_book_id = 1

@router.post("/books/", response_model=models.Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: models.BookCreate):
    global next_book_id
    new_book = models.Book(id=next_book_id, **book.dict())
    fake_books_db.append(new_book)
    next_book_id += 1
    return new_book

@router.get("/books/", response_model=List[models.Book])
async def read_books(skip: int = 0, limit: int = 10):
    return fake_books_db[skip : skip + limit]

@router.get("/books/{book_id}", response_model=models.Book)
async def read_book(book_id: int):
    for book_in_db in fake_books_db:
        if book_in_db.id == book_id:
            return book_in_db
    raise HTTPException(status_code=404, detail="Book not found")

@router.put("/books/{book_id}", response_model=models.Book)
async def update_book(book_id: int, book_update: models.BookCreate):
    for idx, book_in_db in enumerate(fake_books_db):
        if book_in_db.id == book_id:
            updated_book = book_in_db.copy(update=book_update.dict(exclude_unset=True))
            fake_books_db[idx] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    global fake_books_db
    book_to_delete = None
    for book_in_db in fake_books_db:
        if book_in_db.id == book_id:
            book_to_delete = book_in_db
            break
    if book_to_delete:
        fake_books_db.remove(book_to_delete)
        return
    raise HTTPException(status_code=404, detail="Book not found")
