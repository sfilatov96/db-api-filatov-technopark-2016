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
    except MySQLdb.IntegrityError:
        return response_dict[1]



