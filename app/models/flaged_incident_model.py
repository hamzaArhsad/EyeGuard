from app import db
from datetime import datetime
class FlagedIncident(db.Model):
    __tablename__ = 'flaged_incidents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_id = db.Column(db.String(36), db.ForeignKey('cameras.id'), nullable=False)
    camera_loc = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    confidence = db.Column(db.Integer, nullable=False)  # Stores percentage (0-100)
    path = db.Column(db.String(512), nullable=False)  # Path to video clip

    # Relationship with Camera model
    camera = db.relationship('Camera', backref=db.backref('flaged_incidents', lazy=True))

    def __init__(self, camera_id, camera_loc, confidence, path, date_time=None):
        self.camera_id = camera_id
        self.camera_loc = camera_loc
        self.confidence = confidence
        self.path = path
        self.date_time = date_time or datetime.utcnow()

    def __repr__(self):
        return f'<FlagedIncident {self.id} from camera {self.camera_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'camera_loc': self.camera_loc,
            'date_time': self.date_time.isoformat(),
            'confidence': self.confidence,
            'path': self.path
        } 