"""Person model"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import *

from manager.model.meta import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    name = Column(String(100))
    number = Column(Integer)

    def __init__(self, code='', name='', number=0):
        self.code = code
        self.name = name
        self.number = number

    def __repr__(self):
        return "<Course('%s')" % self.name
