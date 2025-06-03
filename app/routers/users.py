from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.user import User, UserCreate
from ..dao.user_dao import UserDAO

router = APIRouter()
user_dao = UserDAO()

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    db_user = user_dao.create_user(username=user.username, email=user.email, is_active=True)
    return User(**db_user)

@router.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    db_users = user_dao.get_users(skip=skip, limit=limit)
    return [User(**u) for u in db_users]

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    db_user = user_dao.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**db_user)

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserCreate):
    db_user = user_dao.update_user(user_id, username=user_update.username, email=user_update.email, is_active=True)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**db_user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    db_user = user_dao.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_dao.delete_user(user_id)
    return
