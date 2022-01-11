from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import socket
from flask_cors import CORS

username = os.environ.get('USER')
password = os.environ.get('DBPASS')
ip = socket.gethostbyname(socket.gethostname() + ".local")
password = "yahoo57Tiss!"

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
