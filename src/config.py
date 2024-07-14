import os
from dotenv import load_dotenv

load_dotenv()

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173&http://127.0.0.1:4040&http://127.0.0.1:5173&http://localhost:4040")
is_development = os.getenv("IS_DEVELOPMENT", "False") == "True"

# Telegram
bot_token = os.getenv("BOT_TOKEN", "")
my_tg_id = int(os.getenv("MY_TG_ID", 0))
admin_tg_id = int(os.getenv("ADMIN_TG_ID", 0))

# Database
connection_string = os.getenv("CONNECTION_STRING", "")
db_username = os.getenv(f"DB_USER")
db_password = os.getenv(f"DB_PASSWORD")
db_host = os.getenv(f"DB_HOST")
db_port = int(os.getenv("DB_PORT") or 5432)
db_name = os.getenv(f"DB_NAME")
