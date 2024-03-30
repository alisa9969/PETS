import sqlalchemy
from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photo'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    photos = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    id_post = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("post.id"))