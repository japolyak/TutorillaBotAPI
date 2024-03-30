from bot_client.bot_token import bot
from bot_client.reply_keyboard_markup import ReplyKeyboardMarkupCreator


def send_accept_message(user):
    markup = ReplyKeyboardMarkupCreator.main_menu_markup(user=user)
    bot.send_message(chat_id=user.id, text='Welcome', reply_markup=markup)


def send_decline_message(tg_user_id):
    bot.send_message(chat_id=tg_user_id, text='Not today')


def send_test_message(tg_user_id: int | str):
    bot.send_message(chat_id=tg_user_id, text='Hello there')
