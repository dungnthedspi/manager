import formencode
import re

class FormatCode(formencode.validators.String):
    def _to_python(self, value, state):
        print value
        if re.search(' ', value):
            raise formencode.Invalid('Code k gom ki tu cach', value, state)
        if len(value) > 10:
            raise formencode.Invalid('Code toi da 10 ki tu', value, state)
        if len(value) < 2:
            raise formencode.Invalid('Code toi thieu 2 ki tu', value, state)
        if re.search(r'[^\w]', value):
            raise formencode.Invalid('Code gom cac chu cai thuong, hoa va cac chu so', value, state)
        else:
            return value