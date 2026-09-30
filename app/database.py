import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")
DATABASE_URL = DATABASE_URL.replace("?sslmode=require", "").replace("&sslmode=require", "")

connect_args = {"ssl": "require"} if "neon.tech" in DATABASE_URL else {}
engine = create_async_engine(DATABASE_URL, echo=True, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session