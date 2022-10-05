from app import app
from app.forms import checkinForm, checkinAndPayForm, eventForm
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    current_app,
    jsonify,
    flash,
)
from werkzeug.urls import url_parse
from sqlalchemy import func, extract
from mapper import user_db, base_db
from threading import Thread
from flask_mail import Message
from flask_mail import Mail
import random
import sqlite3
from sqlalchemy import create_engine
import stripe

mail = Mail()
mail.init_app(app)

stripe.api_key = app.config["STRIPE_SECRET"]
session1 = 0


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(
    user_email, token, subject="Reset Your Password", template="reset_password"
):
    app = current_app._get_current_object()
    msg = Message(
        " " + subject, sender=app.config["FLASKY_MAIL_SENDER"], recipients=[user_email]
    )
    msg.body = render_template(template + ".txt", token=token)
    msg.html = render_template(template + ".html", token=token)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route("/", methods=["GET"])
def index():

    return redirect(url_for("home"))


@app.route("/bookingsuccess", methods=["GET"])
def bookingsuccess():

    return render_template("bookingsuccess.html")


@app.route("/home", methods=["GET"])
def home():
    if session1 == 0:
        session.clear()
    status = False
    print(session.get("username"), "username")
    if session.get("login") == "OK" and session.get("username"):
        status = True
    return render_template(
        "home.html", title="Home", status=status, username=session.get("username")
    )


@app.route("/currentevent", methods=["GET"])
def currentevent():
    if session1 == 0:
        session.clear()
    status = False
    print(session.get("username"), "username")
    if session.get("login") == "OK" and session.get("username"):
        status = True

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Event'")

    return render_template(
        "currentevent.html",
        title="Current Events",
        status=status,
        events=cursor.fetchall(),
        username=session.get("username"),
    )


@app.route("/clientevent", methods=["GET"])
def clientEvent():
    if session1 == 0:
        session.clear()
    status = False
    print(session.get("username"), "username")
    if session.get("login") == "OK" and session.get("username"):
        status = True

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Event'")

    return render_template(
        "currenteventsclient.html",
        title="Current Events",
        status=status,
        events=cursor.fetchall(),
        username=session.get("username"),
    )


@app.route("/users", methods=["GET"])
def users():
    if session1 == 0:
        session.clear()
    status = False
    print(session.get("username"), "username")
    if session.get("login") == "OK" and session.get("username"):
        status = True
    return render_template(
        "users.html", title="Users", status=status, User=session.get("username")
    )


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    form = checkinForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        diet = form.diet.data

        sql = """ INSERT INTO Guest(eventID, firstName, lastName, email, mobileNumber, dietaryReq)
                       VALUES(?,?,?,?,?,?) """
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql, ("1", firstname, lastname, email, phone, diet))
        conn.commit()
        flash("Registered Successfully! Check your email for confirmation")
        return redirect(url_for("bookingsuccess"))

    return render_template("checkin.html", title="Check In", form=form)


@app.route("/checkinAndPay", methods=["GET", "POST"])
def checkinAndPay():
    form = checkinAndPayForm()

    # Return user to events page if no event specified
    if "eventID" not in request.args:
        return redirect(url_for("bookingsuccess"), code=303)

    eventID = request.args["eventID"]

    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        conn = sqlite3.connect("db.sqlite3")
        cursor.execute("SELECT * FROM 'Event' WHERE eventID = (?)", (eventID,))
        event = cursor.fetchone()

        product = stripe.Product.retrieve(event[8], expand=["default_price"])

        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            phone = form.phone.data
            diet = form.diet.data
            guests = int(form.guests.data)

            try:

                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                            "price": product.default_price.id,
                            "quantity": guests + 1,
                        },
                    ],
                    mode="payment",
                    success_url=url_for("bookingsuccess", _external=True),
                    cancel_url=url_for("clientEvent", _external=True),
                    customer_email=email,
                )
            except Exception as e:
                return str(e)

            sql = """ INSERT INTO Guest(firstName, lastName, email, mobileNumber, dietaryReq, eventID)
                    VALUES(?,?,?,?,?,?) """

            cursor.execute(sql, (firstname, lastname, email, phone, diet, eventID))
            conn.commit()

            return redirect(checkout_session.url, code=303)
        unit_price = round(product.default_price.unit_amount / 100, 2)
        unit_price = (
            int(unit_price) if unit_price.is_integer() else unit_price
        )  # Remove .00 unless required
        price = f"${unit_price} per person"

        return render_template(
            "checkinAndPay.html",
            title="Check In & Pay",
            form=form,
            event=event,
            price=price,
        )


