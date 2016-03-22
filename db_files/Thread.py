from mysql_connect import connect
from response import response_dict
import MySQLdb


def create_thread(forum, title, is_closed, user, date, message, slug, is_deleted):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO Thread (forum,title,isClosed,user,date,message,slug,isDeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
         """, (forum, title, is_closed, user, date, message, slug, is_deleted))
        cursor.execute(""" SELECT id FROM Thread WHERE forum=%s AND user=%s AND title=%s""", (forum, user, title))
        db_id = cursor.fetchone()
        results = {
            "code": 0,
            "response": {
                "date": date,
                "forum": forum,
                "id": db_id[0],
                "isClosed": bool(is_closed),
                "isDeleted": False,
                "message": message,
                "slug": slug,
                "title": title,
                "user": user,
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError as e:
        if (e[0] == 1062):
            return response_dict[5]
        elif (e[0] == 1452):
            return response_dict[1]
        else:
            return response_dict[4]


def thread_subscribe(thread_id, follower_email):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO Thread_followers (thread_id,follower_email) VALUES (%s,%s)""",
                       (thread_id, follower_email))
        results = {
            "code": 0,
            "response": {
                "thread": thread_id,
                "user": follower_email,
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError as e:
        print e[0]
        if (e[0] == 1062):
            return response_dict[5]
        elif (e[0] == 1452):
            return response_dict[1]
        else:
            return response_dict[4]


def thread_unsubscribe(thread_id, follower_email):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Thread_followers WHERE thread_id=%s AND follower_email=%s """,
                       (thread_id, follower_email))
        dels = cursor.fetchone()
        print follower_email, thread_id
        if (dels):
            cursor.execute("""DELETE FROM Thread_followers WHERE thread_id=%s AND follower_email=%s """,
                           (thread_id, follower_email))
            results = {
                "code": 0,
                "response": {
                    "thread": thread_id,
                    "user": follower_email,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError as e:
        return response_dict[4]


def thread_remove(thread_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Thread WHERE id=%s  """, thread_id)
        dels = cursor.fetchone()
        if (dels):
            cursor.execute("""UPDATE  Thread SET isDeleted=1  WHERE id=%s """, thread_id)

            results = {
                "code": 0,
                "response": {
                    "thread": thread_id,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError as e:
        return response_dict[4]


def thread_restore(thread_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Thread WHERE id=%s  """, thread_id)
        dels = cursor.fetchone()
        if (dels):

            cursor.execute("""UPDATE  Thread SET isDeleted=0  WHERE id=%s """, thread_id)

            results = {
                "code": 0,
                "response": {
                    "thread": thread_id,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError as e:
        return response_dict[4]


def thread_close(thread_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Thread WHERE id=%s  """, thread_id)
        dels = cursor.fetchone()
        if (dels):
            cursor.execute("""UPDATE  Thread SET isClosed=1  WHERE id=%s """, thread_id)

            results = {
                "code": 0,
                "response": {
                    "thread": thread_id,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError as e:
        return response_dict[4]


def thread_open(thread_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Thread WHERE id=%s  """, thread_id)
        dels = cursor.fetchone()
        if (dels):
            cursor.execute("""UPDATE  Thread SET isClosed=0  WHERE id=%s """, thread_id)

            results = {
                "code": 0,
                "response": {
                    "thread": thread_id,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError as e:
        return response_dict[4]

def detail_thread(related, thread):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Thread WHERE id=%s """, thread)
        db_id = cursor.fetchone()
        cursor.execute("""SELECT * FROM User WHERE email=%s""", db_id[4])
        user_id = cursor.fetchone()
        cursor.execute(""" SELECT * FROM User_followers WHERE User=%s""", db_id[4])
        followers = cursor.fetchall()
        cursor.execute(""" SELECT * FROM User_followers WHERE Followers=%s""", db_id[4])
        following = cursor.fetchall()
        cursor.execute(""" SELECT thread_id FROM Thread_followers WHERE follower_email=%s""", db_id[4])
        sub = cursor.fetchall()
        cursor.execute(""" SELECT * FROM Forum WHERE short_name=%s""", db_id[1])
        forum = cursor.fetchone()

        if ("user" in related and "forum" in related):
            results = {
                "code": 0,
                "response": {
                    "date": db_id[5].strftime("%Y-%m-%d %H:%M:%S"),
                    "dislikes": db_id[10],
                    "forum": {
                        "id": forum[0],
                        "name": forum[1],
                        "short_name": forum[2],
                        "user": forum[3]
                    },
                    "id": db_id[0],
                    "isClosed": db_id[3],
                    "isDeleted": db_id[8],
                    "likes": db_id[9],
                    "message": db_id[6],
                    "points": db_id[12],
                    "posts": db_id[11],
                    "slug": db_id[7],
                    "title": db_id[2],
                    "user": {
                        "about": user_id[2],
                        "email": db_id[4],
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
        elif ("user" in related):
            results = {
                "code": 0,
                "response": {
                    "date": db_id[5].strftime("%Y-%m-%d %H:%M:%S"),
                    "dislikes": db_id[10],
                    "forum": db_id[1],
                    "id": db_id[0],
                    "isClosed": db_id[3],
                    "isDeleted": db_id[8],
                    "likes": db_id[9],
                    "message": db_id[6],
                    "points": db_id[12],
                    "posts": db_id[11],
                    "slug": db_id[7],
                    "title": db_id[2],
                    "user": {
                        "about": user_id[2],
                        "email": db_id[4],
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
        elif ("forum" in related):
            results = {
                "code": 0,
                "response": {
                    "date": db_id[5].strftime("%Y-%m-%d %H:%M:%S"),
                    "dislikes": db_id[10],
                    "forum": {
                        "id": forum[0],
                        "name": forum[1],
                        "short_name": forum[2],
                        "user": forum[3]
                    },
                    "id": db_id[0],
                    "isClosed": db_id[3],
                    "isDeleted": db_id[8],
                    "likes": db_id[9],
                    "message": db_id[6],
                    "points": db_id[12],
                    "posts": db_id[11],
                    "slug": db_id[7],
                    "title": db_id[2],
                    "user": db_id[4]
                }
            }
        else:
            results = {
                "code": 0,
                "response": {
                    "date": db_id[5].strftime("%Y-%m-%d %H:%M:%S"),
                    "dislikes": db_id[10],
                    "forum": db_id[1],
                    "id": db_id[0],
                    "isClosed": db_id[3],
                    "isDeleted": db_id[8],
                    "likes": db_id[9],
                    "message": db_id[6],
                    "points": db_id[12],
                    "posts": db_id[11],
                    "slug": db_id[7],
                    "title": db_id[2],
                    "user": db_id[4]
                }
            }
        cursor.close()
        db.commit()
        db.close()
        return results

    except MySQLdb.IntegrityError as e:
        if (e[0] == 1062):
            return response_dict[5]
        elif (e[0] == 1452):
            return response_dict[1]
        else:
            return response_dict[4]


def update_thread(thread_id, slug, message):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE Thread SET message=%s  slug=%s WHERE id=%s""", (message, slug, thread_id))
        cursor.execute(""" SELECT * FROM Thread WHERE id=%s""", thread_id)
        db_id = cursor.fetchone()
        results = {
            "code": 0,
            "response": {
                "date": db_id[5].strftime("%Y-%m-%d %H:%M:%S"),
                "dislikes": db_id[10],
                "forum": db_id[1],
                "id": db_id[0],
                "isClosed": db_id[3],
                "isDeleted": db_id[8],
                "likes": db_id[9],
                "message": db_id[6],
                "points": db_id[12],
                "posts": db_id[11],
                "slug": db_id[7],
                "title": db_id[2],
                "user": db_id[4]
            }
        }
        cursor.close()
        db.commit()
        db.close()
        return results
    except MySQLdb.IntegrityError as e:
        if (e[0] == 1062):
            return response_dict[5]
        elif (e[0] == 1452):
            return response_dict[1]
        else:
            return response_dict[4]

