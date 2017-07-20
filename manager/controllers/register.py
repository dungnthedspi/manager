import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict

from manager import model
from manager.model import *
import manager.lib.helpers as h

from manager.lib.base import BaseController, render

log = logging.getLogger(__name__)


class RegisterController(BaseController):
    def new(self):
        c.students = Session.query(model.Student)
        c.courses = Session.query(model.Course)
        return render('/register/new.html')

    def create(self):
        student_id = request.params['student_id']
        student = Session.query(model.Student).filter_by(id=student_id).first()
        course_id = request.params['course_id']
        course = Session.query(model.Course).filter_by(id=course_id).first()
        register = Session.query(model.association_table).filter_by(student_id=student_id,
                                                                    course_id=course_id).first()
        if register:
            h.flash('Da dang ki tu truoc', 'error')
        else:
            student.courses.append(course)
            Session.commit()
            h.flash('Dang ki thanh cong', 'success')
        return redirect(url(controller='students', action='show', id=student.id))

    def delete(self):
        student_id = request.params['student_id']
        student = Session.query(model.Student).filter_by(id=student_id).first()
        course_id = request.params['course_id']
        course = Session.query(model.Course).filter_by(id=course_id).first()
        register = Session.query(model.association_table).filter_by(student_id=student_id,
                                                                    course_id=course_id).first()
        if not register:
            abort(404, '404 Register Not Found')
        student.courses.remove(course)
        Session.commit()
        h.flash('Xoa dang ki thanh cong', 'success')
        return redirect(h.url(controller='students', action='show', id=student_id))
