from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr


# properties required during user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: bool = False


# properties not required during user update
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    reset_password: Optional[str]


class ShowUser(BaseModel):  # new
    id: UUID
    username: str
    email: EmailStr
    is_active: bool

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class EmailSchema(BaseModel):
    email: List[EmailStr]