@app.route("/event", methods=["GET", "POST"])
def create_event():
    form = eventForm()
    if form.validate_on_submit():
        name = form.event_name.data
        host = form.event_host.data
        date = form.event_date.data
        start = str(form.event_time_start.data)
        end = str(form.event_time_end.data)
        location = form.event_location.data
        ticketprice = form.ticket_price.data

        if ticketprice:
            product = stripe.Product.create(
                name=f"{name} Ticket",
                shippable=False,
                description=f"{host} - {date} {start} to {end}, {location}.",
                default_price_data={
                    "currency": "aud",
                    "unit_amount_decimal": ticketprice
                    * 100,  # Convert from dollars to cents
                },
            )
            productID = product.id
        else:
            productID = None

        sql = """ INSERT INTO Event(eventName, eventHost, eventDate, startTime, endTime, eventLocation, stripeProductID, eventPrice)
                       VALUES(?,?,?,?,?,?,?) """
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            sql, (name, host, date, start, end, location, productID, ticketprice)
        )
        conn.commit()

        return redirect(url_for("currentevent"))
    if session1 == 0:
        session.clear()
    status = False
    print(session.get("username"), "username")
    if session.get("login") == "OK" and session.get("username"):
        status = True
    return render_template(
        "event.html",
        title="Create Event",
        status=status,
        form=form,
        username=session.get("username"),
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    session["login"] = ""

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("user_name")
        password = request.form.get("password")

        # sql = "select * from user where username = '%s'" % username
        # result = base_db.query(sql)
        result = user_db.get_user_by_name(username)
        # print(result)
        print(result[0][1], password)
        if len(result) != 0:
            if str(result[0][1]) == str(password):
                print(result, "result")
                session["username"] = result[0][0]
                session["login"] = "OK"
                session.permanent = True
                global session1
                session1 = 1
                if username == "admin":
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("users"))
            else:
                return "Incorrect password."
        else:
            return "User does not exist."


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        print(username, password, email)
        if not user_db.check_user_exist(username):
            user_db.insert_new_user(username, password, email)
            uid = user_db.get_user_by_name(username)[0][1]
            return redirect(url_for("login"))
        if user_db.check_user_exist(username):
            return "User already exists."


@app.route("/forgetpassword", methods=["GET", "POST"])
def forgetpassword():
    if request.method == "GET":
        return render_template("forgetpassword.html")
    else:
        username = request.form.get("user_name")
        user_email = request.form.get("email")
        Verification_Code = request.form.get("Verification_Code")
        if not Verification_Code:
            token = "".join([str(i) for i in random.sample(range(100), 4)])
            app = current_app._get_current_object()

            user_db.modify_user_token(username, token)
            send_email(
                user_email,
                token,
                subject="Reset Your Password",
                template="reset_password",
            )

            return render_template("forgetpassword.html")
        elif Verification_Code:
            dbtoken = user_db.get_user_by_name(username)
            if str(dbtoken[0][-1]) == str(Verification_Code):

                newpassword = request.form.get("newpassword")
                user_db.modify_user_pwd(username, newpassword)
                return render_template("home.html", title="Home")

        return render_template("forgetpassword.html")


@app.route("/logout", methods=["GET"])
def logout():
    """logout"""
    # clear session
    session.clear()
    status = False
    global session1
    session1 = 0
    return render_template("home.html", title="Home", status=status)
