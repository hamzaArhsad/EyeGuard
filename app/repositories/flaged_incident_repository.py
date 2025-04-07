from app.models.flaged_incident_model import FlagedIncident
from app.repositories.base_repository import BaseRepository
from app import db
from typing import List, Optional

class FlagedIncidentRepository(BaseRepository):
    def __init__(self):
        super().__init__(FlagedIncident)
        self.model = FlagedIncident  # Explicitly set the model

    def get_all_without_path(self) -> List[FlagedIncident]:
        """Get all incidents without path information"""
        return FlagedIncident.query.with_entities(
            FlagedIncident.id,
            FlagedIncident.camera_id,
            FlagedIncident.camera_loc,
            FlagedIncident.confidence,
            FlagedIncident.date_time
        ).all()

    def get_path_by_id(self, incident_id: int) -> Optional[str]:
        """Get the path of a specific incident"""
        result = FlagedIncident.query.with_entities(FlagedIncident.path).filter_by(id=incident_id).first()
        return result[0] if result else None

    def find_by_confidence_threshold(self, threshold: int) -> List[FlagedIncident]:
        """Find all incidents with confidence greater than or equal to threshold"""
        return FlagedIncident.query.filter(FlagedIncident.confidence >= threshold).all()

    def delete(self, incident_id: int) -> bool:
        try:
            incident = self.get_by_id(incident_id)
            if not incident:
                return False
            
            db.session.delete(incident)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e
