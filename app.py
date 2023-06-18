from flask import Flask, render_template, redirect, url_for, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
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
TOKEN_KEY = 'my_token'

@app.route('/')
def index():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = db.normal_users.find_one({'username':payload.get('id')})
            user_info2 = db.expert_users.find_one({'username':payload.get('id')})
            
            if user_info:
                return render_template('forum_after.html',user_info=user_info)
            elif user_info2:
                return render_template('forum_after.html',user_info=user_info2)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create_post')
def create_post():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = db.normal_users.find_one({'username':payload.get('id')})
            user_info2 = db.expert_users.find_one({'username':payload.get('id')})
            
            if user_info:
                if user_info['role'] == 'admin':
                    return f'<center><h1>You are an admin, you shouldn`t have to post anything</h1><a href="/">Go back to home</a></center>'
                else:   
                    return render_template('create_post.html',user_info=user_info)
            elif user_info2:
                return render_template('create_post.html',user_info=user_info2)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
    
@app.route('/report_data')
def report_data():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = db.normal_users.find_one({'username':payload.get('id')})
            user_info2 = db.expert_users.find_one({'username':payload.get('id')})
            
            if user_info:
                if user_info['role'] == 'admin':
                    return render_template('report_data.html',user_info=user_info)
                else: 
                    return render_template('forum_after.html',user_info=user_info)
            elif user_info2:
                return render_template('forum_after.html',user_info=user_info2)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
    
@app.route('/register')
def register():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = db.normal_users.find_one({'username':payload.get('id')})
            user_info2 = db.expert_users.find_one({'username':payload.get('id')})
            
            if user_info:
                return render_template('forum_after.html',user_info=user_info)
            elif user_info2:
                return render_template('forum_after.html',user_info=user_info2)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    msg = request.args.get('msg')
    token_receive = request.cookies.get(TOKEN_KEY)
    if msg:
        return render_template('login.html',msg=msg)
    else:
        if token_receive:
            try:
                payload = jwt.decode(
                    token_receive,
                    SECRET_KEY,
                    algorithms=['HS256']
                )
                user_info = db.normal_users.find_one({'username':payload.get('id')})
                user_info2 = db.expert_users.find_one({'username':payload.get('id')})
                
                if user_info:
                    return render_template('forum_after.html',user_info=user_info)
                elif user_info2:
                    return render_template('forum_after.html',user_info=user_info2)
            except jwt.ExpiredSignatureError:
                msg='Your token has expired'
                return redirect(url_for('login', msg=msg))
            except jwt.exceptions.DecodeError:
                msg='There was a problem logging you in'
                return redirect(url_for('login', msg=msg))
        else:
            return render_template('login.html',msg=msg)


@app.route('/user/<username>', methods=['GET'])
def user(username):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        status = username == payload.get('id')
        user_data= db.normal_users.find_one(
            {'username':username},
            {'_id':False}
        )
        user_data2= db.expert_users.find_one(
            {'username':username},
            {'_id':False}
        )
        
        user_info= db.normal_users.find_one(
            {'username':payload.get('id')},
            {'_id':False}
        )
        user_info2= db.expert_users.find_one(
            {'username':payload.get('id')},
            {'_id':False}
        )
        
        if username == 'admin':
            if user_info:
                if user_info['role'] == 'admin':
                    return render_template(
                            'normal_profile.html',
                            user_data=user_data,
                            user_info=user_info,
                            status=status
                            )
                else:
                    return redirect(url_for('index'))
            elif user_info2:
                if user_info2['role'] == 'admin':
                    return render_template(
                            'normal_profile.html',
                            user_data=user_data,
                            user_info=user_info,
                            status=status
                            )
                else:
                    return redirect(url_for('index'))
        else:
            if user_info:
                if user_data:
                    return render_template(
                        'normal_profile.html',
                        user_data=user_data,
                        user_info=user_info,
                        status=status
                        )
                elif user_data2:
                    return render_template(
                        'expert_profile.html',
                        user_data=user_data2,
                        user_info=user_info,
                        status=status
                        )
                    
            elif user_info2:
                if user_data:
                    return render_template(
                        'normal_profile.html',
                        user_data=user_data,
                        user_info=user_info2,
                        status=status
                        )
                elif user_data2:
                    return render_template(
                        'expert_profile.html',
                        user_data=user_data2,
                        user_info=user_info2,
                        status=status
                        )
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return redirect(url_for('index'))



