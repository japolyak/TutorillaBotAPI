import os

telegram_web_app = os.getenv("TELEGRAM_WEB_APP") or ''
telegram_bot = os.getenv("TELEGRAM_BOT") or ''
bot_token = os.getenv("BOT_TOKEN") or ''

# Database
debug = bool(os.getenv(f"DEBUG"))
suffix = "_LOCAL" if debug else ""
db_username = os.getenv(f"DB_USER{suffix}")
db_password = os.getenv(f"DB_PASSWORD{suffix}")
db_host = os.getenv(f"DB_HOST{suffix}")
db_port = int(os.getenv("DB_PORT") or 5432)
db_name = os.getenv(f"DB_NAME{suffix}")
