import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict

from manager import model
from manager.model import *
import manager.lib.helpers as h

from manager.lib.base import BaseController, render
from authkit.authorize.pylons_adaptors import authorize

log = logging.getLogger(__name__)


class RegisterController(BaseController):
    @authorize(h.auth.has_admin_role)
    def new(self):
        a = request.environ['authkit.users']
        student_group_id = Session.query(model.Group).filter_by(name='student').first().uid
        c.students = Session.query(model.Users).filter_by(group_id=student_group_id).all()
        c.courses = Session.query(model.Course)
        return render('/register/new.html')

    @authorize(h.auth.has_admin_role)
    def create(self):
        student_id = request.params['student_id']
        student = Session.query(model.Users).filter_by(id=student_id).first()
        course_id = request.params['course_id']
        course = Session.query(model.Course).filter_by(id=course_id).first()
        register = Session.query(model.association_table).filter_by(user_id=student_id,
                                                                    course_id=course_id).first()
        if register:
            h.flash('Da dang ki tu truoc', 'error')
        else:
            student.courses.append(course)
            Session.commit()
            h.flash('Dang ki thanh cong', 'success')
        return redirect(url(controller='students', action='show', id=student_id))

    @authorize(h.auth.has_admin_role)
    def delete(self):
        student_id = request.params['student_id']
        student = Session.query(model.Users).filter_by(id=student_id).first()
        course_id = request.params['course_id']
        course = Session.query(model.Course).filter_by(id=course_id).first()
        register = Session.query(model.association_table).filter_by(user_id=student_id,
                                                                    course_id=course_id).first()
        if not register:
            abort(404, '404 Register Not Found')
        student.courses.remove(course)
        Session.commit()
        h.flash('Xoa dang ki thanh cong', 'success')
        return redirect(h.url(controller='students', action='show', id=student_id))
