from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str  # Stores the hashed password
    organization: Optional[str] = None
    role: Optional[str] = None
    referrer: Optional[str] = None
    points: int = 0
    survey: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # Plain text password for creation
    organization: Optional[str] = None
    role: Optional[str] = None
    referrer: Optional[str] = None
    survey: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
