from fastapi import FastAPI, HTTPException
from database import engine

# models.Base.metadata.create_all(bind=engine)


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import models, schemas
from database import AsyncSessionLocal, engine, get_user_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
# Create DB tables
# Base.metadata.create_all(bind=engine)
from base import Base
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/items/", response_model=schemas.Item)
async def create_item(
    item: schemas.ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).offset(skip).limit(limit)
    )
    items = result.scalars().all()
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id)
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id)
    )
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict().items():
        setattr(db_item, key, value)

    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id)
    )
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(db_item)
    await db.commit()
    return {"detail": "Item deleted"}



from auth import fastapi_users,auth_backend
from user_crud import router as  user_crud_router
from schemas import UserRead, UserCreate, UserUpdate


# app.include_router(user_crud_router)



app.include_router(
    fastapi_users.get_auth_router(auth_backend,True),  # ✅ no [0]
    prefix="/auth/jwt",
    tags=["auth"]
)


#token base varification
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)


#user create 
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)



#user update ,get 
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate,True),  # ✅ provide schemas
    prefix="/users",
    tags=["users"]
)




#password reset
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)









# from fastapi_users.authentication import CookieTransport, AuthenticationBackend
# from fastapi_users.authentication.strategy import OAuth2AuthorizationCodeBearer
# from fastapi_users.authentication import get_oauth_router
# from fastapi_users.oauth import OAuth2AuthorizeCallback

# from fastapi_users.authentication import OAuth2PasswordBearerWithCookie
# from fastapi_users.oauth.client import OAuth2

# google_oauth_client = OAuth2(
#     client_id="your-google-client-id",
#     client_secret="your-google-client-secret",
#     authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
#     access_token_endpoint="https://oauth2.googleapis.com/token",
#     client_kwargs={"scope": "email profile"},
# )

# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=your_cookie_transport,
#     get_strategy=your_strategy
# )

# app.include_router(
#     fastapi_users.get_oauth_router(
#         oauth_client=google_oauth_client,
#         backend=auth_backend,
#         state_secret="SUPER_SECRET_STATE_STRING",
#         redirect_url="http://localhost:8000/auth/google/callback",
#         associate_by_email=True,
#         is_verified_by_default=True
#     ),
#     prefix="/auth/google",
#     tags=["auth"]
# )



# app.include_router(
#     fastapi_users.get_oauth_associate_router(
#         oauth_client=google_oauth_client,
#         user_schema=UserRead,
#         state_secret="SUPER_SECRET_STATE_STRING",
#         redirect_url="http://localhost:8000/link/google/callback",
#         requires_verification=True
#     ),
#     prefix="/auth/link/google",
#     tags=["auth"]
# )

















