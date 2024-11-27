from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, CallbackQueryHandler

from data.callback_patterns import note_pattern, topic_pattern, menu_pattern, assessment_note_pattern
from data.callbacks import view_topic_callback, add_note_callback, exit_note_callback, \
    left_arrow_topic_callback, right_arrow_topic_callback, back_topic_callback, topic_callback, view_note_callback, \
    left_arrow_note_callback, right_arrow_note_callback, back_note_callback, assessment_note_callback, \
    assessment_note_back_callback
from data.decorators import its_register_user
from data.messages.command import menu_command
from data.messages.creator import create_topic_message, create_note_caption, create_assessment_caption
from data.messages.errors import error_message
from data.send_messages import send_message, delete_message, edit_message, send_photo_group
from handlers.client.functions import create_media_group, update_file_ids, assess_note
from keyboards.main_menu import create_menu_keyboard
from keyboards.show_notes import create_topics_keyboard, create_notes_keyboard, create_assessment_note_keyboard


@its_register_user
async def show_menu(update: Update, context: CallbackContext):
    keyboard = create_menu_keyboard()
    await send_message(update, "Выберите пункт меню:", markup=keyboard)


async def show_topics_list(update: Update, context: CallbackContext, index):
    keyboard = create_topics_keyboard(index)
    await edit_message(update, "Выберите тему:", markup=keyboard)


async def show_notes_list(update: Update, context: CallbackContext, topic_id, index=0):
    keyboard = create_notes_keyboard(topic_id, index)
    sent_message = create_topic_message(topic_id)
    await edit_message(update, sent_message, markup=keyboard)


async def show_note(update: Update, context: CallbackContext, note_id):
    keyboard = create_assessment_note_keyboard(update.effective_user.id, note_id)
    media_group = create_media_group(note_id, True)
    caption = create_note_caption(note_id)
    caption_for_asses = create_assessment_caption(note_id)
    await delete_message(update)
    if not await send_photo_group(update, media_group, caption):
        media_group = create_media_group(note_id, False)
        messages = await send_photo_group(update, media_group, caption)
        file_ids = []
        for message in messages:
            file_ids.append(message.photo[-1].file_id)
        update_file_ids(note_id, file_ids)
    if keyboard is not None:
        await send_message(update, caption_for_asses, keyboard)
    await show_menu(update, context)


async def emissions_handler(update: Update, context: CallbackContext):
    sent_message = error_message
    await send_message(update, sent_message, markup=ReplyKeyboardRemove())
    return ConversationHandler.END


@its_register_user
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


@its_register_user
async def open_topic_menu_callback_query(update: Update, context: CallbackContext):
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


@its_register_user
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


@its_register_user
async def assessments_callback_query(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    await update.callback_query.answer()
    if callback == assessment_note_back_callback:
        await delete_message(update)
    elif assessment_note_callback in callback:
        note_id, score = map(int, callback[callback.find(assessment_note_callback) + len(assessment_note_callback):].split())
        await delete_message(update)
        return await assess_note(update.effective_user.id, note_id, score)
    else:
        await  send_message(update, error_message)
        return ConversationHandler.END


show_note_handler = CommandHandler(menu_command, show_menu)
add_and_view_note_handler = CallbackQueryHandler(add_and_view_note_callback_query, menu_pattern)
open_notes_menu_callback_handler = CallbackQueryHandler(open_topic_menu_callback_query, topic_pattern)
view_note_callback_handler = CallbackQueryHandler(view_note_callback_query, note_pattern)
assessments_callback_handler = CallbackQueryHandler(assessments_callback_query, assessment_note_pattern)