from flask import Flask, request
from flask_bootstrap import Bootstrap
from config import Config
from flask_admin import Admin

# from flask_sqlalchemy import SQLAlchemy
# from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
admin = Admin(app)

# admin.add_view(ModelView(Event, db.session))

# Helper for formatting currency in templates
@app.template_filter("currency")
def currency_filter(cents):
    dollars = round(int(cents) / 100, 2)
    if dollars == 0:
        return "Free"
    if dollars.is_integer():
        dollars = int(dollars)
    return f"${dollars}"


from app import routes
