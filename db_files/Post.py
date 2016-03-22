from mysql_connect import connect
from response import response_dict
import MySQLdb



def create_post(date, thread, message, user, forum, is_approved, is_highlighted, is_spam, is_deleted, is_edited,
                parent):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO Post (date, thread, message, user, forum, isApproved, isHighlighted,
         isSpam, isDeleted, isEdited,parent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         """, (date, thread, message, user, forum, is_approved, is_highlighted, is_spam, is_deleted, is_edited, parent))
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
        cursor.execute(""" SELECT count(*) FROM Post WHERE thread=%s""", thread[0])
        posts = cursor.fetchone()
        user_buf = db_id[4]
        if ("user" in related):
            user_buf = {
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

        forum_buf = db_id[5]
        if ("forum" in related):
            forum_buf = {
                "id": forum[0],
                "name": forum[1],
                "short_name": forum[2],
                "user": forum[3]
            }

        thread_buf = db_id[2]
        if ("thread" in related):
            thread_buf = {
                "date": thread[5].strftime("%Y-%m-%d %H:%M:%S"),
                "dislikes": thread[10],
                "forum": thread[1],
                "id": thread[0],
                "isClosed": thread[3],
                "isDeleted": thread[8],
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
                "isApproved": db_id[7],
                "isDeleted": db_id[11],
                "isEdited": db_id[9],
                "isHighlighted": db_id[8],
                "isSpam": db_id[10],
                "likes": db_id[12],
                "message": db_id[3],
                "parent": db_id[6],
                "points": int(db_id[14]),
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
        if (e[0] == 1062):
            return response_dict[5]
        elif (e[0] == 1452):
            return response_dict[1]
        else:
            return response_dict[4]

def list_post(since, order, limit, forum, thread):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT * FROM Post WHERE thread=%s or forum=%s """, (thread, forum))
        db_id = cursor.fetchall()
    except MySQLdb.Error:
        return response_dict[4]

