import pymysql


def get_conn():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 database='Cits3200')
    return connection


def query(sql: str) -> tuple:
    connection = get_conn()
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            print("query sql-", sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            print("query result-", result)
    return result


def update(sql: str) -> int:
    connection = get_conn()
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            print("update sql-", sql)
            cursor.execute(sql)
            affectedRows = cursor.rowcount
            print("update result-", affectedRows)
        connection.commit()

    return affectedRows
