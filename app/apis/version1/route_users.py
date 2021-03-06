from typing import List, Any

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.apis.version1.route_login import get_current_user_from_token
from app.crud import users
from app.db.session import get_db
from app.models.users import User
from app.schemas.users import ShowUser, UserReset
from app.schemas.users import UserCreate, UserUpdate
from app.utils import send_email, random_mdp
from app.core.hashing import Hasher

router = APIRouter()


def verify_rest_password(email: str, password: str, db: Session = Depends(get_db)):
    user = users.get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_reset_password):
        return False
    return user


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = users.create(obj_in=user, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    message = random_mdp()
    user_in = UserUpdate(**{"email": user.email, "reset_password": message})
    users.update(db=db, db_obj=user, obj_in=user_in)
    send_email(user.email, message)
    return user


@router.put("/reset")
def verify_password(user: UserReset, db: Session = Depends(get_db)):
    user = verify_rest_password(user.email, user.reset_password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Code not verified")
    user_in = UserUpdate(**{"email": user.email, "is_selected": True})
    users.update(db=db, db_obj=user, obj_in=user_in)
    return user


@router.get("/", response_model=List[ShowUser])
def get_user(db: Session = Depends(get_db)):
    user = users.get_all_user(db=db)
    return user


@router.put("/", response_model=ShowUser)
def update_user(user_in: UserUpdate, db: Session = Depends(get_db)):
    user = users.get_user_by_email(db=db, email=user_in.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    user = users.update(db=db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/delete/{id}", response_model=ShowUser)
def delete_user(
        id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    user = users.remove(db=db, id=id)
    return user


html = """
<p>Hi this test mail, thanks for using Fastapi-mail </p>
"""


@router.post("/email")
async def simple_send(
        email: str,
        db: Session = Depends(get_db),
) -> Any:
    user = users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    message = random_mdp()
    user_in = UserUpdate(**{"email": email, "reset_password": message})

    users.update(db=db, db_obj=user, obj_in=user_in)
    return send_email(email, message)
