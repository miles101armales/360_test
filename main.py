import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.start import router as start_router
from app.services.settings import BOT_TOKEN


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Укажи BOT_TOKEN в локальном файле .env")

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_router(start_router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
