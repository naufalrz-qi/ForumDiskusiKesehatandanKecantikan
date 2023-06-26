from flask import render_template, redirect, url_for, jsonify, request, Blueprint, current_app, g
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
import pytz

b_posts = Blueprint('posts', __name__)

@b_posts.before_app_request
def before_request():
    g.SECRET_KEY = current_app.config['SECRET_KEY']
    g.db = current_app.config['DB']
    g.TOKEN_KEY = current_app.config['TOKEN_KEY']
    
    

@b_posts.route("/update_like", methods=["POST"])
def update_like():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY,
            algorithms=["HS256"]
            )
        user_info =g.db.normal_users.find_one({"username": payload["id"]})
        user_info2 =g.db.expert_users.find_one({"username": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        if user_info:
            if user_info['role'] != 'admin':
                
                doc = {
                    "post_id": post_id_receive,
                    "id_user":str( user_info["_id"]),
                    "type": type_receive
                }
                if action_receive =="like":
                   g.db.likes.insert_one(doc)
                else:
                   g.db.likes.delete_one(doc)
        elif user_info2:
            if user_info2['role'] != 'admin':
                
                doc = {
                    "post_id": post_id_receive,
                    "id_user": str(user_info2["_id"]),
                    "type": type_receive
                }
                if action_receive =="like":
                   g.db.likes.insert_one(doc)
                else:
                   g.db.likes.delete_one(doc)
        count =g.db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
   
@b_posts.route('/create_post')
def create_post():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                g.SECRET_KEY,
                algorithms=['HS256']
            )
            user_info =g.db.normal_users.find_one({'username':payload.get('id')})
            user_info2 =g.db.expert_users.find_one({'username':payload.get('id')})
            
            if user_info:
                if user_info['role'] == 'admin':
                    return render_template('forum_after.html',user_info=user_info, msg="You are an admin")
                else:   
                    return render_template('create_post.html',user_info=user_info)
            elif user_info2:
                return render_template('create_post.html',user_info=user_info2)
            else:
                return redirect(url_for("index"))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for('auth.login'))
    
@b_posts.route('/edit_post/<id_post>')
def edit_post(id_post):
    token_receive = request.cookies.get(g.TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                g.SECRET_KEY,
                algorithms=['HS256']
            )
            user_info =g.db.normal_users.find_one({'username':payload.get('id')})
            user_info2 =g.db.expert_users.find_one({'username':payload.get('id')})
            post =g.db.posts.find_one({'_id':ObjectId(id_post)})
            
            doc = {
                '_id':str(post['_id']),
                'id_user':post['id_user'],
                'title':post['title'],
                'question':post['question'],
                'topic':post['topic'],
                'date':post['date'],
                'post_pic_real':post['post_pic_real'],
                'post_pic':post['post_pic']
            }
            
            if user_info:
                if user_info['role'] == 'admin':
                    return f'<center><h1>You are an admin, you shouldn`t have to post anything</h1><a href="/">Go back to home</a></center>'
                else:   
                    return render_template('edit_post.html',post=doc,user_info=user_info)
            elif user_info2:
                return render_template('edit_post.html',post=doc,user_info=user_info2)
            else:
                return redirect(url_for("index"))
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for('auth.login'))
    
@b_posts.route('/delete/<id_post>')
def delete_post(id_post):
    token_receive = request.cookies.get(g.TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                g.SECRET_KEY,
                algorithms=['HS256']
            )
            username = payload['id']
            user_info =g.db.normal_users.find_one({'username':payload.get('id')})
            user_info2 =g.db.expert_users.find_one({'username':payload.get('id')})
            post =g.db.posts.find_one({'_id':ObjectId(id_post)})
            
            if post:
                if user_info:
                    if post['id_user'] == str(user_info['_id']):
                        g.db.posts.delete_one({'_id':ObjectId(id_post)})   
                        g.db.answers.delete_many({'id_post':id_post})   
                        return render_template('forum_after.html',user_info=user_info, msg=f'Your post ({post["title"]}) has been deleted')
                    elif user_info['role'] == 'admin':
                        g.db.posts.delete_one({'_id':ObjectId(id_post)})   
                        g.db.answers.delete_many({'id_post':id_post}) 
                        send_notifications(post['id_user'],payload['id'],f'{username} has removed your post due to the violation you committed','#')
                        return render_template('forum_after.html',user_info=user_info, msg=f'Your post ({post["title"]}) has been deleted')
                    else:
                        return redirect(url_for('index'))
                    
                elif user_info2:
                    if post['id_user'] == str(user_info2['_id']):
                        g.db.posts.delete_one({'_id':ObjectId(id_post)})
                        g.db.answers.delete_many({'id_post':id_post})     
                        return render_template('forum_after.html',user_info=user_info2, msg=f'Your post ({post["title"]}) has been deleted')
                    else:
                        return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for('auth.login'))
    
    
