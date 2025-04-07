from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from typing import List, Optional

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    def find_by_username(self, username: str):
        return self.model_class.query.filter_by(username=username).first()
    
    def find_by_role(self, role: str) -> List[User]:
        return User.query.filter_by(role=role).all()
