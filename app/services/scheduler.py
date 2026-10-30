#TODO: логика планировщика сообщений

import asyncio
from datetime import UTC, datetime
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.database.database import SessionLocal
from app.database.enums import MessageStatusEnum
from app.repository.scheduled_messages import get_due_messages, record_attempt, finish_attempt


logger = logging.getLogger(__name__)


async def run_scheduler(bot: Bot):
	logger.info("Запуск планировщика")
	
	while True:
		now = datetime.now(UTC).replace(tzinfo=None)

		async with SessionLocal.begin() as session:
			logger.info("Поиск запланированных задач в БД")
			scheduled_messages = await get_due_messages(session, now)

		for scheduled_message in scheduled_messages:
			tg_id = scheduled_message["tg_id"]
			step_id = scheduled_message["step_id"]

			async with SessionLocal.begin() as session:
				await record_attempt(session, tg_id, step_id)
			try:
				await bot.send_message(
					chat_id=tg_id,
					text=scheduled_message["text"]
				)
			except TelegramAPIError as exc:
				async with SessionLocal.begin() as session:
					await finish_attempt(
						session, 
						tg_id, 
						step_id,
						MessageStatusEnum.FAILED, 
						sent_at=None,
						last_error=str(exc)
					)
				logger.warning(
					"Ошибка отправки задания %s: %s",
					scheduled_message["id"],
					exc
				)
			else:
				sent_at = datetime.now(UTC).replace(tzinfo=None)
				async with SessionLocal.begin() as session:
					await finish_attempt(
						session, 
						tg_id, 
						step_id,
						MessageStatusEnum.SENT, 
						sent_at,
						last_error=None
					)
				logger.info(
					"Задание %s отправлено!",
					scheduled_message["id"]
				)

		await asyncio.sleep(1)



