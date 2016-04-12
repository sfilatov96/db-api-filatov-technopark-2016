from mysql_connect import connect
from response import response_dict
import MySQLdb


def create(username, about, name, email, is_anon):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO User (username,name,email,isAnonymous,about) VALUES (%s,%s,%s,%s,%s) """,
                       (username, name, email, is_anon, about))
        cursor.execute(""" SELECT id FROM User WHERE email='%s'""", email)
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
    except MySQLdb.IntegrityError as e:

        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]
    except MySQLdb.Error:
        results = response_dict[4]
        return results


def detail(email):
    db = connect()
    cursor = db.cursor()
    try:
        email = email.replace("%40", "@")
        print email
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (email,))
        str = cursor.fetchone()
        if not str:
            return response_dict[1]
        else:
            print str
            results = {
                "about": str[2],
                "email": str[4],
                "followers": func_followers(email),
                "following": func_following(email),
                "id": str[0],
                "isAnonymous": bool(str[5]),
                "name": str[3],
                "subscriptions": func_subscribe(email),
                "username": str[1]
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
            print e
            return response_dict[4]


def func_subscribe(email):
    db = connect()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(""" SELECT thread_id FROM Thread_followers WHERE follower_email=%s""", (email,))
    subscribe = [i['thread_id'] for i in cursor.fetchall()]
    cursor.close()
    db.commit()
    db.close()
    print subscribe
    return subscribe


def follow(follower, followee):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (followee,))
        str = cursor.fetchone()
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (follower,))
        str2 = cursor.fetchone()
        if str2:
            cursor.execute("""INSERT INTO User_followers (User,Followers) VALUES (%s,%s) """, (follower, followee))
            cursor.execute(""" SELECT Followers FROM User_followers WHERE User=%s""", (follower,))
            followers = cursor.fetchall()
            cursor.execute(""" SELECT User FROM User_followers WHERE Followers=%s""", (follower,))
            following = cursor.fetchall()
            cursor.execute(""" SELECT count(*) FROM Thread_followers WHERE follower_email=%s""", (followee,))
            count_subscribe = cursor.fetchone()

            print str
            results = {
                "code": 0,
                "response": {
                    "about": str[2],
                    "email": str[4],
                    "followers": func_followers(follower),
                    "following": func_following(follower),
                    "id": str[0],
                    "isAnonymous": bool(str[5]),
                    "name": str[3],
                    "subscriptions": count_subscribe[0],
                    "username": str[1]
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]

    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]
    except TypeError as e:
        print e
        results = response_dict[1]
        return results


def func_followers(email):
    db = connect()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(""" SELECT Followers FROM User_followers WHERE User=%s """, (email,))
    followers = [i['Followers'] for i in cursor.fetchall()]
    cursor.close()
    db.commit()
    db.close()
    print followers
    return followers


def func_following(email):
    db = connect()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(""" SELECT User FROM User_followers WHERE Followers=%s """, (email,))
    following = [i['User'] for i in cursor.fetchall()]
    cursor.close()
    db.commit()
    db.close()
    print following
    return following


def list_followers(email, order, limit, since_id):
    db = connect()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (email,))
        if email is None:
            return response_dict[1]

        if limit is None:
            limit = " "
        else:
            limit = ' LIMIT ' + limit

        try:
            cursor.execute(
                """SELECT about, email, id, isAnonymous, name, username FROM User_followers AS f
                    JOIN User ON User.email = f.Followers
                    WHERE f.User = %s AND User.id >= %s
                    ORDER BY name """ + order + limit + " ;",
                (
                    email,
                    int(since_id)
                )
            )
        except MySQLdb.Error as e:
            print e
            return response_dict[3]
        users = [i for i in cursor.fetchall()]
        for user in users:
            following = func_following(user['email'])
            followers = func_followers(user['email'])

            cursor.execute(
                """SELECT `thread_id`
                    FROM `Thread_followers`
                    WHERE `follower_email` = %s;""",
                (
                    user['email'],
                )
            )
            threads = [i['thread_id'] for i in cursor.fetchall()]
            user.update({'following': following, 'followers': followers, 'subscriptions': threads})
        if users:
            results = {"code": 0, "response": users}
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]


def list_following(email, order, limit, since_id):
    db = connect()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (email,))
        if email is None:
            return response_dict[1]

        if limit is None:
            limit = " "
        else:
            limit = ' LIMIT ' + limit

        try:
            cursor.execute(
                """SELECT about, email, id, isAnonymous, name, username FROM User_followers AS f
                    JOIN User ON User.email = f.User
                    WHERE f.Followers = %s AND User.id >= %s
                    ORDER BY name """ + order + limit + " ;", (email, int(since_id))
            )
        except MySQLdb.Error as e:
            print e
            return response_dict[3]
        users = [i for i in cursor.fetchall()]
        for user in users:
            following = func_following(user['email'])
            followers = func_followers(user['email'])

            cursor.execute(
                """SELECT thread_id
                    FROM Thread_followers
                    WHERE follower_email = %s;""",
                (
                    user['email'],
                )
            )
            threads = [i['thread_id'] for i in cursor.fetchall()]
            user.update({'following': following, 'followers': followers, 'subscriptions': threads})
            if users:
                results = {"code": 0, "response": users}
                return results
            else:
                return response_dict[1]
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]


def profile_update(about, user, name):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" UPDATE User SET name=%s,about=%s WHERE email=%s""", (name, about, user))
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (user,))
        str = cursor.fetchone()

        print str
        results = {
            "code": 0,
            "response": {
                "about": str[2],
                "email": str[4],
                "followers": func_followers(user),
                "following": func_following(user),
                "id": str[0],
                "isAnonymous": bool(str[5]),
                "name": str[3],
                "subscriptions": func_subscribe(user),
                "username": str[1]
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError as e:
        return response_dict[4]


def unfollow(follower, followee):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (followee,))
        str = cursor.fetchone()
        cursor.execute(""" SELECT * FROM User WHERE email=%s""", (follower,))
        str2 = cursor.fetchone()
        if str2:
            cursor.execute("""DELETE FROM User_followers WHERE User=%s AND Followers=%s """, (follower, followee))

            print str
            results = {
                "code": 0,
                "response": {
                    "about": str[2],
                    "email": str[4],
                    "followers": func_followers(follower),
                    "following": func_following(follower),
                    "id": str[0],
                    "isAnonymous": bool(str[5]),
                    "name": str[3],
                    "subscriptions": func_subscribe(follower),
                    "username": str[1]
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]

    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            print e
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]
    except TypeError:
        results = response_dict[1]
        return results


def user_post_list(user, order, since, limit):
    db = connect()
    cursor = db.cursor()
    try:
        query = """SELECT * FROM Post WHERE user=%s """
        query_params = (user,)

        if since is not None:
            query += "AND date >= %s "
            query_params += (since,)
            query += "ORDER BY date " + order + " "

        if limit is not None:
            query += "LIMIT %s;"
            query_params += (int(limit),)

        cursor.execute(query, query_params)
        array = []
        for db_id in cursor.fetchall():
            maps = {
                "date": db_id[1].strftime("%Y-%m-%d %H:%M:%S"),
                "dislikes": db_id[13],
                "forum": db_id[5],
                "id": db_id[0],
                "isApproved": bool(db_id[7]),
                "isDeleted": bool(db_id[11]),
                "isEdited": bool(db_id[9]),
                "isHighlighted": bool(db_id[8]),
                "isSpam": bool(db_id[10]),
                "likes": db_id[12],
                "message": db_id[3],
                "parent": db_id[6],
                "points": int(db_id[16]),
                "thread": db_id[2],
                "user": db_id[4]
            }
            array.append(maps)
        print array

        results = {
            "code": 0,
            "response": array
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.Error as e:
        print e
        return response_dict[1]
    except TypeError as e:
        print e
        return response_dict[1]
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            print e
            return response_dict[1]
        else:
            return response_dict[4]
