from fastapi import FastAPI
from .routers import books, users, transactions
# from .routers import users
from . import database

database.initialize_database()

app = FastAPI()

app.include_router(books.router, prefix="/api/v1", tags=["books"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System API"}
