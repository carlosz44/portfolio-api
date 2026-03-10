import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.work import Work
from app.schemas.work import WorkCreate, WorkRead, WorkUpdate

router = APIRouter(prefix="/work", tags=["work"])


@router.get("/", response_model=list[WorkRead])
def list_work(session: Session = Depends(get_session)):
    statement = select(Work).order_by(Work.start.desc())
    jobs = session.exec(statement).all()
    return [WorkRead.model_validate(j) for j in jobs]


@router.get("/{work_id}", response_model=WorkRead)
def get_work(work_id: uuid.UUID, session: Session = Depends(get_session)):
    job = session.get(Work, work_id)
    if not job:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return job


@router.post("/", response_model=WorkRead, status_code=201)
def create_work(
    body: WorkCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    job = Work.model_validate(body)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@router.patch("/{work_id}", response_model=WorkRead)
def update_work(
    work_id: uuid.UUID,
    body: WorkUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    job = session.get(Work, work_id)
    if not job:
        raise HTTPException(status_code=404, detail="Work experience not found")

    update_data = body.model_dump(exclude_unset=True)
    job.sqlmodel_update(update_data)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@router.delete("/{work_id}", status_code=204)
def delete_work(
    work_id: uuid.UUID,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    job = session.get(Work, work_id)
    if not job:
        raise HTTPException(status_code=404, detail="Work experience not found")

    session.delete(job)
    session.commit()
