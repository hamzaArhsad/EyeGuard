from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class FlagedIncidentCreateDTO:
    camera_id: str
    camera_loc: str
    confidence: int
    path: str
    date_time: Optional[datetime] = None

@dataclass
class FlagedIncidentResponseDTO:
    id: int
    camera_id: str
    camera_loc: str
    confidence: int
    date_time: datetime

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            camera_id=model.camera_id,
            camera_loc=model.camera_loc,
            confidence=model.confidence,
            date_time=model.date_time
        )

    def to_dict(self):
        """Convert DTO to dictionary"""
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'camera_loc': self.camera_loc,
            'confidence': self.confidence,
            'date_time': self.date_time.isoformat() if self.date_time else None
        }
