import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.routers.users import user_router

app = FastAPI(title=settings.app_title)

app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
