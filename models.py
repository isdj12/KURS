from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Account(db.Model):  
    __tablename__ = 'account' 

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)  
    password = db.Column(db.String(128), nullable=False)
    pochta = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, login, password, pochta):  
        self.login = login
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.pochta = pochta

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Account {self.login}>'

class Database(db.Model):
    __tablename__ = 'database'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    teg1 = db.Column(db.String(50))
    teg2 = db.Column(db.String(50))
    teg3 = db.Column(db.String(50))
    image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    login = db.Column(db.String(80))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, opis, teg1=None, teg2=None, teg3=None, image=None, user_id=None, login=None, password=None):
        self.name = name
        self.opis = opis
        self.teg1 = teg1
        self.teg2 = teg2
        self.teg3 = teg3
        self.image = image
        self.user_id = user_id
        self.login = login
        if password:
            self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<Database {self.name}>' 