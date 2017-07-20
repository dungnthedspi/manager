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

import shutil

log = logging.getLogger(__name__)


class StudentsController(BaseController):
    def index(self, format='html'):
        if request.params:
            page = request.params['page']
        else:
            page = 1
        c.students = webhelpers.paginate.Page(Session.query(model.Student), page=page, items_per_page=5)
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
            Session.add(model.Student(name=name, email=email, password=password))
            Session.commit()
            h.flash('Tao moi thanh cong', 'success')
            redirect(url(controller='students', action='index'))

    def new(self, format='html'):
        return render('/student/new.html')

    def update(self, id):
        schema = StudentForm()
        c.id = int(id)
        try:
            form_result = schema.to_python(request.params, c)
        except formencode.validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            h.flash('Cap nhat that bai', 'error')
            return render('/student/edit.html')
        else:
            student = Session.query(model.Student).filter(Student.id == id).first()
            student.name = request.params['name']
            student.email = request.params['email']
            Session.commit()
            h.flash('Cap nhat thanh cong', 'success')
            redirect(url(controller='students', action='index'))

    def delete(self, id):
        Session.delete(Session.query(model.Student).filter(Student.id == id).first())
        Session.commit()
        redirect(url(controller='students', action='index'))

    def show(self, id, format='html'):
        c.student = Session.query(model.Student).filter(Student.id == id).first()
        c.courses = Session.query(model.Course).all()
        return render('/student/show.html')

    def edit(self, id, format='html'):
        schema = StudentForm()
        student = Session.query(model.Student).filter(Student.id == id).first()
        c.form_result = schema.from_python(student.__dict__)
        c.form_errors = {}
        c.id = int(id)
        return render('/student/edit.html')

    def upload(self, id):
        c.student = Session.query(model.Student).filter(Student.id == id).first()
        return render('/student/upload.html')

    def save_image(self):
        id = request.POST['student_id']
        c.student = Session.query(model.Student).filter(Student.id == id).first()
        file = request.POST['file']
        # file.filename = str(random.getrandbits(64)) + file.filename
        file.filename = file.filename.split('.')[0] + str(random.getrandbits(64)) + '.jpg'
        path_image = os.path.join(config['app_conf']['upload_folder'], file.filename)
        path = open(path_image,'wb')
        shutil.copyfileobj(file.file, path)
        file.file.close()
        path.close()
        c.student.avatar = file.filename
        Session.commit()
        # return (h.image('/uploads/' + student.avatar, '100px', '100px'))
        return h.image_name(c.student)
