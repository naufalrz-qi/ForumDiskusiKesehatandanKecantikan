from flask import Flask, render_template, redirect, url_for, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
import zipfile
import os


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'TimProjek2'
MONGODB_CONNECTION_STRING = 'mongodb+srv://user1:123@cluster0.g1iutgc.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.finalprojectForumHnB
TOKEN_KEY = 'my_token'
topics_collection = db["topics"]


def insert_topics():
    if topics_collection.count_documents({}) == 0:
        # Data klasifikasi topik
        classifications = {
            "Kesehatan Umum": {
                "topics": [
                    {"topic": "Gaya hidup sehat", "index": "lifestyle"},
                    {"topic": "Nutrisi dan diet", "index": "nutrition"},
                    {"topic": "Olahraga dan kebugaran", "index": "fitness"},
                    {"topic": "Kesehatan mental dan kesejahteraan", "index": "mental-health"},
                    {"topic": "Pencegahan penyakit", "index": "prevention"},
                    {"topic": "Kesehatan anak-anak dan remaja", "index": "children-health"}
                ]
            },
            "Perawatan Kulit": {
                "topics": [
                    {"topic": "Perawatan wajah", "index": "facial-care"},
                    {"topic": "Produk perawatan kulit", "index": "skincare-products"},
                    {"topic": "Perawatan kulit alami", "index": "natural-skin-care"},
                    {"topic": "Masalah kulit (jerawat, penuaan, hiperpigmentasi)", "index": "skin-issues"},
                    {"topic": "Paparan sinar matahari dan perlindungan dari sinar UV", "index": "sun-protection"}
                ]
            },
            "Rambut dan Perawatan Rambut": {
                "topics": [
                    {"topic": "Perawatan rambut (shampoo, kondisioner, perawatan)", "index": "hair-care"},
                    {"topic": "Gaya rambut", "index": "hairstyles"},
                    {"topic": "Masalah rambut (kerontokan, ketombe, rambut kering atau berminyak)", "index": "hair-issues"}
                ]
            },
            "Make-up dan Produk Kecantikan": {
                "topics": [
                    {"topic": "Aplikasi make-up dan teknik", "index": "makeup-application"},
                    {"topic": "Produk kosmetik (foundation, lipstik, maskara)", "index": "cosmetic-products"},
                    {"topic": "Tips dan trik kecantikan", "index": "beauty-tips"}
                ]
            },
            "Kesehatan Mata": {
                "topics": [
                    {"topic": "Perawatan mata", "index": "eye-care"},
                    {"topic": "Penggunaan lensa kontak", "index": "contact-lenses"},
                    {"topic": "Masalah mata (rabun jauh, rabun dekat, mata kering)", "index": "eye-issues"}
                ]
            },
            "Kesehatan Gigi dan Mulut": {
                "topics": [
                    {"topic": "Perawatan gigi (pembersihan, pemutihan gigi)", "index": "dental-care"},
                    {"topic": "Penyakit gigi dan gusi", "index": "dental-issues"},
                    {"topic": "Kesehatan mulut (nafas segar, perawatan lidah)", "index": "oral-health"}
                ]
            },
            "Kesehatan Wanita": {
                "topics": [
                    {"topic": "Kesehatan reproduksi", "index": "reproductive-health"},
                    {"topic": "Perawatan kewanitaan", "index": "feminine-care"},
                    {"topic": "Kehamilan dan persalinan", "index": "pregnancy"},
                    {"topic": "Masalah menstruasi dan menopause", "index": "menstruation-menopause"}
                ]
            },
            "Kesehatan Pria": {
                "topics": [
                    {"topic": "Kesehatan reproduksi pria", "index": "male-reproductive-health"},
                    {"topic": "Perawatan kulit pria", "index": "male-skin-care"},
                    {"topic": "Gaya hidup sehat untuk pria", "index": "male-lifestyle"}
                ]
            },
            "Suplemen dan Obat-obatan": {
                "topics": [
                    {"topic": "Suplemen makanan", "index": "dietary-supplements"},
                    {"topic": "Vitamin dan mineral", "index": "vitamins-minerals"},
                    {"topic": "Pengobatan alternatif", "index": "alternative-medicine"},
                    {"topic": "Obat-obatan umum", "index": "common-medications"}
                ]
            },
            "Estetika dan Perawatan Tubuh": {
                "topics": [
                    {"topic": "Perawatan tubuh (massage, spa)", "index": "body-care"},
                    {"topic": "Perawatan kuku", "index": "nail-care"},
                    {"topic": "Prosedur kosmetik non-bedah (filler, botox)", "index": "non-surgical-procedures"}
                ]
            },
            "Kesehatan Alamiah": {
                "topics": [
                    {"topic": "Pengobatan herbal dan tradisional", "index": "herbal-traditional-medicine"},
                    {"topic": "Penggunaan minyak essensial", "index": "essential-oils"},
                    {"topic": "Terapi alternatif (akupunktur, refleksiologi)", "index": "alternative-therapies"}
                ]
            },
            "Kesehatan Mental dan Emosional": {
                "topics": [
                    {"topic": "Manajemen stres", "index": "stress-management"},
                    {"topic": "Kesehatan pikiran dan kecerdasan emosional", "index": "mental-wellbeing"},
                    {"topic": "Terapi psikologis dan konseling", "index": "psychological-therapy"}
                ]
            },
            "Kesehatan dan Kecantikan dalam Masyarakat dan Budaya": {
                "topics": [
                    {"topic": "Norma kecantikan", "index": "beauty-norms"},
                    {"topic": "Persepsi tubuh dan citra diri", "index": "body-image"},
                    {"topic": "Kesehatan dan kecantikan dalam budaya populer", "index": "pop-culture-health-beauty"}
                ]
            },
            "Lainnya": {
                "topics": [
                    {"topic": "Lainnya", "index": "others"}
                ]
            }
        }

        # Insert data klasifikasi topik ke dalam collection 'topics'
        for category, data in classifications.items():
            topic_data = {
                "category": category,
                "topics": data["topics"]
            }
            topics_collection.insert_one(topic_data)

        return "Data klasifikasi topik telah diinsert ke dalam MongoDB"
    else:
        return "Collection 'topics' sudah berisi data"
    
