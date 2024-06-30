import os

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS") or 'http://localhost:5173&http://127.0.0.1:4040&http://127.0.0.1:5173&http://localhost:4040'
is_development = os.getenv("IS_DEVELOPMENT") == "True"

# Telegram
bot_token = os.getenv("BOT_TOKEN") or ''
my_tg_id = int(os.getenv("MY_TG_ID") or 0)
admin_tg_id = int(os.getenv("ADMIN_TG_ID") or 0)

# Database
db_username = os.getenv(f"DB_USER")
db_password = os.getenv(f"DB_PASSWORD")
db_host = os.getenv(f"DB_HOST")
db_port = int(os.getenv("DB_PORT") or 5432)
db_name = os.getenv(f"DB_NAME")
db_initialized = False
