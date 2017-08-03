import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from manager.lib.base import BaseController, render

from manager import model
from manager.model import *
from manager.lib import helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

log = logging.getLogger(__name__)

class AccountController(BaseController):
    def signin(self):
        if not h.auth.authorized(h.auth.is_valid_user):
            if request.params:
                user = Session.query(model.Users). \
                    filter_by(email=request.params['email'],
                              password=request.params['password']). \
                    first()
                if user:
                    session['user'] = user
                    session.save()
                    if request.environ['HTTP_REFERER']:
                        print request.environ['HTTP_REFERER']
                        redirect(request.environ['HTTP_REFERER'])
                else:
                    return render('/derived/account/signin.html')
            else:
                return render('/derived/account/signin.html')
        else:
            h.flash('Ban da dang nhap', 'error')
            return redirect(h.url('signedin'))

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
