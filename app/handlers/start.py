from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.services.registration import record_start


router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:

    telegram_user = message.from_user
    if telegram_user is None:
        return 
    await record_start(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        fullname=message.from_user.full_name,
        locale=message.from_user.language_code
    )
    await message.answer(f"Здравствуйте, {message.from_user.full_name}")