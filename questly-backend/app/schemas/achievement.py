from datetime import datetime

from pydantic import BaseModel

from app.models.achievement import AchievementTrigger


class AchievementPublic(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    trigger: AchievementTrigger
    threshold: int
    xp_bonus: int

    model_config = {"from_attributes": True}


class PlayerAchievementPublic(BaseModel):
    achievement: AchievementPublic
    unlocked_at: datetime

    model_config = {"from_attributes": True}