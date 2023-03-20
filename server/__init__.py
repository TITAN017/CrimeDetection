from flask import Flask
from flask_executor import Executor
from flask_mail import Mail
from os import path
import tensorflow

global executor,mail
db_name = 'database.db'

detection_model = tensorflow.keras.models.load_model('final1.h5')


def create_app():
    global executor,mail
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abceefjpdsfa'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

    from .views import views

    app.register_blueprint(views)

    executor = Executor(app)
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'madhvesham.teamchimera@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ggsmuutzsrcshyzb'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SUPPRESS_SEND'] = False
    app.testing = False
    mail = Mail(app)
    return app
    
