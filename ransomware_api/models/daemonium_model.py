import uuid
from typing import Any
from sqlalchemy import Column, Integer, String
from core import Settings


class DaemoniumModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'daemoniums'
    id = Column(String(40),
                primary_key=True,
                default=str(uuid.uuid4()),
                unique=True,
                nullable=False)
    hostname: str = Column(String(100))
    system_release: str = Column(String(100))
    SO: str = Column(String(100))
    disk: str = Column(String(100))
    memory: str = Column(String(100))
    cpu: str = Column(String(100))
    infected_files: str = Column(String(100))
    history_browser: str = Column(String(100))
