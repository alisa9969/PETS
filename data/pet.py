import sqlalchemy

from .db_session import SqlAlchemyBase


class Pet(SqlAlchemyBase):
    __tablename__ = 'pet'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    training = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    breed = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    defects = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    documents = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    connect = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    vaccin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    steril = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("post.id"))