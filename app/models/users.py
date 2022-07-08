import uuid
from sqlalchemy.dialects.postgresql.base import UUID

from app.db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    hashed_reset_password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    jobs = relationship("Job", back_populates="owner")
