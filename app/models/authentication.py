from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class Authentication(BaseModel):  # Changed from Token to Authentication
    __tablename__ = 'authentications'  # Changed from tokens to authentications

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_valid = db.Column(db.Boolean, default=True)

    # Relationship with User
    user = db.relationship('User', backref=db.backref('authentications', lazy=True)) 