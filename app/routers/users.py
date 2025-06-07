from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..models.user_model import User, UserCreate, UserLogin # Add UserLogin
from ..dao.user_dao import UserDAO
# from ..utils.security import get_password_hash, verify_password, create_access_token # Add security utils
from datetime import timedelta

router = APIRouter()
user_dao = UserDAO()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # hashed_password = get_password_hash(user.password)
    db_user = user_dao.create_user(
        username=user.username, 
        email=user.email, 
        password=user.password,  # Assuming password is plain text and hashed by DAO or DB
        organization=user.organization,
        role=user.role,
        referrer=user.referrer,
        survey=user.survey
    )
    return User(**db_user)

@router.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    db_users = user_dao.get_users(skip=skip, limit=limit)
    return [User(**u) for u in db_users]

@router.get("/users/{username}", response_model=User) # Changed user_id to username
async def read_user(username: str): # Changed user_id to username
    db_user = user_dao.get_user(username) # Changed user_id to username
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**db_user)

@router.put("/users/{username}", response_model=User) # Changed user_id to username
async def update_user(username: str, user_update: UserCreate): # Changed user_id to username
    # hashed_password = get_password_hash(user_update.password) if user_update.password else None
    # Note: user_update.username is ignored here as username is the key and shouldn't be changed via this endpoint
    db_user = user_dao.update_user(
        username, # Pass username as the key
        email=user_update.email,
        password=user_update.password, # Assuming password is plain text and hashed by DAO or DB
        organization=user_update.organization,
        role=user_update.role,
        referrer=user_update.referrer,
        survey=user_update.survey
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**db_user)

@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT) # Changed user_id to username
async def delete_user(username: str): # Changed user_id to username
    db_user = user_dao.get_user(username) # Changed user_id to username
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_dao.delete_user(username) # Changed user_id to username
    return

@router.post("/login/token")
async def login(form_data: UserLogin):
    user = user_dao.get_user_by_username(form_data.username)
    if not user or form_data.password != user['password']: # Changed from hashed_password to password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user['username']}, expires_delta=access_token_expires
    # )
    return {"success": True}
