import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase):
    __tablename__ = 'Chat'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    views = sqlalchemy.Column(sqlalchemy.Integer)
