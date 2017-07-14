import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from manager.lib.base import BaseController, render
from manager import model
from manager.model import *
from manager.form.form_student import StudentForm
import webhelpers.paginate
import formencode
from manager.lib import helpers as h

log = logging.getLogger(__name__)


class StudentsController(BaseController):
    def index(self, format='html'):
        if request.params:
            page = request.params['page']
        else:
            page = 1
        c.students = webhelpers.paginate.Page(Session.query(model.Student), page=page, items_per_page=5)
        return render('/student/index.html')

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
            Session.add(model.Student(name=name, email=email))
            Session.commit()
            h.flash('Tao moi thanh cong', 'success')
            redirect(url(controller='students', action='index'))

    def new(self, format='html'):
        return render('/student/new.html')

    def update(self, id):
        schema = StudentForm()
        try:
            form_result = schema.to_python(request.params)
        except formencode.validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            h.flash('Tao moi that bai', 'error')
            return render('/student/new.html')
        else:
            student = Session.query(model.Student).filter(Student.id == id).first()
            student.name = request.params['name']
            student.email = request.params['email']
            Session.commit()
            h.flash('Tao moi thanh cong', 'success')
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
        return render('/student/edit.html')
