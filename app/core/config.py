from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    database_url: str
    secret: str
    debug: bool
    first_superuser_username: str | None = None
    first_superuser_email: str | None = None
    first_superuser_password: str | None = None
    first_superuser_role: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
