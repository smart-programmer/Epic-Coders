from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = 'c9305a6d0899d06a9352c31adf75f8478b'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vvvsdeqbcwyqnw:e92ddeb85c124176843e713e5766ab3bfd0f4bf8fff44f372982d98dea0fb588@ec2-54-243-187-30.compute-1.amazonaws.com:5432/dbnq788gc67rbo"

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = "login"

from EpicCoders import routes



