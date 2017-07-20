import formencode
import re

class SecurePassword(formencode.validators.ByteString):
    def _to_python(self, value, state):
        x = True
        while x:
            if (len(value) < 6):
                break
            elif not re.search('[a-z]', value):
                break
            elif not re.search('[0-9]', value):
                break
            elif re.search('\s', value):
                break
            else:
                x = False
                break
        if x:
            raise formencode.Invalid('Password co tu 6 tro len. gom cac chu cai thuong va cac chu so', value, state)
        return value