from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from dao import Session
from core import Settings

settings: Settings = Settings()


async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    except Exception as e:
        print(e)
    finally:
        await session.close()
