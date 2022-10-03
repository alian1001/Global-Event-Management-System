# from app.models import Attendee
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, IntegerField, DecimalField, SelectField, PasswordField, BooleanField, DateField, TimeField, validators
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length, NumberRange

class checkinForm(FlaskForm):
    firstname = StringField('Firstname:',  validators=[DataRequired()])
    lastname = StringField('Lastname:',  validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    phone = StringField('Mobile Phone:', validators=[DataRequired(), Length(min=10, max=10)])
    diet = StringField('Dietary Requirements:',  validators=[DataRequired()])
    guests = IntegerField(u'Additional Guests:', validators=[NumberRange(min=0)])
    
    submit = SubmitField('Check In')
	
class checkinAndPayForm(FlaskForm):
    firstname = StringField('Firstname:',  validators=[DataRequired()])
    lastname = StringField('Lastname:',  validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    phone = StringField('Mobile Phone:', validators=[DataRequired(), Length(min=10, max=10)])
    diet = StringField('Dietary Requirements:',  validators=[DataRequired()])
    guests = IntegerField(u'Additional Guests:', validators=[NumberRange(min=0)])
    
    submit = SubmitField('Check In & Pay')

class eventForm(FlaskForm):
    event_name = StringField('Event Name:',  validators=[DataRequired()])
    event_host = StringField('Host of Event:',  validators=[DataRequired()])
    event_date = DateField('Date of Event:', format='%Y-%m-%d')
    event_time_start = TimeField('Start Time:', format='%H:%M', validators=[DataRequired()])
    event_time_end = TimeField('End Time:', format='%H:%M', validators=[DataRequired()])
    event_location = StringField('Location:',  validators=[DataRequired()])
    ticket_price = DecimalField(u'Price per Ticket ($):', validators=[NumberRange(min=0)])
	
    submit = SubmitField('Create Event')