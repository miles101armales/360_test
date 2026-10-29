from datetime import datetime

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
			"last_activity": datetime.now()
		}
	)

	await session.execute(statement)