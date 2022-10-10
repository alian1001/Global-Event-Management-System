import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv("stripe.env")


class Config(object):
    DATABASE_PATH = "db.sqlite3"

    STRIPE_SECRET = os.environ.get("STRIPE_SECRET") or ""
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET") or ""
    SECRET_KEY = "425d952458b54d2c9acc1ca13ae5eb08"  # Changing this will invalidate user sessions
    SECRET_PEPPER = "9d2c9ad8c3924181a585a307d290e2c9"  # Changing this will invalidate all user passwords

    # set the email system
    MAIL_DEBUG = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "1131761560@qq.com"
    MAIL_PASSWORD = "wvvppxjujhjwiccc"
    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
    FLASKY_MAIL_SENDER = "1131761560@qq.com"
    FLASKY_ADMIN = "1131761560@qq.com"

    @staticmethod
    def init_app(app):
        pass
