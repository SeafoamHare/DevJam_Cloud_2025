# import psycopg2
# import os

# # 可從環境變數載入敏感資訊比較安全
# DB_HOST = os.getenv("DB_HOST")  # Terraform 輸出的IP
# DB_PORT = 5432 # Default PostgreSQL port, can also be an environment variable if it changes
# DB_NAME = os.getenv("DB_NAME")  # Terraform 中 database 名稱
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# try:
#     conn = psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT NOW();")
#     print("Current timestamp:", cur.fetchone())

#     cur.close()
#     conn.close()
# except Exception as e:
#     print("Error connecting to database:", e)
