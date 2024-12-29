from flask import Blueprint,render_template,redirect,url_for,request,flash
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from .models import User
from . import db
from sqlalchemy import asc,select,update



auth=Blueprint('auth',__name__)



Email=''
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@auth.route("/authentication")
def authenticate():
    return render_template('login.html')

@auth.route("/verify",methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        v_code=str(request.form.get('V_code'))
        print('this is the email' ,Email)
        user=User.query.filter_by(email=Email).first()
        if user:
           if user.verfication_code == v_code:
              stmt=update(User).where(User.email== Email).values(verification_status=bool(True))
              db.session.execute(stmt)
              db.session.commit()
              login_user(user=user,remember=True)
              if user.account_type == 'Admin':
                return  redirect(url_for('views.admin'))
              else:
                return redirect(url_for('views.teacher'))
           else:
              flash('Incorrect Verification code',category='error')
        else:
            flash("There is no account registered on this account",category='error')
    return render_template('login.html')

@auth.route("/login",methods=['GET','POST'])
def login():
    global Email
    email,password,confirm_password ='','',''
    if request.method == 'POST':
        email=request.form.get('email')
        password =request.form.get('passwd')
        user=User.query.filter_by(email=email).first()
        Email=request.form.get('email')
        if user:
            if user.verification_status == True:
                if user.status == True:
                    if check_password_hash(user.password,password):
                       login_user(user,remember=True)
                       if user.account_type == 'Admin':
                          return  redirect(url_for('views.admin'))
                       else:
                          return redirect(url_for('views.teacher'))
                    else:
                       flash('Incorrect password',category='error')
                else:
                    flash("Your account has been blocked",category='error')
            else:
                flash("Your account isn't verified",category='error')
        else:
            flash("There is no account registered on this account",category='error')
    return render_template("login.html")
    
@auth.route("/signup",methods=['GET','POST'])
def signup():
    username,email,password,confirm_password ='','','',''
   
    if request.method == 'POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password =request.form.get('passwd')
        confirm_password=request.form.get('cpasswd')
        user= User.query.filter_by(email=email).first()
        
        if user:
            flash('The Email already exist',category='error')
            return redirect(url_for('auth.authenticate'))
        elif len(username) < 2:
            flash('User name must be greater than 2 charcters.',category='error')
            return redirect(url_for('auth.authenticate'))
        elif password != confirm_password:
            flash('The passwords are not the same.',category='error')
            return redirect(url_for('auth.authenticate'))
            pass
        elif len(password) < 7:
           flash('The password should be at least 8 characters.',category='error')
           return redirect(url_for('auth.authenticate'))
           
        else:
          new_user=User(email=email,password=generate_password_hash( password, method='pbkdf2:sha256')
                        ,username=username,verification_status=False,account_type='Teacher',status=True)
          db.session.add(new_user)
          db.session.commit()
          return redirect(url_for('auth.authenticate'))
          
    return f'Signed up with username {email,username,password,confirm_password}'
    
 