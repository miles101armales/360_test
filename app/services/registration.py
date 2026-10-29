from datetime import datetime

from aiogram.types import Contact, User

from app.database.database import SessionLocal
from app.database.repository import upsert_user, set_phone_once


async def record_start(telegram_user: User) -> None:

	async with SessionLocal.begin() as session:
		await upsert_user(session, telegram_user.id, telegram_user.username, telegram_user.full_name, telegram_user.language_code)

async def register_contact(telegram_user: User, telegram_contact: Contact) -> bool:

	async with SessionLocal.begin() as session:
		await upsert_user(session, telegram_user.id, telegram_user.username, telegram_user.full_name, telegram_user.language_code)
		return await set_phone_once(session, telegram_user.id, telegram_contact.phone_number)