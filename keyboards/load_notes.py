from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from data.callbacks import create_note_topic_callbackF, left_arrow_create_note_topic_callbackF, \
    back_create_note_topic_callback, right_arrow_create_note_topic_callbackF
from data.db.dbClasses.topic import Topic
from data.db.db_session import create_session
from data.messages.buttons import back_text_btn


def create_topics_for_create_note_keyboard(index=0, count=10):
    buttons = []
    db_sess = create_session()
    topics = db_sess.query(Topic).all()
    for topic in topics[index:index + count]:
        buttons.append(
            [InlineKeyboardButton(text=f"{topic.name}", callback_data=create_note_topic_callbackF.format(topic.id))])
    navigate_row = []
    if index - 1 >= 0:
        navigate_row.append(
            InlineKeyboardButton("<-", callback_data=left_arrow_create_note_topic_callbackF.format(index - count)))
    navigate_row.append(InlineKeyboardButton(back_text_btn, callback_data=back_create_note_topic_callback))
    if index + count < len(topics):
        navigate_row.append(
            InlineKeyboardButton("->", callback_data=right_arrow_create_note_topic_callbackF.format(index + count)))
    buttons.append(navigate_row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
