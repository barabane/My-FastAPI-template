from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.config import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
else:
    DATABASE_URL = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(
    url=str(DATABASE_URL),
    pool_size=settings.DB_POOL_SIZE,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    max_overflow=settings.DB_POOL_SIZE_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_TTL,
)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()
