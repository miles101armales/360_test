from datetime import datetime, UTC
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.database.enums import MessageStatusEnum, StepEnum

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	tg_id: Mapped[int] = mapped_column(unique=True)
	username: Mapped[str | None]
	fullname: Mapped[str | None]
	phone_number: Mapped[str | None]
	locale: Mapped[str | None]
	created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC).replace(tzinfo=None))
	registered_at: Mapped[datetime | None]
	last_activity: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC).replace(tzinfo=None))

class ScheduledMessage(Base):
	__tablename__ = "scheduled_message"

	id: Mapped[int] = mapped_column(primary_key=True)
	tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), nullable=False)
	step_id: Mapped[StepEnum]
	text: Mapped[str]
	send_at: Mapped[datetime]
	status: Mapped[MessageStatusEnum] = mapped_column(default=MessageStatusEnum.PENDING)
	attempts: Mapped[int] = mapped_column(default=0)
	sent_at: Mapped[datetime | None]
	last_error: Mapped[str | None]

	__table_args__ = (
		UniqueConstraint("tg_id", "step_id", name="uq_recipient_step"),
	)