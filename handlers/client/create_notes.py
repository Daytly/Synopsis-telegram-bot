import datetime
import os

from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, \
    filters

from data.callback_patterns import add_note_pattern, create_note_topic_pattern
from data.callbacks import add_note_callback, left_arrow_topic_callback, right_arrow_topic_callback, \
    back_topic_callback, topic_callback, left_arrow_create_note_topic_callback, right_arrow_create_note_topic_callback, \
    back_create_note_topic_callback, create_note_topic_callback
from data.decorators import its_register_user
from data.messages.client import confirming_message
from data.messages.command import stop_command
from data.messages.errors import error_message
from data.send_messages import send_message, delete_message, edit_message
from handlers.client.keyboards import create_topics_for_create_note_keyboard
from handlers.client.show_notes import show_menu, show_topics_list


async def show_topics_list_for_create_note(update: Update, context: CallbackContext, index):
    keyboard = create_topics_for_create_note_keyboard(index)
    await edit_message(update, "hi", markup=keyboard)


@its_register_user
async def add_note(update: Update, context: CallbackContext, topic_id):
    await send_message(update, "Отправьте фотографии, одной группой")
    return 1


async def save_photo(update: Update, context: CallbackContext):
    files = []
    path = datetime.datetime.now().strftime("images/%D-%M-%Y/")
    if os.path.isdir(path) is False:
        os.mkdir(path)
    for file in update.message.photo:
        file_obj = await file.get_file()
        await file_obj.download_to_drive(f"{path}/{file_obj.file_unique_id}")
        files.append(file.file_id)
    context.user_data["files"] = files
    return 2


async def save_name(update: Update, context: CallbackContext):
    title  = update.message.text
    context.user_data["title"] = title
    return 2


@its_register_user
async def add_note_query_callback(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    await update.callback_query.answer()
    if callback == add_note_callback:
        await send_message(update, "Загрузка конспекта. Выберите тему конспекта:")
        await show_topics_list_for_create_note(update, context, 0)
        return 0
    else:
        await  send_message(update, error_message)
        return ConversationHandler.END


@its_register_user
async def topic_menu_for_create_note_menu_callback_query(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    await update.callback_query.answer()
    if left_arrow_create_note_topic_callback in callback:
        index = int(callback[
                    callback.find(left_arrow_create_note_topic_callback) + len(left_arrow_create_note_topic_callback):])
        await show_topics_list_for_create_note(update, context, index)
        return 0
    elif right_arrow_create_note_topic_callback in callback:
        index = int(callback[callback.find(right_arrow_create_note_topic_callback) + len(
            right_arrow_create_note_topic_callback):])
        await show_topics_list_for_create_note(update, context, index)
        return 0
    elif callback == back_create_note_topic_callback:
        await delete_message(update)
        await show_menu(update, context)
        return ConversationHandler.END
    elif create_note_topic_callback in callback:
        topic_id = int(callback[callback.find(create_note_topic_callback) + len(create_note_topic_callback):])
        return await add_note(update, context, topic_id)
    else:
        await  send_message(update, error_message)
        return ConversationHandler.END


async def stop(update: Update, context: CallbackContext):
    sent_message = confirming_message
    msg = await send_message(update, sent_message, markup=ReplyKeyboardRemove())
    await delete_message(update, message_id=msg.message_id)
    return ConversationHandler.END


conv_handler_add_note = ConversationHandler(
    entry_points=[CallbackQueryHandler(add_note_query_callback, add_note_pattern)],
    states={
        0: [CallbackQueryHandler(topic_menu_for_create_note_menu_callback_query, create_note_topic_pattern)],
        1: [MessageHandler(filters.PHOTO, save_photo)],
        2: [MessageHandler(filters.TEXT, save_name)],
        3: [MessageHandler(filters.TEXT, save_description)],
    },
    fallbacks=[CommandHandler(stop_command, stop)]
)
