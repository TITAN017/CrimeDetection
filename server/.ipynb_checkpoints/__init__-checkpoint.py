from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import tensorflow

db = SQLAlchemy()
db_name = 'database.db'

detection_model = tensorflow.keras.models.load_model('final.h5')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abceefjpdsfa'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views)

    create_db(app)

    return app

def create_db(app):
    if not path.exists('/web' + db_name):
        with app.app_context():
            db.create_all()
    
