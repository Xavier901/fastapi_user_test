from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from auth import fastapi_users
from models import UserTable as User
from schemas import UserRead, UserUpdate, UserCreate
from Dependencies import require_active_user
from database import get_user_db


router = APIRouter(prefix="/users", tags=["users"])

# @router.get("/", response_model=List[UserRead])
# async def list_users(
#     current_user: User = Depends(require_active_user),
#     user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
# ):
#     if not current_user.is_superuser:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
#     return await user_db.get_all()

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import UserTable

from sqlalchemy.future import select




@router.get("/", response_model=List[UserRead])
async def list_users(
    current_user=Depends(require_active_user),
    session: AsyncSession = Depends(get_async_session),  # inject session directly
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await session.execute(select(UserTable))
    users = result.scalars().all()
    return users



@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: UUID,
    current_user: User = Depends(require_active_user),
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    user = await user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Allow if superuser or own account
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user




@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: User = Depends(require_active_user),
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    user = await user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_user = await user_db.update(user, user_update.dict(exclude_unset=True))
    return updated_user




@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(require_active_user),
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    user = await user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    await user_db.delete(user)
    
    
    
    
    
    
    
# @router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# async def create_active_user(
#     user_create: UserCreate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     # Check if email already exists
#     existing = await session.execute(select(UserTable).where(UserTable.email == user_create.email)) # type: ignore
#     if existing.scalar_one_or_none():
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = get_password_hash(user_create.password)

#     user = UserTable(
#         email=user_create.email,
#         hashed_password=hashed_password,
#         is_active=True,  # <-- active user
#         is_superuser=False,  # default false, or from user_create if allowed
#     )
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)
#     return user


from schemas import UserCreate, UserRead
from user_manager import UserManager, get_user_manager  # your custom manager and dependency
from database import get_async_session


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_active_user(
    user_create: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),  # inject your UserManager
    session: AsyncSession = Depends(get_async_session),  # optional, can be used for extra checks
):
    # Check if email already exists using session or user_manager
    existing = await session.execute(select(UserTable).where(UserTable.email == user_create.email))  # type: ignore
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user via UserManager - it hashes password internally!
    user = await user_manager.create(user_create)

    return user




