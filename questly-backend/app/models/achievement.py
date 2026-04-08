import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class AchievementTrigger(str, enum.Enum):
    """What event can trigger an achievement check."""
    quest_completed = "quest_completed"   # when a quest is marked complete
    level_reached = "level_reached"       # when player levels up
    streak_reached = "streak_reached"     # daily streak milestone
    xp_earned = "xp_earned"              # total XP accumulated
    signup = "signup"                     # first registration


class Achievement(Base, TimestampMixin):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(100), nullable=False)  # emoji or icon name

    # What triggers this achievement
    trigger: Mapped[AchievementTrigger] = mapped_column(Enum(AchievementTrigger, native_enum=False), nullable=False)
    # The threshold value (e.g. reach level 5, complete 10 quests, 7-day streak)
    threshold: Mapped[int] = mapped_column(Integer, default=1)

    # XP bonus awarded on unlock (optional badge bonus)
    xp_bonus: Mapped[int] = mapped_column(Integer, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    player_achievements: Mapped[list["PlayerAchievement"]] = relationship(
        "PlayerAchievement", back_populates="achievement"
    )


class PlayerAchievement(Base):
    """Junction table tracking which achievements a player has unlocked."""
    __tablename__ = "player_achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True
    )
    achievement_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False
    )
    unlocked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.utcnow(),
    )

    # Relationships
    player: Mapped["Player"] = relationship("Player", back_populates="player_achievements")  # noqa: F821
    achievement: Mapped["Achievement"] = relationship("Achievement", back_populates="player_achievements")