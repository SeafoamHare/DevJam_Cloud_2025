import sys
import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.routers import books, users, transactions
from app import database

database.initialize_database()

app = FastAPI()

app.include_router(books.router, prefix="/api/v1", tags=["books"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System API"}
