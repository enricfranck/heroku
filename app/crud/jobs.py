import uuid

from app.models.jobs import Job
from app.schemas.jobs import JobCreate, JobUpdate
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase


class CRUDJobs(CRUDBase[Job, JobCreate, JobUpdate]):
    def create(self, obj_in: JobCreate, db: Session, owner_id: int):
        job_object = Job(**obj_in.dict(), owner_id=owner_id, id=str(uuid.uuid4()))
        db.add(job_object)
        db.commit()
        db.refresh(job_object)
        return job_object

    def retreive_job(self, id: str, db: Session):
        item = db.query(Job).filter(Job.id == id).first()
        return item

    def list_jobs(self, db: Session):  # new
        jobs = db.query(Job).filter(Job.is_active == True).all()
        return jobs

    def delete_job_by_id(self, id: str, db: Session, owner_id):
        existing_job = db.query(Job).filter(Job.id == id)
        if not existing_job.first():
            return 0
        existing_job.delete(synchronize_session=False)
        db.commit()
        return 1

    def search_job(self, query: str, db: Session):
        jobs = db.query(Job).filter(Job.title.contains(query))
        return jobs


job = CRUDJobs(Job)
