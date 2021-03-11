import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<Colonist> {self.id} {self.email} {self.password}'
