from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.quest import Difficulty, Priority, QuestStatus


# ── Request schemas ─────────────────────────────────────────────────────────

class QuestCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None
    difficulty: Difficulty = Difficulty.medium
    priority: Priority = Priority.medium
    # xp_reward and energy_cost are auto-derived from difficulty
    # but can be optionally overridden
    xp_reward: Optional[int] = Field(None, ge=1)
    energy_cost: Optional[int] = Field(None, ge=1)


class QuestUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None
    difficulty: Optional[Difficulty] = None
    priority: Optional[Priority] = None
    status: Optional[QuestStatus] = None


# ── Response schemas ─────────────────────────────────────────────────────────

class QuestPublic(BaseModel):
    id: int
    player_id: int
    name: str
    description: Optional[str]
    due_date: Optional[date]
    difficulty: Difficulty
    priority: Priority
    status: QuestStatus
    xp_reward: int
    energy_cost: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuestCompleteResponse(BaseModel):
    quest: QuestPublic
    xp_gained: int
    new_xp: int
    leveled_up: bool
    new_level: int
    achievements_unlocked: list[str] = []