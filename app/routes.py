import email
from app import app, db
from app.forms import checkinForm
from app.models import Attendee
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.urls import url_parse
from sqlalchemy import func, extract
from mapper import user_db

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

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
       
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        print(username, password, email)
        if (not user_db.check_user_exist(username)):
            user_db.insert_new_user(username, password, email)
            uid = user_db.get_user_by_name(username)[0][0]
            user_db.insert_new_user_role(uid,1)
    
        