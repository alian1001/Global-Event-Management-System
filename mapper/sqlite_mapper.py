import sqlite3
import uuid

path = None


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
        cursor.execute(
            "INSERT INTO Guest(guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID) VALUES(?,?,?,?,?,?,?)",
            (
                new_uuid("guest", "guestID"),
                firstname,
                lastname,
                email,
                phone,
                diet,
                eventID,
            ),
        )
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
