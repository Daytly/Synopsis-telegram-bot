import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin
from data.db.db_session import SqlAlchemyBase


class BlackList(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'black_list'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    user = orm.relationship("User", backref="black_list")

    def __repr__(self):
        return f'<User> {self.id} {self.username} {self.stage}'
