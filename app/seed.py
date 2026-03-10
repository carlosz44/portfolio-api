"""Seed the database from a JSON fixture file."""

import json
import sys
from datetime import date
from pathlib import Path

from sqlmodel import Session, select

from app.auth.service import hash_password
from app.database import engine
from app.models.project import Project, ProjectType
from app.models.skill import Skill, SkillType
from app.models.user import User
from app.models.work import Work


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def seed(filepath: str = "seed_data.json"):
    path = Path(filepath)
    if not path.exists():
        print(f"Error: {filepath} not found.")
        print("Create a seed_data.json file with your data. See seed_data.example.json for format.")
        sys.exit(1)

    data = json.loads(path.read_text())

    with Session(engine) as session:
        existing = session.exec(select(User)).first()
        if existing:
            print("Database already seeded. Skipping.")
            return

        # Admin user
        admin_data = data["admin"]
        session.add(User(
            username=admin_data["username"],
            hashed_password=hash_password(admin_data["password"]),
        ))
        print(f"Created admin user: {admin_data['username']}")

        # Projects
        for item in data.get("projects", []):
            session.add(Project(
                title=item["title"],
                description=item["description"],
                link=item["link"],
                year=item["year"],
                type=ProjectType(item["type"]),
            ))
        print(f"Created {len(data.get('projects', []))} projects")

        # Skills
        for item in data.get("skills", []):
            session.add(Skill(
                title=item["title"],
                start=parse_date(item["start"]),
                end=parse_date(item["end"]),
                type=SkillType(item["type"]),
            ))
        print(f"Created {len(data.get('skills', []))} skills")

        # Work
        for item in data.get("work", []):
            session.add(Work(
                company=item["company"],
                role=item["role"],
                description=item["description"],
                start=parse_date(item["start"]),
                end=parse_date(item["end"]),
                location=item["location"],
                tech_stack=item.get("tech_stack", ""),
            ))
        print(f"Created {len(data.get('work', []))} work experiences")

        session.commit()
        print("Seeding complete!")


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "seed_data.json"
    seed(filepath)
