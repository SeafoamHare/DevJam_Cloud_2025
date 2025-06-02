# from pydantic import BaseModel
# from typing import Optional

# # Pydantic schemas for User
# class UserBase(BaseModel):
#     email: str
#     name: Optional[str] = None

# class UserCreate(UserBase):
#     # password: str # Add if you are handling password creation
#     pass # No extra fields for now, assuming password handled separately or not at all for simplicity

# class UserUpdate(UserBase):
#     email: Optional[str] = None # Allow email to be optional during update
#     name: Optional[str] = None
#     # is_active: Optional[bool] = None # If you add is_active to your model

# class User(UserBase):
#     id: int
#     # is_active: bool # If you add is_active to your model

#     class Config:
#         orm_mode = True # Changed from from_attributes = True for Pydantic v1 compatibility if needed, orm_mode is more common

# # You can add other schemas here, for example, for Books, Borrows, etc.
# # class BookBase(BaseModel):
# #     title: str
# #     author: Optional[str] = None
# #     isbn: str

# # class BookCreate(BookBase):
# #     pass

# # class Book(BookBase):
# #     id: int
# #     class Config:
# #         orm_mode = True
