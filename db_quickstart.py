import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

path = "db.sqlite3"

sql = """
CREATE TABLE Event (eventID TEXT PRIMARY KEY NOT NULL, eventName TEXT NOT NULL, eventHost TEXT NOT NULL, eventDate DATE NOT NULL, startTime TIME NOT NULL, endTime TIME NOT NULL, eventLocation TEXT NOT NULL, eventDescription TEXT, stripeProductID TEXT, eventPrice NOT NULL DEFAULT 0);
CREATE TABLE Guest (guestID TEXT PRIMARY KEY NOT NULL, firstName TEXT NOT NULL, lastName TEXT NOT NULL, email TEXT NOT NULL, mobileNumber TEXT NOT NULL, dietaryReq TEXT NOT NULL, eventID TEXT NOT NULL REFERENCES Event (eventID) ON DELETE CASCADE ON UPDATE CASCADE);
CREATE TABLE Dependent (dependentID TEXT PRIMARY KEY NOT NULL, firstName TEXT NOT NULL, lastName TEXT NOT NULL, guestID TEXT REFERENCES Guest (guestID) ON DELETE CASCADE ON UPDATE CASCADE, dietaryReq TEXT, guestRelationship TEXT NOT NULL);
CREATE TABLE User (userName TEXT NOT NULL UNIQUE PRIMARY KEY, password TEXT NOT NULL, email TEXT, token int);

INSERT INTO User(username,password) VALUES("admin","admin");
"""


def main():
    if os.path.exists(path):
        print(f"{path} already exists. ")
        return

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.executescript(sql)


if __name__ == "__main__":
    main()
