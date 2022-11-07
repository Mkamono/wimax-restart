from email.policy import default
from enum import unique
from numpy import integer
from sqlalchemy import Column, Integer, String, DATETIME, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta, timezone

Base = declarative_base()


class Status(Base):
    JST = timezone(timedelta(hours=+9), 'JST')
    __tablename__ = 'connection'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_OK = Column(Integer, unique=False, default=0)
    status_OK_global = Column(Integer, unique=False, default=0)
    message = Column(String(200), nullable=False)
    created = Column('created', DATETIME,
                     default=datetime.now(JST), nullable=False)
