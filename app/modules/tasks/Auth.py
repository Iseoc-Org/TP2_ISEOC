from functools import wraps
from flask import request, jsonify
import jwt

def verifyToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is invalid!"}), 403
        return f(*args, **kwargs)
    return decorated

def verifyRole(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing!"}), 403
            try:
                data = jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
                user_role = data['role']  
                if user_role != role:
                    return jsonify({"message": "Permission denied!"}), 403
            except:
                return jsonify({"message": "Token is invalid!"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
