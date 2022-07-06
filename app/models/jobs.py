import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Job(Base):
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    company_url = Column(String)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_posted = Column(Date)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(String, ForeignKey("user.id"))
    owner = relationship("User", back_populates="jobs")
