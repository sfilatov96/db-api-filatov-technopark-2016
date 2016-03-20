from mysql_connect import connect
from response import response_dict
import MySQLdb


def create(username, about, name, email, is_anon):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO User (username,name,email,isAnonymous,about) VALUES (%s,%s,%s,%s,%s) """,
                       (username, name, email, is_anon, about))
        cursor.execute(""" SELECT id FROM User WHERE email=%s""", email)
        db_id = cursor.fetchone()
        results = {
            "code": 0,
            "response": {
                "about": about,
                "email": email,
                "id": db_id[0],
                "isAnonymous": bool(is_anon),
                "name": name,
                "username": username
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


def detail(email):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", email)
        str = cursor.fetchone()
        if (not str):
            return response_dict[1]
        else:
            cursor.execute(""" SELECT * FROM User_followers WHERE User=%s""", email)
            followers = cursor.fetchall()
            cursor.execute(""" SELECT * FROM User_followers WHERE Followers=%s""", email)
            following = cursor.fetchall()
            print str
            results = {
                "code": 0,
                "response": {
                    "about": str[2],
                    "email": str[4],
                    "followers": followers,
                    "following": following,
                    "id": str[0],
                    "isAnonymous": bool(str[5]),
                    "name": str[3],
                    "subscriptions": [],
                    "username": str[1]
                }
            }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError:
        results = response_dict[5]
        return results


def follow(follower, followee):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", followee)
        str = cursor.fetchone()
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", follower)
        str2 = cursor.fetchone()
        if(str2):
            cursor.execute("""INSERT INTO User_followers (User,Followers) VALUES (%s,%s) """, (follower, followee))
            cursor.execute(""" SELECT Followers FROM User_followers WHERE User=%s""", follower)
            followers = cursor.fetchall()
            cursor.execute(""" SELECT User FROM User_followers WHERE Followers=%s""", follower)
            following = cursor.fetchall()

            print str
            results = {
                "code": 0,
                "response": {
                    "about": str[2],
                    "email": str[4],
                    "followers": followers,
                    "following": following,
                    "id": str[0],
                    "isAnonymous": bool(str[5]),
                    "name": str[3],
                    "subscriptions": [],
                    "username": str[1]
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]

    except MySQLdb.IntegrityError:
        results = response_dict[5]
        return results
    except TypeError:
        results = response_dict[1]
        return results


def list_followers(email, order):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", email)
        str = cursor.fetchone()
        if (not str):
            return response_dict[1]
        else:
            cursor.execute(""" SELECT Followers FROM User_followers WHERE User=%s ORDER BY %s""", (email, order))
            followers = cursor.fetchall()
            cursor.execute(""" SELECT User FROM User_followers WHERE Followers=%s ORDER BY %s""", (email, order))
            following = cursor.fetchall()
            results = {
                "code": 0,
                "response": {
                    "about": str[2],
                    "email": str[4],
                    "followers": followers,
                    "following": following,
                    "id": str[0],
                    "isAnonymous": bool(str[5]),
                    "name": str[3],
                    "subscriptions": [],
                    "username": str[1]
                }
            }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError:
        results = response_dict[5]
        return results


def list_following(email, order, limit ,since_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", email)
        str = cursor.fetchone()
        if (not str):
            return response_dict[1]
        else:
            cursor.execute(""" SELECT Followers FROM User_followers WHERE User=%s ORDER BY %s""", (email, order))
            followers = cursor.fetchall()
            cursor.execute(""" SELECT User FROM User_followers f
            JOIN User u on f.User = u.email
            WHERE Followers=%s AND id >= %d  ORDER BY %s LIMIT %d """, (email, since_id, order, limit))
            following = cursor.fetchall()
            results = {
                "code": 0,
                "response": {
                    "about": str[2],
                    "email": str[4],
                    "followers": followers,
                    "following": following,
                    "id": str[0],
                    "isAnonymous": bool(str[5]),
                    "name": str[3],
                    "subscriptions": [],
                    "username": str[1]
                }
            }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError:
        results = response_dict[5]
        return results




