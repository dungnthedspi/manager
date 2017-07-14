import formencode
from manager.validation.unique_code import UniqueCode
from manager.validation.format_code import FormatCode

class CourseForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    code = formencode.All(formencode.validators.String(not_empty=True), UniqueCode)
    name = formencode.validators.String(not_empty=True)
    number = formencode.validators.Number(not_empty=True, max=200, min=0)