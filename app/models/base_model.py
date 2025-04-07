from app import db
from datetime import datetime, UTC
class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))