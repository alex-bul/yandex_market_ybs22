from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url_from_env: str = Field(default=None, env='POSTGRES_URL_ENV')
    db_url_from_docker: str = Field(default=None, env='POSTGRES_URL_DOCKER')

    class Config:
        env_file = ".env"


settings = Settings()
