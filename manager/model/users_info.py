"""Users_info model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import *
from manager.model.meta import Base
from authkit.users import Users


class UsersInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.uid'))
    name = Column(String(100))
    avatar = Column(String(100))
    token = Column(String(100))
    active = Column(Integer)

    user = relationship("Users", backref=backref("user_info", uselist=False))

    def __init__(self, name='', avatar='', token='', active=0):
        self.name = name
        self.avatar = avatar
        self.token = token
        self.active = active

    def __repr__(self):
        return "<User_Info('%s')" % self.name