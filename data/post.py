import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    currency = sqlalchemy.Column(sqlalchemy.String, default='₽')
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    coords1 = sqlalchemy.Column(sqlalchemy.Float)
    coords2 = sqlalchemy.Column(sqlalchemy.Float)
    views_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    destination = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    delivery = sqlalchemy.Column(sqlalchemy.Boolean)
    photo = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    breed = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    color = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    documents = sqlalchemy.Column(sqlalchemy.Boolean)
    vaccin = sqlalchemy.Column(sqlalchemy.Boolean)
    steril = sqlalchemy.Column(sqlalchemy.Boolean)
    category = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User")
