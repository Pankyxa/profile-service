from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.db import get_db
from src.schemas.profile import ProfileCreate, ProfileOut, ProfileUpdate
from src.services import profile_service

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{profile_id}", response_model=ProfileOut)
async def get_profile_by_id(profile_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получение профиля по id
    """

    profile = await profile_service.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/", response_model=list[ProfileOut])
async def get_profiles(db: AsyncSession = Depends(get_db)):
    """
    Получение всех профилей
    """

    return await profile_service.get_all_profiles(db)


@router.post("/", response_model=ProfileOut)
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    """
    Создание профиля
    """

    return await profile_service.create_profile(db, profile)


@router.put("/{profile_id}", response_model=ProfileOut)
async def update_profile(
        profile_id: int,
        profile: ProfileUpdate,
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление профиля по id
    """

    return await profile_service.update_profile(db, profile_id, profile)


@router.delete("/{profile_id}")
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаление профиля по id
    """

    success = await profile_service.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
