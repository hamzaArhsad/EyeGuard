from app import db
from typing import TypeVar, Generic, List, Optional, Type

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def create(self, entity: T) -> T:
        db.session.add(entity)
        db.session.commit()
        return entity

    def get_by_id(self, id: str) -> Optional[T]:
        return self.model_class.query.get(id)

    def get_all(self) -> List[T]:
        return self.model_class.query.all()

    def delete(self, entity: T) -> bool:
        try:
            db.session.delete(entity)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def update(self, entity: T) -> T:
        try:
            db.session.commit()
            return entity
        except Exception:
            db.session.rollback()
            raise 