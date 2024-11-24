import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from data.db.db_session import SqlAlchemyBase


class NoteFile(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'note_file'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    note_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("note.id"))
    file_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("file.id"))


    def __repr__(self):
        return f'<NoteFile> {self.id} {self.note_id} {self.file_id}'