from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import date
from ..models.borrow import BorrowRecord, BookBorrowRequest
from ..dao.borrow_dao import BorrowDAO
from ..dao.user_dao import UserDAO
from ..dao.books_dao import BookDAO
from ..vertex_ai_example import generate_book_recommendation

router = APIRouter()
borrow_dao = BorrowDAO()
user_dao = UserDAO()
book_dao = BookDAO()

@router.post("/borrow/", response_model=BorrowRecord, status_code=status.HTTP_201_CREATED)
async def borrow_book(borrow_request: BookBorrowRequest):
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
    return BorrowRecord(**db_record)

@router.post("/return/{borrow_id}/", response_model=BorrowRecord)
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
    return BorrowRecord(**updated_record)

@router.get("/borrow/records/", response_model=List[BorrowRecord])
async def get_all_borrow_records(skip: int = 0, limit: int = 100):
    db_records = borrow_dao.get_borrow_records(skip=skip, limit=limit)
    return [BorrowRecord(**r) for r in db_records]

@router.get("/borrow/records/user/{user_id}", response_model=List[BorrowRecord])
async def get_user_borrow_records(user_id: int):
    user = user_dao.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    records = borrow_dao.get_user_borrow_records(user_id)
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No borrow records found for this user")
    return [BorrowRecord(**r) for r in records]

@router.get("/recommendations/{user_id}", response_model=List[str])
async def get_book_recommendations(user_id: int):
    user = user_dao.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    borrow_records = borrow_dao.get_user_borrow_records(user_id)
    borrowed_book_titles = []
    if borrow_records:
        for record in borrow_records:
            book = book_dao.get_book(record["book_id"])
            if book:
                borrowed_book_titles.append(book["title"])

    all_books = book_dao.get_books(limit=1000)  # Fetch a large number of books
    available_book_titles = [book["title"] for book in all_books if book.get("available_copies", 0) > 0]

    if not available_book_titles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books currently available in the library.")

    # If the user has no borrowing history, we can recommend popular books or new additions
    # For this example, we'll return a subset of available books if no history
    if not borrowed_book_titles:
        # Potentially, call a different Vertex AI function for general recommendations
        # For now, let's return a few available books or an empty list
        # return available_book_titles[:3] # Or handle as a special case
        # Or, inform that recommendations are based on borrowing history which is empty
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No borrowing history to base recommendations on. Here are some available books.", headers={"X-Recommendation-Type": "general"})


    recommendations = generate_book_recommendation(borrowed_book_titles, available_book_titles)

    if not recommendations:
        # This case means Vertex AI returned no specific recommendations based on history
        # We could return a generic list or a specific message
        # For example, return a few generally popular available books
        # return available_book_titles[:3] # Example: return first 3 available books
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Could not generate specific recommendations. Here are some available books.", headers={"X-Recommendation-Type": "general_fallback"})

    return recommendations
