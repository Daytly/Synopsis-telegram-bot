import logging
from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler

from data.db import db_session
from data.CONSTANTS import PATH_DB, BOT_TOKEN
from data.messages.client import start_message
from handlers.create_notes.create_notes import conv_handler_add_note, add_note_query_callback_handler
from keyboards.show_notes import registry_keyboard
from handlers.client.registration import register_handler
from handlers.client.show_notes import show_note_handler, add_and_view_note_handler, open_notes_menu_callback_handler, \
    view_note_callback_handler, assessments_callback_handler

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    sent_message = start_message.format(user.mention_html())
    await update.message.reply_html(sent_message, reply_markup=registry_keyboard)



def main():
    db_session.global_init(PATH_DB)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(show_note_handler)
    application.add_handler(add_and_view_note_handler)
    application.add_handler(open_notes_menu_callback_handler)
    application.add_handler(view_note_callback_handler)
    application.add_handler(register_handler)
    application.add_handler(conv_handler_add_note)
    application.add_handler(assessments_callback_handler)
    application.add_handler(add_note_query_callback_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
