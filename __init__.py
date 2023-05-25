from flask import Flask
from uuid import uuid4
from functools import wraps
from flask import request, jsonify
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid4())

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # If method is GET, get the token from the header, else, get it from the body

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'Token is missing!'})

        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=["HS256"])

        if not data:
            return jsonify({'message': 'Token is invalid!'})


        return f(*args, **kwargs)

    return decorated