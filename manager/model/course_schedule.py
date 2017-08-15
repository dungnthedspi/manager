"""Course model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Date, Enum
from sqlalchemy.orm import relationship, backref
from manager.model.meta import Base
import enum

class ScheduleType(enum.Enum):
    NO_REPEAT = 1
    WEEKLY = 2
    MONTHLY = 3

class CourseSchedule(Base):
    __tablename__ = "course_schedule"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    start = Column(DateTime)
    end = Column(DateTime)
    type = Column(Enum(ScheduleType))
    end_repeat = Column(Date)
    course = relationship("Course", backref=backref("schedule", uselist=False))
    def __init__(self, start=None, end=None, type=None, end_repeat=None):
        self.start = start
        self.end = end
        self.type = type
        self.end_repeat = end_repeat

    def __repr__(self):
        return "<Schedule('%s')" % self.id