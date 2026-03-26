"""
Achievement evaluation engine.
Call `check_and_award_achievements` after any state-changing action.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.achievement import Achievement, AchievementTrigger, PlayerAchievement
from app.models.player import Player


async def seed_achievements(db: AsyncSession) -> None:
    """Seed default achievements if they don't exist yet."""
    defaults = [
        # Signup
        dict(name="In the Beginning", description="Create your account", icon="⚡",
             trigger=AchievementTrigger.signup, threshold=1, xp_bonus=50),

        # Quest completions
        dict(name="First Blood", description="Complete your first quest", icon="🌟",
             trigger=AchievementTrigger.quest_completed, threshold=1, xp_bonus=25),
        dict(name="Getting Warmed Up", description="Complete 10 quests", icon="🔥",
             trigger=AchievementTrigger.quest_completed, threshold=10, xp_bonus=100),
        dict(name="Adventurer", description="Complete 50 quests", icon="⚔️",
             trigger=AchievementTrigger.quest_completed, threshold=50, xp_bonus=250),
        dict(name="Quest Master", description="Complete 100 quests", icon="👑",
             trigger=AchievementTrigger.quest_completed, threshold=100, xp_bonus=500),

        # Level milestones
        dict(name="Rising Hero", description="Reach level 5", icon="🛡️",
             trigger=AchievementTrigger.level_reached, threshold=5, xp_bonus=100),
        dict(name="Veteran", description="Reach level 10", icon="🏆",
             trigger=AchievementTrigger.level_reached, threshold=10, xp_bonus=250),
        dict(name="Legend", description="Reach level 25", icon="💎",
             trigger=AchievementTrigger.level_reached, threshold=25, xp_bonus=1000),

        # Streaks
        dict(name="Consistent", description="Maintain a 3-day streak", icon="📅",
             trigger=AchievementTrigger.streak_reached, threshold=3, xp_bonus=50),
        dict(name="On a Roll", description="Maintain a 7-day streak", icon="🗓️",
             trigger=AchievementTrigger.streak_reached, threshold=7, xp_bonus=150),
        dict(name="Unstoppable", description="Maintain a 30-day streak", icon="🌊",
             trigger=AchievementTrigger.streak_reached, threshold=30, xp_bonus=500),

        # XP milestones
        dict(name="An Unexpected Journey", description="First sign-up — your journey begins", icon="🧭",
             trigger=AchievementTrigger.signup, threshold=1, xp_bonus=0),
        dict(name="XP Collector", description="Earn 1,000 total XP", icon="✨",
             trigger=AchievementTrigger.xp_earned, threshold=1000, xp_bonus=100),
        dict(name="XP Hoarder", description="Earn 10,000 total XP", icon="💰",
             trigger=AchievementTrigger.xp_earned, threshold=10000, xp_bonus=500),
    ]

    for data in defaults:
        existing = await db.execute(
            select(Achievement).where(Achievement.name == data["name"])
        )
        if not existing.scalar_one_or_none():
            db.add(Achievement(**data))
    await db.commit()


async def check_and_award_achievements(
    player: Player,
    db: AsyncSession,
    trigger: AchievementTrigger,
) -> list[Achievement]:
    """
    Evaluate all achievements for the given trigger.
    Awards any not yet unlocked that the player now qualifies for.
    Returns list of newly unlocked achievements.
    """
    # Load all active achievements for this trigger
    result = await db.execute(
        select(Achievement).where(
            Achievement.trigger == trigger,
            Achievement.is_active == True,  # noqa: E712
        )
    )
    achievements = result.scalars().all()

    # Load already-unlocked achievement IDs for this player
    unlocked_result = await db.execute(
        select(PlayerAchievement.achievement_id).where(
            PlayerAchievement.player_id == player.id
        )
    )
    already_unlocked = set(unlocked_result.scalars().all())

    newly_unlocked: list[Achievement] = []

    for achievement in achievements:
        if achievement.id in already_unlocked:
            continue

        # Check threshold
        value = _get_trigger_value(player, trigger)
        if value >= achievement.threshold:
            pa = PlayerAchievement(
                player_id=player.id,
                achievement_id=achievement.id,
            )
            db.add(pa)
            newly_unlocked.append(achievement)

            # Award XP bonus if any
            if achievement.xp_bonus > 0:
                player.current_xp += achievement.xp_bonus
                player.total_xp_earned += achievement.xp_bonus

    return newly_unlocked


def _get_trigger_value(player: Player, trigger: AchievementTrigger) -> int:
    if trigger == AchievementTrigger.quest_completed:
        return player.quests_completed
    elif trigger == AchievementTrigger.level_reached:
        return player.level
    elif trigger == AchievementTrigger.streak_reached:
        return player.streak_days
    elif trigger == AchievementTrigger.xp_earned:
        return player.total_xp_earned
    elif trigger == AchievementTrigger.signup:
        return 1
    return 0