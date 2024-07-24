import os
from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "DEBUG")

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173&http://127.0.0.1:4040&http://127.0.0.1:5173&http://localhost:4040").split('&')
is_development = os.getenv("IS_DEVELOPMENT", "False") == "True"

# Telegram
bot_token = os.getenv("BOT_TOKEN", "")
my_tg_id = int(os.getenv("MY_TG_ID", 0))
admin_tg_id = int(os.getenv("ADMIN_TG_ID", 0))

# Database
_database_username = os.getenv(f"DB_USER")
_database_password = os.getenv(f"DB_PASSWORD")
database_host = os.getenv(f"DB_HOST")
database_port = int(os.getenv("DB_PORT") or 5432)
database_name = os.getenv(f"DB_NAME")
sqlalchemy_database_url = f"postgresql+psycopg2://{_database_username}:{_database_password}@{database_host}:{database_port}/{database_name}"