# insert_topics()

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

@app.route("/update_like", methods=["POST"])
def update_like():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY,
            algorithms=["HS256"]
            )
        user_info = db.normal_users.find_one({"username": payload["id"]})
        user_info2 = db.expert_users.find_one({"username": payload["id"]})
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
                    db.likes.insert_one(doc)
                else:
                    db.likes.delete_one(doc)
        elif user_info2:
            if user_info2['role'] != 'admin':
                
                doc = {
                    "post_id": post_id_receive,
                    "id_user": str(user_info2["_id"]),
                    "type": type_receive
                }
                if action_receive =="like":
                    db.likes.insert_one(doc)
                else:
                    db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@app.route('/expert_verification', methods=['POST'])
def submit_data_expert():
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    id_number = request.form['id_number']
    workplace = request.form['workplace']
    files = []
    file1 = request.files['fileData1']
    file2 = request.files['fileData2']
    file3 = request.files['fileData3']
    file4 = request.files['fileData4']
    files.append(file1)
    files.append(file2)
    files.append(file3)
    files.append(file4)
    
    print(files)
    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_names=[]
    print(file_names)
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
                    return redirect(url_for('index',msg="You are an admin"))
                else:            
                    return redirect(url_for('index',msg="You are not an expert"))
            elif user_info2:
                check_data = db.expert_datas.find_one({'id_user':str(user_info2['_id'])})
                if check_data:
                    return redirect(url_for('expert_verification',msg="You already submitted your data, please wait until we done review it"))
                else:
                    a = 0
                    for file in files:
                        if file:
                            a += 1
                            filename = f"{a}_{file.filename}"
                            file.save('./static/expert_files/' + filename)
                            file_names.append(filename)

                    
                    if file_names:
                        zip_file = 'expert_files/'+user_info2['username']+'_'+date+'.zip'
                        zip_filename = './static/' + zip_file
                        with zipfile.ZipFile(zip_filename, 'w') as zip:
                            for filename in file_names:
                                zip.write('./static/expert_files/' + filename, filename)
                                
                            for filename in file_names:
                                os.remove('./static/expert_files/' + filename)
                        
                        
                        document = {
                            'id_user': str(user_info2['_id']),
                            'name': name,
                            'email': email,
                            'phone_number': phone_number,
                            'id_number': id_number,
                            'workplace': workplace,
                            'file_data': zip_file
                        }
                        db.expert_datas.insert_one(document)
                        return redirect(url_for('expert_verification',msg="Your data have been submitted"))
                    
                    else:
                        return redirect(url_for('expert_verification',msg="Please upload your files"))
            
                    
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('index'))

