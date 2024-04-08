import sqlalchemy

from .db_session import SqlAlchemyBase


class Pet(SqlAlchemyBase):
    __tablename__ = 'pet'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    breed = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    color = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    documents = sqlalchemy.Column(sqlalchemy.String)
    vaccin = sqlalchemy.Column(sqlalchemy.Boolean)
    steril = sqlalchemy.Column(sqlalchemy.Boolean)
    category = sqlalchemy.Column(sqlalchemy.String)
    post_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("post.id"))
