from data.db.dbClasses.note import Note
from data.db.dbClasses.topic import Topic
from data.db.db_session import create_session


def create_topic_message(topic_id):
    db_sess = create_session()
    topic = db_sess.query(Topic).get(topic_id)
    return f"{topic.name}"

def create_note_caption(note_id):
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)
    return f"{note.title}\n{note.description}"

def create_assessment_caption(note_id):
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)
    return f"Оцените данный конспект: \n{note.title}"