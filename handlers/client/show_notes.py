from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, filters, \
    MessageHandler, CallbackQueryHandler

from data.callback_patterns import note_pattern, topic_pattern, menu_pattern
from data.callbacks import view_topic_callback, add_note_callback, exit_note_callback, \
    left_arrow_topic_callback, right_arrow_topic_callback, back_topic_callback, topic_callback, view_note_callback, \
    left_arrow_note_callback, right_arrow_note_callback, back_note_callback
from data.dialog_IDs import SHOW_NOTE_CONDITION, ADD_AND_VIEW_NOTE_CALLBACK_CONDITION
from data.messages.client import confirming_message
from data.messages.creator import create_topic_message
from data.messages.errors import error_message
from data.send_messages import send_message, delete_message, edit_message, send_photo_group
from handlers.client.functions import create_media_group, update_file_ids
from handlers.client.keyboards import create_topics_keyboard, create_menu_keyboard, create_notes_keyboard, \
    create_note_keyboard


async def show_menu(update: Update, context: CallbackContext):
    keyboard = create_menu_keyboard()
    await send_message(update, "hi", markup=keyboard)


async def show_topics_list(update: Update, context: CallbackContext, index):
    keyboard = create_topics_keyboard(index)
    await edit_message(update, "hi", markup=keyboard)


async def show_notes_list(update: Update, context: CallbackContext, topic_id, index=0):
    keyboard = create_notes_keyboard(topic_id, index)
    sent_message = create_topic_message(topic_id)
    await edit_message(update, sent_message, markup=keyboard)


async def show_note(update: Update, context: CallbackContext, note_id):
    keyboard = create_note_keyboard()
    media_group = create_media_group(note_id, True)
    await delete_message(update)
    if not await send_photo_group(update, media_group):
        media_group = create_media_group(note_id, False)
        messages = await send_photo_group(update, media_group)
        file_ids = []
        for message in messages:
            file_ids.append(message.photo[-1].file_id)
        update_file_ids(note_id, file_ids)



async def stop(update: Update, context: CallbackContext):
    sent_message = confirming_message
    msg = await send_message(update, sent_message, markup=ReplyKeyboardRemove())
    await delete_message(update, message_id=msg.message_id)
    return ConversationHandler.END


async def emissions_handler(update: Update, context: CallbackContext):
    sent_message = error_message
    await send_message(update, sent_message, markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def add_and_view_note_callback_query(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    await update.callback_query.answer()
    if callback == view_topic_callback:
        return await show_topics_list(update, context, 0)
    elif callback == add_note_callback:
        return await show_topics_list(update, context, 0)
    elif callback == exit_note_callback:
        return await delete_message(update)
    else:
        await  send_message(update, error_message)
        return ConversationHandler.END


async def open_notes_menu_callback_query(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    await update.callback_query.answer()
    if left_arrow_topic_callback in callback:
        index = int(callback[callback.find(left_arrow_topic_callback) + len(left_arrow_topic_callback):])
        return await show_topics_list(update, context, index)
    elif right_arrow_topic_callback in callback:
        index = int(callback[callback.find(right_arrow_topic_callback) + len(right_arrow_topic_callback):])
        return await show_topics_list(update, context, index)
    elif callback == back_topic_callback:
        await delete_message(update)
        return await show_menu(update, context)
    elif topic_callback in callback:
        topic_id = int(callback[callback.find(topic_callback) + len(topic_callback):])
        return await show_notes_list(update, context, topic_id)
    else:
        await  send_message(update, error_message)
        return ConversationHandler.END


async def view_note_callback_query(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    await update.callback_query.answer()
    if left_arrow_note_callback in callback:
        note_id, index = map(int,
                             callback[callback.find(left_arrow_note_callback) + len(left_arrow_note_callback):].split())
        return await show_notes_list(update, context, note_id, index)
    elif right_arrow_note_callback in callback:
        note_id, index = map(int, callback[
                                  callback.find(right_arrow_note_callback) + len(right_arrow_note_callback):].split())
        return await show_notes_list(update, context, note_id, index)
    elif callback == back_note_callback:
        await delete_message(update)
        return await show_menu(update, context)
    elif view_note_callback in callback:
        note_id = int(callback[callback.find(view_note_callback) + len(view_note_callback):])
        return await show_note(update, context, note_id)
    else:
        await  send_message(update, error_message)
        return ConversationHandler.END


show_note_handler = CommandHandler("show_note", show_menu)
add_and_view_note_handler = CallbackQueryHandler(add_and_view_note_callback_query, menu_pattern)
open_notes_menu_callback_handler = CallbackQueryHandler(open_notes_menu_callback_query, topic_pattern)
view_note_callback_handler = CallbackQueryHandler(view_note_callback_query, note_pattern)
