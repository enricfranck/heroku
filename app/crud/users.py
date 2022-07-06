import os
import uuid
from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder

from app.core.hashing import Hasher
from app.models.users import User
from app.schemas.users import UserCreate, ShowUser, UserUpdate
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase


class CRUDUsers(CRUDBase[User, UserCreate, UserUpdate]):

    def create(self, obj_in: UserCreate, db: Session) -> User:
        user = User(
            id=str(uuid.uuid4()),
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=Hasher.get_password_hash(obj_in.password),
            is_active=True,
            is_superuser=obj_in.is_superuser
                    )
        obj_in_data = jsonable_encoder(user)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_supper_admin(self, user: UserCreate, db: Session):
        user = User(
                    id=str(uuid.uuid4()),
                    username=user.username,
                    email=user.email,
                    hashed_password=Hasher.get_password_hash(user.password),
                    is_active=True,
                    is_superuser=True
                    )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, email: str, db: Session):  # new
        user = db.query(User).filter(User.email == email).first()
        return user

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = Hasher.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_all_user(self, db: Session) -> List[ShowUser]:  # new
        user = db.query(User).all()
        return user


users = CRUDUsers(User)
