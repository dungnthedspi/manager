import formencode
from manager.validation.unique_email import UniqueEmail
from manager.validation.secure_password import SecurePassword

class StudentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    email = UniqueEmail(not_empty=True)
    name = formencode.validators.PlainText(not_empty=True)
    password = SecurePassword()
    password_confirm = formencode.validators.ByteString(not_empty=True)
    chained_validators = [formencode.validators.FieldsMatch('password', 'password_confirm')]
