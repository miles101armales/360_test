from datetime import datetime, UTC

from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import MessageStatusEnum, StepEnum
from app.database.models import ScheduledMessage


async def create_scheduled_messages(session: AsyncSession, messages_data: dict) -> None:
	statement = insert(ScheduledMessage).values(
		tg_id=messages_data["tg_id"],
		step_id=messages_data["id"],
		text=messages_data["text"],
		send_at=messages_data["send_at"],
		status=MessageStatusEnum.PENDING,
		attempts=0,
		sent_at=None,
		last_error=None
	)

	await session.execute(statement)

async def get_due_messages(session: AsyncSession, now: datetime) -> list[dict]:
	statement = select(
		ScheduledMessage.id,
		ScheduledMessage.tg_id,
		ScheduledMessage.step_id,
		ScheduledMessage.text,
		ScheduledMessage.send_at
	).where(
		ScheduledMessage.status == MessageStatusEnum.PENDING,
		ScheduledMessage.send_at <= now
	).order_by(
		ScheduledMessage.send_at
	).limit(50)

	result = await session.execute(statement)
	return [dict(row) for row in result.mappings().all()]

async def record_attempt(session: AsyncSession, tg_id: int, step_id: StepEnum) -> None:
	statement = update(ScheduledMessage).where(
		ScheduledMessage.tg_id == tg_id,
		ScheduledMessage.step_id == step_id
	).values(
		attempts = ScheduledMessage.attempts + 1
	)

	await session.execute(statement)

async def finish_attempt(
	session: AsyncSession, 
	tg_id: int, 
	step_id: StepEnum,
	status: MessageStatusEnum, 
	sent_at: datetime | None, 
	last_error: str| None) -> None:

	if status not in (
		MessageStatusEnum.SENT,
		MessageStatusEnum.FAILED
	):
		raise ValueError("Ожидается статус SENT или FAILED")

	statement = update(ScheduledMessage).where(
		ScheduledMessage.tg_id == tg_id,
		ScheduledMessage.step_id == step_id
	).values(
		status=status,
		sent_at=sent_at,
		last_error=last_error
	)

	await session.execute(statement)