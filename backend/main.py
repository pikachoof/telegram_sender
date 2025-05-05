from telethon import TelegramClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from contextlib import asynccontextmanager

phone_number = '77054093667'
api_id = 28685416
api_hash = '3cb68c7edad94ad4e0cd8c5a150f3837'
session_name = 'Pikachoof_Session'

client = TelegramClient(session_name, api_id, api_hash)
user_id: int = None

class MessageRequest(BaseModel):
    text: str

class TelegramState:
    user_id: int = None

telegram_state = TelegramState()

async def connect_client(state: TelegramState):
    try:
        await client.start(phone=phone_number, password=input('Enter your Telegram password (if any): '), code_callback=lambda: input('Enter the code you received: '))
        me = await client.get_me()
        print(f"Logged in as {me.first_name} (ID: {me.id})")
        state.user_id = me.id
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        raise

async def disconnect_client():
    if await client.is_connected():
        await client.disconnect()
    print("Telegram client disconnected.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_client(telegram_state)
    yield
    await disconnect_client()

app = FastAPI(lifespan=lifespan)

origins = ["null"] # NOT recommended - need to fix

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send_to_saved")
async def send_to_saved(message_request: MessageRequest):
    if telegram_state.user_id is None:
        raise HTTPException(status_code=503, detail="Telegram client not initialized.")
    try:
        await client.send_message('me', message_request.text)
        return {"status": "success", "message": "Sent to Saved Messages"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    async def main():
        config = uvicorn.Config(app=app, host="0.0.0.0", port=5000)
        server = uvicorn.Server(config)
        await server.serve()
    asyncio.run(main())