from datetime import datetime
from os.path import join as pathJoin, dirname, abspath
from pyodbc import connect as dbConnect, Error as bdError

baseDir = dirname(abspath(__file__))
filePath = pathJoin(baseDir, "users.accdb")

conn = None
cur = None
try:
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + filePath + ';'
    conn = dbConnect(conn_str, timeout=10, attrs_before={})
    cur = conn.cursor()
except bdError as e:
    print(e)


def get_all_users():
    cur.execute('select * from users where user_number not in (?)', "-")

    users = []
    for row in cur.fetchall():
        for i, value in enumerate(row):
            if cur.description[i][0] == "user_number":
                users.append(value)

    return users


def set_current_user(num, code):
    cur.execute('update users set current_user = ?, existance_code = ? '
                'where user_number = ? and user_parameters = ?',
                num, code, "-", "-")
    conn.commit()


def get_current_user():
    cur.execute('select current_user, existance_code from users '
                'where user_number = ? and user_parameters = ?',
                "-", "-")

    usr = cur.fetchone()

    return {"number": usr[0], "code": usr[1]}


def update_parameters(num="-", params=None):
    if params is None:
        params = "0; 0; 0"
    else:
        params = "; ".join(map(str, params))

    cur.execute('update users set user_parameters = ? where user_number = ?',
                params, num)
    conn.commit()


def get_parameters(num):
    cur.execute('select user_parameters from users '
                'where user_number = ?', num)

    vals = cur.fetchval().split("; ")

    return {"left": vals[0], "right": vals[1], "seat": vals[2]}


def insert_user(num="-", params=None):
    if params is None:
        params = "0; 0; 0"
    else:
        params = "; ".join(map(str, params))

    cur.execute('insert into users values (?, ?, ?, ?)', num, params, "-", "-")
    conn.commit()


def write_log(num, code):
    t = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

    cur.execute('insert into log values (?, ?, ?)', t, code, num)
    conn.commit()


def user_exists():
    cur.execute('select existance_code from users '
                'where user_number = ? and user_parameters = ?', "-", "-")

    if cur.fetchval() == "0":
        return True
    elif cur.fetchval() == "1":
        return False


def last_message_info():
    cur.execute('select record_date, code from log')
    res = cur.fetchall()

    return (datetime.now() - res[len(res) - 1][0]).total_seconds() / 60.0, res[len(res) - 1][1]
