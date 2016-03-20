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
        cursor.execute("""SELECT * FROM Thread_followers WHERE thread_id=%s AND follower_email=%s """, (thread_id, follower_email))
        dels = cursor.fetchone()
        print follower_email,thread_id
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
            cursor.execute("""UPDATE  Thread SET isDeleted=1  WHERE id=%s """,  thread_id)
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
            cursor.execute("""UPDATE  Thread SET isDeleted=0  WHERE id=%s """,  thread_id)
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
            cursor.execute("""UPDATE  Thread SET isClosed=1  WHERE id=%s """,  thread_id)
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
            cursor.execute("""UPDATE  Thread SET isClosed=0  WHERE id=%s """,  thread_id)
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
