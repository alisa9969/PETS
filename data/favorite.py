import sqlalchemy
from .db_session import SqlAlchemyBase


class Favorite(SqlAlchemyBase):
    __tablename__ = 'favorite'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    post_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
