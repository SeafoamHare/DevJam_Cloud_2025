# from fastapi import APIRouter, HTTPException, status, Depends
# from typing import List
# from sqlalchemy.orm import Session
# from .. import models, schemas  # Assuming schemas.py contains Pydantic models for request/response
# from ..database import get_db
# # from passlib.context import CryptContext # For password hashing if you add it

# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Example for password hashing

# router = APIRouter(
#     prefix="/users",
#     tags=["users"]
# )

# @router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)  # Changed path to /
# async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # hashed_password = pwd_context.hash(user.password) # Example if hashing password
#     # db_user = models.User(email=user.email, hashed_password=hashed_password, name=user.name)
#     db_user = models.User(**user.dict())  # Assuming your User model matches UserCreate directly for now
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.get("/", response_model=List[schemas.User])  # Changed path to /
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = db.query(models.User).offset(skip).limit(limit).all()
#     return users

# @router.get("/{user_id}", response_model=schemas.User)
# async def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.put("/{user_id}", response_model=schemas.User)
# async def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     update_data = user_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_user, key, value)
        
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(db_user)
#     db.commit()
#     return

# # TODO: 考慮為書籍資訊 (Cloud SQL) 和借閱紀錄 (Cloud SQL) 建立類似的路由器。
# # TODO: 考慮為使用者偏好 (Firestore)、即時評論 (Firestore)、書籍標籤 (Firestore) 建立路由器或服務層。
