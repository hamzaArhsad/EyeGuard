from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.dtos.user_dto import UserCreateDTO, UserUpdateDTO
from typing import List, Optional
from app import db  # Import db from app package

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, user_dto: UserCreateDTO) -> User:
        user = User(
            username=user_dto.username,
            role=user_dto.role
        )
        user.password = user_dto.password
        return self.repository.create(user)

    def get_all_users(self) -> List[User]:
        return self.repository.get_all()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repository.find_by_username(username)

    def update_user(self, user_id: str, user_dto: UserUpdateDTO) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        if user_dto.username:
            user.username = user_dto.username
        if user_dto.role:
            user.role = user_dto.role
        if user_dto.password:
            user.password = user_dto.password

        return self.repository.update(user)

    def delete_user(self, user_id: str) -> bool:
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            # First, delete related authentication records
            db.session.execute(db.text('DELETE FROM authentications WHERE user_id = :user_id'), {'user_id': user_id})
            
            # Then delete the user
            db.session.delete(user)
            db.session.commit()
            return True
        
        except Exception as e:
            print(f"Error in delete_user service: {str(e)}")
            db.session.rollback()
            raise e
