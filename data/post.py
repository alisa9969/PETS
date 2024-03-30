import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'post'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    currency = sqlalchemy.Column(sqlalchemy.Integer, default='$')
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo = orm.relationship('Photo')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    views_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    id_pet = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("pet.id"))
    user = orm.relationship('User')
