from app.database.database import SessionLocal
from app.database.enums import MessageStatusEnum
from app.repository.statistics import users_stats, messages_stats


async def get_statistics() -> dict:
	async with SessionLocal.begin() as session:
		users_stats_dict = await users_stats(session)
		total_users = users_stats_dict["total_users"]
		registered_users = users_stats_dict["registered_users"]
		messages_stats_dict = await messages_stats(session)
		sent_messages = messages_stats_dict.get(MessageStatusEnum.SENT, 0)
		failed_messages = messages_stats_dict.get(MessageStatusEnum.FAILED, 0)
		pending_messages = messages_stats_dict.get(MessageStatusEnum.PENDING, 0)
		processed_messages = sent_messages + failed_messages

		users_conversion = (
			round(registered_users / total_users * 100, 2)
			if total_users
			else 0.0
		)

		msg_conversion = (
			round(sent_messages / processed_messages * 100, 2)
			if processed_messages
			else None
		)

		return {
			"total_users": total_users,
			"registered_users": registered_users,
			"sent_messages": sent_messages,
			"failed_messages": failed_messages,
			"pending_messages": pending_messages,
			"users_conversion": users_conversion,
			"msg_conversion": msg_conversion
		}