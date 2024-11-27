from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from data.callbacks import back_topic_callback, right_arrow_topic_callbackF, \
    left_arrow_topic_callbackF, topic_callbackF, view_note_callbackF, back_note_callback, left_arrow_note_callbackF, \
    right_arrow_note_callbackF, assessment_note_callbackF
from data.db.dbClasses.assessments import Assessment
from data.db.dbClasses.topic import Topic
from data.db.db_session import create_session
from data.messages.buttons import save_text_btn, back_text_btn
from data.messages.client import registration_caption
from data.messages.command import menu_command

buttons = [[KeyboardButton(registration_caption, request_contact=True)]]
registry_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

buttons = [[KeyboardButton(f"/{menu_command}")]]
menu_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

buttons = [[KeyboardButton(save_text_btn)]]
save_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def create_topics_keyboard(index=0, count=10):
    buttons = []
    db_sess = create_session()
    topics = db_sess.query(Topic).all()
    for topic in topics[index:index + count]:
        buttons.append([InlineKeyboardButton(text=topic.name, callback_data=topic_callbackF.format(topic.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(InlineKeyboardButton("<-", callback_data=left_arrow_topic_callbackF.format(index - count)))
    navigate_row.append(InlineKeyboardButton(back_text_btn, callback_data=back_topic_callback))
    if index + count < len(topics):
        navigate_row.append(InlineKeyboardButton("->", callback_data=right_arrow_topic_callbackF.format(index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def create_notes_keyboard(topic_id, index=0, count=10):
    buttons = []
    db_sess = create_session()
    topic = db_sess.query(Topic).get(topic_id)
    for note in topic.notes[index:index + count]:
        if len(note.assessments) > 0:
            assessment = f"({round(sum([i.score for i in note.assessments]) / len(note.assessments), 1)}★)"
        else:
            assessment = ""
        buttons.append(
            [InlineKeyboardButton(f"{note.title} {assessment}", callback_data=view_note_callbackF.format(note.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(
            InlineKeyboardButton("<-", callback_data=left_arrow_note_callbackF.format(topic_id, index - count)))
    navigate_row.append(InlineKeyboardButton(back_text_btn, callback_data=back_note_callback))
    if index + count < len(topic.notes):
        navigate_row.append(
            InlineKeyboardButton("->", callback_data=right_arrow_note_callbackF.format(topic_id, index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def create_assessment_note_keyboard(user_id, note_id):
    db_sess = create_session()
    assessment = db_sess.query(Assessment).filter_by(note_id=note_id, user_id=user_id).first()
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
