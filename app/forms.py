# from app.models import Attendee
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    TextAreaField,
    StringField,
    IntegerField,
    DecimalField,
    SelectField,
    PasswordField,
    BooleanField,
    DateField,
    TimeField,
    validators,
    FileField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    ValidationError,
    EqualTo,
    Length,
    NumberRange,
)
from flask_wtf.file import (
    FileAllowed,
)


class checkinForm(FlaskForm):
    firstname = StringField("Firstname:", validators=[DataRequired()])
    lastname = StringField("Lastname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    phone = IntegerField(
        "Mobile Phone:", validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)]
    )
    diet = StringField("Dietary Requirements:", validators=[DataRequired()])
    guests = IntegerField("Additional Guests:", validators=[NumberRange(min=0)])
    image = FileField("Upload Badge Image (.png .jpg .jpeg only!):", validators=[DataRequired(), FileAllowed(['png', 'jpg', 'jpeg'], "invalid image format!")])

    submit = SubmitField("Check In")

    #Create a checkbox for terms and conditions
    terms = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    


class eventForm(FlaskForm):
    event_name = StringField("Event Name:", validators=[DataRequired()])
    event_host = StringField("Host of Event:", validators=[DataRequired()])
    event_date = DateField("Date of Event:", format="%Y-%m-%d")
    event_time_start = TimeField(
        "Start Time:", format="%H:%M", validators=[DataRequired()]
    )
    event_time_end = TimeField("End Time:", format="%H:%M", validators=[DataRequired()])
    event_location = StringField("Location:", validators=[DataRequired()])
    ticket_price = DecimalField(
        "Price per Ticket ($):", validators=[NumberRange(min=0)]
    )

    submit = SubmitField("Create Event")
    
