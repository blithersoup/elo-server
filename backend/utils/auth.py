from models import Person
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from flask import request, jsonify


def Login():
    username = request.json["username"]
    password = request.json["passwd"]
    
    password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

    user = Person.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401



    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)