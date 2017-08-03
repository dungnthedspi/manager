"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
# from pylons.templating import render_mako as render
from pylons.templating import render_jinja2 as render
from jinja2 import Environment, PackageLoader, select_autoescape
from pylons import request, response, session, tmpl_context as c, url

from manager.model.meta import Session

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        user = session.get('user')
        if user:
            request.environ['REMOTE_USER'] = user.email
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()
