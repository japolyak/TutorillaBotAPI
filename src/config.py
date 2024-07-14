import os

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS") or 'http://localhost:5173&http://127.0.0.1:4040&http://127.0.0.1:5173&http://localhost:4040'
is_development = os.getenv("IS_DEVELOPMENT") == "True"

# Telegram
bot_token = os.getenv("BOT_TOKEN") or ''
my_tg_id = int(os.getenv("MY_TG_ID") or 0)
admin_tg_id = int(os.getenv("ADMIN_TG_ID") or 0)

# Database
connection_string = os.getenv("CONNECTION_STRING") or ''
db_initialized = False
