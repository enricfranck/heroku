import os

from sqlalchemy.orm import Session

from app.core.hashing import Hasher
from app.crud import users
from app.models.users import User


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = users.get_user_by_email(db=db, email=os.getenv("SUPPER_ADMIN_EMAIL"))
    if not user:
        user_in = User(
            username=os.getenv("SUPPER_ADMIN_EMAIL"),
            email=os.getenv("SUPPER_ADMIN_EMAIL"),
            hashed_password=os.getenv("SUPPER_ADMIN_PASSWORD"),
            is_active=True,
            is_superuser=True
        )
        user = users.create_supper_admin(db=db, user=user_in)  # noqa: F841
