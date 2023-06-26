from flask import render_template, redirect, url_for, jsonify, request, Blueprint, current_app, g
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
import pytz

b_answers = Blueprint('answers', __name__)

@b_answers.before_app_request
def before_request():
    g.SECRET_KEY = current_app.config['SECRET_KEY']
    g.db = current_app.config['DB']
    g.TOKEN_KEY = current_app.config['TOKEN_KEY']
    
  
@b_answers.route('/submit_report_answer', methods=['POST'])
def submit_report_answer():
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
            answer_id = request.form.get('id_answer')
            issue_type = request.form.get('issueType')
            description = request.form.get('description')
            
            # Create a new report document
           
            
            if user_info:
                report = {
                    'by_user':str(user_info['_id']),
                    'link':'/post_detail/'+id_post+'#answer_'+answer_id,
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
                    'link':'/post_detail/'+id_post+'/#answer_'+answer_id,
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
   
   
@b_answers.route("/edit_answer", methods=["POST"])
def edit_answer():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY, 
            algorithms=["HS256"]
            )
        username = payload.get('id')
        user_info = g.db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = g.db.expert_users.find_one({'username':payload.get('id')})
        
        
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        answer_receive = request.form["answer_give"]
        id_post = request.form["id_post"]
        id_answer = request.form["id_answer"]
        date_receive = request.form["date_give"]
        
        if user_info:
            if user_info['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:
                doc = {
                    "id_post": id_post,
                    "id_user": str(user_info["_id"]),
                    "answer": answer_receive,
                    "date": date_receive
                }
                
                if "file_give" in request.files:
                    file = request.files["file_give"]
                    filename = secure_filename(file.filename)
                    extension = filename.split(".")[-1]
                    file_path = f"answer_pics/{username}_{date}.{extension}"
                    file.save("./static/" + file_path)
                    doc["answer"] = filename
                    doc["answer_pic_real"] = file_path 
                else:
                    doc["answer_pic"] = ''
                    doc["answer_pic_real"] = ''  
                    
                    
                g.db.answers.update_one({"_id": ObjectId(id_answer)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
            
        elif user_info2:
            if user_info2['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:
                doc = {
                    "id_post": id_post,
                    "id_user": str(user_info2["_id"]),
                    "answer": answer_receive,
                    "date": date_receive
                }
                
                
                if "file_give" in request.files:
                    file = request.files["file_give"]
                    filename = secure_filename(file.filename)
                    extension = filename.split(".")[-1]
                    file_path = f"answer_pics/{username}_{date}.{extension}"
                    file.save("./static/" + file_path)
                    doc["answer_pic"] = filename
                    doc["answer_pic_real"] = file_path
                else:
                    doc["answer_pic"] = ''
                    doc["answer_pic_real"] = ''  
                    
                g.db.answers.update_one({"_id": ObjectId(id_answer)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
    
@b_answers.route("/delete_answer", methods=["POST"])
def delete_answer():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY, 
            algorithms=["HS256"]
            )
        username = payload['id']
        user_info = g.db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = g.db.expert_users.find_one({'username':payload.get('id')})
        

        id_answer = request.form["id_answer"]
        answer = g.db.answers.find_one({'_id':ObjectId(id_answer)})
        if user_info:
            if user_info['role'] == 'admin':
                g.db.answers.delete_one({"_id": ObjectId(id_answer)})
                send_notifications(answer['id_user'],payload['id'],f'{username} has removed your answer due to the violation you committed','#')
                return jsonify({
                    "result": "success",
                    "msg": "Answering successfully deleted!"
                    })
            elif answer['id_user'] == str(user_info['_id']):
                g.db.answers.delete_one({"_id": ObjectId(id_answer)})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successfully deleted!"
                    })
            else:
                return jsonify({
                    "result": "failed",
                    "msg": "Something went wrong"
                }) 
        
            
        elif user_info2:
            if answer['id_user'] == str(user_info2['_id']):               
                g.db.answers.delete_one({"_id": ObjectId(id_answer)})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successfully deleted!"
                    })
            else:
                return jsonify({
                    "result": "failed",
                    "msg": "Something went wrong"
                }) 
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

   
@b_answers.route("/get_answers", methods=["POST"])
def get_answers():
    id_post_receive = request.form['id_post']
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY,
            algorithms=["HS256"]
            )
        list_answers = []

        answers = list(g.db.answers.find({'id_post':id_post_receive}).sort("date", -1))
    
        for answer in answers:
            user1 = g.db.normal_users.find_one({'_id':ObjectId(answer['id_user'])})
            user2 = g.db.expert_users.find_one({'_id':ObjectId(answer['id_user'])})
            count_replies = g.db.replies.count_documents({"answer_id": str(answer['_id'])})
            if user1:
                doc = {
                    '_id':str(answer['_id']),
                    'username':user1['username'],
                    'profile_name':user1['profile_name'],
                    'profile_pic_real':user1['profile_pic_real'],
                    'role':user1['role'],
                    'answer':answer['answer'],
                    'date':answer['date'],
                    'answer_pic_real':answer['answer_pic_real'],
                    'answer_pic':answer['answer_pic'],
                    'count_replies':count_replies,
                    'status':'',
                    
                }
                
            if user2:
                doc = {
                    '_id':str(answer['_id']),
                    'username':user2['username'],
                    'profile_name':user2['profile_name'],
                    'profile_pic_real':user2['profile_pic_real'],
                    'role':user2['role'],
                    'answer':answer['answer'],
                    'date':answer['date'],
                    'answer_pic_real':answer['answer_pic_real'],
                    'answer_pic':answer['answer_pic'],
                    'count_replies':count_replies,
                    'status': user2['status'],
                    
                    
                }
            list_answers.append(doc)
        
        
        return jsonify({
            "result": "success",
            "msg": "Successful fetched all answers",
            'answers':list_answers
            })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@b_answers.route("/answering", methods=["POST"])
