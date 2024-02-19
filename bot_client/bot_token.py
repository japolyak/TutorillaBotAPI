import telebot
from config import bot_token

bot = telebot.TeleBot(token=bot_token, threaded=False)
