from flask import Blueprint, request, jsonify
from app.services.camera_service import CameraService
from http import HTTPStatus


camera_bp = Blueprint('cameras', __name__, url_prefix='/api/cameras')
camera_service = CameraService()

@camera_bp.route('/create', methods=['POST'])
def create_camera():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['location', 'rtsp_url', 'id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), HTTPStatus.BAD_REQUEST
    
    try:
        # Check if camera with this ID already exists
        existing_camera = camera_service.get_camera_by_id(data['id'])
        if existing_camera:
            return jsonify({
                'error': f'Camera with ID {data["id"]} already exists'
            }), HTTPStatus.CONFLICT  # 409 Conflict
        
        camera = camera_service.create_camera(
            id=data['id'],
            location=data['location'],
            rtsp_url=data['rtsp_url'],
            status=data.get('status', 'deactive'),
            res_width=data.get('res_width', 1920),
            res_height=data.get('res_height', 1080),
            fps=data.get('fps', 25)
        )
        return jsonify({
            'id': camera.id,
            'location': camera.location,
            'status': camera.status,
            'res_width': camera.res_width,
            'res_height': camera.res_height,
            'fps': camera.fps
        }), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTPStatus.BAD_REQUEST

@camera_bp.route('/get-all', methods=['GET'])
def get_all_cameras():
    cameras = camera_service.get_all_cameras()
    return jsonify([{
        'id': camera.id,
        'location': camera.location,
        'status': camera.status,
        'res_width': camera.res_width,
        'res_height': camera.res_height,
        'fps': camera.fps
    } for camera in cameras]), HTTPStatus.OK

@camera_bp.route('/get-by-id/<camera_id>', methods=['GET'])
def get_camera(camera_id):
    camera = camera_service.get_camera_by_id(camera_id)
    if not camera:
        return jsonify({'error': 'Camera not found'}), HTTPStatus.NOT_FOUND
    
    return jsonify({
        'id': camera.id,
        'location': camera.location,
        'status': camera.status,
        'res_width': camera.res_width,
        'res_height': camera.res_height,
        'fps': camera.fps
    }), HTTPStatus.OK

@camera_bp.route('/delete-by-id/<camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    if camera_service.delete_camera(camera_id):
        return '', HTTPStatus.NO_CONTENT
    return jsonify({'error': 'Camera not found'}), HTTPStatus.NOT_FOUND

@camera_bp.route('/activate-by-id/<camera_id>', methods=['POST'])
def activate_camera(camera_id):
    if camera_service.activate_camera(camera_id):
        return '', HTTPStatus.NO_CONTENT
    return jsonify({'error': 'Camera not found'}), HTTPStatus.NOT_FOUND

@camera_bp.route('/deactivate-by-id/<camera_id>', methods=['POST'])
def deactivate_camera(camera_id):
    if camera_service.deactivate_camera(camera_id):
        return '', HTTPStatus.NO_CONTENT
    return jsonify({'error': 'Camera not found'}), HTTPStatus.NOT_FOUND

@camera_bp.route('/update-by-id/<camera_id>', methods=['PUT'])
def update_camera(camera_id):
    data = request.get_json()
    updated_camera = camera_service.update_camera(camera_id, **data)
    if updated_camera:  
        return jsonify({
            'id': updated_camera.id,
            'location': updated_camera.location,
            'status': updated_camera.status,
            'res_width': updated_camera.res_width,
            'res_height': updated_camera.res_height,
            'fps': updated_camera.fps
        }), HTTPStatus.OK
    return jsonify({'error': 'Camera not found'}), HTTPStatus.NOT_FOUND

