from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
import socket
from models import Person, Game, League

#username = os.environ.get('USER')
#password = os.environ.get('DBPASS')
#tablename= os.environ.get('TABLENAME')
uri = os.environ.get('DATABASE_URL')
uri = uri.split(':')
uri[0] = 'postgresql'
uri = ':'.join(uri)

key = os.environ.get('SECRETKEY')
ip = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = key
app.config["SECRET_KEY"] = key
#app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost/{tablename}'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
# jwt = JWTManager(app)


with app.app_context():
    db.create_all()
