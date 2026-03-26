from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Questly API"
    debug: bool = True

    # Database
    database_url: str = "sqlite+aiosqlite:///./questly.db"

    # JWT
    secret_key: str = "changeme-use-a-strong-secret-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week

    # Game config
    base_xp_per_level: int = 1000        # XP needed for level 1 → 2
    xp_level_multiplier: float = 1.5     # each level costs 50% more XP
    daily_energy_max: int = 100          # max energy per day
    energy_regen_per_day: int = 100      # full refill every day

    # XP rewards by difficulty
    xp_easy: int = 10
    xp_medium: int = 50
    xp_hard: int = 100
    xp_legendary: int = 250

    # Energy costs by difficulty
    energy_easy: int = 5
    energy_medium: int = 15
    energy_hard: int = 30
    energy_legendary: int = 50

    class Config:
        env_file = ".env"


settings = Settings()