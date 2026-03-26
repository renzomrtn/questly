from fastapi import APIRouter, Depends

from app.core.deps import get_current_player
from app.models.player import Player
from app.services.game import xp_for_level, xp_to_next_level
from pydantic import BaseModel

router = APIRouter(prefix="/progression", tags=["progression"])


class ProgressionInfo(BaseModel):
    level: int
    current_xp: int
    xp_in_current_level: int
    xp_needed_for_next_level: int
    xp_to_next_level: int
    total_xp_earned: int
    progress_percent: float


@router.get("/", response_model=ProgressionInfo)
async def get_progression(player: Player = Depends(get_current_player)):
    level_start = xp_for_level(player.level)
    level_end = xp_for_level(player.level + 1)
    span = level_end - level_start
    xp_in_level = player.current_xp
    needed = xp_to_next_level(player.level, player.current_xp)
    progress = round((xp_in_level / span * 100) if span else 100, 1)

    return ProgressionInfo(
        level=player.level,
        current_xp=player.current_xp,
        xp_in_current_level=xp_in_level,
        xp_needed_for_next_level=span,
        xp_to_next_level=needed,
        total_xp_earned=player.total_xp_earned,
        progress_percent=min(progress, 100.0),
    )