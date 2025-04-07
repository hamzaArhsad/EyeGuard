from flask import Blueprint, request, jsonify, send_file
from app.services.flaged_incident_service import FlagedIncidentService
from app.dtos.flaged_incident_dto import FlagedIncidentCreateDTO
from datetime import datetime

flaged_incident_bp = Blueprint('flaged_incidents', __name__, url_prefix='/api/flaged-incidents')
incident_service = FlagedIncidentService()

@flaged_incident_bp.route('/create', methods=['POST'])
def create_incident():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
            
        video_file = request.files['video']
        if video_file.filename == '':
            return jsonify({'error': 'No selected video file'}), 400

        data = request.form
        incident_dto = FlagedIncidentCreateDTO(
            camera_id=data['camera_id'],
            camera_loc=data['camera_loc'],
            confidence=int(data['confidence']),
            path='',  # Will be set by service
            date_time=datetime.fromisoformat(data['date_time']) if 'date_time' in data else None
        )
        
        result = incident_service.create_incident(incident_dto, video_file.read())
        return jsonify(result.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flaged_incident_bp.route('/get-all', methods=['GET'])
def get_all_incidents():
    """Get all incidents metadata (without video paths)"""
    try:
        incidents = incident_service.get_all_incidents()
        return jsonify([incident.to_dict() for incident in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flaged_incident_bp.route('/get-incident-video/<incident_id>', methods=['GET'])
def get_incident_video(incident_id):
    """Stream the video file for a specific incident"""
    try:
        video_path = incident_service.get_incident_video_path(incident_id)
        if not video_path:
            return jsonify({'error': 'Video not found'}), 404
            
        return send_file(video_path, mimetype='video/mp4')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flaged_incident_bp.route('/delete/<incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """Delete an incident and its video file"""
    try:
        success = incident_service.delete_incident(incident_id)
        if not success:
            return jsonify({'error': 'Incident not found'}), 404
            
        return jsonify({'message': 'Incident and video file deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete incident: {str(e)}'}), 500

@flaged_incident_bp.route('/incidents/sort/date', methods=['GET'])
def get_incidents_sorted_by_date():
    """Get incidents sorted by date"""
    try:
        # Get sort order from query parameter (default to descending/newest first)
        ascending = request.args.get('ascending', 'false').lower() == 'true'
        incidents = incident_service.get_incidents_sorted_by_date(ascending)
        return jsonify([incident.to_dict() for incident in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flaged_incident_bp.route('incidents/sort/confidence', methods=['GET'])
def get_incidents_sorted_by_confidence():
    """Get incidents sorted by confidence level"""
    try:
        # Get sort order from query parameter (default to descending/highest first)
        ascending = request.args.get('ascending', 'false').lower() == 'true'
        incidents = incident_service.get_incidents_sorted_by_confidence(ascending)
        return jsonify([incident.to_dict() for incident in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flaged_incident_bp.route('incidents/sort/camera', methods=['GET'])
def get_incidents_sorted_by_camera():
    """Get incidents sorted by camera_id"""
    try:
        # Get sort order from query parameter (default to ascending)
        ascending = request.args.get('ascending', 'true').lower() == 'true'
        incidents = incident_service.get_incidents_sorted_by_camera_id(ascending)
        return jsonify([incident.to_dict() for incident in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 