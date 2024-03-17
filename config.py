import os

telegram_web_app = os.getenv("TELEGRAM_WEB_APP") or ''
bot_token = os.getenv("BOT_TOKEN") or ''

# Database
is_development = bool(os.getenv("IS_DEVELOPMENT"))
db_username = os.getenv(f"DB_USER")
db_password = os.getenv(f"DB_PASSWORD")
db_host = os.getenv(f"DB_HOST")
db_port = int(os.getenv("DB_PORT") or 5432)
db_name = os.getenv(f"DB_NAME")
db_initialized = False
