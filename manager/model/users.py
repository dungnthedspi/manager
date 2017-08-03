"""Users model"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import *
from manager.model.meta import Base


class Users(Base):
    __tablename__ = "users"

    id = Column('uid', Integer, primary_key=True)
    email = Column('username', String(100))
    password = Column('password', String(100))
    group_id = Column('group_uid', Integer)

    courses = relationship("Course",
                           secondary='association',
                           backref="users")

    def __repr__(self):
        return "<User ('%s')" % self.email