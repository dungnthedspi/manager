import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
import webhelpers.paginate

from manager import model
from manager.model import *
from pylons.decorators.rest import restrict

from manager.lib.base import BaseController, render

log = logging.getLogger(__name__)


class SearchController(BaseController):
    def search_student(self):
        return render('/search/student.html')

    @restrict('GET')
    def student(self):
        if request.method == "GET":
            search_text = request.params['search_text']
        else:
            search_text = ''
        if request.params.has_key('page'):
            page = request.params['page']
        else:
            page = 1
        c.student = Session.query(model.Student).filter(model.Student.name.like('%' + search_text + '%')).all()
        c.students = webhelpers.paginate.Page(c.student, page=page, items_per_page=5)
        c.form_result = request.params
        if 'partial' in request.params:
            return render('/search/search-list-student-partial.html')
        else:
            return render('/search/search-list-student-full.html')

    def search_course(self):
            return render('search/course.html')

    @restrict('GET')
    def course(self):
        if request.method == "GET":
            search_text = request.params['search_text']
        else:
            search_text = ''
        if request.params.has_key('page'):
            page = request.params['page']
        else:
            page = 1
        c.course = Session.query(model.Course).filter(model.Course.name.like('%' + search_text + '%')).all()
        c.courses = webhelpers.paginate.Page(c.course, page=page, items_per_page=5)
        c.form_result = request.params
        if 'partial' in request.params:
            return render('/search/search-list-course-partial.html')
        else:
            return render('/search/search-list-course-full.html')

    # @restrict('GET')
    # def course(self):
    #     if request.params.has_key('code') or request.params.has_key('name'):
    #         code = request.params['code']
    #         name = request.params['name']
    #         if not code and not name:
    #             c.courses = []
    #         else:
    #             c.courses = Session.query(model.Course)
    #             if code:
    #                 c.courses = c.courses.filter(model.Course.code.like('%' + code + '%'))
    #             if name:
    #                 c.courses = c.courses.filter(model.Course.name.like('%' + name + '%'))
    #             c.courses = c.courses.all()
    #             if request.params.has_key('page'):
    #                 page = request.params['page']
    #             else:
    #                 page = 1
    #             c.courses = webhelpers.paginate.Page(c.courses, page=page, items_per_page=2)
    #         c.form_result = request.params
    #     return render('/search/course_old.html')
