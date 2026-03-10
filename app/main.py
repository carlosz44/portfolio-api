from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.auth.router import router as auth_router
from app.config import settings
from app.routers import projects, skills, work

app = FastAPI(
    title="Portfolio API",
    description="Personal portfolio CMS API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

if settings.environment == "production":
    allowed_hosts = [origin.replace("https://", "").replace("http://", "")
                     for origin in settings.cors_origins]
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


app.include_router(auth_router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(work.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
