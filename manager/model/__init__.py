"""The application's model objects"""
from manager.model.meta import Session, Base
from manager.model.users import Users
from manager.model.course import Course
from manager.model.users_info import UsersInfo
from manager.model.course_schedule import CourseSchedule
from manager.model.course_schedule import ScheduleType
import sqlalchemy as sa
from sqlalchemy import orm

from manager.model import meta


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine


association_table = sa.Table('association', Base.metadata,
                             sa.Column('user_id', sa.types.Integer, sa.ForeignKey('users.uid')),
                             sa.Column('course_id', sa.types.Integer, sa.ForeignKey('course.id'))
                             )
