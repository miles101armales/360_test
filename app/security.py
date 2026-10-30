from time import time

from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import HTTPException, Request

from app.settings import ADMIN_IDS, BOT_TOKEN


def require_admin(request: Request) -> bool:
    init_data = request.headers.get("X-Telegram-Init-Data")

    if not init_data:
        raise HTTPException(
            status_code=401,
            detail="Откройте дашборд внутри Telegram",
        )

    try:
        data = safe_parse_webapp_init_data(
            token=BOT_TOKEN,
            init_data=init_data,
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Некорректные данные Telegram",
        ) from None

    age = time() - data.auth_date.timestamp()

    if age < -30 or age > 3600:
        raise HTTPException(
            status_code=401,
            detail="Сессия истекла. Откройте миниапп заново",
        )

    if data.user is None:
        raise HTTPException(status_code=401, detail="Нет данных пользователя")

    if data.user.id not in ADMIN_IDS:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    return True