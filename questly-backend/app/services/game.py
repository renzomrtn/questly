"""
Core game mechanics: XP, leveling, energy regeneration.
"""
import math
from datetime import date, datetime, timezone

from app.config import settings
from app.models.quest import Difficulty


# ── XP & Level ───────────────────────────────────────────────────────────────

def xp_for_level(level: int) -> int:
    """Total XP required to reach `level` from level 1."""
    if level <= 1:
        return 0
    return int(settings.base_xp_per_level * ((settings.xp_level_multiplier ** (level - 1) - 1)
               / (settings.xp_level_multiplier - 1)))


def xp_to_next_level(current_level: int, current_xp: int) -> int:
    """XP still needed to reach next level."""
    next_threshold = xp_for_level(current_level + 1)
    current_threshold = xp_for_level(current_level)
    progress = current_xp  # current_xp is the XP earned within this level
    return max(0, (next_threshold - current_threshold) - progress)


def calculate_level_from_total_xp(total_xp: int) -> tuple[int, int]:
    """
    Given total lifetime XP, return (level, xp_within_current_level).
    """
    level = 1
    while True:
        needed = xp_for_level(level + 1)
        if total_xp < needed:
            break
        level += 1
    current_level_start = xp_for_level(level)
    xp_in_level = total_xp - current_level_start
    return level, xp_in_level


# ── Difficulty helpers ────────────────────────────────────────────────────────

_XP_MAP = {
    Difficulty.easy: settings.xp_easy,
    Difficulty.medium: settings.xp_medium,
    Difficulty.hard: settings.xp_hard,
    Difficulty.legendary: settings.xp_legendary,
}

_ENERGY_MAP = {
    Difficulty.easy: settings.energy_easy,
    Difficulty.medium: settings.energy_medium,
    Difficulty.hard: settings.energy_hard,
    Difficulty.legendary: settings.energy_legendary,
}


def default_xp(difficulty: Difficulty) -> int:
    return _XP_MAP[difficulty]


def default_energy_cost(difficulty: Difficulty) -> int:
    return _ENERGY_MAP[difficulty]


# ── Energy regeneration ───────────────────────────────────────────────────────

def regenerate_energy(player) -> bool:
    """
    Refill energy to max if last regen was on a previous calendar day.
    Returns True if energy was refilled (so caller can persist the change).
    """
    today = datetime.now(timezone.utc).date()
    if player.last_energy_regen < today:
        player.current_energy = player.max_energy
        player.last_energy_regen = today
        return True
    return False


# ── Streak ────────────────────────────────────────────────────────────────────

def update_streak(player) -> None:
    """Update the player's daily streak based on activity."""
    today = datetime.now(timezone.utc).date()
    if player.last_active_date is None:
        player.streak_days = 1
    elif (today - player.last_active_date).days == 1:
        player.streak_days += 1
    elif (today - player.last_active_date).days > 1:
        player.streak_days = 1
    # same day — no change
    player.last_active_date = today