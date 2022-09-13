from app import app, db
from app.forms import checkinForm, eventForm
from app.models import Attendee, Event
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.urls import url_parse
from sqlalchemy import func, extract

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', title = 'Home')

@app.route('/checkin', methods = ['GET', 'POST'])
def checkin():
    form = checkinForm()
    if form.validate_on_submit():
        attendee = Attendee(firstname = form.firstname.data, lastname = form.lastname.data,
                            email = form.email.data, phone = form.phone.data, diet = form.diet.data)
        db.session.add(attendee)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('checkin.html', title = 'Check In', form=form)

@app.route('/event', methods = ['GET', 'POST'])
def create_event():
    form = eventForm()
    if form.validate_on_submit():
        event = Event(event_name = form.event_name.data, event_date = form.event_date.data, 
                        event_time = form.event_time.data, event_location = form.event_location.data)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('event.html', title = 'Create Event', form=form)