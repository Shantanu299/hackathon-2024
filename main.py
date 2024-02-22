import logging
import uvicorn
from dotenv import load_dotenv; load_dotenv()
from fastapi import FastAPI
from app.routers import wallace

app = FastAPI(title="Start Hack", description="Hackathon Application", version="0.1.0")

logger = logging.getLogger(__name__)
logger.level = logging.INFO

app.include_router(wallace.router)


if __name__ == "__main__":
    FORMAT = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d]- %(message)s'
    logging.basicConfig(format=FORMAT)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
