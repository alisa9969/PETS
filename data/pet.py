import sqlalchemy

from .db_session import SqlAlchemyBase


class Pet(SqlAlchemyBase):
    __tablename__ = 'pet'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    breed = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    documents = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vaccin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    steril = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("post.id"))