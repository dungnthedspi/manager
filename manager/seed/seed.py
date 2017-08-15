from random import randint
from faker import Faker
from manager.model.meta import Session
import sqlalchemy as sa
import manager.model as model
from paste.script.command import Command
# from pylons import request

DB_URL = "sqlite:///development.db"
engine = sa.create_engine(DB_URL)
model.init_model(engine)
faker = Faker()
# users = request.environ['authkit.users']

class Seed(Command):
    summary = "--NO SUMMARY--"
    usage = "--NO USAGE--"
    group_name = "manage1"
    parser = Command.standard_parser(verbose=False)

    def command(self):
        print("----Delete Database----")
        Session.query(model.Course).delete()
        Session.query(model.CourseSchedule).delete()
        # Session.query(model.Users).delete()
        print("----Delete Done----")
        # users.role_create("admin")
        # users.role_create("delete")
        # users.role_create("editor")
        # users.group_create("student")
        #
        # users.user_create("tung@gmail.com", password="a123456")
        # users.user_add_role("tung@gmail.com", role="editor")
        # users.user_set_group("tung@gmail.com", 'student')
        # users.user_create("admin@gmail.com", password="admin123")
        # users.user_add_role("admin@gmail.com", role="delete")
        # users.user_add_role("admin@gmail.com", role="admin")
        Session.commit()
        print("----Seed Database----")

        # for i in range(100):
        #     student = model.Users(email=faker.email(), password='a123456', group_id = 2)
        #     student.user_info = model.UsersInfo(name=faker.name())
        #     Session.add(student)
        import datetime
        start = []
        end = []
        start.append(datetime.datetime(year=2017, month=8, day=01, hour=8, minute=20))
        end.append(datetime.datetime(year=2017, month=8, day=01, hour=10, minute=10))

        start.append(datetime.datetime(year=2017, month=8, day=01, hour=10, minute=30))
        end.append(datetime.datetime(year=2017, month=8, day=01, hour=12, minute=45))

        start.append(datetime.datetime(year=2017, month=8, day=02, hour=13, minute=20))
        end.append(datetime.datetime(year=2017, month=8, day=02, hour=15, minute=10))

        start.append(datetime.datetime(year=2017, month=8, day=02, hour=15, minute=30))
        end.append(datetime.datetime(year=2017, month=8, day=02, hour=17, minute=45))

        start.append(datetime.datetime(year=2017, month=8, day=03, hour=8, minute=20))
        end.append(datetime.datetime(year=2017, month=8, day=03, hour=10, minute=10))

        start.append(datetime.datetime(year=2017, month=8, day=03, hour=10, minute=30))
        end.append(datetime.datetime(year=2017, month=8, day=03, hour=12, minute=45))

        start.append(datetime.datetime(year=2017, month=8, day=03, hour=13, minute=20))
        end.append(datetime.datetime(year=2017, month=8, day=03, hour=15, minute=10))

        start.append(datetime.datetime(year=2017, month=8, day=03, hour=15, minute=30))
        end.append(datetime.datetime(year=2017, month=8, day=03, hour=17, minute=45))

        start.append(datetime.datetime(year=2017, month=8, day=9, hour=8, minute=30))
        end.append(datetime.datetime(year=2017, month=8, day=10, hour=16, minute=45))

        for i in range(20):
            name = faker.sentence(nb_words=4)
            code = 'IT' + str(randint(1000, 10000))
            a = randint(0,8)
            start_course = start[a]
            end_course = end[a]
            type = model.ScheduleType.NO_REPEAT
            course = model.Course(code=code, name=name, number=randint(10, 100))
            course.schedule = model.CourseSchedule(start=start_course, end=end_course, type=type)
            Session.add(course)

        for i in range(20):
            name = faker.sentence(nb_words=4)
            code = 'IT' + str(randint(1000, 10000))
            a = randint(0,8)
            end_repeat = datetime.date(start[a].year, start[a].month+3, start[a].day)
            start_course = start[a]
            end_course = end[a]
            type = model.ScheduleType.WEEKLY
            course = model.Course(code=code, name=name, number=randint(10, 100))
            course.schedule = model.CourseSchedule(start=start_course, end=end_course, type=type, end_repeat=end_repeat)
            Session.add(course)

        Session.commit()
        print("----Seed Done----")