import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    legendary = "legendary"


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class QuestStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"      # overdue and not completed
    abandoned = "abandoned"


class Quest(Base, TimestampMixin):
    __tablename__ = "quests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Quest details
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Classification
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(Difficulty), default=Difficulty.medium, nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority), default=Priority.medium, nullable=False
    )
    status: Mapped[QuestStatus] = mapped_column(
        Enum(QuestStatus), default=QuestStatus.pending, nullable=False
    )

    # Rewards / costs — derived from difficulty but can be overridden
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_cost: Mapped[int] = mapped_column(Integer, nullable=False)

    # Lifecycle
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    player: Mapped["Player"] = relationship("Player", back_populates="quests")  # noqa: F821