from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        email=obj_in.email,
        password=hash_password(obj_in.password),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
