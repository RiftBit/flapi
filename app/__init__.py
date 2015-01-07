from flask import Flask
from hashlib import md5
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask_jsonrpc import JSONRPC
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, API_URL

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

jsonrpc = JSONRPC(app, API_URL, enable_web_browsable_api=True)
auth = HTTPBasicAuth()

if not app.debug and MAIL_SERVER != '':
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'flapi fail', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/flapi.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('FLAPI startup')


users = {"ergoz": "81dc9bdb52d04dc20036dbd8313ed055", "admin": "21232f297a57a5a743894a0e4a801fc3"}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@auth.hash_password
def hash_pw(password):
    return md5(password).hexdigest()


# @auth.verify_password
# def verify_pw(username, password):
#     return call_custom_verify_function(username, password)


from app import views
from app.models import *
from app.api import *
