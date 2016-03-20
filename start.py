from bottle import route, request, run, post

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


@route("/db/api/user/detail/", method="GET")
def detail_index():
    email = request.GET.get("email");
    if (email):
        result = detail(email)
        print json.dumps(result)
        return json.dumps(result)
    else:
        return response_dict[2]


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
        short_name = obj["short_name"]
        user = obj["user"]
        result = create_forum(name, short_name, user)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
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
        result = create_post(date, thread, message, user, forum, is_approved, is_highlighted, is_spam,
                             is_deleted, is_edited)
        print json.dumps(result)
        return json.dumps(result)
    except ValueError:
        return json.dumps(response_dict[2])
    except SyntaxError:
        return json.dumps(response_dict[2])
    except NameError:
        return json.dumps(response_dict[2])


run(host='localhost', port=8080)
