import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.models.project import Project, ProjectType
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

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


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(
    body: ProjectCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    project = Project.model_validate(body)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = body.model_dump(exclude_unset=True)
    project.sqlmodel_update(update_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: uuid.UUID,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()
