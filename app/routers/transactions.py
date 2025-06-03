from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import date
from .. import models
from ..dao.borrow_dao import BorrowDAO
from ..dao.user_dao import UserDAO
from ..dao.books_dao import BookDAO

router = APIRouter()
borrow_dao = BorrowDAO()
user_dao = UserDAO()
book_dao = BookDAO()

@router.post("/borrow/", response_model=models.BorrowRecord, status_code=status.HTTP_201_CREATED)
async def borrow_book(borrow_request: models.BookBorrowRequest):
    user = user_dao.get_user(borrow_request.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user["is_active"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is inactive")

    book = book_dao.get_book(borrow_request.book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.get("available_copies", 1) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not available")

    # 檢查是否已借未還
    records = borrow_dao.get_user_borrow_records(borrow_request.user_id)
    for record in records:
        if record["book_id"] == borrow_request.book_id and record["return_date"] is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already borrowed this book and not returned it yet")

    # 更新書籍可借數量
    book_dao.update_book(borrow_request.book_id, available_copies=book.get("available_copies", 1) - 1)

    db_record = borrow_dao.create_borrow_record(
        user_id=borrow_request.user_id,
        book_id=borrow_request.book_id,
        borrow_date=date.today()
    )
    return models.BorrowRecord(**db_record)

@router.post("/return/{borrow_id}/", response_model=models.BorrowRecord)
async def return_book(borrow_id: int):
    borrow_record = borrow_dao.get_borrow_record(borrow_id)
    if not borrow_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    if borrow_record["return_date"] is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already returned")

    book = book_dao.get_book(borrow_record["book_id"])
    if not book:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Book associated with record not found")

    # 更新書籍可借數量
    book_dao.update_book(borrow_record["book_id"], available_copies=book.get("available_copies", 0) + 1)

    updated_record = borrow_dao.return_book(borrow_id, return_date=date.today())
    return models.BorrowRecord(**updated_record)

@router.get("/borrow/records/", response_model=List[models.BorrowRecord])
async def get_all_borrow_records(skip: int = 0, limit: int = 100):
    db_records = borrow_dao.get_borrow_records(skip=skip, limit=limit)
    return [models.BorrowRecord(**r) for r in db_records]

@router.get("/borrow/records/user/{user_id}", response_model=List[models.BorrowRecord])
async def get_user_borrow_records(user_id: int):
    user = user_dao.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    records = borrow_dao.get_user_borrow_records(user_id)
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No borrow records found for this user")
    return [models.BorrowRecord(**r) for r in records]
