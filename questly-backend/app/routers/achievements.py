from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_player
from app.database import get_db
from app.models.achievement import Achievement
from app.models.player import Player
from app.schemas.achievement import AchievementPublic

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=list[AchievementPublic])
async def list_all_achievements(
    db: AsyncSession = Depends(get_db),
    _player: Player = Depends(get_current_player),  # require auth
):
    """Return the full catalogue of achievements (regardless of unlock status)."""
    result = await db.execute(
        select(Achievement)
        .where(Achievement.is_active == True)  # noqa: E712
        .order_by(Achievement.trigger, Achievement.threshold)
    )
    return result.scalars().all()