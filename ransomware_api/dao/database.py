from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core import get_instance_from_settings, Settings


settings: Settings = get_instance_from_settings()
engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
