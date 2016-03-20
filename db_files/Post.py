from mysql_connect import connect
from response import response_dict
import MySQLdb


def create_post(date, thread, message, user, forum, is_approved, is_highlighted, is_spam, is_deleted, is_edited):
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO Post (date, thread, message, user, forum, isApproved, isHighlighted,
         isSpam, isDeleted, isEdited) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         """, (date, thread, message, user, forum, is_approved, is_highlighted, is_spam, is_deleted, is_edited))
        cursor.execute(""" SELECT id FROM Post WHERE forum=%s AND user=%s AND message=%s AND thread="%s" """, (forum, user, message, thread))
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
