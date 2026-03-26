from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_player
from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models.achievement import AchievementTrigger
from app.models.player import Player
from app.schemas.player import PlayerLogin, PlayerPublic, PlayerRegister, TokenResponse
from app.services.achievement import check_and_award_achievements

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: PlayerRegister, db: AsyncSession = Depends(get_db)):
    # Check email uniqueness
    existing = await db.execute(select(Player).where(Player.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    player = Player(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(player)
    await db.flush()  # get the ID

    # Award signup achievement
    await check_and_award_achievements(player, db, AchievementTrigger.signup)
    await db.commit()
    await db.refresh(player)

    token = create_access_token(player.id)
    return TokenResponse(access_token=token, player=PlayerPublic.model_validate(player))


@router.post("/login", response_model=TokenResponse)
async def login(payload: PlayerLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Player).where(Player.email == payload.email))
    player = result.scalar_one_or_none()

    if not player or not verify_password(payload.password, player.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not player.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account inactive")

    token = create_access_token(player.id)
    return TokenResponse(access_token=token, player=PlayerPublic.model_validate(player))


@router.get("/me", response_model=PlayerPublic)
async def me(player: Player = Depends(get_current_player)):
    return player