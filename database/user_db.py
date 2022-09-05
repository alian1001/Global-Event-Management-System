from mapper import base_db


def get_all_users() -> tuple:
    sql = "select * from user"
    return base_db.query(sql)

# page_num 从 0 开始
def get_all_users_by_page(page_num, page_len) -> tuple:
    sql = "select * from user limit %s, %s" % (page_len * page_num, page_len)
    return base_db.query(sql)


def check_user_exist(name) -> bool:
    sql = "select * from user where username='%s'" % (name)
    if len(base_db.query(sql)) > 0:
        return True
    else:
        return False



def check_user_pwd(name, pwd) -> bool:
    sql = "select * from user where username='%s' and password='%s'" % (name, pwd)
    if len(base_db.query(sql)) > 0:
        return True
    else:
        return False


def get_user_by_name(name) -> tuple:
    sql = "select * from user where username='%s'" % (name)
    return base_db.query(sql)


def get_user_role_by_uid(user_id: int) -> str:
    sql = "select rid from user_role where uid='%s'" % (user_id)
    res = base_db.query(sql)
    if len(res) > 0:
        return res[0][0]
    return 'none'


def modify_user_pwd(name, newpwd, oldpwd) -> bool:
    sql = "update user set password='%s' where username='%s' and password='%s'" % (newpwd, name, oldpwd)
    if base_db.update(sql) > 0:
        return True
    else:
        return False


def insert_new_user(name, pwd, mail) -> bool:
    sql = "insert into user(username, password, email) values ('%s', '%s', '%s')" % (name, pwd, mail)
    if base_db.update(sql) > 0:
        return True
    else:
        return False


def insert_new_user_role(uid, rid) -> bool:
    sql = "insert into user_role(uid, rid) values ('%s', '%s')" % (uid, rid)
    if base_db.update(sql) > 0:
        return True
    else:
        return False


