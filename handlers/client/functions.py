from telegram import InputMediaPhoto

from data.db.dbClasses.note import Note
from data.db.db_session import create_session


def create_media_group(note_id, is_fast):
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)

    files = []
    for file in note.files:
        try:
            files.append(InputMediaPhoto(file.file_id if is_fast else open(file.path, 'rb')))
        except FileNotFoundError:
            pass
    return files


def update_file_ids(note_id, file_ids):
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)

    files = []
    for ind, file in zip(range(len(note.files)), note.files):
        file.file_id = file_ids[ind]
        db_sess.merge(file)
    db_sess.commit()
    db_sess.close()
    return files