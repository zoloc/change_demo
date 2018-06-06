from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100),nullable=False)

class Impact_list(db.Model):
    __tablename__ = 'impact_list'
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    change_number = db.Column(db.Text)
    cfg_of_change_authority = db.Column(db.Text)
    change_type = db.Column(db.Text)
    pn_bef = db.Column(db.Text)
    edition_bef = db.Column(db.Text)
    quantity_bef = db.Column(db.Integer)
    effectivity_bef = db.Column(db.Integer)
    pn_after = db.Column(db.Text)
    edition_aft = db.Column(db.Text)
    quantity_aft = db.Column(db.Text)
    effectivity_aft = db.Column(db.Text)
    edz = db.Column(db.Integer)

class Hi_dm_list(db.Model):
    __tablename__ = 'hi_dm_list'
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edz = db.Column(db.Integer, nullable=False)
    dci = db.Column(db.String(50),nullable=False)
    AC103_pn = db.Column(db.String(20))
    AC104_pn = db.Column(db.String(20))

db.create_all()