import sqlite3
import uuid
import hashlib

path = None
pepper = ""


def new_uuid(table=None, column=None) -> str:
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


def hash_user_password(username, password):
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
        cursor.execute("SELECT * FROM 'Guest' WHERE eventID = (?)", (eventID,))
        return cursor.fetchall()


def add_guest(firstname, lastname, email, phone, diet, eventID) -> None:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        userID = new_uuid("guest", "guestID")
        cursor.execute(
            "INSERT INTO Guest(guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID) VALUES(?,?,?,?,?,?,?)",
            (
                userID,
                firstname,
                lastname,
                email,
                phone,
                diet,
                eventID,
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
                new_uuid("event", "eventID"),
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
        cursor.execute("SELECT * FROM 'admin' WHERE username = (?)", (username,))
        user = cursor.fetchone()

        if user is None:
            return False

        hash = hash_user_password(username, password)

        if user["password"] == hash:
            return True
        return False


def get_user_by_email(email) -> sqlite3.Row:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'admin' WHERE email = (?)", (email,))
        user = cursor.fetchone()

        return user


def add_user(username, password, email):
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        password_hash = hash_user_password(username, password)

        cursor.execute(
            "INSERT INTO admin(username, password, email, firstname) VALUES(?, ?, ?, '')",
            (
                username,
                password_hash,
                email,
            ),
        )
