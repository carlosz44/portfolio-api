import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.work import Work
from app.schemas.work import WorkRead

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
