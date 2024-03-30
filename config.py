import os

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS") or ''

# Telegram
bot_token = os.getenv("BOT_TOKEN") or ''
my_tg_id = int(os.getenv("MY_TG_ID") or 0)
admin_tg_id = int(os.getenv("ADMIN_TG_ID") or 0)

# Database
is_development = bool(os.getenv("IS_DEVELOPMENT"))
db_username = os.getenv(f"DB_USER")
db_password = os.getenv(f"DB_PASSWORD")
db_host = os.getenv(f"DB_HOST")
db_port = int(os.getenv("DB_PORT") or 5432)
db_name = os.getenv(f"DB_NAME")
db_initialized = False
