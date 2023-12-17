from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.secret_key = 'alsdkfja;ksdfjádfa;skdfa;lkdfj;laksdhj;alsdhg;'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanlychuyenbay?charset=utf8mb4" % quote(
    'root')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
login_manager = LoginManager(app)
