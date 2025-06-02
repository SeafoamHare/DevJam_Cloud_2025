# from pydantic import BaseModel, EmailStr
# from typing import Optional, List
# from datetime import date
# from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey # Added SQLAlchemy components
# from sqlalchemy.orm import relationship # Added relationship
# # from ..database import Base # Import Base from the new database.py

# # Pydantic models (remain mostly the same for request/response validation)

# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     # is_active: bool = True # is_active will be handled by DB model default or logic

# class UserCreate(UserBase):
#     password: str # Assuming password is required on creation

# class User(UserBase):
#     id: int
#     is_active: bool

#     class Config:
#         orm_mode = True

# # SQLAlchemy models for Cloud SQL (PostgreSQL)

# class DBUser(Base): # Renamed from UserInDB to DBUser for clarity, inherits from Base
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String) # Store hashed password
#     is_active = Column(Boolean, default=True)

#     # Relationships (example, if you have borrowing records linked to users)
#     # borrowing_records = relationship("DBBorrowingRecord", back_populates="user")

# class DBBook(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     author = Column(String, index=True)
#     isbn = Column(String, unique=True, index=True, nullable=True)
#     published_year = Column(Integer, nullable=True) # Changed from published_date to published_year to match previous Pydantic
#     copies_available = Column(Integer, default=1)

#     # borrowing_records = relationship("DBBorrowingRecord", back_populates="book")

# class DBBorrowingRecord(Base):
#     __tablename__ = "borrowing_records"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     book_id = Column(Integer, ForeignKey("books.id"))
#     borrow_date = Column(Date) # Using Date type
#     due_date = Column(Date)
#     return_date = Column(Date, nullable=True)
#     returned = Column(Boolean, default=False)

#     # user = relationship("DBUser", back_populates="borrowing_records")
#     # book = relationship("DBBook", back_populates="borrowing_records")


# # Pydantic models for request/response - these might need adjustment based on DB models

# class BookBase(BaseModel):
#     title: str
#     author: str
#     isbn: Optional[str] = None
#     published_year: Optional[int] = None
#     copies_available: int = 1

# class BookCreate(BookBase):
#     pass

# class Book(BookBase):
#     id: int

#     class Config:
#         orm_mode = True

# class BorrowingRecordBase(BaseModel):
#     user_id: int
#     book_id: int
#     # due_date: date # Pydantic model should align with DB model

# class BorrowingRecordCreate(BorrowingRecordBase):
#     pass

# class BorrowingRecord(BorrowingRecordBase):
#     id: int
#     borrow_date: date
#     return_date: Optional[date] = None
#     # returned: bool # Add if needed in response

#     class Config:
#         orm_mode = True

# # Firestore Models (Pydantic) - these remain as they are not SQLAlchemy-based

# class UserPreferenceBase(BaseModel):
#     # user_id: int # This might be a string if it's the Firestore document ID itself
#     preferred_genres: Optional[List[str]] = None
#     notification_settings: Optional[dict] = None

# class UserPreferenceCreate(UserPreferenceBase):
#     pass

# class UserPreference(UserPreferenceBase):
#     id: str # Firestore document ID
#     user_id: str # Or int, depending on your design

#     class Config:
#         orm_mode = True

# class ReviewBase(BaseModel):
#     book_id: str # Or int
#     user_id: str # Or int
#     rating: int
#     comment: Optional[str] = None

# class ReviewCreate(ReviewBase):
#     pass

# class Review(ReviewBase):
#     id: str # Firestore document ID
#     timestamp: str # Consider datetime

#     class Config:
#         orm_mode = True

# class TagBase(BaseModel):
#     name: str

# class TagCreate(TagBase):
#     pass

# class Tag(TagBase):
#     id: str # Firestore document ID or unique name

#     class Config:
#         orm_mode = True

# from sqlalchemy import Column, Integer, String, Boolean # Add Boolean if you have is_active
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     name = Column(String)
#     # hashed_password = Column(String, nullable=False) # If you implement password hashing
#     # is_active = Column(Boolean, default=True) # Optional: if you want to activate/deactivate users

# # You can add other models here, for example, for Books, Borrows, etc.
# # class Book(Base):
# #     __tablename__ = "books"
# #     id = Column(Integer, primary_key=True, index=True)
# #     title = Column(String, index=True)
# #     author = Column(String)
# #     isbn = Column(String, unique=True, index=True)
# #     # Add relationships if needed, e.g., to a Borrow model
