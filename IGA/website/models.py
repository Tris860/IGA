from flask_login import UserMixin
from . import db
from sqlalchemy import func

class User(db.Model,UserMixin):
    __tablename__='User'
    id =db.Column(db.Integer,primary_key = True,autoincrement=True)
    email=db.Column(db.String(150),unique =True)
    password=db.Column(db.String(150))
    username=db.Column(db.String(150))
    account_type=db.Column(db.String(150))
    verfication_code=db.Column(db.String(150),nullable=True)
    verification_status=db.Column(db.Boolean)
    status=db.Column(db.Boolean)
    posts=db.relationship('Files',backref='author',lazy=True)
    def __repr__(self): return f'<User {self.username}>'
    def to_dict(self): 
        return { 
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'username': self.username, 
            'account_type': self.account_type,
            'verfication_code': self.verfication_code, 
            'verification_status': self.verification_status,
            'status':self.status
              }
    pass

class Files(db.Model):
    __tablename__= 'posts'
    document_id=db.Column(db.Integer,primary_key = True,autoincrement=True)
    email=db.Column(db.String(150), db.ForeignKey('User.email'), nullable=False)
    title=db.Column(db.String(1000),nullable=False)
    link=db.Column(db.String(1000),nullable=False)
    level=db.Column(db.String(150),nullable=False)
    lesson=db.Column(db.String(150),nullable=False)
    dateuploaded=db.Column(db.DateTime,server_default = func.now())
    status=db.Column(db.Boolean,nullable=False)
    def __repr__(self): return f'<User {self.title}>'
    def to_dict(self): 
        return { 
            'id':self.document_id,
            'email':self.email,
            'title':self.title,
            'link':self.link,
            'level':self.level, 
            'lesson':self.lesson,
              }

    