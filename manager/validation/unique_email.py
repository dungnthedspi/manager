from manager import model
from manager.model import *
import formencode


class UniqueEmail(formencode.validators.Email):

    def _to_python(self, value, c):
        email = Session.query(model.Student).filter_by(email = value).first()
        if email > 0 and hasattr(c, 'id') and c.id != email.id:
            raise formencode.Invalid('That email abcd already exists', value, c)
        if email > 0 and not hasattr(c, 'id'):
            raise formencode.Invalid('That email hbhbhb already exists', value, c)
        return formencode.validators.Email._to_python(self, value, c)