from flask import render_template, redirect, url_for, jsonify, request, Blueprint, current_app, g
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename

b_profile = Blueprint('user_profile', __name__)

@b_profile.before_app_request
def before_request():
    g.SECRET_KEY = current_app.config['SECRET_KEY']
    g.db = current_app.config['DB']
    g.TOKEN_KEY = current_app.config['TOKEN_KEY']
    

@b_profile.route('/user/<username>', methods=['GET'])
def user(username):
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            g.SECRET_KEY,
            algorithms=['HS256']
        )
        status = username == payload.get('id')
        user_data= g.db.normal_users.find_one(
            {'username':username},
            {'_id':False}
        )
        user_data2= g.db.expert_users.find_one(
            {'username':username},
            {'_id':False}
        )
        
        user_info= g.db.normal_users.find_one(
            {'username':payload.get('id')},
            {'_id':False}
        )
        user_info2= g.db.expert_users.find_one(
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
            else:
                return redirect(url_for("index"))
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@b_profile.route("/update_profile", methods=["POST"])
def save_img():
    token_receive = request.cookies.get(g.TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            g.SECRET_KEY,
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
            user_info= g.db.normal_users.find_one(
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
            g.db.normal_users.update_one({"username": payload["id"]}, {"$set": new_doc})
            return jsonify({
                "result": "success", 
                "msg": "Your profile has been updated"
                })
            
        elif role == 'expert':
            user_info= g.db.expert_users.find_one(
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
            g.db.expert_users.update_one({"username": payload["id"]}, {"$set": new_doc})
            return jsonify({
                "result": "success", 
                "msg": "Your profile has been updated"
                })
        else:
            return redirect(url_for("index"))
            
        
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

