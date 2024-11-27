from telegram import Update
from telegram.ext import CallbackContext

from data.send_messages import send_message


async def show_menu(update: Update, context: CallbackContext):
    await send_message(update, "")