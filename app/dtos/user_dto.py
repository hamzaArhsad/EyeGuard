from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserCreateDTO:
    username: str
    password: str
    role: str = "operator"

@dataclass
class UserResponseDTO:
    id: int
    username: str
    role: str
    created_at: datetime

@dataclass
class UserUpdateDTO:
    username: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None

@dataclass
class UserLoginDTO:
    username: str
    password: str 