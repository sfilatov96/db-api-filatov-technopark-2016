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
        cursor.execute("""SELECT * FROM User WHERE email=%s""", user)
        cursor.execute("""INSERT INTO Forum (name,short_name,user) VALUES (%s,%s,%s) """, (name, short_name, user))
        cursor.execute(""" SELECT id FROM Forum WHERE name=%s """, name)
        db_id = cursor.fetchone()
        print db_id
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
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]


def detail_forum(related, forum):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Forum WHERE short_name=%s """, forum)
        db_id = cursor.fetchone()
        cursor.execute("""SELECT * FROM User WHERE email=%s""", db_id[3])
        user_id = cursor.fetchone()
        cursor.execute(""" SELECT * FROM User_followers WHERE User=%s""", db_id[3])
        followers = cursor.fetchall()
        cursor.execute(""" SELECT * FROM User_followers WHERE Followers=%s""", db_id[3])
        following = cursor.fetchall()
        cursor.execute(""" SELECT thread_id FROM Thread_followers WHERE follower_email=%s""", db_id[3])
        sub = cursor.fetchall()
        if related:
            results = {
                "code": 0,
                "response": {
                    "id": db_id[0],
                    "name": db_id[1],
                    "short_name": db_id[2],
                    "user": {
                        "about": user_id[2],
                        "email": db_id[3],
                        "followers": followers,
                        "following": following,
                        "id": user_id[0],
                        "isAnonymous": user_id[5],
                        "name": user_id[3],
                        "subscriptions": sub,
                        "username": user_id[1]
                    }
                }
            }
        else:
            results = {
                "code": 0,
                "response": {
                    "id": db_id[0],
                    "name": db_id[1],
                    "short_name": db_id[2],
                }
            }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.Error:
        return response_dict[1]
    except TypeError:
        return response_dict[1]
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]
