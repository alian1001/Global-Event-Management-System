import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    STRIPE_SECRET = os.environ.get('STRIPE_SECRET') or 'stripe_secret'
    
    #set the email system
    SECRET_KEY = 'hard to guess string'
    MAIL_DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = '1131761560@qq.com'
    MAIL_PASSWORD = "wvvppxjujhjwiccc"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '1131761560@qq.com'
    FLASKY_ADMIN = '1131761560@qq.com'

    @staticmethod
    def init_app(app):
        pass