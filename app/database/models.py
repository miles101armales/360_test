from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	tg_id: Mapped[int] = mapped_column(unique=True)
	username: Mapped[str | None]
	fullname: Mapped[str | None]
	phone_number: Mapped[str | None]
	locale: Mapped[str | None]
	created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
	registered_at: Mapped[datetime | None]
	last_activity: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

	