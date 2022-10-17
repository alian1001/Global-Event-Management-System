import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

path = "db.sqlite3"

sql = """
CREATE TABLE Guest (
    guestID TEXT PRIMARY KEY NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT NOT NULL,
    mobileNumber TEXT NOT NULL,
    dietaryReq TEXT NOT NULL,
    eventID TEXT NOT NULL REFERENCES Event (eventID) ON DELETE CASCADE ON UPDATE CASCADE,
    badgeLocation TEXT NOT NULL,
    paymentStatus BOOL NOT NULL DEFAULT 0,
    bookingTime NOT NULL DEFAULT CURRENT_TIMESTAMP
    numDependents INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Dependent (
    dependentID TEXT PRIMARY KEY NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    guestID TEXT REFERENCES Guest (guestID) ON DELETE CASCADE ON UPDATE CASCADE,
    dietaryReq TEXT,
    guestRelationship TEXT NOT NULL
);

CREATE TABLE Event (
    eventID TEXT NOT NULL,
    eventName TEXT NOT NULL,
    eventHost TEXT NOT NULL,
    eventDate DATE NOT NULL,
    startTime TIME NOT NULL,
    endTime TIME NOT NULL,
    eventLocation TEXT NOT NULL,
    eventDescription TEXT,
    stripeProductID TEXT,
    eventPrice INTEGER NOT NULL DEFAULT 0,
    eventAdmin TEXT REFERENCES Admin (userName),
    PRIMARY KEY (eventID)
);

CREATE TABLE Admin (
    userName TEXT NOT NULL UNIQUE PRIMARY KEY,
    password TEXT NOT NULL,
    firstName TEXT NOT NULL,
    email TEXT UNIQUE
);

INSERT INTO Admin(userName, password, firstName, email)
VALUES("root","51df5b80cc61c677e340be9b3b6adae7aedd5dece961d3a25fcefe95d62d3b66283a8f5b2b80916042811c671a6bb751fca595ae115917a10179005def346e02","root","");

INSERT INTO Admin(userName, password, firstName, email)
VALUES("oliver","65228aec4d505e9a86737c935597988b4a5a68a41dfac88b8a569267db218487272034128ec6c56ed056bfadca82ed947f98ff65e9f1d840cbd517d26808a685","Oliver","22989775@student.uwa.edu.au");

INSERT INTO Event 
VALUES("67a459b1","Public Art Exhibit","Jane Artist","2022-12-30","12:00:00","20:00:00","James Oval, UWA","","",0,"root");

INSERT INTO Event 
VALUES ("caef73db","Exclusive Music Event","David Musician","2022-12-29","19:00:00","21:00:00","Octagon Theatre, UWA","","prod_MYkBLqlc7Zdv7f",1500,"oliver");

INSERT INTO Guest (guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID, badgeLocation, paymentStatus)
VALUES ("bb83530c", "Sally", "Davidson", "sally.d@gmail.com", "1234512345", "Vegetarian", "67a459b1", "badge-0001.pdf", 0);

INSERT INTO Guest (guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID, badgeLocation, paymentStatus)
VALUES ("9bd38e1f", "David", "Appleseed", "d.appleseed@gmail.com", "0123401234", "None", "67a459b1", "badge-0002.pdf", 0);

INSERT INTO Guest (guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID, badgeLocation, paymentStatus)
VALUES ("c4df9b63", "Jane", "French", "j.french@hotmail.com", "5432154321", "Vegan", "caef73db", "badge-0003.pdf", 0);

INSERT INTO Guest (guestID, firstName, lastName, email, mobileNumber, dietaryReq, eventID, badgeLocation, paymentStatus)
VALUES ("00d1cc8e", "Ronald", "McDonald", "ronald@maccas.com", "1234512345", "Meal must include toy", "caef73db", "badge-0004.pdf", 0);
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
