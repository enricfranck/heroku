from typing import List

from app.core.hashing import Hasher
from app.models.users import User
from app.schemas.users import UserCreate, ShowUser
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    user = User(username=user.username,
                email=user.email,
                hashed_password=Hasher.get_password_hash(user.password),
                is_active=True,
                is_superuser=False
                )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):  # new
    user = db.query(User).filter(User.email == email).first()
    return user


def get_all_user(db: Session) -> List[ShowUser]:  # new
    user = db.query(User).all()
    return user
