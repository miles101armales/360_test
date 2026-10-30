from datetime import datetime, UTC, timedelta

from aiogram.types import Contact, User

from app.database.database import SessionLocal
from app.repository.scheduled_messages import create_scheduled_messages
from app.repository.users import upsert_user, set_phone_once


async def record_start(telegram_user: User) -> None:

	async with SessionLocal.begin() as session:
		await upsert_user(
			session, 
			telegram_user.id, 
			telegram_user.username,
			telegram_user.full_name, 
			telegram_user.language_code
		)

async def register_contact(telegram_user: User, telegram_contact: Contact, steps: list[dict]) -> bool:

	async with SessionLocal.begin() as session:
		await upsert_user(
			session, 
			telegram_user.id, 
			telegram_user.username, 
			telegram_user.full_name, 
			telegram_user.language_code
		)

		registered_datetime = datetime.now(UTC).replace(tzinfo=None)
		
		success_registeration = await set_phone_once(session, telegram_user.id, telegram_contact.phone_number, registered_datetime)
		
		if not success_registeration:
			return False

		for step in steps:
			messages_data = {
				"tg_id": telegram_user.id,
				"id": step["id"],
				"delay_seconds": step["delay_seconds"],
				"text": step["text"],
				"send_at": registered_datetime + timedelta(seconds=step["delay_seconds"])
			}
			await create_scheduled_messages(session, messages_data)

		return True