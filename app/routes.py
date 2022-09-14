import email
from genericpath import exists
from re import U
from unittest import result
from webbrowser import get
from app import app, db
from app.forms import checkinForm
from app.models import Attendee
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.urls import url_parse
from sqlalchemy import func, extract
from mapper import user_db, base_db, Apply_db
import json
import time
import os

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
        db.ssesion.add(attendee)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('checkin.html', title = 'Check In', form=form)