@b_posts.route("/post_detail/<id_post>/")
def post_detail_slash(id_post):
    # Mengarahkan permintaan ke versi URL tanpa slash
    return redirect(url_for('posts.post_detail', id_post=id_post))

@b_posts.route("/post_detail/<id_post>")
def post_detail(id_post):
    token_receive = request.cookies.get(g.TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                g.SECRET_KEY,
                algorithms=['HS256']
            )
            user_info =g.db.normal_users.find_one({'username':payload.get('id')})
            user_info2 =g.db.expert_users.find_one({'username':payload.get('id')})
        
            post =g.db.posts.find_one({'_id':ObjectId(id_post)})
        
            user1 =g.db.normal_users.find_one({'_id':ObjectId(post['id_user'])})
            user2 =g.db.expert_users.find_one({'_id':ObjectId(post['id_user'])})
            
            doc = {}
            if user1:
                doc = {
                    '_id':str(post['_id']),
                    'username':user1['username'],
                    'profile_name':user1['profile_name'],
                    'profile_pic_real':user1['profile_pic_real'],
                    'role':user1['role'],
                    'title':post['title'],
                    'question':post['question'],
                    'topic':post['topic'],
                    'date':post['date'],
                    'post_pic_real':post['post_pic_real'],
                    'post_pic':post['post_pic'],
                    'status':''
                }
                doc["count_up"] =g.db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))
                
            if user2:
                doc = {
                    '_id':str(post['_id']),
                    'username':user2['username'],
                    'profile_name':user2['profile_name'],
                    'profile_pic_real':user2['profile_pic_real'],
                    'role':user2['role'],
                    'title':post['title'],
                    'question':post['question'],
                    'topic':post['topic'],
                    'date':post['date'],
                    'post_pic_real':post['post_pic_real'],
                    'post_pic':post['post_pic'],
                    'status': user2['status'],

                }
                doc["count_up"] =g.db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))        
            
            if user_info:
                return render_template('post_detail.html',
                                       user_info=user_info,
                                        post=doc
                )
            elif user_info2:
                return render_template('post_detail.html',
                                       user_info=user_info2,
                                        post=doc
                )
            else:
                return redirect(url_for("index"))
                
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for('index'))

        
@b_posts.route("/posting", methods=["POST"])
def posting():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY, 
            algorithms=["HS256"]
            )
        username = payload.get('id')
        user_info =g.db.normal_users.find_one({'username':payload.get('id')})
        user_info2 =g.db.expert_users.find_one({'username':payload.get('id')})

        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        title_receive = request.form["title_give"]
        question_receive = request.form["question_give"]
        topic_receive = request.form["topic_give"]
        date_receive = request.form["date_give"]
        
        if user_info:
            doc = {
                "id_user": str(user_info["_id"]),
                "title": title_receive,
                "question": question_receive,
                "topic": topic_receive,
                "date": date_receive
            }
            
            if "file_give" in request.files:
                file = request.files["file_give"]
                filename = secure_filename(file.filename)
                extension = filename.split(".")[-1]
                file_path = f"post_pics/{username}_{date}.{extension}"
                file.save("./static/" + file_path)
                doc["post_pic"] = filename
                doc["post_pic_real"] = file_path
            else:
                doc["post_pic"] = 'post1.jpg'
                doc["post_pic_real"] = 'post_pics/post1.jpg'    
                
                
            g.db.posts.insert_one(doc)
            return jsonify({
                "result": "success",
                "msg": "Posting successful!"
                })
            
        elif user_info2:
            doc = {
                "id_user": str(user_info2["_id"]),
                "title": title_receive,
                "question": question_receive,
                "topic": topic_receive,
                "date": date_receive
            }
            
            if "file_give" in request.files:
                file = request.files["file_give"]
                filename = secure_filename(file.filename)
                extension = filename.split(".")[-1]
                file_path = f"post_pics/{username}_{date}.{extension}"
                file.save("./static/" + file_path)
                doc["post_pic"] = filename
                doc["post_pic_real"] = file_path
            else:
                doc["post_pic"] = 'post1.jpg'
                doc["post_pic_real"] = 'post_pics/post1.jpg'
                
            g.db.posts.insert_one(doc)
            return jsonify({
                "result": "success",
                "msg": "Posting successful!"
                })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
