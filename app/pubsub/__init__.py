from google.cloud import pubsub_v1
import asyncio
import os
from fastapi import WebSocket
from dotenv import load_dotenv

load_dotenv()

# 全域 event loop（讓 callback thread 能存取）
event_loop = asyncio.get_event_loop()

async def listen_pubsub(user_id: int, websocket: WebSocket):
    print('🔄 開始監聽 Pub/Sub 訊息')
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_SUBSCRIPTION_NAME")  # e.g. white-board-sub
    )

    def callback(message):
        try:
            data = message.data.decode("utf-8")

            # 使用 run_coroutine_threadsafe 將 coroutine 丟回 asyncio 的主 loop
            future = asyncio.run_coroutine_threadsafe(
                websocket.send_text(f"📩 PubSub: {data}"),
                event_loop
            )
            future.result()  # 可選：等待傳送完成

            message.ack()
        except Exception as e:
            print(f"❌ 發送 PubSub 訊息錯誤：{e}")
            message.nack()

    subscriber.subscribe(subscription_path, callback=callback)
    print(f"✅ 開始監聽 Pub/Sub 訂閱 {subscription_path}")

    await asyncio.Event().wait()  # 防止協程提前結束
