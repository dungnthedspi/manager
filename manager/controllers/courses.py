import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from manager.lib.base import BaseController, render
from manager import model
from manager.model import *
from manager.form.form_course import CourseForm
import webhelpers.paginate
import formencode
from manager.lib import helpers as h

from authkit.permissions import ValidAuthKitUser
from authkit.authorize.pylons_adaptors import authorize

log = logging.getLogger(__name__)


class CoursesController(BaseController):
    def index(self, format='html'):
        if request.params:
            page = request.params['page']
        else:
            page = 1
        c.courses = webhelpers.paginate.Page(Session.query(model.Course), page=page, items_per_page=5)
        if 'partial' in request.params:
            return render('/course/list-partial.html')
        else:
            return render('/course/list-full.html')


    def create(self):
        schema = CourseForm()
        try:
            form_result = schema.to_python(request.params)
        except formencode.validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            return render('/course/new.html')
        else:
            code = request.params['code']
            name = request.params['name']
            number = request.params['number']
            Session.add(model.Course(code=code, name=name, number=number))
            Session.commit()
            redirect(url(controller='courses', action='index'))

    def new(self, format='html'):
        return render('/course/new.html')

    @authorize(h.auth.user_in(['admin', 'editor']))
    def update(self, id):
        schema = CourseForm()
        c.id = int(id)
        try:
            form_result = schema.to_python(request.params, c)
        except formencode.validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            return render('/course/edit.html')
        else:
            course = Session.query(model.Course).filter(Course.id == id).one()
            course.code = request.params['code']
            course.name = request.params['name']
            course.number = request.params['number']
            Session.commit()
            redirect(url(controller='courses', action='index'))

    @authorize(h.auth.has_delete_role)
    def delete(self, id):
        Session.delete(Session.query(model.Course).filter(Course.id == id).one())
        Session.commit()
        redirect(url(controller='courses', action='index'))

    def show(self, id, format='html'):
        c.course = Session.query(model.Course).filter(Course.id == id).one()
        return render('/course/show.html')

    @authorize(h.auth.is_valid_user)
    def edit(self, id, format='html'):
        schema = CourseForm()
        course = Session.query(model.Course).filter(Course.id == id).one()
        c.form_result = schema.from_python(course.__dict__)
        c.form_errors = {}
        return render('/course/edit.html')
