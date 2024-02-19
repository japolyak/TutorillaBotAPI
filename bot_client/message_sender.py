from bot_client.bot_token import bot
from bot_client.reply_keyboard_markup import ReplyKeyboardMarkupCreator


def send_accept_message(user):
    markup = ReplyKeyboardMarkupCreator.main_menu_markup(user=user)
    bot.send_message(chat_id=user.id, text='Welcome', reply_markup=markup)


def send_decline_message(user):
    bot.send_message(chat_id=user.id, text='Not today')
