from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.deps import get_current_player
from app.database import get_db
from app.models.achievement import PlayerAchievement
from app.models.player import Player
from app.schemas.achievement import PlayerAchievementPublic
from app.schemas.player import PlayerPublic, PlayerStats, PlayerUpdate
from app.services.game import calculate_level_from_total_xp, xp_to_next_level

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/me", response_model=PlayerPublic)
async def get_profile(player: Player = Depends(get_current_player)):
    return player


@router.patch("/me", response_model=PlayerPublic)
async def update_profile(
    payload: PlayerUpdate,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(player, field, value)
    await db.commit()
    await db.refresh(player)
    return player


@router.get("/me/stats", response_model=PlayerStats)
async def get_stats(player: Player = Depends(get_current_player)):
    xp_needed = xp_to_next_level(player.level, player.current_xp)
    return PlayerStats(
        level=player.level,
        current_xp=player.current_xp,
        xp_to_next_level=xp_needed,
        total_xp_earned=player.total_xp_earned,
        current_energy=player.current_energy,
        max_energy=player.max_energy,
        quests_completed=player.quests_completed,
        quests_failed=player.quests_failed,
        streak_days=player.streak_days,
    )


@router.get("/me/achievements", response_model=list[PlayerAchievementPublic])
async def get_my_achievements(
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PlayerAchievement)
        .where(PlayerAchievement.player_id == player.id)
        .options(selectinload(PlayerAchievement.achievement))
        .order_by(PlayerAchievement.unlocked_at.desc())
    )
    return result.scalars().all()