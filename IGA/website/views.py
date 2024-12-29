
from flask import Flask,Blueprint,render_template,request,jsonify,current_app
import os
from flask_login import LoginManager
from flask_login import login_required,current_user
from . import allowed_file,folder_config
from sqlalchemy.exc import SQLAlchemyError
from . import db
import json
import random
from .models import User,Files
from .mailer import send_email
from sqlalchemy import select,and_,or_,desc,create_engine,asc,update
from werkzeug.security import generate_password_hash ,check_password_hash


myDB=[
       {'level':'1','lesson':'Biology','title':"Biology S1"} ,
       {'level':'1','lesson':'Chemistry','title':"Chemistry S1"},
       {'level':'2','lesson':'Biology','title':"Biology S2"},
       {'level':'2','lesson':'Chemistry','title':"Chemistry S2"},
       {'level':'3','lesson':'Biology','title':"Biology S3"} ,
       {'level':'3','lesson':'Chemistry','title':"Chemistry S3"},
       {'level':'4','lesson':'Biology','title':"Biology S4"},
       {'level':'4','lesson':'Chemistry','title':"Chemistry S4"},
       {'level':'2','lesson':'Maths','title':"Maths S2"},
       {'level':'2','lesson':'Physics','title':"Physics S2"},
       {'level':'3','lesson':'Maths','title':"Maths S3"} ,
       {'level':'3','lesson':'Physics','title':"Physics S3"},
       {'level':'4','lesson':'Maths','title':"Maths S4"},
       {'level':'4','lesson':'Physics','title':"Physics S4"}
    ]
      
views = Blueprint('views',__name__)



def generate_random_number(digits):
    if digits < 1:
        raise ValueError("Number of digits must be at least 1")
    lower_bound = 10**(digits - 1)
    upper_bound = 10**digits - 1
    random_number= random.randint(lower_bound, upper_bound)
    return random_number

@views.route('/')
def home():
    return render_template('index.html',user=current_user)

@views.route('/teacher')
def  teacher():
    return render_template('tris.html',user=current_user)

@views.route('/admin')
def admin():
    return render_template('admin.html',user=current_user)

@views.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # Get JSON data from request
    level = (data.get('name', 'Unknown'))
    lesson =(data.get('lesson', 'Unknown') ) # Extract 'name' field
   
    # Process the data and prepare a response
    print(level," ",lesson)
    
    myresponses={'message':''}
    myresponse=''
    for book in myDB:
        if lesson != None and level != None:
           if book['level'] == level and book['lesson'] == lesson:
              myresponse=myresponse + " " +book['title']+"\n"
        elif level is not None and  lesson == None:
             if book['level'] == level :
              myresponse=myresponse + " " +book['title']+"\n"
           
        elif lesson is not None and level == None:
             if book['lesson'] == lesson:
              myresponse=myresponse + " " +book['title']+"\n"
    
    response = {'message': f'Hello, {level}! Do you study {lesson}'}
    print(myresponse)
    myresponses['message']=myresponse
    return jsonify(myresponses)

@views.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)  # Save the file to the server
        return jsonify({'message': f'File successfully uploaded {filepath}', 'filepath': filepath}), 200
    
    
    return jsonify({'error': 'File type not allowed'}), 400

@views.route('/request',methods=['POST','GET'])
def requests():
    try:
        stmt=select(User).where(
            User.verification_status == False).order_by(desc(User.id))
        with current_app.app_context():
             results=db.session.execute(stmt).scalars().all()
             if len(results) >0:
                 return jsonify([User.to_dict() for User in results])
             else:
                 response = {'message':'No User Requests '}
                 return jsonify(response)
    except SQLAlchemyError  as e :
        return jsonify({'message':str(e)}),500

@views.route('/users',methods=['POST','GET'])
def Users():
    try:
        stmt=select(User).where(
            User.verification_status == True).order_by(asc(User.id))
        with current_app.app_context():
             results=db.session.execute(stmt).scalars().all()
             if len(results) >0:
                 return jsonify([User.to_dict() for User in results])
             else:
                 response = {'message':'No Users Yet  '}
                 return jsonify(response)
    except SQLAlchemyError  as e :
        return jsonify({'message':str(e)}),500

@views.route('/content',methods=['POST','GET'])
def content():
    try:
        stmt=select(Files).order_by(desc(Files.document_id))
        with current_app.app_context():
             results=db.session.execute(stmt).scalars().all()
             if len(results) >0:
                 return jsonify([Files.to_dict() for Files in results])
             else:
                 response = {'message':'No Documents Uploaded Yet  '}
                 return jsonify(response)
    except SQLAlchemyError  as e :
        return jsonify({'message':str(e)}),500
    
