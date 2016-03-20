import MySQLdb

host = "localhost"
user = "root"
password = "258147"
db = "forum"


def connect():
    con = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
    return con
