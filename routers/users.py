from fastapi import APIRouter, HTTPException, status
from typing import List
import models # Use relative import for models

router = APIRouter()

# In-memory storage for users (replace with database later)
fake_users_db = []
next_user_id = 1

@router.post("/users/", response_model=models.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: models.UserCreate):
    global next_user_id
    new_user = models.User(id=next_user_id, **user.dict(), is_active=True)
    fake_users_db.append(new_user)
    next_user_id += 1
    return new_user

@router.get("/users/", response_model=List[models.User])
async def read_users(skip: int = 0, limit: int = 10):
    return fake_users_db[skip : skip + limit]

@router.get("/users/{user_id}", response_model=models.User)
async def read_user(user_id: int):
    for user_in_db in fake_users_db:
        if user_in_db.id == user_id:
            return user_in_db
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=models.User)
async def update_user(user_id: int, user_update: models.UserCreate):
    for idx, user_in_db in enumerate(fake_users_db):
        if user_in_db.id == user_id:
            # Update existing user fields, keep is_active as is unless specified
            updated_user_data = user_in_db.dict()
            updated_user_data.update(user_update.dict(exclude_unset=True))
            updated_user = models.User(**updated_user_data)
            fake_users_db[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    global fake_users_db
    user_to_delete = None
    for user_in_db in fake_users_db:
        if user_in_db.id == user_id:
            user_to_delete = user_in_db
            break
    if user_to_delete:
        fake_users_db.remove(user_to_delete)
        return
    raise HTTPException(status_code=404, detail="User not found")
