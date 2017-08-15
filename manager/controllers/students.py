import logging

import os
import hashlib
import random
from pylons import config

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from manager.lib.base import BaseController, render
from manager import model
from manager.model import *
from manager.form.form_student import StudentForm
import webhelpers.paginate
import formencode
from manager.lib import helpers as h

from authkit.authorize.pylons_adaptors import authorize

from dateutil.relativedelta import relativedelta
from pylons.decorators.rest import restrict

import shutil

log = logging.getLogger(__name__)


class StudentsController(BaseController):
    def index(self, format='html'):
        a = request.environ['authkit.users']
        student_group_id = Session.query(model.Group).filter_by(name='student').first().uid
        c.students = Session.query(model.Users).filter_by(group_id=student_group_id).all()
        if request.params:
            page = request.params['page']
        else:
            page = 1
        c.students = webhelpers.paginate.Page(c.students, page=page, items_per_page=5)
        if 'partial' in request.params:
            return render('/student/list-partial.html')
        else:
            return render('/student/list-full.html')

    def create(self):
        schema = StudentForm()
        try:
            form_result = schema.to_python(request.params)
        except formencode.validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            h.flash('Tao moi that bai', 'error')
            return render('/student/new.html')
        else:
            name = request.params['name']
            email = request.params['email']
            password = request.params['password']
            string = name + email + password
            token = hashlib.md5(string).hexdigest()
            c.user = model.Users(email=email, password=password)
            c.user.user_info = model.UsersInfo(name=name, token=token)
            Session.add(c.user)
            request.environ['authkit.users'].user_set_group(c.user.email, 'student')
            Session.commit()

            print 'commit xong'
            from rq import Queue
            from manager.queue.worker import conn
            email_content = render('/layout/email_layout/signup.html')
            print email_content
            q = Queue(connection=conn)
            print c.user.email
            q.enqueue(h.send_mail, 'Subject', email_content, c.user.email)

            h.flash('Successfully', 'success')
            return redirect(url(controller='students', action='notice'))

    def notice(self, format='html'):
        return render('/student/notice.html')

    def new(self, format='html'):
        if request.environ.has_key('REMOTE_USER') and \
                        'admin' not in request.environ['authkit.users'].user_group(request.environ['REMOTE_USER']):
            h.flash('Ban da dang nhap. Signout de tiep tuc', 'error')
            return redirect(h.url(controller='account', action='signedin'))
        return render('/student/new.html')

    def update(self, id):
        schema = StudentForm()
        student = Session.query(model.Users).filter(Users.id == id).first()
        c.id = int(id)
        if not student:
            abort(404, '404 Not Found')
        try:
            form_result = schema.to_python(request.params, c)
        except formencode.validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            h.flash('Cap nhat that bai', 'error')
            return render('/student/edit.html')
        else:
            student.user_info.name = request.params['name']
            student.email = request.params['email']
            student.password = request.params['password']
            Session.commit()
            h.flash('Cap nhat thanh cong', 'success')
            redirect(url(controller='students', action='index'))

    def delete(self, id):
        student = Session.query(model.Users).filter(Users.id == id).first()
        if not student:
            abort(404, '404 Not Found')
        request.environ['authkit.users'].user_delete(student.email)
        Session.delete(student.user_info)
        Session.commit()
        redirect(url(controller='students', action='index'))

    @authorize(h.auth.is_valid_user)
    def show(self, id, format='html'):
        c.student = Session.query(model.Users).filter(Users.id == id).first()
        if not c.student:
            abort(404, '404 Not Found')
        if request.environ['REMOTE_USER'] == c.student.email or \
                ('admin' in request.environ['authkit.users'].user_group(request.environ['REMOTE_USER']) and \
                 'admin' not in request.environ['authkit.users'].user_group(c.student.email)):
            c.courses = Session.query(model.Course).all()
            return render('/student/show.html')
        else:
            abort(403)

    def edit(self, id, format='html'):
        schema = StudentForm()
        student = Session.query(model.Users).filter(Users.id == id).first()
        dict = student.__dict__
        c.form_result = dict.update(student.user_info.__dict__)
        c.form_result = dict
        c.form_errors = {}
        c.id = int(id)
        return render('/student/edit.html')

    def save_image(self):
        id = request.POST['student_id']
        c.student = Session.query(model.Users).filter(Users.id == id).first()
        file = request.POST['file']
        file.filename = file.filename.split('.')[0] + str(random.getrandbits(64)) + '.jpg'
        path_image = os.path.join(config['app_conf']['upload_folder'], file.filename)
        path = open(path_image, 'wb')
        shutil.copyfileobj(file.file, path)
        file.file.close()
        path.close()
        print file.filename
        c.student.user_info.avatar = file.filename
        Session.commit()
        # return (h.image('/uploads/' + student.avatar, '100px', '100px'))
        return h.image_name(c.student)

    from pylons.decorators import jsonify
    @jsonify
    def events(self):
        result = []
        student_id = request.params['student_id']
        student = Session.query(model.Users).filter_by(id=student_id).first()
        if not student:
            return result
        courses = student.courses
        for course in courses:
            type = course.schedule.type
            if type == model.ScheduleType.NO_REPEAT:
                result.append({
                    'title': course.name,
                    'start': str(course.schedule.start),
                    'end': str(course.schedule.end),
                    'url': h.url(controller='courses', action='show', id=course.id)
                })
            else:
                start = course.schedule.start
                end = course.schedule.end
                while start.date() < course.schedule.end_repeat:
                    result.append({
                        'title': course.name,
                        'start': str(start),
                        'end': str(end),
                        'url': h.url(controller='courses', action='show', id=course.id),
                    })
                    if type == model.ScheduleType.WEEKLY:  # repeat weekly
                        start = start + relativedelta(weeks=1)
                        end = end + relativedelta(weeks=1)
                    elif type == model.ScheduleType.MONTHLY:  # repeat monthly
                        start = start + relativedelta(months=1)
                        end = end + relativedelta(months=1)
        return result

    @restrict('GET')
    def active(self):
        token = request.params['token']
        student = Session.query(model.UsersInfo).filter_by(token=token).first()
        if student:
            student.active = 1
            Session.commit()
            h.flash('Tai khoan cua ban da active thanh cong. Moi ban dang nhap de tiep tuc su dung.', 'success')

        else:
            h.flash('Duong dan kich hoat chua chinh xac.', 'error')
        redirect(url(controller='account', action='signin'))

