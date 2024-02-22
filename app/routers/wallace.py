import logging
from fastapi import APIRouter, status, Depends, Request
from typing import List

from app.workflow.engine import Engine

logger = logging.getLogger(__name__)
logger.level = logging.INFO

router = APIRouter(
    prefix="",
)


@router.post("/predictions")
async def predictions(request: Request):
    engine = Engine(workflow_name='wallace', seed=await request.json())
    engine.run(engine.arrange_jobs())
    return engine.context['response_processor'].data
