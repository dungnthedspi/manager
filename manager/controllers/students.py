import logging

import os
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
            c.user = model.Users(email=email, password=password)
            c.user.user_info = model.UsersInfo(name=name)
            Session.add(c.user)
            request.environ['authkit.users'].user_set_group(c.user.email, 'student')
            Session.commit()
            h.flash('Tao moi thanh cong', 'success')
            redirect(url(controller='students', action='index'))

    def new(self, format='html'):
        if request.environ.has_key('REMOTE_USER') and \
                        'admin' not in request.environ['authkit.users'].user_group(request.environ['REMOTE_USER']):
            h.flash('Ban da dang nhap. Signout de tiep tuc', 'error')
            return redirect(h.url(controller='account', action='signedin'))
        return render('/student/new.html')
        # return redirect(h.url(controller='students', action='index'))

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
            student.name = request.params['name']
            student.email = request.params['email']
            student.password = request.params['password']
            Session.commit()
            h.flash('Cap nhat thanh cong', 'success')
            redirect(url(controller='students', action='index'))

    def delete(self, id):
        student = Session.query(model.Users).filter(Users.id == id).first()
        if not student:
            abort(404, '404 Not Found')
        Session.delete(student)
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
        c.form_result = dict.update(student.user.__dict__)
        c.form_result = dict
        c.form_errors = {}
        c.id = int(id)
        return render('/student/edit.html')

    def upload(self, id):
        c.student = Session.query(model.Student).filter(Student.id == id).first()
        return render('/student/upload.html')

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
