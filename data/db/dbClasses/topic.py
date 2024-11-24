from datetime import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.util.preloaded import orm
from data.db.db_session import SqlAlchemyBase


class Topic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topic'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    notes = orm.relationship('Note', secondary='topic_note', back_populates='topics')


    def __repr__(self):
        return f'<Topic> {self.id} {self.name}'
