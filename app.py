import os
from fileinput import filename

from torchvision.models.detection.backbone_utils import mobilenet_backbone
from unicodedata import category

from dlmodel import predict
from flask import Flask, request, redirect, render_template, jsonify, session,g,send_from_directory
from flask_sqlalchemy.model import Model
from datetime import datetime,timedelta
import config
from flask_sqlalchemy import SQLAlchemy
from exts import db,migrate,mail
from models import User,EmailCode,Vegetable,VegetableCategory
import random
import string
from flask_mail import Mail,Message
import commands
from decorators import login_required
import uuid

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate.init_app(app,db)
mail.init_app(app)
app.cli.command('init_category')(commands.init_vegetable_category)

@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User,user_id)
        g.user = user
    else:
        g.user = None
@app.context_processor
def context_processor():
    categories = db.session.scalars(db.select(VegetableCategory)).all()
    return {
        'user':g.user,
        'categories':categories,
    }

@app.route('/')
def index_login():  # put application's code here
    category_id = request.args.get('category')
    if category_id:
        stmt = db.select(Vegetable).where(Vegetable.category_id == category_id)
    else:
        stmt = db.select(Vegetable)
    vegetables = db.session.scalars(stmt.order_by(Vegetable.pub_date.desc())).all()
    return render_template('index.html',vegetables=vegetables,category_id = category_id)

@app.post('/logout')
def logout():
    # session.pop('user_id')
    # session.pop('email')
    # session.pop('username')
    session.clear()
    return redirect('/')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = db.session.scalar(db.select(User).where(User.email == email))
        if email and user.check_password_hash(password):
            session['user_id'] = user.id
            if remember:
                session.permanent = True
            return redirect('/')
        else:
            print('邮箱或密码错误')
            return redirect('login')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        code = request.form.get('code')
        code_model = db.session.scalar(db.select(EmailCode).where(EmailCode.code == code,EmailCode.email == email))
        if not code_model or (datetime.now()-code_model.created_time) >= timedelta(minutes=10):
            return jsonify({"result":False,'message':'请输入正确的验证码！'})
        user = User(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result":True,'message':None})

@app.get('/email/code')
def email_code():
    email = request.args.get('email')
    if not email:
        return jsonify({"result":False,"message":'请传入邮箱'})
    # 生成验证码
    source = string.digits*4
    code = ''.join(random.sample(source,4))
    message = Message(
        subject= '【开朗的网友】注册验证码',
        recipients = [email],
        body= f'【开朗的网友】注册验证码：{code}',
    )
    try:
        mail.send(message)
    except Exception as e:
        return jsonify({"result":False,"message":str(e)})

    code_model = EmailCode(code=code,email=email)
    db.session.add(code_model)
    db.session.commit()
    return jsonify({"result":True,'message':None})

@app.route('/pub',methods=['GET','POST'])
@login_required
def pub():
    if request.method == 'GET':
        categories = db.session.scalars(db.select(VegetableCategory)).all()
        return render_template('pub.html',categories=categories)
    else:
        picture = request.form.get('picture')
        # 其他字段用 request.form
        category_id = request.form.get('category')
        name = request.form.get('name')
        content = request.form.get('content')
        price = request.form.get('price')
        provider = request.form.get('provider')
        mobile = request.form.get('mobile')
        place = request.form.get('place')

        vegetable = Vegetable(
            name=name,
            content=content,
            price=price,
            provider=provider,
            mobile=mobile,
            place=place,
            category_id=category_id,
            picture=picture,
            publish_id = g.user.id
        )
        db.session.add(vegetable)
        db.session.commit()
        return redirect('/')

@app.post('/upload/picture')
def upload_picture():
    picture = request.files.get('picture')
    ext = picture.filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    picture_path = os.path.join(app.config['MEDIA_DIR'], filename)
    picture.save(picture_path)
    category_name = predict(picture_path)
    category = db.session.scalar(db.select(VegetableCategory).where(VegetableCategory.name == category_name))

    return jsonify({"result":True,'filename':filename,'category':{'name':category_name,'id':category.id}})

@app.route('/detail/<int:vegetable_id>')
def detail(vegetable_id):
    vegetable = db.session.get(Vegetable, vegetable_id)
    return render_template('detail.html',vegetable=vegetable,vegetable_id=vegetable_id)
@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(config.MEDIA_DIR, filename)
if __name__ == '__main__':
    app.run(debug=True,port = 5050,host='0.0.0.0')
