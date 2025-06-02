# from fastapi import FastAPI
# from .database import engine, Base # Assuming Base is defined in database.py or models.py
# from .routers import users # Import the users router
# # from . import models # If Base is in models.py, ensure it's created

# # Create database tables if Base is correctly imported and models are defined
# # models.Base.metadata.create_all(bind=engine) # If Base is in models.py
# Base.metadata.create_all(bind=engine) # If Base is in database.py or imported there

# app = FastAPI()

# app.include_router(users.router) # Include the users router

# @app.get("/")
# async def root():
#     return {"message": "Hello Library Management System"}

# # TODO: 在這裡包含其他路由器 (例如書籍、借閱)
# # TODO: 設定 Firestore 用戶端 (如果尚未在其他地方完成)
# # TODO: 考慮新增錯誤處理、日誌記錄和更進階的組態設定
