import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.project import Project, ProjectType
from app.schemas.project import ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=dict[str, list[ProjectRead]])
def list_projects(
    type: ProjectType | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Project).order_by(Project.year.desc())

    if type:
        statement = statement.where(Project.type == type)
        projects = session.exec(statement).all()
        return {type.value: [ProjectRead.model_validate(p) for p in projects]}

    projects = session.exec(statement).all()
    grouped: dict[str, list[ProjectRead]] = {}
    for p in projects:
        key = p.type.value
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(ProjectRead.model_validate(p))
    return grouped


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: uuid.UUID, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
