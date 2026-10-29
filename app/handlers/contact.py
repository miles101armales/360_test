#TODO: handler для регистрации номера в БД

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from app.services.registration import register_contact


router = Router()

@router.message(F.contact, F.chat.type == "private")
async def handle_contact(message: Message, funnel_config: dict) -> None:
	telegram_user = message.from_user
	contact = message.contact

	if contact.user_id != telegram_user.id:
		await message.answer(funnel_config["messages"]["invalid_contact"])
		return

	success_registeration = await register_contact(telegram_user, contact)

	reply_markup=ReplyKeyboardRemove()

	if not success_registeration:
		await message.answer(funnel_config["messages"]["already_registered"], reply_markup=reply_markup)
		return
	await message.answer(funnel_config["messages"]["registration_success"], reply_markup=reply_markup)
	return