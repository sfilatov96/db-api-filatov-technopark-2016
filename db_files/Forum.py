from mysql_connect import connect
from response import response_dict
import MySQLdb


def status():
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT count(*) FROM Forum """)
        count_forum = cursor.fetchone()
        cursor.execute("""SELECT count(*) FROM Post """)
        count_post = cursor.fetchone()
        cursor.execute("""SELECT count(*) FROM Thread """)
        count_thread = cursor.fetchone()
        cursor.execute("""SELECT count(*) FROM User """)
        count_user = cursor.fetchone()
        result = {
            "code": 0,
            "response": {
                "user": count_user[0],
                "thread": count_thread[0],
                "forum": count_forum[0],
                "post": count_post[0]
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return result
    except MySQLdb.Error:
        return response_dict[4]


def clear():
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SET foreign_key_checks = 0""")
        cursor.execute("""TRUNCATE Forum""")
        cursor.execute("""TRUNCATE User""")
        cursor.execute("""TRUNCATE Thread""")
        cursor.execute("""TRUNCATE Post""")
        cursor.execute("""TRUNCATE Thread_followers""")
        cursor.execute("""TRUNCATE User_followers""")
        result = {
            "code": 0,
            "response": "OK"
        }
        cursor.close()
        db.commit()
        db.close()
        return result
    except MySQLdb.Error:
        return response_dict[4]


def create_forum(name, short_name, user):
    db = connect()
    cursor = db.cursor()
    try:
        try:
            cursor.execute("""SELECT * FROM User WHERE email=%s""", user)
        except MySQLdb.Error:
            return response_dict[1]

        cursor.execute("""INSERT INTO Forum (name,short_name,user) VALUES (%s,%s,%s) """, (name, short_name, user))
        cursor.execute(""" SELECT id FROM Forum WHERE name=%s """, name)
        db_id = cursor.fetchone()
        results = {
            "code": 0,
            "response": {
                "id": db_id[0],
                "name": name,
                "short_name": short_name,
                "user": user
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError:
        results = response_dict[5]
        return results
    except MySQLdb.Error:
        results = response_dict[4]
        return results

def detail_forum(related,forum):
    db = connect()
    cursor = db.cursor()
    try:
        try:
            cursor.execute("""SELECT * FROM Forum WHERE short_name=%s AND user=%s""", (forum,user))
        except MySQLdb.Error:
            return response_dict[1]

        cursor.execute("""INSERT INTO Forum (name,short_name,user) VALUES (%s,%s,%s) """, (name, short_name, user))
        cursor.execute(""" SELECT id FROM Forum WHERE name=%s """, name)
        db_id = cursor.fetchone()
        results = {
            "code": 0,
            "response": {
                "id": db_id[0],
                "name": name,
                "short_name": short_name,
                "user": user
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError:
        results = response_dict[5]
        return results
    except MySQLdb.Error:
        results = response_dict[4]
        return results

