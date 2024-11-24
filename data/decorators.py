from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from data.checks_for_role import check_is_admin, check_is_register
from data.messages.client import access_lock_message
from data.send_messages import send_message


def its_admin(function_to_decorate):
    async def check_admin(update: Update, context: CallbackContext):
        if check_is_admin(update.effective_user.id):
            return await function_to_decorate(update, context)
        else:
            sent_message = access_lock_message
            await send_message(update, sent_message)
            return ConversationHandler.END

    return check_admin

def its_register_user(function_to_decorate):
    async def check_register(update: Update, context: CallbackContext, *args, **kwargs):
        if check_is_register(update.effective_user.id):
            return await function_to_decorate(update, context, *args, **kwargs)
        else:
            sent_message = access_lock_message
            await send_message(update, sent_message)
            return ConversationHandler.END

    return check_register


