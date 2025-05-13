import sqlalchemy
from sqlalchemy import orm

from sqlalchemy_serializer import SerializerMixin

from project.data.db_session import SqlAlchemyBase


class Snowboards(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'snowboards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    owner_weight = sqlalchemy.Column(sqlalchemy.Integer)
    owner_height = sqlalchemy.Column(sqlalchemy.Integer)
    owner_style = sqlalchemy.Column(sqlalchemy.String)
    owner_level = sqlalchemy.Column(sqlalchemy.String)

    stiffness = sqlalchemy.Column(sqlalchemy.String)
    shape = sqlalchemy.Column(sqlalchemy.Integer)
    deflection = sqlalchemy.Column(sqlalchemy.String)
    height = sqlalchemy.Column(sqlalchemy.Integer)
    high_tramps = sqlalchemy.Column(sqlalchemy.Boolean)

    user = orm.relationship('User')