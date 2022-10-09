from app import app
from app.forms import checkinForm, eventForm
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    session,
    current_app,
    flash,
    abort,
    jsonify,
)

from mapper import sqlite_mapper as db
from threading import Thread
from flask_mail import Message, Mail
from functools import wraps
import stripe
import json

mail = Mail()
mail.init_app(app)

stripe.api_key = app.config["STRIPE_SECRET"]
endpoint_secret = app.config["STRIPE_WEBHOOK_SECRET"]


db.pepper = app.config["SECRET_PEPPER"]
db.path = app.config["DATABASE_PATH"]


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = session.get("username")
        if username is not None:
            if db.check_user_exists(username):
                return f(*args, **kwargs)

        return redirect(url_for("login"))

    return wrap


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


@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", title="Home", username=session.get("username"))


@app.route("/bookingsuccess", methods=["GET"])
def bookingsuccess():
    return render_template(
        "bookingsuccess.html",
        username=session.get("username"),
    )


@app.route("/events", methods=["GET"])
def events():
    events = db.get_events()

    return render_template(
        "events.html",
        title="Current Events",
        events=events,
        username=session.get("username"),
    )


@app.route("/users", methods=["GET"])
@login_required
def users():
    admin = session.get("username")
    events = db.get_admin_events(admin)

    return render_template(
        "users.html",
        title="Users",
        events=events,
        username=session.get("username"),
    )


@app.route("/checkin/<eventID>", methods=["GET", "POST"])
def checkin(eventID):
    form = checkinForm()

    event = db.get_event_by_id(eventID)

    if not event:
        return abort(404)

    product = None
    if event["stripeProductID"]:
        product = stripe.Product.retrieve(
            event["stripeProductID"], expand=["default_price"]
        )

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        diet = form.diet.data
        guests = int(form.guests.data)

        user = db.add_guest(firstname, lastname, email, phone, diet, eventID)

        if product:
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
                    cancel_url=url_for("events", _external=True),
                    customer_email=email,
                    client_reference_id=user,
                )
            except Exception as e:
                return str(e)

            return redirect(checkout_session.url, code=303)

        return redirect(url_for("bookingsuccess"))

    return render_template(
        "checkin.html",
        title="Check In",
        form=form,
        event=event,
        username=session.get("username"),
    )


@app.route("/newEvent", methods=["GET", "POST"])
@login_required
def create_event():
    form = eventForm()
    if form.validate_on_submit():
        name = form.event_name.data
        host = form.event_host.data
        date = form.event_date.data
        start = str(form.event_time_start.data)
        end = str(form.event_time_end.data)
        location = form.event_location.data
        ticketPrice = (
            float(form.ticket_price.data) * 100
        )  # Convert from dollars to cents
        admin = session.get("username")

        if ticketPrice:
            product = stripe.Product.create(
                name=f"{name} Ticket",
                shippable=False,
                description=f"{host} - {date} {start} to {end}, {location}.",
                default_price_data={
                    "currency": "aud",
                    "unit_amount_decimal": ticketPrice,
                },
            )
            productID = str(product.id)
        else:
            productID = ""

        db.add_event(
            name, host, date, start, end, location, productID, ticketPrice, admin
        )

        return redirect(url_for("currentevent"))

    return render_template(
        "newEvent.html",
        title="Create Event",
        form=form,
        username=session.get("username"),
    )


@app.route("/event/<eventID>", methods=["GET", "POST"])
def bookings(eventID):
    guests = db.get_guests_by_event(eventID)

    return render_template(
        "bookings.html",
        guests=guests,
        username=session.get("username"),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    session["username"] = ""

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("user_name")
    password = request.form.get("password")

    if db.check_user_password(username, password):
        session["username"] = username
        session.permanent = True

        return redirect(url_for("users"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if db.check_user_exists(username):
        return redirect(url_for("register"))

    db.add_user(username, password, email)

    flash("User Added!")
    return redirect(url_for("register"))


@app.route("/forgetpassword", methods=["GET", "POST"])
def forgetpassword():
    if request.method == "GET":
        return render_template("forgetpassword.html")

    # if request.method == "GET":
    #     return render_template("forgetpassword.html")
    # else:
    #     username = request.form.get("user_name")
    #     user_email = request.form.get("email")
    #     Verification_Code = request.form.get("Verification_Code")
    #     if not Verification_Code:
    #         token = "".join([str(i) for i in random.sample(range(100), 4)])
    #         app = current_app._get_current_object()

    #         user_db.modify_user_token(username, token)
    #         send_email(
    #             user_email,
    #             token,
    #             subject="Reset Your Password",
    #             template="reset_password",
    #         )

    #         return render_template("forgetpassword.html")
    #     elif Verification_Code:
    #         dbtoken = user_db.get_user_by_name(username)
    #         if str(dbtoken[0][-1]) == str(Verification_Code):

    #             newpassword = request.form.get("newpassword")
    #             user_db.modify_user_pwd(username, newpassword)
    #             return render_template("home.html", title="Home")

    #     return render_template("forgetpassword.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/webhook", methods=["POST"])
def webhook():
    event = None
    payload = request.data

    try:
        event = json.loads(payload)
    except:
        print("⚠️  Webhook error while parsing basic request.")
        return jsonify(success=False)

    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except stripe.error.SignatureVerificationError as e:
            print("⚠️  Webhook signature verification failed.")
            return jsonify(success=False)

        # Handle the event
    if event and event["type"] == "checkout.session.completed":
        checkout_session = event["data"]["object"]  # contains a stripe.PaymentIntent
        print(f"Payment for guest {checkout_session['client_reference_id']} succeeded")

        db.set_payment_status(checkout_session["client_reference_id"], 1)

    elif event["type"] == "checkout.session.expired":
        checkout_session = event["data"]["object"]  # contains a stripe.PaymentMethod
        print(f"Payment for guest {checkout_session['client_reference_id']} expired")

        db.delete_guest(checkout_session["client_reference_id"])

    else:
        # Unexpected event type
        print("Unhandled event type {}".format(event["type"]))

    return jsonify(success=True)
