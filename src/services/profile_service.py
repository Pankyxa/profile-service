from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.profile import Profile
from src.schemas.profile import ProfileCreate, ProfileUpdate


async def get_profile(db: AsyncSession, profile_id: int) -> Profile | None:
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    return result.scalar_one_or_none()


async def get_all_profiles(db: AsyncSession) -> Sequence[Profile]:
    result = await db.execute(select(Profile))
    return result.scalars().all()


async def create_profile(db: AsyncSession, profile_data: ProfileCreate) -> Profile:
    new_profile = Profile(**profile_data.model_dump())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


async def update_profile(
        db: AsyncSession,
        profile_id: int,
        profile_data: ProfileUpdate
) -> Profile | None:
    profile = await get_profile(db, profile_id)
    if profile is None:
        return None

    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_profile(db: AsyncSession, profile_id: int) -> bool:
    profile = await get_profile(db, profile_id)
    if profile is None:
        return False

    await db.delete(profile)
    await db.commit()
    return True
