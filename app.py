from flask import Flask, render_template, redirect, url_for, jsonify, request
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'TimProjek2'
MONGODB_CONNECTION_STRING = 'mongodb+srv://user1:123@cluster0.g1iutgc.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.finalprojectForumHnB
TOKEN_KEY = 'mytoken'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/sign_up/save', methods=['POST'])
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
            "gender":"",
            "academic_info":"",
            "workplace":"",
            "service":"",
            "phone_number":"",
            "profile_pic": "",                                          
            "profile_pic_real": "profile_pics/profile_placeholder.png", 
            "profile_info": ""                                            
            }
        db.expert_users.insert_one(doc)
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
        db.normal_users.insert_one(doc)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failed'})

@app.route("/sign_up/check_dup", methods=["POST"])
def check_dup():
    username_receive = request.form.get('username_give')
    exists = bool(db.normal_users.find_one({'username':username_receive}))
    exists2 = bool(db.expert_users.find_one({'username':username_receive}))
    return jsonify({"result": "success", 'exists':exists+exists2})

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 