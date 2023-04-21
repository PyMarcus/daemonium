from fastapi import APIRouter
from .v1.endpoints import *


api_router = APIRouter()
api_router.include_router(router, prefix="/ransoms", tags=["ransoms"])
