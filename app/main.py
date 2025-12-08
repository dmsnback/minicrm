from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.routers.users import user_router

from app.core.init_db import create_first_superuser
from app.core.logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Приложение miniCRM запущено")
    await create_first_superuser()
    yield
    logging.info("Приложение miniCRM остановлено")


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
