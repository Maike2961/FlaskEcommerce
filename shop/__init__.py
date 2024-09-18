from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
login_manage = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mercado.db'
app.config["SECRET_KEY"]= '5b61281ebbac0ab023297a36'

db.init_app(app)
login_manage.init_app(app)
login_manage.login_view = "login"
login_manage.login_message = "Por favor, Faça o login"
login_manage.login_message_category = "info"
bcrypt = Bcrypt(app)

from shop import route
from shop import models