def answering():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY, 
            algorithms=["HS256"]
            )
        username = payload.get('id')
        user_info = g.db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = g.db.expert_users.find_one({'username':payload.get('id')})
        
        
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        answer_receive = request.form["answer_give"]
        id_post = request.form["id_post"]
        date_receive = request.form["date_give"]
        post = g.db.posts.find_one({'_id':ObjectId(id_post)})
        
        if user_info:
            if user_info['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:
                doc = {
                    "id_post": id_post,
                    "id_user": str(user_info["_id"]),
                    "answer": answer_receive,
                    "date": date_receive
                }
                
                if "file_give" in request.files:
                    file = request.files["file_give"]
                    filename = secure_filename(file.filename)
                    extension = filename.split(".")[-1]
                    file_path = f"answer_pics/{username}_{date}.{extension}"
                    file.save("./static/" + file_path)
                    doc["answer"] = filename
                    doc["answer_pic_real"] = file_path 
                else:
                    doc["answer_pic"] = ''
                    doc["answer_pic_real"] = ''  
                
                g.db.answers.insert_one(doc)
                send_notifications(post['id_user'],username,f'{username} answered your post',f'/post_detail/{id_post}')
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
            
        elif user_info2:
            if user_info2['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:
                doc = {
                    "id_post": id_post,
                    "id_user": str(user_info2["_id"]),
                    "answer": answer_receive,
                    "date": date_receive
                }
                
                
                if "file_give" in request.files:
                    file = request.files["file_give"]
                    filename = secure_filename(file.filename)
                    extension = filename.split(".")[-1]
                    file_path = f"answer_pics/{username}_{date}.{extension}"
                    file.save("./static/" + file_path)
                    doc["answer_pic"] = filename
                    doc["answer_pic_real"] = file_path
                else:
                    doc["answer_pic"] = ''
                    doc["answer_pic_real"] = ''  
                send_notifications(post['id_user'],username,f'{username} answered your post',f'/post_detail/{id_post}')
                g.db.answers.insert_one(doc)
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
 
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