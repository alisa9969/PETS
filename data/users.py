import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
import werkzeug
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    posts = orm.relationship("Post", back_populates='user')
    city = sqlalchemy.Column(sqlalchemy.String, default='Москва')

    def set_password(self, password):
        self.hashed_password = werkzeug.security.generate_password_hash(password)

    def check_password(self, password):
        return werkzeug.security.check_password_hash(self.hashed_password, password)
