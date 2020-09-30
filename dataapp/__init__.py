from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# package wide global variable
nyse_stats = []
beer_stats = []

app = Flask(__name__)
app.secret_key = "ghost1007"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/data_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_JSONEDITOR'] = True
app.config['CELERY_BROKER_URL'] = 'amqp://user:password@rabbitmq:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'db+mysql://test:test@db/data_app'


app.wsgi_app = ProxyFix(app.wsgi_app)

bcrypt = Bcrypt(app)

db = None
try:
    
    db = SQLAlchemy(app)
    print("Db created.")
except Exception as e:
        print(e)
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
