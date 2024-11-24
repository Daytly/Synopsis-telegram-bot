from sqlalchemy.orm import registry
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from data.callbacks import topic_callback, exit_note_callback, back_topic_callback, left_arrow_topic_callback, \
    right_arrow_topic_callback, add_note_callback, view_topic_callback, right_arrow_topic_callbackF, \
    left_arrow_topic_callbackF, topic_callbackF, view_note_callbackF, back_note_callback, left_arrow_note_callbackF, \
    right_arrow_note_callbackF, assessment_note_callbackF, left_arrow_create_note_topic_callbackF, \
    create_note_topic_callbackF, back_create_note_topic_callback, right_arrow_create_note_topic_callbackF
from data.db.dbClasses.assessments import Assessment
from data.db.dbClasses.note import Note
from data.db.dbClasses.topic import Topic
from data.db.db_session import create_session
from data.messages.client import registration_caption, menu_command

buttons = [[KeyboardButton(registration_caption, request_contact=True)]]
registry_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

buttons = [[KeyboardButton(menu_command)]]
menu_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)



def create_topics_keyboard(index=0, count=10):
    buttons = []
    db_sess = create_session()
    topics = db_sess.query(Topic).all()
    for topic in topics[index:index + count]:
        buttons.append([InlineKeyboardButton(text=topic.name, callback_data=topic_callbackF.format(topic.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(InlineKeyboardButton("<-", callback_data=left_arrow_topic_callbackF.format(index - count)))
    navigate_row.append(InlineKeyboardButton("Назад", callback_data=back_topic_callback))
    if index + count < len(topics):
        navigate_row.append(InlineKeyboardButton("->", callback_data=right_arrow_topic_callbackF.format(index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def create_topics_for_create_note_keyboard(index=0, count=10):
    buttons = []
    db_sess = create_session()
    topics = db_sess.query(Topic).all()
    for topic in topics[index:index + count]:
        buttons.append([InlineKeyboardButton(text=topic.name, callback_data=create_note_topic_callbackF.format(topic.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(InlineKeyboardButton("<-", callback_data=left_arrow_create_note_topic_callbackF.format(index - count)))
    navigate_row.append(InlineKeyboardButton("Назад", callback_data=back_create_note_topic_callback))
    if index + count < len(topics):
        navigate_row.append(InlineKeyboardButton("->", callback_data=right_arrow_create_note_topic_callbackF.format(index + count)))
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
    for note in topic.notes[index:index + count]:
        buttons.append([InlineKeyboardButton(note.name, callback_data=view_note_callbackF.format(note.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(
            InlineKeyboardButton("<-", callback_data=left_arrow_note_callbackF.format(topic_id, index - count)))
    navigate_row.append(InlineKeyboardButton("Назад", callback_data=back_note_callback))
    if index + count < len(topic.notes):
        navigate_row.append(
            InlineKeyboardButton("->", callback_data=right_arrow_note_callbackF.format(topic_id, index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def create_assessment_note_keyboard(user_id, note_id):
    db_sess = create_session()
    assessment = db_sess.query(Assessment).filter(note_id=note_id, user_id=user_id).first()
    if assessment:
        return None
    buttons = []
    assessment_row = []
    for i in range(1, 5 + 1):
        assessment_row.append(InlineKeyboardButton(f"{i}★",
                                                   callback_data=assessment_note_callbackF.format(note_id, i)))
    buttons.append(assessment_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
