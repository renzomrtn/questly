from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Player(Base, TimestampMixin):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Adventurer stats
    level: Mapped[int] = mapped_column(Integer, default=1)
    current_xp: Mapped[int] = mapped_column(Integer, default=0)
    total_xp_earned: Mapped[int] = mapped_column(Integer, default=0)

    # Energy system
    current_energy: Mapped[int] = mapped_column(Integer, default=100)
    max_energy: Mapped[int] = mapped_column(Integer, default=100)
    last_energy_regen: Mapped[date] = mapped_column(
        Date, default=lambda: datetime.now(timezone.utc).date()
    )

    # Progress tracking
    quests_completed: Mapped[int] = mapped_column(Integer, default=0)
    quests_failed: Mapped[int] = mapped_column(Integer, default=0)  # (future: overdue quests)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    last_active_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Profile
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    quests: Mapped[list["Quest"]] = relationship(  # noqa: F821
        "Quest", back_populates="player", cascade="all, delete-orphan"
    )
    player_achievements: Mapped[list["PlayerAchievement"]] = relationship(  # noqa: F821
        "PlayerAchievement", back_populates="player", cascade="all, delete-orphan"
    )