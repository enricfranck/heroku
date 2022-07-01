from app.crud.users import create_new_user
from app.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from app.schemas.users import ShowUser
from app.schemas.users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
