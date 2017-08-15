import formencode
from manager.validation.secure_password import SecurePassword

class LoginForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    email = formencode.All(formencode.validators.Email(not_empty = True))
    password = SecurePassword(not_empty=True)
