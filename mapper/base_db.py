from sqlalchemy import create_engine




def get_conn():
    engine = create_engine('sqlite:///db.sqlite3')
    connection = engine.raw_connection()
    return connection


def query(sql: str) -> tuple:
    connection = get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result


def update(sql: str) -> int:
    connection = get_conn()
    cursor = connection.cursor()
    # Create a new record
    print("update sql-", sql)
    cursor.execute(sql)
    affectedRows = cursor.rowcount
    print("update result-", affectedRows)
    connection.commit()
    cursor.close()
    connection.close()
    return affectedRows
