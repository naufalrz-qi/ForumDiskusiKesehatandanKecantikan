from flask import render_template, redirect, url_for, jsonify, request, Blueprint, current_app, g
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
import pytz


b_replies = Blueprint('replies', __name__)

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

@b_replies.before_app_request
def before_request():
    g.SECRET_KEY = current_app.config['SECRET_KEY']
    g.db = current_app.config['DB']
    g.TOKEN_KEY = current_app.config['TOKEN_KEY']
    

@b_replies.route("/edit_reply", methods=["POST"])
def edit_reply():
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
        
        

        reply_receive = request.form["reply_give"]
        id_answer= request.form["id_answer"]
        id_reply = request.form["id_reply"]
        date_receive = request.form["date_give"]
        
        if user_info:
            if user_info['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:
                doc = {
                    "answer_id": id_answer,
                    "id_user": str(user_info["_id"]),
                    "reply": reply_receive,
                    "date": date_receive
                }
                
               
                g.db.replies.update_one({"_id": ObjectId(id_reply)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Edit reply successful!"
                    })
            
        elif user_info2:
            if user_info2['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:
                doc = {
                    "answer_id": id_answer,
                    "id_user": str(user_info2["_id"]),
                    "reply": reply_receive,
                    "date": date_receive
                }
               
                g.db.replies.update_one({"_id": ObjectId(id_reply)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Edit reply successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    

@b_replies.route("/delete_reply", methods=["POST"])
def delete_reply():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY, 
            algorithms=["HS256"]
            )
        user_info = g.db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = g.db.expert_users.find_one({'username':payload.get('id')})
        username = payload['id']

        id_reply = request.form["id_reply"]
        reply = g.db.replies.find_one({'_id':ObjectId(id_reply)})
        if user_info:
            if user_info['role'] == 'admin':
                g.db.replies.delete_one({"_id": ObjectId(id_reply)})
                send_notifications(reply['id_user'],payload['id'],f'{username} has removed your replies due to the violation you committed','#')
                return jsonify({
                    "result": "success",
                    "msg": "Reply successfully deleted!"
                    })
            elif reply['id_user'] == str(user_info['_id']):
                g.db.replies.delete_one({"_id": ObjectId(id_reply)})
                return jsonify({
                    "result": "success",
                    "msg": "Reply successfully deleted!"
                    })
            else:
                return jsonify({
                    "result": "failed",
                    "msg": "Something went wrong"
                }) 
            
        elif user_info2:
            if reply['id_user'] == str(user_info2['_id']):              
                g.db.replies.delete_one({"_id": ObjectId(id_reply)})
                return jsonify({
                    "result": "success",
                    "msg": "Reply successfully deleted!"
                    })
            else:
                return jsonify({
                    "result": "failed",
                    "msg": "Something went wrong"
                })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
    
@b_replies.route("/get_replies", methods=["POST"])
def get_replies():
    id_answer_receive = request.form['id_answer']
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            g.SECRET_KEY,
            algorithms=["HS256"]
            )
        list_replies = []

        replies = list(g.db.replies.find({'answer_id':id_answer_receive}).sort("date", 1))
    
        for reply in replies:
            user1 = g.db.normal_users.find_one({'_id':ObjectId(reply['id_user'])})
            user2 = g.db.expert_users.find_one({'_id':ObjectId(reply['id_user'])})
            count_replies = g.db.replies.count_documents({"answer_id": str(reply['_id'])})
            if user1:
                doc = {
                    '_id':str(reply['_id']),
                    'username':user1['username'],
                    'profile_name':user1['profile_name'],
                    'profile_pic_real':user1['profile_pic_real'],
                    'role':user1['role'],
                    'reply':reply['reply'],
                    'date':reply['date'],
                    'count_replies':count_replies,
                    'status': '',
                }
                
            if user2:
                doc = {
                    '_id':str(reply['_id']),
                    'username':user2['username'],
                    'profile_name':user2['profile_name'],
                    'profile_pic_real':user2['profile_pic_real'],
                    'role':user2['role'],
                    'reply':reply['reply'],
                    'date':reply['date'],
                    'count_replies':count_replies,
                    'status': user2['status'],
                    
                    
                }
            list_replies.append(doc)
        
        
        return jsonify({
            "result": "success",
            "msg": "Successful fetched all replies",
            'replies':list_replies
            })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
 
@b_replies.route("/submit_reply", methods=["POST"])
def submit_reply():
    post_id = request.form['post_id']
    answer_id = request.form['answer_id']
    date = request.form['date']
    reply = request.form['reply']
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
      
        answer = g.db.answers.find_one({'_id':ObjectId(answer_id)})
        if user_info:
            if user_info['role'] != 'admin':
                g.db.replies.insert_one({
                    'id_user': str(user_info['_id']),
                    'post_id': post_id,
                    'answer_id': answer_id,
                    'reply': reply,
                    'date': date,
                })
                
                count_replies = g.db.replies.count_documents({"answer_id": answer_id})
                send_notifications(answer['id_user'],username,f'{username} replied your answer',f'/post_detail/{post_id}#answer_{answer_id}')
                return jsonify({
                    "result": "success",
                    "msg": "Reply has been sended",
                    'count_replies':count_replies
                })
            else:
                count_replies = g.db.replies.count_documents({"answer_id": answer_id})
                
                return jsonify({
                "result": "success",
                "msg": "You are an admin",
                'count_replies':count_replies
            })
        elif user_info2:
            g.db.replies.insert_one({
                'id_user': str(user_info2['_id']),
                'post_id': post_id,
                'answer_id': answer_id,
                'reply': reply,
                'date': date,
                
            })
            send_notifications(answer['id_user'],username,f'{username} replied your answer',f'/post_detail/{post_id}#answer_{answer_id}')
            count_replies = g.db.replies.count_documents({"answer_id": answer_id})
            
            return jsonify({
                "result": "success",
                "msg": "Reply has been sended",
                'count_replies':count_replies
                
            })
            
        else:
            count_replies = g.db.replies.count_documents({"answer_id": answer_id})
            return jsonify({
                "result": "success",
                "msg": "You are an admin",
                'count_replies':count_replies
            })
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@b_replies.route('/submit_report_reply', methods=['POST'])
def submit_report_reply():
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
            
            id_reply = request.form.get('id_reply')
            answer_id = request.form.get('id_answer')
            issue_type = request.form.get('issueType')
            description = request.form.get('description')
            
            # Create a new report document
           
            reply = g.db.replies.find_one({'_id':ObjectId(id_reply)})
            if user_info:
                report = {
                    'by_user':str(user_info['_id']),
                    'link':'/post_detail/'+reply['post_id']+'#reply_'+id_reply,
                    'username':user_info['username'],
                    'id_post':reply['post_id'],
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
                    'link':'/post_detail/'+reply['post_id']+'#reply_'+id_reply,
                    'username':user_info2['username'],
                    'id_post':reply['post_id'],
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
 