@views.route('/approve',methods=['POST','GET'])
def approve():
    data=request.get_json()
    email=data.get('email','unknown')
    user=User.query.filter_by(email=email).first()
    recipient=[email]
    print(recipient)
    if user:
        if user.verification_status == False :
            v_code=generate_random_number(6)
            body="Your verification code for your IGA account is: "+ str(v_code)
            email_status=send_email(subject="Verification code from IGA ELP",
                       recipients=recipient,body=body)
            if email_status[0] == True:
                stmt=update(User).where(User.email== email).values(verfication_code = str(v_code))
                try:
                    db.session.execute(stmt)
                    db.session.commit()
                    return jsonify({'Success': 'Account has been verified'})
                except SQLAlchemyError  as e :
                   return jsonify({'Error':str(e)}),500
            else:
                return jsonify({'Error': f'Code not sent {email_status[1]}'})
        else:
            return jsonify({'Error': 'Account already verified'})
    else:
        return jsonify({'Error': 'Account already verified'})

@views.route('/disapprove',methods=['POST','GET'])
def disapprove():
    data=request.get_json()
    email=data.get('email','unknown')
    user=User.query.filter_by(email=email).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'Success': 'Account has been disapproved'})
        except SQLAlchemyError  as e :
          return jsonify({'Error':str(e)}),500
    else:
        return jsonify({'Error': "Account Doesn't exist"})

@views.route('/block_user',methods=['POST','GET'])
def block_user():
    data=request.get_json()
    email=data.get('email','unknown')
    user=User.query.filter_by(email=email).first()
    if user:
        if user.verification_status == True:
           stmt=update(User).where(User.email == email).values(status = bool(False))
           try:
              db.session.execute(stmt)
              db.session.commit()
              return jsonify({'Block': 'Account has been blocked'})
           except SQLAlchemyError  as e :
               return jsonify({'Error':str(e)}),500
        else:
          return jsonify({'Error': "Account is already blocked from log in"})  
    else:    
        return jsonify({'Error': "Account Doesn't exist"})

@views.route('/activate_user',methods=['POST','GET'])
def activate_user():
    data=request.get_json()
    email=data.get('email','unknown')
    user=User.query.filter_by(email=email).first()
    if user:
        if user.status == False:
           stmt=update(User).where(User.email == email).values(status = bool(True))
           try:
              db.session.execute(stmt)
              db.session.commit()
              return jsonify({'Block': 'Account has been activited'})
           except SQLAlchemyError  as e :
               return jsonify({'Error':str(e)}),500
        else:
          return jsonify({'Error': "Account is already active for log in"})  
    else:    
        return jsonify({'Error': "Account Doesn't exist"})

@views.route('/myposts',methods=['POST','GET'])
def  myposts():
    data=request.get_json()
    email=data.get('email','unknown')
    user=User.query.filter_by(email=email).first()
    if user:
        stmt=select(Files).where(Files.email==email).order_by(desc(Files.dateuploaded))
        with current_app.app_context():
            results=db.session.execute(stmt).scalars().all()
            if len(results) >0:
                return jsonify([Files.to_dict() for User in results])
            else:
                response = {'message':'No Post Yet '}
            return jsonify(response)
    else:    
        return jsonify({'Error': "Account Doesn't exist"})
    
@views.route("change_credentions",methods=['GET','POST'])
def  change_credentions():
    data=request.get_json()
    email=current_user.email
    # email='adelinshimo@gmail.com'
    field=data.get('field_name','unknown')
    value=data.get('field_value','unknown')
    user=User.query.filter_by(email=email).first()
    stmt=''
    print(email)
    if user:
        if user.status == True:
           if field =='password':
               stmt=update(User).where(User.email == email).values(password = generate_password_hash(value, method='pbkdf2:sha256'))
           elif field == 'username':
               stmt=update(User).where(User.email == email).values(username = value)
           elif field == 'email':
               stmt=update(User).where(User.email == email).values(email = value)
           try:
              db.session.execute(stmt)
              db.session.commit()
              return jsonify({'Success': f'{field} has been changed'})
           except SQLAlchemyError  as e :
               return jsonify({'Error':str(e)}),500
        else:
          return jsonify({'Error': f"{field} couldn't be changed"})  
    else:    
        return jsonify({'Error': "Account Doesn't exist"})

@views.route("/mycredentials",methods=['POST','GET'])
def mycredentials():
    data=request.get_json()
    email=data.get('email','unknown')
    
    try:
        stmt=select(User).where(User.email == email)
        with current_app.app_context():
             results=db.session.execute(stmt).scalars().all()
             if len(results) >0:
                 return jsonify([User.to_dict() for User in results])
             else:
                 response = {'Error':'No Such User '}
                 return jsonify(response)
    except SQLAlchemyError  as e :
        return jsonify({'Error':str(e)}),500




