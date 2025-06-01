from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import date
import models
from routers.books import fake_books_db  # Assuming books router manages this
from routers.users import fake_users_db  # Assuming users router manages this

router = APIRouter()

# In-memory storage for borrow records (replace with database later)
fake_borrow_records_db: List[models.BorrowRecord] = []
next_borrow_id = 1

def find_book_by_id(book_id: int):
    for book in fake_books_db:
        if book.id == book_id:
            return book
    return None

def find_user_by_id(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user
    return None

@router.post("/borrow/", response_model=models.BorrowRecord, status_code=status.HTTP_201_CREATED)
async def borrow_book(borrow_request: models.BookBorrowRequest):
    global next_borrow_id
    user = find_user_by_id(borrow_request.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is inactive")

    book = find_book_by_id(borrow_request.book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not available")

    # Check if user already borrowed this specific book and hasn't returned it
    for record in fake_borrow_records_db:
        if record.user_id == borrow_request.user_id and record.book_id == borrow_request.book_id and record.return_date is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already borrowed this book and not returned it yet")

    book.available_copies -= 1
    
    new_borrow_record = models.BorrowRecord(
        id=next_borrow_id,
        user_id=borrow_request.user_id,
        book_id=borrow_request.book_id,
        borrow_date=date.today()
    )
    fake_borrow_records_db.append(new_borrow_record)
    next_borrow_id += 1
    return new_borrow_record

@router.post("/return/{borrow_id}/", response_model=models.BorrowRecord)
async def return_book(borrow_id: int):
    borrow_record = None
    for record in fake_borrow_records_db:
        if record.id == borrow_id:
            borrow_record = record
            break
    
    if not borrow_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    if borrow_record.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already returned")

    book = find_book_by_id(borrow_record.book_id)
    if not book:
        # This should ideally not happen if data integrity is maintained
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Book associated with record not found")

    book.available_copies += 1
    borrow_record.return_date = date.today()
    return borrow_record

@router.get("/borrow/records/", response_model=List[models.BorrowRecord])
async def get_all_borrow_records(skip: int = 0, limit: int = 100):
    return fake_borrow_records_db[skip : skip + limit]

@router.get("/borrow/records/user/{user_id}", response_model=List[models.BorrowRecord])
async def get_user_borrow_records(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    records = [record for record in fake_borrow_records_db if record.user_id == user_id]
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No borrow records found for this user")
    return records
