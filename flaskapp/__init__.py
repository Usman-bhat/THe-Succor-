from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/the_succor"
app.config['SECRET_KEY'] = 'super_secret_key'
# app.secret_key = 'super_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
with open('config.json', 'r') as c:
    params = json.load(c)["params"]


from flaskapp import routs