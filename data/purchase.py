import datetime
from datetime import time
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Purchase(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    purchase = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_buyer = sqlalchemy.Column(sqlalchemy.Integer)
    created_date = sqlalchemy.Column(sqlalchemy.String,
                                     default=datetime.datetime.now().strftime('%Y-%m-%d'))
    created_time = sqlalchemy.Column(sqlalchemy.String,
                                     default=str(datetime.datetime.now().time())[:5])