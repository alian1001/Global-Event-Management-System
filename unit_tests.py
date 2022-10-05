import unittest
from app import app
import sqlite3
import stripe


class TestDBModel(unittest.TestCase):
    def test_connection_to_database(self):
        try:
            self.connection = sqlite3.connect("db.sqlite3")
        except:
            print("Could not connect the database")
        finally:
            pass


class TestEventModel(unittest.TestCase):
    def test_adding_new_event(self):

        name = "Jim's BBQ"
        host = "Jim"
        date = "30/09/2022"
        start = "1pm"
        end = "3pm"
        location = "Jim's House"
        productid = 12345

        sql = """ INSERT INTO Event(eventName, eventHost, eventDate, startTime, endTime, eventLocation, stripeProductID)
                       VALUES(?,?,?,?,?,?,?) """
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql, (name, host, date, start, end, location, productid))
        conn.commit()


if __name__ == "__main__":
    unittest.main()
