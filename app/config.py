from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    jwt_private_key: str = Field(default="HolaMundo"
, env="SECRET_KEY_JWT")

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