@app.route('/expert_verification')
def expert_verification():
    msg = request.args.get('msg')
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
                    return render_template('forum_after.html',user_info=user_info, msg="You are an admin")
                else:            
                    return render_template('forum_after.html',user_info=user_info, msg="You are not an expert")
            elif user_info2:
                return render_template('expert_verification.html',user_info=user_info2,msg=msg)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('index'))
    
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
                    return render_template('forum_after.html',user_info=user_info, msg="You are an admin")
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
    
@app.route('/edit_post/<id_post>')
def edit_post(id_post):
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
            post = db.posts.find_one({'_id':ObjectId(id_post)})
            
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
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
    
@app.route('/delete/<id_post>')
def delete_post(id_post):
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
            post = db.posts.find_one({'_id':ObjectId(id_post)})
            
            if post:
                if user_info:
                    if user_info['role'] == 'admin':
                        return f'<center><h1>You are an admin, you shouldn`t have to post anything</h1><a href="/">Go back to home</a></center>'
                    else:
                        db.posts.delete_one({'_id':ObjectId(id_post)})   
                        db.answers.delete_many({'id_post':id_post})   
                        return render_template('forum_after.html',user_info=user_info, msg=f'Your post ({post["title"]}) has been deleted')
                elif user_info2:
                    db.posts.delete_one({'_id':ObjectId(id_post)})
                    db.answers.delete_many({'id_post':id_post})     
                    return render_template('forum_after.html',user_info=user_info2, msg=f'Your post ({post["title"]}) has been deleted')
            else:
                return redirect(url_for('index'))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
    
@app.route('/verification_datas')
def verification_datas():
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
                    expertDatas = list(db.expert_datas.find({}))
                    list_expertDatas = []
                    for expertData in expertDatas:
                        user = db.expert_users.find_one({'_id':ObjectId(str(expertData['id_user']))})
                        doc = {
                            '_id':str(expertData['_id']),
                            'id_user':expertData['id_user'],
                            'name':expertData['name'],
                            'email':expertData['email'],
                            'phone_number':expertData['phone_number'],
                            'id_number':expertData['id_number'],
                            'workplace':expertData['workplace'],
                            'file_data':expertData['file_data'],
                            'username':user['username'],
                            'user_status':user['status']
                            
                        }
                        list_expertDatas.append(doc)
                    return render_template('verification_datas.html',user_info=user_info,expertDatas=list_expertDatas)
                else: 
                    return redirect(url_for('index'))
            elif user_info2:
                return redirect(url_for('index'))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('index'))
    
@app.route('/verifying', methods=['POST'])
def verifying():
    user_id = request.form['user_id']
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
                    user = db.expert_users.find_one({'_id':ObjectId(user_id)})
                    db.expert_users.update_one({'_id':ObjectId(user_id)},{'$set':{'status':'verified'}})
                    return jsonify({
                        'result':'success',
                        'msg':'User '+user['username']+' has been verified'
                    })
                else: 
                    return redirect(url_for('index'))
            elif user_info2:
                return redirect(url_for('index'))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('index'))
    
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
                    reportDatas = list(db.reports.find({},{'_id':False}))
                    return render_template('report_data.html',user_info=user_info,reportDatas=reportDatas)
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
    
@app.route('/topics')
def topics():
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
                return render_template('topics.html',user_info=user_info)
            elif user_info2:
                return render_template('topics.html',user_info=user_info2)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
    
@app.route('/submit_report', methods=['POST'])
def submit_report():
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
                db.reports.insert_one(report)
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
                db.reports.insert_one(report)
                return jsonify({
                    "msg":"Your report has been submitted. We will review it as soon as possible."
                })
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
   
