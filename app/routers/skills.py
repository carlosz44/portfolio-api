import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.skill import Skill, SkillType
from app.schemas.skill import SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/", response_model=dict[str, list[SkillRead]])
def list_skills(
    type: SkillType | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Skill).order_by(Skill.title.asc())

    if type:
        statement = statement.where(Skill.type == type)
        skills = session.exec(statement).all()
        return {type.value: [SkillRead.model_validate(s) for s in skills]}

    skills = session.exec(statement).all()
    grouped: dict[str, list[SkillRead]] = {}
    for s in skills:
        key = s.type.value
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(SkillRead.model_validate(s))
    return grouped


@router.get("/{skill_id}", response_model=SkillRead)
def get_skill(skill_id: uuid.UUID, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill
