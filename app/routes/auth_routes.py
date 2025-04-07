from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from http import HTTPStatus
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), HTTPStatus.UNAUTHORIZED

        if not auth_service.validate_token(token):
            return jsonify({'error': 'Token is invalid'}), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'error': 'Username, password, and role are required'}), HTTPStatus.BAD_REQUEST
    
    token, error = auth_service.login(data['username'], data['password'], data['role'])
    
    if error:
        return jsonify({'error': error}), HTTPStatus.UNAUTHORIZED
    
    return jsonify({'token': token}), HTTPStatus.OK

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    token = request.headers.get('Authorization')
    auth_service.logout(token)
    return '', HTTPStatus.NO_CONTENT

@auth_bp.route('/validate', methods=['GET'])
@token_required
def validate_token():
    return jsonify({'message': 'Token is valid'}), HTTPStatus.OK 