@app.route('/submit_report_reply', methods=['POST'])
def submit_report_reply():
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
            
            id_reply = request.form.get('id_reply')
            answer_id = request.form.get('id_answer')
            issue_type = request.form.get('issueType')
            description = request.form.get('description')
            
            # Create a new report document
           
            reply = db.replies.find_one({'_id':ObjectId(id_reply)})
            if user_info:
                report = {
                    'by_user':str(user_info['_id']),
                    'link':'/post_detail/'+reply['post_id']+'#answer_'+answer_id,
                    'username':user_info['username'],
                    'id_post':reply['post_id'],
                    'issue_type': issue_type,
                    'description': description
                }
                db.reports.insert_one(report)
                return jsonify({
                    "msg":"Your report has been submitted. We will review it as soon as possible."
                })
            elif user_info2:
                report = {
                    'by_user':str(user_info2['_id']),
                    'link':'/post_detail/'+reply['post_id']+'#answer_'+answer_id,
                    'username':user_info['username'],
                    'id_post':reply['post_id'],
                    'issue_type': issue_type,
                    'description': description
                }
                db.reports.insert_one(report)
                return jsonify({
                    "msg":"Your report has been submitted. We will review it as soon as possible."
                })
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for('login'))
   
@app.route('/submit_report_answer', methods=['POST'])
def submit_report_answer():
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
                db.reports.insert_one(report)
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
                db.reports.insert_one(report)
                return jsonify({
                    "msg":"Your report has been submitted. We will review it as soon as possible."
                })
            
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
                    
                db.answers.insert_one(doc)
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
@app.route("/edit_answer", methods=["POST"])
def edit_answer():
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
                    
                    
                db.answers.update_one({"_id": ObjectId(id_answer)}, {"$set": doc})
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
                    
                db.answers.update_one({"_id": ObjectId(id_answer)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
@app.route("/edit_reply", methods=["POST"])
def edit_reply():
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
                
               
                db.replies.update_one({"_id": ObjectId(id_reply)}, {"$set": doc})
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
               
                db.replies.update_one({"_id": ObjectId(id_reply)}, {"$set": doc})
                return jsonify({
                    "result": "success",
                    "msg": "Edit reply successful!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
    
@app.route("/delete_answer", methods=["POST"])
def delete_answer():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
            )
        user_info = db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = db.expert_users.find_one({'username':payload.get('id')})
        

        id_answer = request.form["id_answer"]
        
        if user_info:
            if user_info['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:

                db.answers.delete_one({"_id": ObjectId(id_answer)})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successfully deleted!"
                    })
        
            
        elif user_info2:
            if user_info2['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:               
                db.answers.delete_one({"_id": ObjectId(id_answer)})
                return jsonify({
                    "result": "success",
                    "msg": "Answering successfully deleted!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
@app.route("/delete_reply", methods=["POST"])
def delete_reply():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
            )
        user_info = db.normal_users.find_one({'username':payload.get('id')})
        user_info2 = db.expert_users.find_one({'username':payload.get('id')})
        

        id_reply = request.form["id_reply"]
        
        if user_info:
            if user_info['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:

                db.replies.delete_one({"_id": ObjectId(id_reply)})
                return jsonify({
                    "result": "success",
                    "msg": "Reply successfully deleted!"
                    })
        
            
        elif user_info2:
            if user_info2['role'] == 'admin':
                return jsonify({
                    "result": "failed",
                    "msg": "You're an admin"
                })
            else:               
                db.replies.delete_one({"_id": ObjectId(id_reply)})
                return jsonify({
                    "result": "success",
                    "msg": "Reply successfully deleted!"
                    })
        
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
    
@app.route("/get_replies", methods=["POST"])
def get_replies():
    id_answer_receive = request.form['id_answer']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY,
            algorithms=["HS256"]
            )
        list_replies = []

        replies = list(db.replies.find({'answer_id':id_answer_receive}).sort("date", -1))
    
        for reply in replies:
            user1 = db.normal_users.find_one({'_id':ObjectId(reply['id_user'])})
            user2 = db.expert_users.find_one({'_id':ObjectId(reply['id_user'])})
            count_replies = db.replies.count_documents({"answer_id": str(reply['_id'])})
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
            count_replies = db.replies.count_documents({"answer_id": str(answer['_id'])})
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

@app.route("/submit_reply", methods=["POST"])
def submit_reply():
    post_id = request.form['post_id']
    answer_id = request.form['answer_id']
    date = request.form['date']
    reply = request.form['reply']
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
      
        if user_info:
            if user_info['role'] != 'admin':
                db.replies.insert_one({
                    'id_user': str(user_info['_id']),
                    'post_id': post_id,
                    'answer_id': answer_id,
                    'reply': reply,
                    'date': date,
                })
                
                count_replies = db.replies.count_documents({"answer_id": answer_id})
                
                return jsonify({
                    "result": "success",
                    "msg": "Reply berhasil dikirim",
                    'count_replies':count_replies
                })
        elif user_info2:
            db.replies.insert_one({
                'id_user': str(user_info2['_id']),
                'post_id': post_id,
                'answer_id': answer_id,
                'reply': reply,
                'date': date,
                
            })
            
            count_replies = db.replies.count_documents({"answer_id": answer_id})
            
            return jsonify({
                "result": "success",
                "msg": "Reply berhasil dikirim",
                'count_replies':count_replies
                
            })
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
@app.route("/post_detail/<id_post>/")
def post_detail_slash(id_post):
    # Mengarahkan permintaan ke versi URL tanpa slash
    return redirect(url_for('post_detail', id_post=id_post))

@app.route("/post_detail/<id_post>")
def post_detail(id_post):
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
        
            post = db.posts.find_one({'_id':ObjectId(id_post)})
        
            user1 = db.normal_users.find_one({'_id':ObjectId(post['id_user'])})
            user2 = db.expert_users.find_one({'_id':ObjectId(post['id_user'])})
            
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
                doc["count_up"] = db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))
                
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
                doc["count_up"] = db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))        
            
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
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return redirect(url_for(index))

        
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
    
