# import uuid
# from typing import Optional

# from fastapi import Depends, Request
# from fastapi_users import BaseUserManager, UUIDIDMixin

# from models import UserTable as User
# from database import get_user_db

# SECRET = "SECRET"


# class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
#     reset_password_token_secret = SECRET
#     verification_token_secret = SECRET

#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         print(f"User {user.id} has registered.")

#     async def on_after_forgot_password(
#         self, user: User, token: str, request: Optional[Request] = None
#     ):
#         print(f"User {user.id} has forgot their password. Reset token: {token}")

#     async def on_after_request_verify(
#         self, user: User, token: str, request: Optional[Request] = None
#     ):
#         print(f"Verification requested for user {user.id}. Verification token: {token}")


# async def get_user_manager(user_db=Depends(get_user_db)):
#     yield UserManager(user_db)






import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from pydantic import EmailStr

from models import UserTable as User
from database import get_user_db
from send_reset_email import send_email
import os

SECRET = "SUPER_SECRET"  # Use a strong secret in production

RESET_PASSWORD_URL = os.getenv("RESET_PASSWORD_URL", "https://yourfrontend.com/reset-password")
VERIFY_EMAIL_URL = os.getenv("VERIFY_EMAIL_URL", "https://yourfrontend.com/verify-email")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"[REGISTER] User {user.email} registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        reset_link = f"{RESET_PASSWORD_URL}?token={token}"
        print(f"[FORGOT PASSWORD] Reset link: {reset_link}")

        subject = "Reset your password"
        body = f"Hello {user.email},\n\nTo reset your password, click this link:\n{reset_link}\n\nIf you didn't request this, ignore it."

        await send_email(user.email, subject, body)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        verify_link = f"{VERIFY_EMAIL_URL}?token={token}"
        print(f"[VERIFY EMAIL] Verification link: {verify_link}")

        subject = "Verify your email"
        body = f"Hi {user.email},\n\nClick the link to verify your email:\n{verify_link}\n\nThank you!"

        await send_email(user.email, subject, body)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)







