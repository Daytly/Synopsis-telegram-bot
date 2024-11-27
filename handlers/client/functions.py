from telegram import InputMediaPhoto

from data.db.dbClasses.assessments import Assessment
from data.db.dbClasses.file import File
from data.db.dbClasses.note import Note
from data.db.dbClasses.topic import Topic
from data.db.dbClasses.user import User
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

def assess_note(user_id, note_id, score):
    db_sess = create_session()
    assessment = db_sess.query(Assessment).filter_by(note_id=note_id, user_id=user_id).first()
    if assessment:
        return False
    assessment = Assessment(note_id=note_id, user_id=user_id, score=score)
    db_sess.add(assessment)
    db_sess.commit()
    return True


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


def register_user(user_id, name, surname, username, phone_number):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if user is not None:
        return False
    user = User(id=user_id, name=name, surname=surname, username=username, phone_number=phone_number)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return True


def create_note(title, description, files, user_id, topic_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if user is None:
        return False

    topic = db_sess.query(Topic).get(topic_id)
    if topic is None:
        return False
    note = Note()
    note.title = title
    note.description = description
    files_obj = []
    for file in files:
        file = File(path=file["path"], file_id=file["file_id"])
        db_sess.add(file)
        files_obj.append(file)
    db_sess.commit()
    for file in files_obj:
        note.files.append(file)
    note.user = user
    note.topics.append(topic)
    db_sess.add(note)
    db_sess.commit()
    db_sess.close()
    return True



