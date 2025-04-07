from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.dtos.user_dto import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from http import HTTPStatus

user_bp = Blueprint('users', __name__, url_prefix='/api/users')
user_service = UserService()

@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    
    try:
        # Check if user with this username already exists
        existing_user = user_service.get_user_by_username(data['username'])
        if existing_user:
            return jsonify({
                'error': f'Username {data["username"]} is already taken'
            }), HTTPStatus.CONFLICT  # 409 Conflict

        user_dto = UserCreateDTO(
            username=data['username'],
            password=data['password'],
            role=data.get('role', 'operator')
        )
        
        user = user_service.create_user(user_dto)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'created_at': user.created_at
        }), HTTPStatus.CREATED
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@user_bp.route('/get-all', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'created_at': user.created_at
    } for user in users]), HTTPStatus.OK

@user_bp.route('/get-by-id/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'created_at': user.created_at
    }), HTTPStatus.OK

@user_bp.route('/update-by-id/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    try:
        # If username is being updated, check if it's already taken by another user
        if 'username' in data:
            existing_user = user_service.get_user_by_username(data['username'])
            if existing_user and str(existing_user.id) != user_id:
                return jsonify({
                    'error': f'Username {data["username"]} is already taken'
                }), HTTPStatus.CONFLICT

        user_dto = UserUpdateDTO(
            username=data.get('username'),
            role=data.get('role'),
            password=data.get('password')
        )
        
        if user_service.update_user(user_id, user_dto):
            return '', HTTPStatus.NO_CONTENT
        return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@user_bp.route('/delete-by-id/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # First check if user exists
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND

        # Add logging to help debug
        print(f"Attempting to delete user with ID: {user_id}")
        
        # Try to delete the user
        success = user_service.delete_user(user_id)
        if success:
            print(f"Successfully deleted user with ID: {user_id}")
            return jsonify({'message': 'User deleted successfully'}), HTTPStatus.OK
        else:
            print(f"Failed to delete user with ID: {user_id}")
            return jsonify({'error': 'Failed to delete user'}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
