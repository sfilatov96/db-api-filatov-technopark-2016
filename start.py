from bottle import route, request, run

import json

from db_files.User import *
from db_files.Thread import *
from db_files.Forum import *
from db_files.Post import *
from response import response_dict


@route("/db/api/status/", method="POST")
def status_index():
    try:
        result = status()
        print json.dumps(result)
        return json.dumps(result)
    except MySQLdb.Error:
        return response_dict[4]


@route("/db/api/clear/", method="POST")
def clear_index():
    try:
        result = clear()
        print json.dumps(result)
        return json.dumps(result)
    except MySQLdb.Error:
        return response_dict[4]


@route("/db/api/user/create/", method="POST")
def create_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        username = obj["username"]
        about = obj["about"]
        name = obj["name"]
        email = obj["email"]
        is_anonymous = int(obj["isAnonymous"])
        result = create(username, about, name, email, is_anonymous)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/user/details/", method="GET")
def detail_index():
    email = request.GET.get('user');
    print email
    if (email):
        result = detail(email)
        print json.dumps(result)
        return json.dumps(result)
    else:
        print "exit"
        return json.dumps(response_dict[2])


@route("/db/api/user/follow/", method="POST")
def create_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        follower = obj["follower"]
        followee = obj["followee"]
        result = follow(followee, follower)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/user/listFollowers/", method="GET")
def list_followers_index():
    email = request.GET.get("user");
    order = request.GET.get("order")
    print email
    print order
    if (email and (order == "asc" or order == "desc")):
        result = list_followers(email, order)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[2]


@route("/db/api/user/listFollowing/", method="GET")
def list_following_index():
    email = request.GET.get("user")
    order = request.GET.get("order")
    since_id = request.GET.get("since_id")
    limit = request.GET.get("limit")
    print email
    print order
    if (email and since_id and limit and (order == "asc" or order == "desc")):
        result = list_following(email, order, since_id)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[2]


@route("/db/api/thread/create/", method="POST")
def create_thread_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        title = obj["title"]
        forum = obj["forum"]
        slug = obj["slug"]
        date = obj["date"]
        user = obj["user"]
        message = obj["message"]
        is_closed = int(obj["isClosed"])
        is_deleted = int(obj["isDeleted"])
        result = create_thread(forum, title, is_closed, user, date, message, slug, is_deleted)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/forum/create/", method="POST")
def create_forum_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        name = obj["name"]
        print name
        short_name = obj["short_name"]
        user = obj["user"]
        result = create_forum(name, short_name, user)
        print json.dumps(result)
        return json.dumps(result)
    except TypeError:
        return json.dumps(response_dict[4])
    except SyntaxError:
        return json.dumps(response_dict[4])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/post/create/", method="POST")
def create_post_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread = obj["thread"]
        forum = obj["forum"]
        date = obj["date"]
        user = obj["user"]
        message = obj["message"]
        is_approved = int(obj["isApproved"])
        is_edited = int(obj["isEdited"])
        is_deleted = int(obj["isDeleted"])
        is_highlighted = int(obj["isHighlighted"])
        is_spam = int(obj["isSpam"])
        parent = obj["parent"]
        result = create_post(date, thread, message, user, forum, is_approved, is_highlighted, is_spam,
                             is_deleted, is_edited, parent)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/forum/details/", method="GET")
def forum_detail_index():
    related = request.GET.get("related")
    forum = request.GET.get("forum")
    if (forum):
        result = detail_forum(related, forum)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[2]


@route("/db/api/thread/details/", method="GET")
def thread_detail_index():
    related = request.GET.getlist("related")
    print related
    thread = request.GET.get("thread")
    if (thread and "thread" not in related):
        result = detail_thread(related, thread)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[3]


@route("/db/api/thread/subscribe/", method="POST")
def thread_subscribe_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        follower_email = obj["user"]
        result = thread_subscribe(thread_id, follower_email)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/thread/unsubscribe/", method="POST")
def thread_subscribe_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        follower_email = obj["user"]
        result = thread_unsubscribe(thread_id, follower_email)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/thread/remove/", method="POST")
def thread_remove_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        result = thread_remove(thread_id)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/thread/restore/", method="POST")
def thread_restore_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        result = thread_restore(thread_id)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/thread/close/", method="POST")
def thread_close_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        result = thread_close(thread_id)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/thread/open/", method="POST")
def thread_open_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        result = thread_open(thread_id)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


@route("/db/api/thread/update/", method="POST")
def thread_update_index():
    try:
        request_data = request.json
        obj = json.loads(json.dumps(request_data))
        thread_id = obj["thread"]
        slug = obj["slug"]
        message = obj["message"]

        result = update_thread(thread_id, slug, message)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])

@route("/db/api/post/details/", method="GET")
def post_detail_index():
    related = request.GET.getlist("related")
    print related
    post = request.GET.get("post")
    if (post):
        result = detail_post(related, post)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[2]

@route("/db/api/post/list/", method="GET")
def post_list_index():
    since = request.GET.get("since")
    order = request.GET.get("order")
    limit = request.GET.get("limit")
    forum = request.GET.get("forum")
    thread = request.GET.get("thread")
    if (forum or thread):
        result = list_post(since, order, limit, forum, thread)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[2]

run(host='localhost', port=8080)
