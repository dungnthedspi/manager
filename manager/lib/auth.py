from authkit.permissions import ValidAuthKitUser
from authkit.permissions import HasAuthKitRole
from authkit.permissions import RemoteUser
from authkit.permissions import UserIn
from authkit.authorize.pylons_adaptors import authorized
from pylons.templating import render_jinja2 as render

is_valid_user = ValidAuthKitUser()
has_delete_role = HasAuthKitRole(['delete'])
has_edit_role = HasAuthKitRole(['editor'])
has_admin_role = HasAuthKitRole('admin')
remote_user = RemoteUser()
user_in = UserIn
def render_signin():
    result = render('/derived/account/signin.html')
    return result