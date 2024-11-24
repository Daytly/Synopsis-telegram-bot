from data.db.dbClasses.topic import Topic
from data.db.db_session import create_session


def create_topic_message(topic_id):
    db_sess = create_session()
    topic = db_sess.query(Topic).get(topic_id)
    return f"{topic.name}"