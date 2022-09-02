from app.models import Attendee
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length

class checkinForm(FlaskForm):
    firstname = StringField('Firstname:',  validators=[DataRequired()])
    lastname = StringField('Lastname:',  validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    phone = StringField('Phone:', validators=[DataRequired()])
    diet = StringField('Diet:', validators=[DataRequired()])
    guests = StringField('Guests:', validators=[DataRequired()])
    
    submit = SubmitField('Check In')
    

    def validate_email(self, email):
        attendee = Attendee.query.filter_by(email=email.data).first()
        if attendee is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        attendee = Attendee.query.filter_by(email=phone.data).first()
        if attendee is not None:
            raise ValidationError('Please use a different phone number.')
