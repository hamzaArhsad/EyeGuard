from app.repositories.base_repository import BaseRepository
from app.models.camera_model import Camera
from typing import List
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CameraRepository(BaseRepository[Camera]):
    def __init__(self):
        super().__init__(Camera)
    
    # Camera-specific repository methods can be added here
    def find_by_location(self, location: str) -> List[Camera]:
        return Camera.query.filter_by(location=location).all()
    
    def find_active_cameras(self) -> List[Camera]:
        return Camera.query.filter_by(status='active').all()
    
    def find_deactive_cameras(self) -> List[Camera]:
        return Camera.query.filter_by(status='deactive').all()

    

