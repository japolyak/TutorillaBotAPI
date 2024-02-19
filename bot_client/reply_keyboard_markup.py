from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import service_utils
from typing import List


class ReplyKeyboardMarkupCreator:
    @staticmethod
    def main_menu_markup(user) -> ReplyKeyboardMarkup:
        markup = CustomReplyKeyboardMarkup(resize_keyboard=True)

        profile_btn = KeyboardButton(text="Profile")
        support_btn = KeyboardButton(text="Support")
        top_row = []

        if user.is_tutor:
            office_btn = KeyboardButton(text="Office")
            top_row.append(office_btn)

        if user.is_student:
            my_courses_btn = KeyboardButton(text="Classroom")
            top_row.append(my_courses_btn)

        if user.is_admin:
            my_courses_btn = KeyboardButton(text="Admin panel")
            top_row.append(my_courses_btn)

        markup.add_row(top_row)
        markup.add(profile_btn, support_btn)

        return markup


class CustomReplyKeyboardMarkup(ReplyKeyboardMarkup):
    def add_row(self, buttons: List[KeyboardButton], row_width=None):
        if row_width is None:
            row_width = self.row_width

        for row in service_utils.chunks(buttons, row_width):
            button_array = []
            for button in row:
                if service_utils.is_string(button):
                    button_array.append({'text': button})
                elif service_utils.is_bytes(button):
                    button_array.append({'text': button.decode('utf-8')})
                else:
                    button_array.append(button.to_dict())
            self.keyboard.append(button_array)

        return self
