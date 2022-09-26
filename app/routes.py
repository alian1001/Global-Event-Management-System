from app import app
from app.forms import checkinForm, eventForm
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.urls import url_parse
from sqlalchemy import func, extract
from mapper import user_db, base_db, Apply_db

import stripe
stripe.api_key = app.config["STRIPE_SECRET"]

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home'))
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html', title='Home')

@app.route('/checkin', methods = ['GET', 'POST'])
def checkin():
    form = checkinForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        diet = form.diet.data
        guests = form.guests.data

        user_db.insert_new_checkin(firstname, lastname, email, phone, diet, guests)
        return redirect(url_for('home'))
    
    return render_template('checkin.html', title = 'Check In', form=form)

@app.route('/event', methods = ['GET', 'POST'])
def create_event():
    form = eventForm()
    if form.validate_on_submit():
        
        stripe.Product.create(name=form.event_name.data, shippable=False)



        # event = Event(event_name = form.event_name.data, event_date = form.event_date.data, 
        #                 event_time = form.event_time.data, event_location = form.event_location.data)
        # db.session.add(event)
        # db.session.commit()
        # return redirect(url_for('home'))
    return render_template('event.html', title = 'Create Event', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('user_name')
        password = request.form.get('password')

        sql = "select * from user where username = '%s'" % username
        result = base_db.query(sql)
        # print(result)
        print(password)
        if len(result) != 0:
            if result[0][2] == password:
                session['username'] = result[0][0]
                session.permanent = True
                if username == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return render_template('home.html')
            else:
                return u'wrong password'
        else:
            return u'user does not exist'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        print(username,password, email)
        if not user_db.check_user_exist(username):
            user_db.insert_new_user(username, password, email)
            uid = user_db.get_user_by_name(username)[0][1]
            return redirect(url_for('login'))
        if user_db.check_user_exist(username):
            return u'user has exist'
