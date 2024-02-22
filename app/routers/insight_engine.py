import logging
from fastapi import APIRouter, status, Depends
from typing import List


logger = logging.getLogger(__name__)
logger.level = logging.INFO


router = APIRouter(
    prefix="",
)


@router.post("/dssat", status_code=status.HTTP_200_OK)
async def call_dssat_model():
    return None


@router.post("/dry-down", status_code=status.HTTP_200_OK)
async def call_dry_down_model():
    return None

