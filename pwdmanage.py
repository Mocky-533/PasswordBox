import sqlite3
from encryption import encrypt, decrypt, get_md5

def register_check():
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    try:
        cur.execute("CREATE TABLE auth (account text, pass text)")
        cur.execute("""CREATE TABLE passwd (
            id integer primary key autoincrement,
            site text,
            account text,
            password text,
            date text,
            index_ac text
            )""")
    except sqlite3.OperationalError:
        pass
    cur.execute(f"""SELECT * FROM auth""")
    r = cur.fetchall()
    db.close()
    return r

def register(pwd):
    login_pwd_hashed = get_md5(pwd)
    user = ['admin']
    user.append(login_pwd_hashed)
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    register_command = """INSERT INTO auth VALUES (?,?)"""
    cur.execute(register_command, tuple(user))
    db.commit()
    db.close()

def login_check(pwd):
    pwd_hashed = get_md5(pwd)
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    cur.execute("""SELECT * FROM auth WHERE account='admin'""")
    result=cur.fetchone()
    db.close()
    return pwd_hashed == result[1]

def add(info: list):
    info[2] = encrypt(info[2], int(info[3][-2:]))
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    cur.execute(f"""INSERT INTO passwd (site, account, password, date, index_ac) VALUES {tuple(info)}""")
    db.commit()
    db.close()


def search_site(site: str):
    name = []
    name.append(site)
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    search = """SELECT * FROM passwd WHERE site=?"""
    cur.execute(search, tuple(name))
    result = cur.fetchall()
    db.close()
    re = []
    for col in result:
        col = list(col)
        col[3] = decrypt(col[3], int(col[4][-2:]))
        re.append(col)
    return re

def search_account(account: str):
    name = []
    name.append(account)
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    search = """SELECT * FROM passwd WHERE index_ac=?"""
    cur.execute(search, tuple(name))
    result = cur.fetchall()
    db.close()
    res = []
    for col in result:
        col = list(col)
        col[3] = decrypt(col[3], int(col[4][-2:]))
        res.append(col[:-1])
    return res

def update_pwd(info: list):
    info[1] = encrypt(info[1], int(info[2][-2:]))
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    update_command = """UPDATE passwd SET password=?, date=? WHERE id=?"""
    cur.execute(update_command, tuple(info))
    db.commit()
    db.close()

def delete(id):
    empty_list = []
    empty_list.append(id)
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    delete_command = """DELETE FROM passwd WHERE id=?"""
    cur.execute(delete_command, tuple(empty_list))
    db.commit()
    db.close()

def change_login(pwd_real: str):
    pwd = get_md5(pwd_real)
    empty_list = []
    empty_list.append(pwd)
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    change_login_command = """UPDATE auth SET pass=? WHERE account='admin'"""
    cur.execute(change_login_command, tuple(empty_list))
    db.commit()
    db.close()