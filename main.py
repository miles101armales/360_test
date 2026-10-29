import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.database.database import close_db, init_db
from app.handlers.start import router as start_router
from app.settings import BOT_TOKEN
from app.database import models


async def main() -> None:
    try:
        if not BOT_TOKEN:
            raise RuntimeError("Укажи BOT_TOKEN в локальном файле .env")
    
        await init_db()
    
        logging.basicConfig(level=logging.INFO)
        bot = Bot(token=BOT_TOKEN)
        dispatcher = Dispatcher()
        dispatcher.include_router(start_router)
        await dispatcher.start_polling(bot)
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())
