from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext

from data.send_messages import send_message
from handlers.client.functions import register_user
from handlers.client.keyboards import menu_keyboard


async def register(update: Update, context: CallbackContext):
    user = update.effective_user
    if register_user(user.id, user.first_name, user.last_name, user.username, update.message.contact.phone_number):
        await send_message(update, "Вы успешно зарегистрировались", markup=menu_keyboard)
    else:
        await send_message(update, "Вы уже были зарегистрированы", markup=menu_keyboard)


register_handler = MessageHandler(filters.CONTACT, register)