@app.route("/update_profile", methods=["POST"])
def save_img():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=["HS256"]
            )
        username = payload.get('id')
        name_receive = request.form["name_give"]
        info_receive = request.form["info_give"]
        role = request.form['role']
        new_doc = {
                "profile_name": name_receive, 
                "profile_info": info_receive
                    }
        if role == 'normal':
            user_info= db.normal_users.find_one(
                    {'username':username},
                )
            
            if "file_give" in request.files:
                file = request.files["file_give"]
                filename = secure_filename(file.filename)
                extension = filename.split(".")[-1]
                file_path = f"profile_pics/{str(user_info['_id'])}.{extension}"
                file.save("./static/" + file_path)
                new_doc["profile_pic"] = filename
                new_doc["profile_pic_real"] = file_path
            db.normal_users.update_one({"username": payload["id"]}, {"$set": new_doc})
            return jsonify({
                "result": "success", 
                "msg": "Your profile has been updated"
                })
            
        elif role == 'expert':
            user_info= db.expert_users.find_one(
                    {'username':username},
                )
            gender = request.form["gender_give"]
            acinfo_receive = request.form["academic_give"]
            workplace_receive = request.form["workplace_give"]
            service_receive = request.form["service_give"]
            number_receive = request.form["number_give"]
            
            
            new_doc["gender"] = gender
            new_doc["academic_info"] = acinfo_receive
            new_doc["workplace"] = workplace_receive
            new_doc["service"] = service_receive
            new_doc["phone_number"] = number_receive
            
            if "file_give" in request.files:
                file = request.files["file_give"]
                filename = secure_filename(file.filename)
                extension = filename.split(".")[-1]
                file_path = f"profile_pics/{str(user_info['_id'])}.{extension}"
                file.save("./static/" + file_path)
                new_doc["profile_pic"] = filename
                new_doc["profile_pic_real"] = file_path
            db.expert_users.update_one({"username": payload["id"]}, {"$set": new_doc})
            return jsonify({
                "result": "success", 
                "msg": "Your profile has been updated"
                })
        
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))



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
    

@app.route('/sign_in', methods=['POST'])
def sign_in():
       # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.normal_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    
    result2 = db.expert_users.find_one(
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
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

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
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

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
@app.route("/answering", methods=["POST"])
def answering():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
            )
        username = payload.get('id')
        user_info = db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = db.expert_users.find_one({'username':payload.get('id')})
        
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
         
        answer_receive = request.form["answer_give"]
        id_post = request.form["id_post"]
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
                    
                    
                db.answers.insert_one(doc)
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
                    doc["answer_pic"] = filename
                    doc["answer_pic_real"] = file_path
                else:
                    doc["answer_pic"] = ''
                    doc["answer_pic_real"] = ''  
                    
                db.answers.insert_one(doc)
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
    
@app.route("/get_answers", methods=["POST"])
def get_answers():
    id_post_receive = request.form['id_post']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY,
            algorithms=["HS256"]
            )
        list_answers = []

        answers = list(db.answers.find({'id_post':id_post_receive}).sort("date", -1))
    
        for answer in answers:
            user1 = db.normal_users.find_one({'_id':ObjectId(answer['id_user'])})
            user2 = db.expert_users.find_one({'_id':ObjectId(answer['id_user'])})
            
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
                    'answer_pic':answer['answer_pic']
                }
                
            if user2:
                doc = {
                    '_id':str(answer['_id']),
                    'username':user1['username'],
                    'profile_name':user1['profile_name'],
                    'profile_pic_real':user1['profile_pic_real'],
                    'role':user1['role'],
                    'answer':answer['answer'],
                    'date':answer['date'],
                    'answer_pic_real':answer['answer_pic_real'],
                    'answer_pic':answer['answer_pic']
                }
            list_answers.append(doc)
        
        
        return jsonify({
            "result": "success",
            "msg": "Successful fetched all answers",
            'answers':list_answers
            })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

    
    
@app.route("/posting", methods=["POST"])
def posting():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
            )
        username = payload.get('id')
        user_info = db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = db.expert_users.find_one({'username':payload.get('id')})
        
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
                
                
            db.posts.insert_one(doc)
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
                
            db.posts.insert_one(doc)
            return jsonify({
                "result": "success",
                "msg": "Posting successful!"
                })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))



@app.route("/get_posts", methods=["GET"])
def get_posts():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY,
            algorithms=["HS256"]
            )
        username_receive = request.args.get('username_give')
        list_posts = []
        if username_receive == '':
            posts = list(db.posts.find({}).sort("date", -1).limit(10))
        else:
            posts = list(db.posts.find({'username':username_receive}).sort("date", -1).limit(10))
    
        for post in posts:
            user1 = db.normal_users.find_one({'_id':ObjectId(post['id_user'])})
            user2 = db.expert_users.find_one({'_id':ObjectId(post['id_user'])})
            
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
                    'post_pic':post['post_pic']
                }
                
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
                    'post_pic':post['post_pic']
                }
            list_posts.append(doc)
        
        
        return jsonify({
            "result": "success",
            "msg": "Successful fetched all posts",
            'posts':list_posts
            })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 