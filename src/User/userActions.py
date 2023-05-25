from flask import jsonify, request
from src.models import Usuario as UserModel
from __init__ import token_required

@token_required
def get_user():
    data = request.get_json()
    user = UserModel(data)
    return user.get_user()

@token_required
def get_asesorias():
    data = request.get_json()
    user = UserModel(data)
    return user.get_asesorias()

@token_required
def send_calificacion():
    data = request.get_json()
    user = UserModel(data)
    return user.send_calificacion()

@token_required
def create_asesoria():
    data = request.get_json()
    user = UserModel(data)
    return user.create_asesoria()

@token_required
def get_asesorias():
    print('Entrada a get_asesorias')
    data = request.get_json()
    print("Data recuperada: ", data)
    user = UserModel(data)
    asesorias = user.get_asesorias()
    print("Asesorias: ", asesorias)
    return asesorias

