from typing import List

from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from app.apis.version1.route_login import get_current_user_from_token
from app.crud import users
from app.db.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.schemas.users import ShowUser, EmailSchema
from app.schemas.users import UserCreate
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.users import User

router = APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = users.create(obj_in=user, db=db)
    return user


@router.get("/", response_model=List[ShowUser])
def get_user(db: Session = Depends(get_db)):
    user = users.get_all_user(db=db)
    return user


@router.delete("/delete/{id}", response_model=ShowUser)
def delete_user(
        id:str,
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
async def send_email(
        email: EmailSchema
) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype="html"
    )
    fm = FastMail(settings.conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
