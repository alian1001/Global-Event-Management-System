from app import app
from app.forms import checkinForm, checkinAndPayForm, eventForm
from flask import Flask, render_template, redirect, url_for, request, session,current_app
from werkzeug.urls import url_parse
from sqlalchemy import func, extract
from mapper import user_db, base_db
from threading import Thread
from flask_mail import Message
from flask_mail import Mail
import random
import sqlite3
from sqlalchemy import create_engine
mail = Mail()
mail.init_app(app)


   

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(user_email,token, subject='Reset Your Password', template='reset_password'):
    app = current_app._get_current_object()
    msg = Message( ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[user_email])
    msg.body = render_template(template + '.txt',token=token)
    msg.html = render_template(template + '.html',token=token)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr



@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home'))
    
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html', title='Home')

@app.route('/currentevent', methods=['GET'])
def currentevent():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Event'")
	
    return render_template('currentevent.html', title='Current Events', events=cursor.fetchall())

@app.route('/users', methods=['GET'])
def users():
    return render_template('users.html', title='Users')

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

@app.route('/checkinAndPay', methods = ['GET', 'POST'])
def checkinAndPay():
    form = checkinAndPayForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        diet = form.diet.data
        guests = form.guests.data

        user_db.insert_new_checkin(firstname, lastname, email, phone, diet, guests)
        return redirect(url_for('home'))
    
    return render_template('checkinAndPay.html', title = 'Check In & Pay', form=form)

@app.route('/event', methods = ['GET', 'POST'])
def create_event():
    form = eventForm()
    if form.validate_on_submit():
        name = form.event_name.data
        host = form.event_host.data
        date = form.event_date.data
        start = str(form.event_time_start.data)
        end = str(form.event_time_end.data)
        location = form.event_location.data
		
        sql = ''' INSERT INTO Event(eventName, eventHost, eventDate, startTime, endTime, eventLocation)
                       VALUES(?,?,?,?,?,?) '''
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(sql, (name, host, date, start, end, location) )
        conn.commit()
        return redirect(url_for('home'))

    return render_template('event.html', title = 'Create Event', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('user_name')
        password = request.form.get('password')

        # sql = "select * from user where username = '%s'" % username
        # result = base_db.query(sql)
        result =user_db.get_user_by_name(username)
        # print(result)
        print(result[0][1],password)
        if len(result) != 0:
            if str(result[0][1]) == str(password):
                session['username'] = result[0][0]
                session.permanent = True
                if username == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return render_template('home.html')
            else:
                return u'Incorrect password.'
        else:
            return u'User does not exist.'

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
            return u'User already exists.'

@app.route ('/forgetpassword', methods=['GET', 'POST'])
def forgetpassword():
    if request.method == 'GET':
        return render_template('forgetpassword.html')
    else:
        username = request.form.get('user_name')
        user_email= request.form.get('email')
        Verification_Code =  request.form.get('Verification_Code')
        if not Verification_Code:
            token = ''.join([str(i) for i in random.sample(range(100),4)])    
            app = current_app._get_current_object()

            user_db.modify_user_token(username, token)
            send_email(user_email,token, subject='Reset Your Password', template='reset_password')

            return render_template('forgetpassword.html')
        elif Verification_Code:
            dbtoken =  user_db.get_user_by_name(username)
            if str(dbtoken[0][-1]) == str(Verification_Code):
                

                newpassword=  request.form.get('newpassword')
                user_db.modify_user_pwd(username, newpassword)
                return render_template('home.html', title='Home')

        return render_template('forgetpassword.html')