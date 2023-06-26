from flask import Flask, render_template, redirect, url_for, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
import zipfile
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pytz

from auth import b_auth
from answers import b_answers
from posts import b_posts
from replies import b_replies
from user_profile import b_profile


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

SECRET_KEY = 'TimProjek2'

client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[DB_NAME]
TOKEN_KEY = 'my_token'
topics_collection = db["topics"]


app.config['DB'] = db
app.config['TOKEN_KEY'] = TOKEN_KEY
app.config['SECRET_KEY'] = SECRET_KEY
app.register_blueprint(b_auth, db=db, TOKEN_KEY=TOKEN_KEY, SECRET_KEY=SECRET_KEY)
app.register_blueprint(b_answers, db=db, TOKEN_KEY=TOKEN_KEY, SECRET_KEY=SECRET_KEY)
app.register_blueprint(b_posts, db=db, TOKEN_KEY=TOKEN_KEY, SECRET_KEY=SECRET_KEY)
app.register_blueprint(b_replies, db=db, TOKEN_KEY=TOKEN_KEY, SECRET_KEY=SECRET_KEY)
app.register_blueprint(b_profile, db=db, TOKEN_KEY=TOKEN_KEY, SECRET_KEY=SECRET_KEY)

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
    
#insert_topics()

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
            else:
                return render_template('index.html')
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

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
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
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
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
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
                    send_notifications(user_id,payload['id'],'You has been verified as an expert','#')
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
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for('index'))
    
@app.route('/decline_expert', methods=['POST'])
def decline_expert():
    id = request.form['id']
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
                    db.expert_datas.delete_one({'_id':ObjectId(id)})
                    send_notifications(user_id,payload['id'],'Your request or expert verification has been declined by admin. Please check your data and try to submit it again.','#')
                    return jsonify({
                        'result':'success',
                        'msg':'User '+user['username']+' request has been declined'
                    })
                else: 
                    return redirect(url_for('index'))
            elif user_info2:
                return redirect(url_for('index'))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
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
            else:
                return redirect(url_for("index"))
            
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
        return redirect(url_for("index"))
    
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
 
@app.route("/get_notifications", methods=["GET"])
def get_notifications():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user = db.normal_users.find_one({'username':payload['id']})
            user2 = db.expert_users.find_one({'username':payload['id']})
            
            if user:
                count = db.notifications.count_documents({'to_user':str(user['_id']),'status':'unread'})
                notifications = list(db.notifications.find({'to_user':str(user['_id'])},{'_id':False}).sort("date", -1).limit(10))
                db.notifications.update_many({'to_user':str(user['_id'])},{'$set':{'status':'read'}})
                return jsonify({
                    "result": "success",
                    "notifications": notifications,
                    'count':count
                })
            elif user2:
                count = db.notifications.count_documents({'to_user':str(user2['_id']),'status':'unread'})
                notifications = list(db.notifications.find({'to_user':str(user2['_id'])},{'_id':False}).sort("date", -1).limit(10))
                db.notifications.update_many({'to_user':str(user2['_id'])},{'$set':{'status':'read'}})
                return jsonify({
                    "result": "success",
                    "notifications": notifications,
                    'count':count
                })
            else:
                return jsonify({
                    "result": "failed",
                    'count':count
                })
        except jwt.ExpiredSignatureError:
            msg='Your token has expired'
            return redirect(url_for('auth.login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg='There was a problem logging you in'
            return redirect(url_for('auth.login', msg=msg))
    else:
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
    db.notifications.insert_one(doc)
    
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 