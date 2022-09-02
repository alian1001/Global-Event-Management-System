from app import db
from datetime import date

class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    diet = db.Column(db.String(64), index=True)
    guests = db.Column(db.String(120), index=True, unique=True)

