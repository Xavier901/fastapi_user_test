# create_superuser.py

import sys
import asyncio
from sqlalchemy import insert, select
from passlib.context import CryptContext
from uuid import uuid4

from database import AsyncSessionLocal
from models import UserTable

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_superuser(email: str, password: str):
    async with AsyncSessionLocal() as session:
        # Check if user already exists
        result = await session.execute(select(UserTable).where(UserTable.email == email)) # type: ignore
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"❌ Superuser already exists: {email}")
            return

        hashed_password = pwd_context.hash(password)

        stmt = insert(UserTable).values(
            id=uuid4(),
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )

        await session.execute(stmt)
        await session.commit()

        print(f"✅ Superuser created: {email}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_superuser.py <email> <password>")
        sys.exit(1)

    email_arg = sys.argv[1]
    password_arg = sys.argv[2]

    asyncio.run(create_superuser(email_arg, password_arg))
