import logging

import formencode
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from manager.lib.base import BaseController, render

from manager import model
from manager.model import *
from manager.lib import helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser
from manager.form.form_login import LoginForm

log = logging.getLogger(__name__)

class AccountController(BaseController):
    def signin(self):
        if not h.auth.authorized(h.auth.is_valid_user):
            if not request.params:
                return render('/derived/account/signin.html')
            schema = LoginForm()
            try:
                form_result = schema.to_python(request.params)
            except formencode.validators.Invalid, error:
                c.form_result = error.value
                c.form_errors = error.error_dict or {}
                h.flash('Dang nhap that bai', 'error')
                return render('/derived/account/signin.html')
            else:
                user = meta.Session.query(model.Users). \
                    filter_by(email=request.params['email'],
                              password=request.params['password']). \
                    first()
                if user:
                    if user.group_id == 1:
                        session['user'] = user
                        session.save()
                        if request.environ['HTTP_REFERER']:
                            print request.environ['HTTP_REFERER']
                            redirect(request.environ['HTTP_REFERER'])
                    else:
                        user_info = meta.Session.query(model.UsersInfo). \
                            filter_by(user_id=user.id). \
                            first()
                        if user_info.active == 1:
                            session['user'] = user
                            session.save()
                            if request.environ['HTTP_REFERER']:
                                print request.environ['HTTP_REFERER']
                                redirect(request.environ['HTTP_REFERER'])
                        else:
                            h.flash('Tai khoan cua ban chua duoc active, Vui long xac nhan bang dia chi email!', 'error')
                            return render('/derived/account/signin.html')
                else:
                    c.form_result = {'email': request.params['email'], 'password': request.params['password']}
                    c.form_errors = {'email': 'Email va Password khong khop voi bat ki tai khoan nao'}
                    if c.form_errors:
                        h.flash('Dang nhap that bai', 'error')
                    return render('/derived/account/signin.html')
        else:
            h.flash('Ban da dang nhap', 'success')
            return redirect(h.url(controller='account', action='signedin'))

    @authorize(ValidAuthKitUser())
    def signout(self):
        # The actual removal of the AuthKit cookie occurs when the response passes
        # through the AuthKit middleware, we simply need to display a page
        # confirming the user is signed out
        del session['user']
        return render('/derived/account/signedout.html')

    @authorize(ValidAuthKitUser())
    def signedin(self):
        # The actual removal of the AuthKit cookie occurs when the response passes
        # through the AuthKit middleware, we simply need to display a page
        # confirming the user is signed out
        # print(1)
        # print(authorize(h.auth.has_auth_kit_role('admin')))
        return render('/derived/account/signedin.html')
