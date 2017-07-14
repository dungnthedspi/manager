"""The application's model objects"""
from manager.model.meta import Session, Base
from manager.model.student import Student
from manager.model.course import Course
import sqlalchemy as sa
from sqlalchemy import orm

from manager.model import meta


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine


association_table = sa.Table('association', Base.metadata,
                             sa.Column('student_id', sa.types.Integer, sa.ForeignKey('student.id')),
                             sa.Column('course_id', sa.types.Integer, sa.ForeignKey('course.id'))
                             )
