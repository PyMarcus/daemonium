import uuid
from typing import Optional
from pydantic import BaseModel as SCBaseModel


class DaemoniumSchema(SCBaseModel):
    id: Optional[str]
    hostname: str
    system_release: str
    SO: str
    disk: str
    memory: str
    cpu: str
    infected_files: str
    history_browser: str

    class Config:
        orm_mode = True
