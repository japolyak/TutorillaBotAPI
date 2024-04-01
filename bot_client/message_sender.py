from bot_client.bot_token import bot


def send_decline_message(tg_user_id):
    bot.send_message(chat_id=tg_user_id, text='Not today')


def send_test_message(tg_user_id: int | str):
    bot.send_message(chat_id=tg_user_id, text='Hello there')
