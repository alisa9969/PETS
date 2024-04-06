import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'post'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    currency = sqlalchemy.Column(sqlalchemy.String, default='₽')
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    views_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    pet = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("pet.id"))
    destination = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    delivery = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')
