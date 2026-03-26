from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ── Request schemas ─────────────────────────────────────────────────────────

class PlayerRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class PlayerLogin(BaseModel):
    email: EmailStr
    password: str


class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=512)


# ── Response schemas ─────────────────────────────────────────────────────────

class PlayerPublic(BaseModel):
    id: int
    name: str
    email: str
    level: int
    current_xp: int
    total_xp_earned: int
    current_energy: int
    max_energy: int
    quests_completed: int
    streak_days: int
    avatar_url: Optional[str]
    bio: Optional[str]
    joined_at: datetime
    last_active_date: Optional[date]

    model_config = {"from_attributes": True}


class PlayerStats(BaseModel):
    """Summary stats used on the profile screen."""
    level: int
    current_xp: int
    xp_to_next_level: int
    total_xp_earned: int
    current_energy: int
    max_energy: int
    quests_completed: int
    quests_failed: int
    streak_days: int

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    player: PlayerPublic