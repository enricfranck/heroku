from typing import List
from typing import Optional

from app.apis.version1.route_login import get_current_user_from_token
from app.models.users import User
from app.crud import job
from app.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.templating import Jinja2Templates
from app.schemas.jobs import JobCreate, JobUpdate
from app.schemas.jobs import ShowJob
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/create-job/", response_model=ShowJob)
def create_job(
        jobs: JobCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    jobs = job.create(obj_in=jobs, db=db, owner_id=current_user.id)
    return jobs


@router.get(
    "/get/{id}", response_model=ShowJob
)  # if we keep just "{id}" . it would stat catching all routes
def read_job(id: str, db: Session = Depends(get_db)):
    jobs = job.get(id=id, db=db)
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with this id {id} does not exist",
        )
    return jobs


@router.get("/all", response_model=List[ShowJob])
def read_jobs(db: Session = Depends(get_db)):
    jobs = job.get_multi(db=db)
    return jobs


@router.put("/update/{id}", response_model=ShowJob)
def update_job(id: str, obj_in: JobUpdate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user_from_token)):

    jobs = job.get(id=id, db=db)
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {id} not found"
        )
    if jobs.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    jobs = job.update(db=db, db_obj=jobs, obj_in=obj_in)
    return jobs


@router.delete("/delete/{id}")
def delete_job(
        id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    jobs = job.get(id=id, db=db)
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {id} not found"
        )
    if jobs.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    jobs = job.remove(db=db, id=id)
    return jobs


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    jobs = job.search_job(term, db=db)
    job_titles = []
    for item_job in jobs:
        job_titles.append(item_job.title)
    return job_titles
