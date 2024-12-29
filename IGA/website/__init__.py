from flask import Flask
import os
from flask_mail import Mail
from os import path
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager


db=SQLAlchemy()
mail = Mail()
DB_NAME="IGA"
UPLOAD_FOLDER = 'uploads'
folder_config=None
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"]="IGA"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    folder_config=app.config['UPLOAD_FOLDER']

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
    app.config['MAIL_PORT'] = 587  # Port number for the SMTP server
    app.config['MAIL_USE_TLS'] = True  # Use TLS for security
    app.config['MAIL_USERNAME'] = 'sezeranoshimo@gmail.com'  # Your email address
    app.config['MAIL_PASSWORD'] = 'ewge ypsk bzwb txaq'  # Your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'sezeranoshimo@gmail.com' # Default sender email address
  # Default sender email address
    
    from .models import User

    # Ensure the upload folder exists
    db.__init__(app)
    mail.__init__(app)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
     
    login_manager =LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import  views
    from .auth import auth
    with app.app_context():
        create_db(app)
    

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    return app
def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print("Database Created !")
    pass