import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

path = "db.sqlite3"

sql = """
CREATE TABLE Event (eventID TEXT PRIMARY KEY NOT NULL, eventName TEXT NOT NULL, eventHost TEXT NOT NULL, eventDate DATE NOT NULL, startTime TIME NOT NULL, endTime TIME NOT NULL, eventLocation TEXT NOT NULL, eventDescription TEXT, stripeProductID TEXT, eventPrice NOT NULL DEFAULT 0);
CREATE TABLE Guest (guestID TEXT PRIMARY KEY NOT NULL, firstName TEXT NOT NULL, lastName TEXT NOT NULL, email TEXT NOT NULL, mobileNumber TEXT NOT NULL, dietaryReq TEXT NOT NULL, eventID TEXT NOT NULL REFERENCES Event (eventID) ON DELETE CASCADE ON UPDATE CASCADE);
CREATE TABLE Dependent (dependentID TEXT PRIMARY KEY NOT NULL, firstName TEXT NOT NULL, lastName TEXT NOT NULL, guestID TEXT REFERENCES Guest (guestID) ON DELETE CASCADE ON UPDATE CASCADE, dietaryReq TEXT, guestRelationship TEXT NOT NULL);
CREATE TABLE User (userName TEXT NOT NULL UNIQUE PRIMARY KEY, password TEXT NOT NULL, email TEXT, token int);

INSERT INTO User(username,password) VALUES("root","root");
INSERT INTO Event VALUES ("67a459b1","Public Art Exhibit","Jane Artist","2022-12-30","12:00:00","20:00:00","James Oval, UWA","","",0);
INSERT INTO Event VALUES ("caef73db","Exclusive Music Event","David Musician","2022-12-29","19:00:00","21:00:00","Octagon Theatre, UWA","","prod_MYkBLqlc7Zdv7f",1500);

INSERT INTO Guest VALUES ("bb83530c", "Sally", "Davidson", "sally.d@gmail.com", "1234512345", "Vegetarian", "67a459b1");
INSERT INTO Guest VALUES ("9bd38e1f", "David", "Appleseed", "d.appleseed@gmail.com", "0123401234", "None", "67a459b1");
INSERT INTO Guest VALUES ("c4df9b63", "Jane", "French", "j.french@hotmail.com", "5432154321", "Vegan", "caef73db");
INSERT INTO Guest VALUES ("00d1cc8e", "Ronald", "McDonald", "ronald@maccas.com", "1234512345", "Meal must include toy", "caef73db");
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
