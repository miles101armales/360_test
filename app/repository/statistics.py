from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import ScheduledMessage, User


async def users_stats(session: AsyncSession) -> dict:
	statement = select(
		func.count(User.id).label("total_users"),
		func.count(User.registered_at).label("registered_users")
	)

	result = await session.execute(statement)
	return dict(result.mappings().one())

async def messages_stats(session: AsyncSession) -> dict:
	statement = select(
		ScheduledMessage.status,
		func.count(ScheduledMessage.id)
	).group_by(
		ScheduledMessage.status
	)

	result = await session.execute(statement)

	return {
		status.value: count
		for status, count in result.all()
	}