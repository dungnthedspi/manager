"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from pylons import url
from manager.lib import auth
from webhelpers.pylonslib.flash import Flash as _Flash
import hashlib
flash = _Flash()

from pylons import config
# email_from = 'beannguyen9xtb@gmail.com'
# email_password = 'thanhhuyen1208'
email_from = 'thequan159@gmail.com'
email_password = 'quanchua'

def create_courses_options(type_list):
    options = [(ct.id, ct.code+'--'+ ct.name) for ct in type_list]
    return Options(options)

def create_students_options(type_list):
    options = [(ct.id, ct.user_info.name+'--'+ ct.email) for ct in type_list]
    return Options(options)

def image_name(student):
    gravatar_id = student.email
    if student.user_info and student.user_info.avatar:
        return '/uploads/'+student.user_info.avatar
    else:
        gravatar_url = 'https://www.gravatar.com/avatar/' + hashlib.md5(gravatar_id.lower()).hexdigest() + '?'
        return gravatar_url

def send_mail(SUBJECT, BODY, TO):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = TO
    msg['Subject'] = SUBJECT
    HTML_BODY = MIMEText(BODY, 'html')
    msg.attach(HTML_BODY)
    print 'Start send'
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email_from, email_password)
    server.sendmail(email_from, TO, msg.as_string())
    server.close()
    print 'Send done'