import sqlite3
import uuid
import hashlib

path = None
pepper = ""


def _new_uuid(table=None, column=None) -> str:
    key = uuid.uuid4().hex[:8]
    if table:
        # check for collisions
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            while True:
                match = cursor.execute(
                    f"SELECT * FROM {table} WHERE {column} = (?)", (key,)
                ).fetchone()
                if match is None:
                    break
                key = uuid.uuid4().hex[:8]

    return str(key)


def _hash_user_password(username, password):
    hash = hashlib.sha512()
    hash.update(pepper.encode("utf-8"))  # Pepper
    hash.update(username.encode("utf-8"))  # Salt
    hash.update(password.encode("utf-8"))
    return hash.hexdigest()


def get_events() -> list:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'Event'")
        return cursor.fetchall()


def get_admin_events(admin) -> list:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'Event' WHERE eventAdmin = (?)", (admin,))
        return cursor.fetchall()


def get_event_by_id(eventID) -> sqlite3.Row:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'Event' WHERE eventID = (?)", (eventID,))
        return cursor.fetchone()


def get_guests_by_event(eventID) -> list:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM 'Guest' WHERE eventID = (?) ORDER BY paymentStatus DESC, bookingTime",
            (eventID,),
        )
        return cursor.fetchall()


def add_guest(
    firstname, lastname, email, phone, diet, eventID, badgeLocation, guests, paymentStatus=0
) -> str:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        userID = _new_uuid("guest", "guestID")
        cursor.execute(
            "INSERT INTO Guest(guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID, badgeLocation, numDependents, paymentStatus) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                userID,
                firstname,
                lastname,
                email,
                phone,
                diet,
                eventID,
                badgeLocation,
                guests,
                paymentStatus,
            ),
        )
        conn.commit()
    return userID


def set_payment_status(guestID, status):
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE 'Guest' SET paymentStatus = (?) WHERE guestID = (?)",
            (
                status,
                guestID,
            ),
        )
        conn.commit()


def delete_guest(guestID):
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'Guest' WHERE guestID = (?)", (guestID,))
        conn.commit()


def add_event(
    name,
    host,
    date,
    start,
    end,
    location,
    admin,
    productID="",
    ticketPrice=0,
) -> None:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Event(eventID, eventName, eventHost, eventDate, startTime, endTime, eventLocation, stripeProductID, eventPrice, eventAdmin) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                _new_uuid("event", "eventID"),
                name,
                host,
                date,
                start,
                end,
                location,
                admin,
                productID,
                ticketPrice,
            ),
        )
        conn.commit()


# def get_admin_by_username(username) -> sqlite3.Row:
#     with sqlite3.connect(path) as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM 'admin' WHERE username = (?)", (username,))
#         return cursor.fetchone()


def check_user_exists(username) -> bool:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'admin' WHERE username = (?)", (username,))
        exists = cursor.fetchone() is not None
        return exists


def check_user_password(username, password) -> bool:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = (?)", (username,))
        user = cursor.fetchone()

        if user is None:
            return False

        hash = _hash_user_password(username, password)

        if user["password"] == hash:
            return True
        return False


def get_user_email(username) -> sqlite3.Row:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = (?)", (username,))
        user = cursor.fetchone()

        if user:
            return user["email"]

        return None


def add_user(username, password, email):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        password_hash = _hash_user_password(username, password)

        cursor.execute(
            "INSERT INTO admin(username, password, email, firstname) VALUES(?, ?, ?, '')",
            (
                username,
                password_hash,
                email,
            ),
        )
        conn.commit()


def change_password(username, password):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        password_hash = _hash_user_password(username, password)

        cursor.execute(
            "UPDATE admin SET password = (?) WHERE username = (?)",
            (password_hash, username),
        )
        conn.commit()


def add_token(username) -> str:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        token = _new_uuid("token", "token")

        cursor.execute(
            "INSERT INTO token(username, token) VALUES (?,?)", (username, token)
        )
        conn.commit()

        return token


def check_token(username, token) -> bool:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Delete tokens that are older than an hour
        cursor.execute("DELETE FROM token WHERE age <= datetime('now','-1 hour')")
        conn.commit()

        cursor.execute(
            "SELECT * FROM token WHERE username = (?) AND token = (?)",
            (username, token),
        )
        user_token = cursor.fetchone()

        cursor.execute(
            "DELETE FROM token WHERE username = (?) AND token = (?)", (username, token)
        )
        conn.commit()

        return bool(user_token)
