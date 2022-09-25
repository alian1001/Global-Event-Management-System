# from app.models import Attendee
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, BooleanField, DateField, TimeField, validators
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length

class checkinForm(FlaskForm):
    firstname = StringField('Firstname:',  validators=[DataRequired()])
    lastname = StringField('Lastname:',  validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    phone = StringField('Phone:', validators=[DataRequired()])
    diet = StringField('Diet:', validators=[DataRequired()])
    guests = StringField('Guests:', validators=[DataRequired()])
    
    submit = SubmitField('Check In')

class eventForm(FlaskForm):
    event_name = StringField('Event Name:',  validators=[DataRequired()])
    event_host = StringField('Host of Event:',  validators=[DataRequired()])
    event_date = DateField('Date of Event:', format='%Y-%m-%d')
    event_time_start = TimeField('Start Time:', format='%H:%M', validators=[DataRequired()])
    event_time_end = TimeField('End Time:', format='%H:%M', validators=[DataRequired()])
    event_location = StringField('Location:',  validators=[DataRequired()])
    submit = SubmitField('Create Event')