from datetime import datetime
import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from .note_file import NoteFile
from data.db.db_session import SqlAlchemyBase


class Note(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'note'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=-1)


    user = orm.relationship("User", backref="notes")
    files = orm.relationship('File', secondary='note_file', back_populates='notes')
    topics = orm.relationship('Topic', secondary='topic_note', back_populates='notes')

    def __repr__(self):
        return f'<Note> {self.user_id} {self.name}'
