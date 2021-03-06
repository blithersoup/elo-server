from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
import socket


username = os.environ.get('USER')
password = os.environ.get('DBPASS')
key = os.environ.get('SECRETKEY')
ip = socket.gethostbyname(socket.gethostname() + ".local")

app = Flask(__name__)
CORS(app)


app.config["JWT_SECRET_KEY"] = key
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
