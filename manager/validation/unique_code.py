from manager import model
from manager.model import *
import formencode


class UniqueCode(formencode.validators.PlainText):

    def _to_python(self, value, c):
        course = Session.query(model.Course).filter_by(code = value).first()
        if course > 0 and hasattr(c, 'id') and c.id != course.id:
            raise formencode.Invalid('That course already exists', value, c)
        if course > 0 and not hasattr(c, 'id'):
            raise formencode.Invalid('That course already exists', value, c)
        return formencode.validators.PlainText._to_python(self, value, c)