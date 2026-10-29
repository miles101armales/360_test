from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from app.services.registration import record_start


router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def handle_start(message: Message, funnel_config: dict) -> None:

    telegram_user = message.from_user
    if telegram_user is None:
        return 
    await record_start(telegram_user)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text=funnel_config["messages"]["phone_button"],
                request_contact=True
            )
        ]],
        resize_keyboard=True
    )
    await message.answer(funnel_config["messages"]["greeting"])
    await message.answer(funnel_config["messages"]["phone_request"], reply_markup=keyboard)