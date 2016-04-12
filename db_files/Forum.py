from mysql_connect import connect
from response import response_dict
from User import detail,func_followers,func_following,func_subscribe
from Thread import detail_thread
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
        cursor.execute("""SELECT * FROM User WHERE email=%s""", (user,))
        cursor.execute("""INSERT INTO Forum (name,short_name,user) VALUES (%s,%s,%s) """, (name, short_name, user))
        cursor.execute(""" SELECT id FROM Forum WHERE name=%s """, (name,))
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
        cursor.execute("""SELECT * FROM Forum WHERE short_name=%s """, (forum,))
        db_id = cursor.fetchone()
        cursor.execute("""SELECT * FROM User WHERE email=%s""", (db_id[3],))
        user_id = cursor.fetchone()
        if related:
            results = {
                "id": db_id[0],
                "name": db_id[1],
                "short_name": db_id[2],
                "user": {
                    "about": user_id[2],
                    "email": db_id[3],
                    "followers": func_followers(db_id[3]),
                    "following": func_following(db_id[3]),
                    "id": user_id[0],
                    "isAnonymous": user_id[5],
                    "name": user_id[3],
                    "subscriptions": func_subscribe(db_id[3]),
                    "username": user_id[1]
                }
            }
        else:
            results = {
                "id": db_id[0],
                "name": db_id[1],
                "short_name": db_id[2],
                "user": db_id[3]
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


def post_list_forum(related, forum, order, since, limit):
    db = connect()
    cursor = db.cursor()
    try:
        query = """SELECT * FROM Post WHERE forum = %s """
        query_params = (forum,)

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
        #print array
        print related
        for iter in array:
            if 'user' in related:
                user = detail(iter['user'])
                iter.update({'user': user})

            if 'forum' in related:
                forum = detail_forum(None, iter['forum'])
                print forum
                iter.update({'forum': forum})

            if 'thread' in related:
                thread = detail_thread([], iter['thread'])
                iter.update({'thread': thread})

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
    #except TypeError as e:
    #    print e
    #    return response_dict[1]
    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]


def list_thread_forum(since, order, limit, forum, related):
    db = connect()
    cursor = db.cursor()
    try:
        query = """SELECT * FROM Thread WHERE forum = %s """
        query_params = (forum,)

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
                "date": db_id[5].strftime("%Y-%m-%d %H:%M:%S"),
                "dislikes": db_id[10],
                "forum": db_id[1],
                "id": db_id[0],
                "isClosed": bool(db_id[3]),
                "isDeleted": bool(db_id[8]),
                "likes": db_id[9],
                "message": db_id[6],
                "points": db_id[12],
                "posts": db_id[11],
                "slug": db_id[7],
                "title": db_id[2],
                "user": db_id[4]
            }
            array.append(maps)

        print array

        for iter in array:
            if 'user' in related:
                user = detail(iter['user'])
                iter.update({'user': user})

            if 'forum' in related:
                forum = detail_forum(None, iter['forum'])
                iter.update({'forum': forum})

        results = {
            "code": 0,
            "response": array
        }
        return results

    except MySQLdb.Error:
        return response_dict[4]

def list_user_forum(since_id, order, limit, forum):
    db = connect()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:

        if since_id is None:
            since_id = " "
        else:
            since_id = " AND `id` >=  " + since_id

        if limit is None:
            limit = " "
        else:
            limit = ' LIMIT ' + limit

        cursor.execute("""SELECT * FROM User
            WHERE email IN (SELECT DISTINCT user FROM Post WHERE forum = %s)""" + since_id +
            " ORDER BY name " + order + limit + " ;", (forum,))
        array = []
        users = [i for i in cursor.fetchall()]
        for user in users:
            user = detail(user['email'])
            array.append(user)
        results = {"code": 0, "response": array}
        return results

    except MySQLdb.Error:
        return response_dict[4]
