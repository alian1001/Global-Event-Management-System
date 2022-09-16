from mapper import base_db


def get_all_appointment() -> tuple:
    sql = "select * from apply"
    return base_db.query(sql)
