from datetime import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.util.preloaded import orm
from data.db.db_session import SqlAlchemyBase


class File(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'file'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    file_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    notes = orm.relationship('Note', secondary='note_file', back_populates='files')

    def __repr__(self):
        return f'<File> {self.id} {self.path}'
