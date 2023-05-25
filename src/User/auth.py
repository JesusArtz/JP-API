from flask import request, jsonify, session
from src.models import Usuario as UserModel


def login():
    data = request.get_json()
    user = UserModel(data)
    response = user.login()
    return jsonify(response)

def register():
    data = request.get_json()
    user = UserModel(data)
    response = user.register()
    return jsonify(response)