@app.route("/post_editing", methods=["POST"])
def post_editing():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
            )
        
        id_post = request.form['id_post']
        id_user = request.form['id_user']
        username = payload.get('id')
        user_info = db.normal_users.find_one({'username':username})
        user_info2 = db.expert_users.find_one({'username':username})
     
                
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
                    
                    
                db.posts.update_one({"_id": ObjectId(id_post)}, {"$set": doc})
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
                    
                db.posts.update_one({"_id": ObjectId(id_post)}, {"$set": doc})
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


@app.route("/topic/<string:topic>", methods=["GET"])
def urltopics(topic):
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
                return render_template('post_by_topics.html',user_info=user_info, topic=topic)
            elif user_info2:
                return render_template('post_by_topics.html',user_info=user_info2, topic=topic)
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return render_template('index.html')
    
@app.route("/get_topics", methods=["GET"])
def get_topics():
    categories = db.topics.distinct("category")  # Ambil daftar kategori dari database
    topics = {}  # Buat kamus untuk menyimpan daftar topik berdasarkan kategori

    for category in categories:
        category_topics = db.topics.find({"category": category}).distinct("topics")
        topics[category] = category_topics

    return jsonify({
        "result": "success",
        "topics": topics
    })    
    
@app.route("/topic/<string:topic>", methods=["POST"])
def get_posts_by_topic(topic):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.normal_users.find_one({"username": payload["id"]})
        user_info2 = db.expert_users.find_one({"username": payload["id"]})
        list_posts = []

        posts = list(db.posts.find({"topic": topic}).sort("date", -1).limit(10))
        print(posts)

        for post in posts:
            user1 = db.normal_users.find_one({'_id': ObjectId(post['id_user'])})
            user2 = db.expert_users.find_one({'_id': ObjectId(post['id_user'])})

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
                doc["count_up"] = db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

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
                doc["count_up"] = db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

            list_posts.append(doc)

        return jsonify({
            "result": "success",
            "msg": f"Successful fetched posts by topic '{topic}'",
            'posts': list_posts
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
        user_info = db.normal_users.find_one({"username": payload["id"]})
        user_info2 = db.expert_users.find_one({"username": payload["id"]})
        list_posts = []
        if username_receive == '':
            posts = list(db.posts.find({}).sort("date", -1).limit(10))
        else:
            posts = list(db.posts.find({'id_user':username_receive}).sort("date", -1).limit(10))

        
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
                    'status': '',
                    'title':post['title'],
                    'question':post['question'],
                    'topic':post['topic'],
                    'date':post['date'],
                    'post_pic_real':post['post_pic_real'],
                    'post_pic':post['post_pic']
                }
                doc["count_up"] = db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

                
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
                doc["count_up"] = db.likes.count_documents({"post_id": str(post['_id']), "type": "up"})
                if user_info:
                    if user_info['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info['_id'])}))
                elif user_info2:
                    if user_info2['role'] != 'admin':
                        doc["up_by_me"] = bool(db.likes.find_one({"post_id": str(post['_id']), "type": "up", "id_user": str(user_info2['_id'])}))

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
 