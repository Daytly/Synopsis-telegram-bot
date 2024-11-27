from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from data.callbacks import add_note_callback, view_topic_callback, exit_note_callback


def create_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("Загрузить конспект", callback_data=add_note_callback)],
        [InlineKeyboardButton("Открыть конспект", callback_data=view_topic_callback)],
        [InlineKeyboardButton("Выйти", callback_data=exit_note_callback)],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
