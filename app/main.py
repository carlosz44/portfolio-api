from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.routers import projects, skills, work

app = FastAPI(
    title="Portfolio API",
    description="Personal portfolio CMS API",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(work.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
