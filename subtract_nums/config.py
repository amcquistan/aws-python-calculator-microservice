from pydantic import BaseSettings


class Settings(BaseSettings):
  env: str = "local"
  port: int = 8001


def configure() -> Settings:
  return Settings()
