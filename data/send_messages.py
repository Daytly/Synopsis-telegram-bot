from telegram import Update
from telegram.error import BadRequest

from data.messages.errors import error_message


async def send_message(update: Update, message="", markup=None):
    try:
        return await update.message.reply_html(message, reply_markup=markup)
    except AttributeError:
        return await update.callback_query.message.reply_html(message, reply_markup=markup)


async def send_long_message(update: Update, message="", markup=None):
    text_msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    msgs = []
    for text in text_msgs[:-1]:
        try:
            print(text)
            msgs.append(await update.message.reply_html(text))
        except AttributeError:
            msgs.append(await update.callback_query.message.reply_html(text))
    try:
        msgs.append(await update.message.reply_html(text_msgs[-1], reply_markup=markup))
    except AttributeError:
        msgs.append(await update.callback_query.message.reply_html(text_msgs[-1], reply_markup=markup))
    return msgs


async def edit_message(update: Update, message="", chat_id=None, message_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        if message_id is None:
            message_id = update.callback_query.message.message_id
    except AttributeError:
        raise AttributeError
    try:
        return await update.get_bot().edit_message_text(message, reply_markup=markup, chat_id=chat_id,
                                                        message_id=message_id)
    except Exception as error:
        return error


async def edit_caption(update: Update, message="", chat_id=None, message_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        if message_id is None:
            message_id = update.callback_query.message.message_id
    except AttributeError:
        raise AttributeError
    try:
        return await update.get_bot().edit_message_caption(caption=message, reply_markup=markup, chat_id=chat_id,
                                                           message_id=message_id)
    except Exception as error:
        return error


async def send_audio(update: Update, file_id, message, chat_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        await update.get_bot().send_audio(chat_id, file_id, reply_markup=markup, caption=message)
    except BadRequest:
        await update.get_bot().send_message(chat_id, text=error_message, reply_markup=markup)


async def send_document(update: Update, file_id, message, chat_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        await update.get_bot().send_document(chat_id, file_id, reply_markup=markup, caption=message)
    except BadRequest:
        await update.get_bot().send_message(chat_id, text=error_message, reply_markup=markup)


async def send_photo(update: Update, file_id, message, chat_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat_id
    try:
        await update.get_bot().send_photo(chat_id, file_id, reply_markup=markup, caption=message)
    except BadRequest:
        await update.get_bot().send_message(chat_id, text=error_message, reply_markup=markup)


async def send_video(update: Update, file_id, message, chat_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        await update.get_bot().send_video(chat_id, file_id, reply_markup=markup, caption=message)
    except BadRequest:
        await update.get_bot().send_message(chat_id, text=error_message, reply_markup=markup)


async def send_voice(update: Update, file_id, message, chat_id=None, markup=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        await update.get_bot().send_voice(chat_id, file_id, reply_markup=markup, caption=message)
    except BadRequest:
        await update.get_bot().send_message(chat_id, text=error_message, reply_markup=markup)


async def delete_message(update: Update, chat_id=None, message_id=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        if message_id is None:
            message_id = update.message.message_id
    except AttributeError:
        message_id = update.callback_query.message.message_id
    try:
        await update.get_bot().delete_message(chat_id, message_id)
    except BadRequest:
        return


async def send_photo_group(update: Update, media_group, caption="", chat_id=None):
    try:
        if chat_id is None:
            chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id
    try:
        messages = await update.get_bot().send_media_group(chat_id, media_group, caption=caption)
        return messages
    except BadRequest:
        return False
