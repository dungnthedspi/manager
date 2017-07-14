import formencode
from manager.validation.unique_email import UniqueEmail

class StudentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    email = UniqueEmail(not_empty=True)
    name = formencode.validators.PlainText(not_empty=True)