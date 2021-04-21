import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    like = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    dislike = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')