from mysql_connect import connect
from response import response_dict
import MySQLdb
from numconv import int2str


def create_post(date, thread, message, user, forum, is_approved, is_highlighted, is_spam, is_deleted, is_edited,
                parent):
    db = connect()
    cursor = db.cursor()
    try:

        if parent is None:
            is_root = 0
            path = ' '
        else:
            is_root = 1
            cursor.execute("""SELECT path FROM Post WHERE id = %s""", (parent,))
            path = cursor.fetchone()[0]

        cursor.execute("""INSERT INTO Post (date, thread, message, user, forum, isApproved, isHighlighted,
         isSpam, isDeleted, isEdited,parent,isRoot) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         """, (date, thread, message, user, forum, is_approved, is_highlighted, is_spam, is_deleted, is_edited, parent,
               is_root))
        cursor.execute(""" SELECT * FROM Post WHERE forum=%s AND user=%s AND message=%s AND thread="%s" """,
                       (forum, user, message, thread))
        db_id = cursor.fetchone()
        results = {
            "code": 0,
            "response": {
                "date": date,
                "forum": forum,
                "id": db_id[0],
                "isApproved": is_approved,
                "isDeleted": is_deleted,
                "isEdited": is_edited,
                "isHighlighted": is_highlighted,
                "isSpam": is_spam,
                "message": message,
                "parent": db_id[5],
                "thread": thread,
                "user": user
            }
        }
        post_id = cursor.lastrowid

        base36 = int2str(int(post_id), radix=36)
        path += str(len(base36)) + base36

        cursor.execute("""UPDATE Post SET path = %s WHERE id = %s""", (path, post_id))
        cursor.execute(""" SELECT count(*) FROM Post WHERE thread=%s and isDeleted=0""", thread)
        posts_count = cursor.fetchone()
        cursor.execute(""" UPDATE Thread SET posts=%s  WHERE id=%s""", (str(posts_count[0]), thread))
        print posts_count[0]
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


def detail_post(related, post):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Post WHERE id=%s """, post)
        db_id = cursor.fetchone()
        cursor.execute("""SELECT * FROM User WHERE email=%s""", db_id[4])
        user_id = cursor.fetchone()
        cursor.execute(""" SELECT * FROM User_followers WHERE User=%s""", db_id[4])
        followers = cursor.fetchall()
        cursor.execute(""" SELECT * FROM User_followers WHERE Followers=%s""", db_id[4])
        following = cursor.fetchall()
        cursor.execute(""" SELECT thread_id FROM Thread_followers WHERE follower_email=%s""", db_id[4])
        sub = cursor.fetchall()
        cursor.execute(""" SELECT * FROM Forum WHERE short_name=%s""", db_id[5])
        forum = cursor.fetchone()
        cursor.execute(""" SELECT * FROM Thread WHERE id=%s""", db_id[2])
        thread = cursor.fetchone()
        cursor.execute(""" SELECT count(*) FROM Post WHERE thread=%s and isDeleted=0""", thread[0])
        posts = cursor.fetchone()
        user_buf = db_id[4]
        if "user" in related:
            user_buf = {
                "about": user_id[2],
                "email": db_id[4],
                "followers": followers,
                "following": following,
                "id": user_id[0],
                "isAnonymous": bool(user_id[5]),
                "name": user_id[3],
                "subscriptions": sub,
                "username": user_id[1]
            }

        forum_buf = db_id[5]
        if "forum" in related:
            forum_buf = {
                "id": forum[0],
                "name": forum[1],
                "short_name": forum[2],
                "user": forum[3]
            }

        thread_buf = db_id[2]
        if "thread" in related:
            thread_buf = {
                "date": thread[5].strftime("%Y-%m-%d %H:%M:%S"),
                "dislikes": thread[10],
                "forum": thread[1],
                "id": thread[0],
                "isClosed": bool(thread[3]),
                "isDeleted": bool(thread[8]),
                "likes": thread[9],
                "message": thread[6],
                "points": thread[12],
                "posts": posts[0],
                "slug": thread[7],
                "title": thread[2],
                "user": thread[4]
            }

        results = {
            "code": 0,
            "response": {
                "date": db_id[1].strftime("%Y-%m-%d %H:%M:%S"),
                "dislikes": db_id[13],
                "forum": forum_buf,
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
                "thread": thread_buf,
                "user": user_buf
            }
        }

        cursor.close()
        db.commit()
        db.close()
        return results
    except TypeError:
        return response_dict[1]

    except MySQLdb.IntegrityError as e:
        if e[0] == 1062:
            return response_dict[5]
        elif e[0] == 1452:
            return response_dict[1]
        else:
            return response_dict[4]


def list_post(since, order, limit, forum, thread):
    db = connect()
    cursor = db.cursor()
    try:
        if thread is None and forum is None:
            return response_dict[3]
        if forum is not None:
            query = """SELECT * FROM Post WHERE forum = %s """
            query_params = (forum,)
        else:
            query = """SELECT * FROM Post WHERE thread = %s """
            query_params = (thread,)

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
        result = {
            "code": 0,
            "response": array
        }
        return result

    except MySQLdb.Error:
        return response_dict[4]


def post_remove(post_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Post WHERE id=%s  """, post_id)
        del_sel = cursor.fetchone()
        if del_sel:
            cursor.execute("""UPDATE  Post SET isDeleted=1  WHERE id=%s """, post_id)
            results = {
                "code": 0,
                "response": {
                    "post": post_id,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError:
        return response_dict[4]


def post_restore(post_id):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Post WHERE id=%s  """, post_id)
        del_sel = cursor.fetchone()
        if del_sel:
            cursor.execute("""UPDATE  Post SET isDeleted=0  WHERE id=%s """, post_id)
            results = {
                "code": 0,
                "response": {
                    "post": post_id,
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError:
        return response_dict[4]


def post_update(post_id, message):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Post WHERE id=%s  """, post_id)
        db_id = cursor.fetchone()
        if db_id:
            cursor.execute("""UPDATE  Post SET message=%s  WHERE id=%s """, (message, post_id))

            results = {
                "code": 0,
                "response": {
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
                    "message": message,
                    "parent": db_id[6],
                    "points": int(db_id[16]),
                    "thread": db_id[5],
                    "user": db_id[4]
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError:
        return response_dict[4]


def post_vote(post_id, vote):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Post WHERE id=%s  """, post_id)
        is_id = cursor.fetchone()
        if is_id:
            print vote
            if vote == 1:
                cursor.execute("""UPDATE  Post SET likes=likes+1, points=points+1 WHERE id=%s """, post_id)
            elif vote == -1:
                cursor.execute("""UPDATE  Post SET dislikes=dislikes+1, points=points-1 WHERE id=%s """, post_id)
            else:
                return response_dict[3]

            cursor.execute("""SELECT * FROM Post WHERE id=%s  """, post_id)
            db_id = cursor.fetchone()
            results = {
                "code": 0,
                "response": {
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
                    "points": db_id[14],
                    "thread": db_id[5],
                    "user": db_id[4]
                }
            }
            cursor.close()
            db.commit()
            db.close()
            return results
        else:
            return response_dict[1]
    except MySQLdb.IntegrityError:
        return response_dict[4]
