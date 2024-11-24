from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from data.callbacks import topic_callback, exit_note_callback, back_topic_callback, left_arrow_topic_callback, \
    right_arrow_topic_callback, add_note_callback, view_topic_callback, right_arrow_topic_callbackF, \
    left_arrow_topic_callbackF, topic_callbackF, view_note_callbackF, back_note_callback, left_arrow_note_callbackF, \
    right_arrow_note_callbackF
from data.db.dbClasses.note import Note
from data.db.dbClasses.topic import Topic
from data.db.db_session import create_session


def create_topics_keyboard(index=0, count=10):
    buttons = []
    db_sess = create_session()
    topics = db_sess.query(Topic).all()
    for topic in topics[index:index+count]:
        buttons.append([InlineKeyboardButton(text=topic.name, callback_data=topic_callbackF.format(topic.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(InlineKeyboardButton("<-", callback_data=left_arrow_topic_callbackF.format(index - count)))
    navigate_row.append(InlineKeyboardButton("Назад", callback_data=back_topic_callback))
    if index+count < len(topics):
        navigate_row.append(InlineKeyboardButton("->", callback_data=right_arrow_topic_callbackF.format(index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("Загрузить конспект", callback_data=add_note_callback)],
        [InlineKeyboardButton("Открыть конспект", callback_data=view_topic_callback)],
        [InlineKeyboardButton("Выйти", callback_data=exit_note_callback)],
               ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_notes_keyboard(topic_id, index=0, count=10):
    buttons = []
    db_sess = create_session()
    topic = db_sess.query(Topic).get(topic_id)
    for note in topic.notes[index:index+count]:
        buttons.append([InlineKeyboardButton(note.name, callback_data=view_note_callbackF.format(note.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(InlineKeyboardButton("<-", callback_data=left_arrow_note_callbackF.format(topic_id, index - count)))
    navigate_row.append(InlineKeyboardButton("Назад", callback_data=back_note_callback))
    if index + count < len(topic.notes):
        navigate_row.append(InlineKeyboardButton("->", callback_data=right_arrow_note_callbackF.format(topic_id, index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_note_keyboard():
    buttons = []
    navigate_row = [InlineKeyboardButton("Назад", callback_data=back_note_callback)]
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

