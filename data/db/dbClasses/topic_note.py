import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from data.db.db_session import SqlAlchemyBase


class NoteTopic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topic_note'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    note_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("note.id"))
    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topic.id"))


    def __repr__(self):
        return f'<TopicNote> {self.id} {self.note_id} {self.topic_id}'