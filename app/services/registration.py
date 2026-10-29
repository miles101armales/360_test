from app.database.database import SessionLocal
from app.database.models import User
from app.database.repository import upsert_user


async def record_start(
		tg_id: int, 
		username: str | None, 
		fullname: str | None, 
		locale: str | None) -> None:
	async with SessionLocal.begin() as session:
		await upsert_user(session, tg_id, username, fullname, locale)