from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_player
from app.database import get_db
from app.models.achievement import AchievementTrigger
from app.models.player import Player
from app.models.quest import Difficulty, Quest, QuestStatus
from app.schemas.quest import QuestCompleteResponse, QuestCreate, QuestPublic, QuestUpdate
from app.services.achievement import check_and_award_achievements
from app.services.game import (
    calculate_level_from_total_xp,
    default_energy_cost,
    default_xp,
    regenerate_energy,
    update_streak,
)

router = APIRouter(prefix="/quests", tags=["quests"])


# Helpers

def _get_quest_or_404(quest: Quest | None, player_id: int) -> Quest:
    if not quest or quest.player_id != player_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quest not found")
    return quest


# CRUD

@router.post("/", response_model=QuestPublic, status_code=status.HTTP_201_CREATED)
async def create_quest(
    payload: QuestCreate,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    # Regenerate energy at the start of each interaction
    regenerate_energy(player)

    xp = payload.xp_reward or default_xp(payload.difficulty)
    energy = payload.energy_cost or default_energy_cost(payload.difficulty)

    quest = Quest(
        player_id=player.id,
        name=payload.name,
        description=payload.description,
        due_date=payload.due_date,
        difficulty=payload.difficulty,
        priority=payload.priority,
        xp_reward=xp,
        energy_cost=energy,
    )
    db.add(quest)
    await db.commit()
    await db.refresh(quest)
    return quest


@router.get("/", response_model=list[QuestPublic])
async def list_quests(
    status_filter: QuestStatus | None = Query(None, alias="status"),
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    regenerate_energy(player)
    await db.commit()

    q = select(Quest).where(Quest.player_id == player.id)
    if status_filter:
        q = q.where(Quest.status == status_filter)
    q = q.order_by(Quest.created_at.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{quest_id}", response_model=QuestPublic)
async def get_quest(
    quest_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    return _get_quest_or_404(result.scalar_one_or_none(), player.id)


@router.patch("/{quest_id}", response_model=QuestPublic)
async def update_quest(
    quest_id: int,
    payload: QuestUpdate,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = _get_quest_or_404(result.scalar_one_or_none(), player.id)

    if quest.status == QuestStatus.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot edit a completed quest",
        )

    updates = payload.model_dump(exclude_unset=True)

    # If difficulty is changing, recalculate defaults (unless explicit xp/energy set)
    new_difficulty = updates.get("difficulty")
    if new_difficulty and new_difficulty != quest.difficulty:
        quest.xp_reward = default_xp(new_difficulty)
        quest.energy_cost = default_energy_cost(new_difficulty)

    # Handle status transitions
    new_status = updates.pop("status", None)
    if new_status:
        _apply_status_transition(quest, new_status)

    for field, value in updates.items():
        setattr(quest, field, value)

    await db.commit()
    await db.refresh(quest)
    return quest


@router.delete("/{quest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quest(
    quest_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = _get_quest_or_404(result.scalar_one_or_none(), player.id)

    if quest.status == QuestStatus.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a completed quest",
        )
    await db.delete(quest)
    await db.commit()


# Quest actions

@router.post("/{quest_id}/start", response_model=QuestPublic)
async def start_quest(
    quest_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    """Spend energy and mark quest as in_progress."""
    regenerate_energy(player)

    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = _get_quest_or_404(result.scalar_one_or_none(), player.id)

    if quest.status != QuestStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quest is already {quest.status.value}",
        )

    if player.current_energy < quest.energy_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Not enough energy. You need {quest.energy_cost}, "
                f"You have {player.current_energy}. Energy refills daily."
            ),
        )

    player.current_energy -= quest.energy_cost
    quest.status = QuestStatus.in_progress
    quest.started_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(quest)
    return quest


@router.post("/{quest_id}/complete", response_model=QuestCompleteResponse)
async def complete_quest(
    quest_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    """Award XP, check level-up, check achievements."""
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = _get_quest_or_404(result.scalar_one_or_none(), player.id)

    if quest.status not in (QuestStatus.pending, QuestStatus.in_progress):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quest cannot be completed (status: {quest.status.value})",
        )

    # If it was never started, deduct energy now
    if quest.status == QuestStatus.pending:
        regenerate_energy(player)
        if player.current_energy < quest.energy_cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Not enough energy. You need {quest.energy_cost}, "
                    f"You have {player.current_energy}."
                ),
            )
        player.current_energy -= quest.energy_cost

    xp_gained = quest.xp_reward
    old_level = player.level

    # Update XP
    player.total_xp_earned += xp_gained
    player.current_xp += xp_gained
    player.quests_completed += 1

    # Recalculate level
    new_level, xp_in_level = calculate_level_from_total_xp(player.total_xp_earned)
    player.level = new_level
    player.current_xp = xp_in_level

    leveled_up = new_level > old_level

    # Update streak
    update_streak(player)

    # Mark quest complete
    quest.status = QuestStatus.completed
    quest.completed_at = datetime.now(timezone.utc)

    # Flush so achievement service sees updated player state
    await db.flush()

    # Check achievements
    newly_unlocked = []
    for trigger in (
        AchievementTrigger.quest_completed,
        AchievementTrigger.xp_earned,
        AchievementTrigger.streak_reached,
    ):
        unlocked = await check_and_award_achievements(player, db, trigger)
        newly_unlocked.extend(unlocked)

    if leveled_up:
        unlocked = await check_and_award_achievements(player, db, AchievementTrigger.level_reached)
        newly_unlocked.extend(unlocked)

    await db.commit()
    await db.refresh(quest)

    return QuestCompleteResponse(
        quest=QuestPublic.model_validate(quest),
        xp_gained=xp_gained,
        new_xp=player.current_xp,
        leveled_up=leveled_up,
        new_level=player.level,
        achievements_unlocked=[a.name for a in newly_unlocked],
    )


@router.post("/{quest_id}/abandon", response_model=QuestPublic)
async def abandon_quest(
    quest_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = _get_quest_or_404(result.scalar_one_or_none(), player.id)

    if quest.status not in (QuestStatus.pending, QuestStatus.in_progress):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending or in-progress quests can be abandoned",
        )

    quest.status = QuestStatus.abandoned
    await db.commit()
    await db.refresh(quest)
    return quest


# Internal

def _apply_status_transition(quest: Quest, new_status: QuestStatus) -> None:
    now = datetime.now(timezone.utc)
    if new_status == QuestStatus.in_progress and quest.status == QuestStatus.pending:
        quest.started_at = now
    elif new_status == QuestStatus.completed:
        quest.completed_at = now
    quest.status = new_status