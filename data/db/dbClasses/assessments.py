from datetime import datetime
import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from .note_file import NoteFile
from data.db.db_session import SqlAlchemyBase


class Assessment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'assessment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    note_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("note.id"))
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)


    user = orm.relationship("User", backref="assessments")
    note = orm.relationship('Note', backref="assessments")

    def __repr__(self):
        return f'<Assessment> {self.user_id} {self.note_id}'
