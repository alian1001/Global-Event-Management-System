from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
admin = Admin(app)

# admin.add_view(ModelView(Event, db.session))

from app import routes
