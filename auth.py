from flask import render_template, redirect, url_for, jsonify, request, Blueprint, current_app, g
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename

b_auth = Blueprint('auth', __name__)


@b_auth.before_app_request
def before_request():
    g.SECRET_KEY = current_app.config['SECRET_KEY']
    g.db = current_app.config['DB']
    g.TOKEN_KEY = current_app.config['TOKEN_KEY']

@b_auth.route('/register')
def register():

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
            
            if user_info:
                return render_template('forum_after.html',user_info=user_info)
            elif user_info2:
                return render_template('forum_after.html',user_info=user_info2)
            else:
                return render_template('register.html')
                
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return render_template('register.html')

@b_auth.route('/login', methods=['GET'])
def login():
    msg = request.args.get('msg')
    token_receive = request.cookies.get(g.TOKEN_KEY)
    if msg:
        return render_template('login.html',msg=msg)
    else:
        if token_receive:
            try:
                payload = jwt.decode(
                    token_receive,
                    g.SECRET_KEY,
                    algorithms=['HS256']
                )
                user_info = g.db.normal_users.find_one({'username':payload.get('id')})
                user_info2 = g.db.expert_users.find_one({'username':payload.get('id')})
                
                if user_info:
                    return render_template('forum_after.html',user_info=user_info)
                elif user_info2:
                    return render_template('forum_after.html',user_info=user_info2)
                else:
                    return render_template('login.html')
                    
            except jwt.ExpiredSignatureError:
                msg='Your token has expired'
                return redirect(url_for('login', msg=msg))
            except jwt.exceptions.DecodeError:
                msg='There was a problem logging you in'
                return redirect(url_for('login', msg=msg))
        else:
            return render_template('login.html',msg=msg)


@b_auth.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form["username_give"]
    email_receive = request.form["email_give"]
    password_receive = request.form["password_give"]
    role_receive = request.form["role_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    if(role_receive == 'expert'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,                                  
            "profile_name": username_receive,
            "email":email_receive,
            "role":role_receive,
            "status":"unverified",                           
            "gender":"",
            "academic_info":"",
            "workplace":"",
            "service":"",
            "phone_number":"",
            "profile_pic": "",                                          
            "profile_pic_real": "profile_pics/profile_placeholder.png", 
            "profile_info": ""                                            
            }
        g.db.expert_users.insert_one(doc)
        return jsonify({'result': 'success'})
    elif(role_receive == 'normal'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,     
            "email":email_receive,
            "role":role_receive,                                 
            "profile_name": username_receive,                           
            "profile_pic": "",                                          
            "profile_pic_real": "profile_pics/profile_placeholder.png", 
            "profile_info": ""                                          
            }
        g.db.normal_users.insert_one(doc)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failed'})

@b_auth.route("/sign_up/check_dup", methods=["POST"])
def check_dup():
    username_receive = request.form.get('username_give')
    exists = bool(g.db.normal_users.find_one({'username':username_receive}))
    exists2 = bool(g.db.expert_users.find_one({'username':username_receive}))
    return jsonify({"result": "success", 'exists':exists+exists2})
    

@b_auth.route('/sign_in', methods=['POST'])
def sign_in():
       # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = g.db.normal_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    
    result2 = g.db.expert_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, g.SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    elif result2:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, g.SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )