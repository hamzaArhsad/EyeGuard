import secrets
import hashlib
from datetime import datetime
from app.models.authentication import Authentication
from app.services.user_service import UserService
from app.models.user_model import UserRole
from app import db
import os

class AuthService:
    def __init__(self):
        self.user_service = UserService()
        self.token_file = 'local_token.txt'

    def generate_token(self) -> str:
        """Generate a secure random token"""
        return secrets.token_hex(32)

    def hash_token(self, token: str) -> str:
        """Hash a token for storage"""
        return hashlib.sha256(token.encode()).hexdigest()

    def login(self, username: str, password: str, role: str) -> tuple[str | None, str | None]:
        """Authenticate user and generate token"""
        user = self.user_service.get_user_by_username(username)
        
        if not user or not user.verify_password(password):
            return None, "Invalid username or password"
        
        # Verify role
        if role.lower() != user.role.lower():
            return None, "Invalid role for this user"

        # Generate and hash token
        token = self.generate_token()
        hashed_token = self.hash_token(token)

        # Store token in database
        db_token = Authentication(
            user_id=user.id,
            token=hashed_token
        )
        db.session.add(db_token)
        db.session.commit()

        # Store token locally
        self._store_local_token(token)

        return token, None

    def logout(self, token: str):
        """Invalidate token and remove local storage"""
        hashed_token = self.hash_token(token)
        token_record = Authentication.query.filter_by(token=hashed_token, is_valid=True).first()
        
        if token_record:
            token_record.is_valid = False
            db.session.commit()

        # Remove local token
        if os.path.exists(self.token_file):
            os.remove(self.token_file)

    def validate_token(self, token: str) -> bool:
        """Validate a token against database"""
        hashed_token = self.hash_token(token)
        token_record = Authentication.query.filter_by(token=hashed_token, is_valid=True).first()
        return token_record is not None

    def _store_local_token(self, token: str):
        """Store token in local file"""
        with open(self.token_file, 'w') as f:
            f.write(token)

    def get_stored_token(self) -> str | None:
        """Get token from local storage"""
        try:
            with open(self.token_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None 