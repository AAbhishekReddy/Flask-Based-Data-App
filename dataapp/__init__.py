from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "ghost1007"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_JSONEDITOR'] = True

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'

from dataapp.account.routes import account
from dataapp.main.routes import main
from dataapp.predictions.routes import predict
from dataapp.errors.handler import errors
from dataapp.api.routes import api_blueprint

app.register_blueprint(account)
app.register_blueprint(main)
app.register_blueprint(predict)
app.register_blueprint(errors)
app.register_blueprint(api_blueprint)

