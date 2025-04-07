from app import db
from app.models.base_model import BaseModel
from sqlalchemy.dialects.postgresql import TEXT
from enum import Enum

class CameraStatus(str, Enum):
    ACTIVE = "active"
    DEACTIVE = "deactive"

class Camera(BaseModel):
    __tablename__ = 'cameras'

    id = db.Column(db.String(36), primary_key=True)  # User-set ID
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), nullable=False, default=CameraStatus.DEACTIVE.value)
    res_width = db.Column(db.Integer, nullable=False,default=1920)
    res_height = db.Column(db.Integer, nullable=False,default=1080)
    fps = db.Column(db.Integer, nullable=False,default=25)
    rtsp_url = db.Column(db.String(512), nullable=False, unique=True)

    def __repr__(self):
        return f"<Camera {self.id} at {self.location}>"
