from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.routers.users import user_router

from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    print('SuperUser создан или уже существует')
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
