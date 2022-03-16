import sqlite3
import hashlib
import re


# serach by RE
def regexp(expr, item):
    reg = re.compile(expr, re.I) # case-incensitive
    return reg.search(item) is not None

class DataOp:
    def __init__(self):
        pass
    def register_check(self):
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        try:
            cur.execute("CREATE TABLE auth (account text, pass text)")
            cur.execute("""CREATE TABLE passwd (
                id integer primary key autoincrement,
                site text,
                account text,
                password text,
                date text
                )""")
        except sqlite3.OperationalError:
            pass
        cur.execute(f"""SELECT * FROM auth""")
        r = cur.fetchall()
        db.close()
        return r

    def register(self, pwd):
        login_pwd_hashed = self.get_md5(pwd)
        user = ['admin']
        user.append(login_pwd_hashed)
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        register_command = """INSERT INTO auth VALUES (?,?)"""
        cur.execute(register_command, tuple(user))
        db.commit()
        db.close()

    def login_check(self, pwd):
        pwd_hashed = self.get_md5(pwd)
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        cur.execute("""SELECT * FROM auth WHERE account='admin'""")
        result=cur.fetchone()
        db.close()
        return pwd_hashed == result[1]

    def add(self, info: list):
        info[2] = self.encrypt(info[2], int(info[3][-2:]))
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        add_command = """INSERT INTO passwd (site, account, password, date) VALUES (?,?,?,?)"""
        cur.execute(add_command, tuple(info))
        db.commit()
        db.close()

    def dulplicated(self, s: str, a: str):
        db = sqlite3.connect("database.db")
        db.create_function("REGEXP", 2, regexp)
        cur = db.cursor()
        dup_command = """SELECT * FROM passwd WHERE site=? AND account REGEXP ?"""
        cur.execute(dup_command, (s, a))
        result = cur.fetchall()
        db.close()
        re = []
        for col in result:
            col = list(col)
            col[3] = self.decrypt(col[3], int(col[4][-2:]))
            re.append(col)
        return re

    def search_site(self, site: str):
        db = sqlite3.connect("database.db")
        db.create_function("REGEXP", 2, regexp)
        cur = db.cursor()
        search = """SELECT * FROM passwd WHERE site REGEXP ?"""
        cur.execute(search, [site])
        result = cur.fetchall()
        db.close()
        re = []
        for col in result:
            col = list(col)
            col[3] = self.decrypt(col[3], int(col[4][-2:]))
            re.append(col)
        return re

    def search_account(self, account: str):
        db = sqlite3.connect("database.db")
        db.create_function("REGEXP", 2, regexp)
        cur = db.cursor()
        search = """SELECT * FROM passwd WHERE account REGEXP ?"""
        cur.execute(search, [account])
        result = cur.fetchall()
        db.close()
        res = []
        for col in result:
            col = list(col)
            col[3] = self.decrypt(col[3], int(col[4][-2:]))
            res.append(col)
        return res

    def search_id(self, id: int):
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        search = """SELECT * FROM passwd WHERE id=?"""
        cur.execute(search, [id])
        result = cur.fetchall()
        db.close()
        res = []
        for col in result:
            col = list(col)
            col[3] = self.decrypt(col[3], int(col[4][-2:]))
            res.append(col)
        return res

    def update_pwd(self, info: list):
        info[0] = self.encrypt(info[0], int(info[1][-2:]))
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        update_command = """UPDATE passwd SET password=?, date=? WHERE id=?"""
        cur.execute(update_command, tuple(info))
        db.commit()
        db.close()

    def delete(self, id):
        empty_list = []
        empty_list.append(id)
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        delete_command = """DELETE FROM passwd WHERE id=?"""
        cur.execute(delete_command, tuple(empty_list))
        db.commit()
        db.close()

    def change_login(self, pwd_real: str):
        pwd = self.get_md5(pwd_real)
        empty_list = []
        empty_list.append(pwd)
        db = sqlite3.connect("database.db")
        cur = db.cursor()
        change_login_command = """UPDATE auth SET pass=? WHERE account='admin'"""
        cur.execute(change_login_command, tuple(empty_list))
        db.commit()
        db.close()

    def get_md5(self, s):
        md = hashlib.md5()
        md.update(s.encode("utf-8"))
        return md.hexdigest()  # hash the login password

    def encrypt(self, psw: str, offset: int) -> str:
        ascii_num = []
        for i in psw:
            ascii_num.append(self.enascii(ord(i), offset + 15))
        encrypted = [chr(a) for a in ascii_num]
        return "".join(encrypted)

    def decrypt(self, s: str, offset: int) -> str:
        pwd = [chr(self.deascii(ord(a), offset + 15)) for a in s]
        return "".join(pwd)

    def enascii(self, num: int, offset: int) -> int:
        if num - offset >= 33:
            return num - offset
        else:
            return 93 + num - offset

    def deascii(self, num: int, offset: int) -> int:
        if num + offset <= 126:
            return num + offset
        else:
            return num + offset - 93