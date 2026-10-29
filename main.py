import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.database.database import close_db, init_db
from app.handlers.start import router as start_router
from app.handlers.contact import router as contact_router
from app.settings import BOT_TOKEN, load_funnel_config
from app.database import models


async def main() -> None:
    try:
        if not BOT_TOKEN:
            raise RuntimeError("Укажи BOT_TOKEN в локальном файле .env")
    
        await init_db()
        funnel_config = await asyncio.to_thread(load_funnel_config)
    
        logging.basicConfig(level=logging.INFO)
        bot = Bot(token=BOT_TOKEN)
        dispatcher = Dispatcher()
        dispatcher.include_routers(start_router, contact_router)
        dispatcher["funnel_config"] = funnel_config
        await dispatcher.start_polling(bot)
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())
