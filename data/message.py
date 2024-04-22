import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'message'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer)
    sender = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    recipient = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    sms = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)