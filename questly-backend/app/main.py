from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routers import achievements, auth, players, progression, quests
from app.services.achievement import seed_achievements
from app.database import AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_tables()
    async with AsyncSessionLocal() as db:
        await seed_achievements(db)
    yield
    # Shutdown (nothing to clean up for SQLite)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Questly — gamified productivity API",
    lifespan=lifespan,
)

# CORS — allow Vue dev server and mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://questly-backend-0d8g.onrender.com",  # ← replace Railway URL with this
        "capacitor://localhost",
        "http://localhost",
        "https://localhost",
        "http://localhost:3000",
        "https://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(players.router)
app.include_router(quests.router)
app.include_router(achievements.router)
app.include_router(progression.router)


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok", "app": settings.app_name}