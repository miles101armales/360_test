from datetime import datetime, UTC

from sqlalchemy import update
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User

async def upsert_user(
	session: AsyncSession,
	tg_id: int,
	username: str | None,
	fullname: str| None,
	locale: str | None) -> None:
	
	statement = insert(User).values(
		tg_id=tg_id,
		username=username,
		fullname=fullname,
		locale=locale
	)

	statement = statement.on_conflict_do_update(
		index_elements=[User.tg_id],
		set_={
			"tg_id": tg_id,
			"username": username,
			"fullname": fullname,
			"locale": locale,
			"last_activity": datetime.now(UTC).replace(tzinfo=None)
		}
	)

	await session.execute(statement)

async def set_phone_once(
	session: AsyncSession,
	tg_id: int,
	phone_number: str,
	registered_at: datetime) -> bool:

	statement = update(User).where(
		User.tg_id == tg_id,
		User.registered_at.is_(None)
	).values(
		phone_number=phone_number,
		registered_at=registered_at,
		last_activity=registered_at
	).returning(User.id)

	result = await session.execute(statement)

	success = result.scalar_one_or_none()

	return success is not None