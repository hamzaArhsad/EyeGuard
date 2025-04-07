from app.models.flaged_incident_model import FlagedIncident
from app.repositories.flaged_incident_repository import FlagedIncidentRepository
from app.dtos.flaged_incident_dto import FlagedIncidentCreateDTO, FlagedIncidentResponseDTO
from flask import current_app
import os
from typing import List, Optional
from datetime import datetime
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FlagedIncidentService:
    def __init__(self):
        self.repository = FlagedIncidentRepository()

    def create_incident(self, incident_dto: FlagedIncidentCreateDTO, video_data: bytes) -> FlagedIncidentResponseDTO:
        """Create a new incident and save the video file"""
        try:
            # Create incident in database first to get the ID
            incident = FlagedIncident(
                camera_id=incident_dto.camera_id,
                camera_loc=incident_dto.camera_loc,
                confidence=incident_dto.confidence,
                date_time=incident_dto.date_time or datetime.utcnow(),
                path=''  # Temporary empty path
            )
            created_incident = self.repository.create(incident)
            
            # Generate file path using the incident ID
            filename = f"flaged_incident_{created_incident.id}.mp4"
            relative_path = os.path.join('flaged_incidents', filename)
            full_path = os.path.join(current_app.config['FLAGED_INCIDENTS_DIR'], filename)
            
            # Save the video file
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as f:
                f.write(video_data)
            
            # Update the path in database
            created_incident.path = relative_path
            self.repository.update(created_incident)
            
            return FlagedIncidentResponseDTO.from_model(created_incident)
            
        except Exception as e:
            # Cleanup if anything fails
            if 'created_incident' in locals():
                self.repository.delete(created_incident.id)
            raise e

    def get_all_incidents(self) -> List[FlagedIncidentResponseDTO]:
        """Get all incidents (without path information)"""
        incidents = self.repository.get_all_without_path()
        return [FlagedIncidentResponseDTO.from_model(incident) for incident in incidents]

    def get_incident_video_path(self, incident_id: int) -> Optional[str]:
        """Get the full system path for a video file"""
        relative_path = self.repository.get_path_by_id(incident_id)
        if not relative_path:
            return None
        return os.path.join(current_app.config['FLAGED_INCIDENTS_DIR'], 
                          os.path.basename(relative_path))
    def delete_incident(self, incident_id: int) -> bool:
        """Delete incident from database and remove video file"""
        try:
            # Use repository to get the incident
            incident = self.repository.get_by_id(incident_id)
            if not incident:
                return False

            # Get the full file path before deleting
            filename = os.path.basename(incident.path)
            full_path = os.path.join(current_app.config['FLAGED_INCIDENTS_DIR'], filename)

            # Use repository to delete from database
            success = self.repository.delete(incident_id)
            if not success:
                return False

            # Delete the video file if it exists
            if os.path.exists(full_path):
                os.remove(full_path)

            return True

        except Exception as e:
            print(f"Error deleting incident: {str(e)}")
            raise e

    def get_incidents_sorted_by_date(self, ascending: bool = False) -> List[FlagedIncidentResponseDTO]:
        """Get incidents sorted by date_time"""
        try:
            query = FlagedIncident.query
            if ascending:
                incidents = query.order_by(FlagedIncident.date_time).all()
            else:
                incidents = query.order_by(desc(FlagedIncident.date_time)).all()
            return [FlagedIncidentResponseDTO.from_model(incident) for incident in incidents]
        except Exception as e:
            print(f"Error sorting incidents by date: {str(e)}")
            raise e

    def get_incidents_sorted_by_confidence(self, ascending: bool = False) -> List[FlagedIncidentResponseDTO]:
        """Get incidents sorted by confidence level"""
        try:
            query = FlagedIncident.query
            if ascending:
                incidents = query.order_by(FlagedIncident.confidence).all()
            else:
                incidents = query.order_by(desc(FlagedIncident.confidence)).all()
            return [FlagedIncidentResponseDTO.from_model(incident) for incident in incidents]
        except Exception as e:
            print(f"Error sorting incidents by confidence: {str(e)}")
            raise e

    def get_incidents_sorted_by_camera_id(self, ascending: bool = True) -> List[FlagedIncidentResponseDTO]:
        """Get incidents sorted by camera_id"""
        try:
            query = FlagedIncident.query
            if ascending:
                incidents = query.order_by(FlagedIncident.camera_id).all()
            else:
                incidents = query.order_by(desc(FlagedIncident.camera_id)).all()
            return [FlagedIncidentResponseDTO.from_model(incident) for incident in incidents]
        except Exception as e:
            print(f"Error sorting incidents by camera_id: {str(e)}")
            raise e
