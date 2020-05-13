from flask import Flask
app = Flask(__name__)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lists.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


from application import views

from application.lists import models
from application.lists import views

from application.auth import models
from application.auth import views

from application.content import models
from application.content import views

from application.genres import models
from application.genres import views

from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except:
    pass