@b_posts.route("/post_editing", methods=["POST"])
def post_editing():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY, 
            algorithms=["HS256"]
            )
        
        id_post = request.form['id_post']
        id_user = request.form['id_user']
        username = payload.get('id')
        user_info =g.db.normal_users.find_one({'username':username})
        user_info2 =g.db.expert_users.find_one({'username':username})
     
                
        title_receive = request.form["title_give"]
        question_receive = request.form["question_give"]
        topic_receive = request.form["topic_give"]
        date_receive = request.form["date_give"]
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        if user_info:
            if str(user_info['_id']) == id_user:
                doc = {
                    "id_user": str(user_info["_id"]),
                    "title": title_receive,
                    "question": question_receive,
                    "topic": topic_receive,
                    "date": date_receive
                }
                
                if "file_give" in request.files:
                    file = request.files["file_give"]
                    filename = secure_filename(file.filename)
                    extension = filename.split(".")[-1]
                    file_path = f"post_pics/{username}_{date}.{extension}"
                    file.save("./static/" + file_path)
                    doc["post_pic"] = filename
                    doc["post_pic_real"] = file_path
                    
                    
                g.db.posts.update_one({"_id": ObjectId(id_post)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Post has been edited"
                    })
            elif user_info['_id'] != id_user:
                return jsonify({
                    "result": "failed",
                    "msg": "You don't have permission to do this"
                    })
                    
        elif user_info2:
            if str(user_info2['_id']) == id_user:
                doc = {
                    "id_user": str(user_info2["_id"]),
                    "title": title_receive,
                    "question": question_receive,
                    "topic": topic_receive,
                    "date": date_receive
                }
                
                if "file_give" in request.files:
                    file = request.files["file_give"]
                    filename = secure_filename(file.filename)
                    extension = filename.split(".")[-1]
                    file_path = f"post_pics/{username}_{date}.{extension}"
                    file.save("./static/" + file_path)
                    doc["post_pic"] = filename
                    doc["post_pic_real"] = file_path
                    
                g.db.posts.update_one({"_id": ObjectId(id_post)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Post has been edited"
                    })
            elif user_info2['_id'] != id_user:
                return jsonify({
                    "result": "failed",
                    "msg": "You don't have permission to do this"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

   
@b_posts.route("/get_posts", methods=["GET"])
def get_posts():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY,
            algorithms=["HS256"]
            )
        username_receive = request.args.get('username_give')
        user_info =g.db.normal_users.find_one({"username": payload["id"]})
        user_info2 =g.db.expert_users.find_one({"username": payload["id"]})
        list_posts = []
        if username_receive == '':
            posts = list(g.db.posts.find({}).sort("date", -1).limit(10))
        else:
            posts = list(g.db.posts.find({'id_user':username_receive}).sort("date", -1).limit(10))

        
        for post in posts:
            user1 =g.db.normal_users.find_one({'_id':ObjectId(post['id_user'])})
            user2 =g.db.expert_users.find_one({'_id':ObjectId(post['id_user'])})
            
            if user1:
                doc = {
                    '_id':str(post['_id']),
                    'username':user1['username'],
                    'profile_name':user1['profile_name'],
                    'profile_pic_real':user1['profile_pic_real'],
                    'role':user1['role'],
                    'status': '',
                    'title':post['title'],
                    'question':post['question'],
                    'topic':post['topic'],
                    'date':post['date'],
                    'post_pic_real':post['post_pic_real'],
                    'post_pic':post['post_pic']
                }
                doc["count_up"] =g.db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

                
            if user2:
                doc = {
                    '_id':str(post['_id']),
                    'username':user2['username'],
                    'profile_name':user2['profile_name'],
                    'profile_pic_real':user2['profile_pic_real'],
                    'role':user2['role'],
                    'status': user2['status'],
                    'title':post['title'],
                    'question':post['question'],
                    'topic':post['topic'],
                    'date':post['date'],
                    'post_pic_real':post['post_pic_real'],
                    'post_pic':post['post_pic']
                }
                doc["count_up"] =g.db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

            list_posts.append(doc)
            
        return jsonify({
            "result": "success",
            "msg": "Successful fetched all posts",
            'posts':list_posts
            })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

   
@b_posts.route("/topic/<string:topic>", methods=["POST"])
def get_posts_by_topic(topic):
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, g.SECRET_KEY, algorithms=["HS256"])
        user_info =g.db.normal_users.find_one({"username": payload["id"]})
        user_info2 =g.db.expert_users.find_one({"username": payload["id"]})
        list_posts = []

        posts = list(g.db.posts.find({"topic": topic}).sort("date", -1).limit(10))
        print(posts)

        for post in posts:
            user1 =g.db.normal_users.find_one({'_id': ObjectId(post['id_user'])})
            user2 =g.db.expert_users.find_one({'_id': ObjectId(post['id_user'])})

            if user1:
                doc = {
                    '_id': str(post['_id']),
                    'username': user1['username'],
                    'profile_name': user1['profile_name'],
                    'profile_pic_real': user1['profile_pic_real'],
                    'role': user1['role'],
                    'status': '',
                    'title': post['title'],
                    'question': post['question'],
                    'topic': post['topic'],
                    'date': post['date'],
                    'post_pic_real': post['post_pic_real'],
                    'post_pic': post['post_pic']
                }
                doc["count_up"] =g.db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

            if user2:
                doc = {
                    '_id': str(post['_id']),
                    'username': user2['username'],
                    'profile_name': user2['profile_name'],
                    'profile_pic_real': user2['profile_pic_real'],
                    'role': user2['role'],
                    'status': user2['status'],
                    'title': post['title'],
                    'question': post['question'],
                    'topic': post['topic'],
                    'date': post['date'],
                    'post_pic_real': post['post_pic_real'],
                    'post_pic': post['post_pic']
                }
                doc["count_up"] =g.db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(g.db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

            list_posts.append(doc)

        return jsonify({
            "result": "success",
            "msg": f"Successful fetched posts by topic '{topic}'",
            'posts': list_posts
        })

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
 
@b_posts.route('/submit_report', methods=['POST'])
def submit_report():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                g.SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = g.db.normal_users.find_one({'username':payload.get('id')})
            user_info2 = g.db.expert_users.find_one({'username':payload.get('id')})
            
            id_post = request.form.get('id_post')
            issue_type = request.form.get('issueType')
            description = request.form.get('description')
            
            # Create a new report document
           
            
            if user_info:
                report = {
                    'by_user':str(user_info['_id']),
                    'link':'/post_detail/'+id_post,
                    'username':user_info['username'],
                    'id_post':id_post,
                    'issue_type': issue_type,
                    'description': description
                }
                g.db.reports.insert_one(report)
                return jsonify({
                    "msg":"Your report has been submitted. We will review it as soon as possible."
                })
            elif user_info2:
                report = {
                    'by_user':str(user_info2['_id']),
                    'link':'/post_detail/'+id_post,
                    'username':user_info2['username'],
                    'id_post':id_post,
                    'issue_type': issue_type,
                    'description': description
                }
                g.db.reports.insert_one(report)
                return jsonify({
                    "msg":"Your report has been submitted. We will review it as soon as possible."
                })
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for('auth.login'))
   
def send_notifications(to_user,by_user,message,link):
    date = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    doc = {
        'to_user':to_user,
        'by_user':by_user,
        'message':message,
        'status':'unread',
        'link':link,
        'date':date
    }
    g.db.notifications.insert_one(doc) 