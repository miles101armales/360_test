import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import yaml


BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
ADMIN_IDS = {
	int(value.strip())
	for value in os.getenv("ADMIN_IDS", "").split(",")
	if value.strip()
}

def load_funnel_config() -> dict:
	
	with (BASE_DIR / "config.yaml").open("r", encoding="utf-8") as file:
		config_dict = yaml.safe_load(file)
	
	if not isinstance(config_dict, dict):
		raise ValueError(f"Конфигураця должна быть словарем: {config_dict}")
	
	if "messages" not in config_dict or "steps" not in config_dict:
		raise ValueError("Конфигурация должен содержать ключи `messages` и `steps`")

	return config_dict