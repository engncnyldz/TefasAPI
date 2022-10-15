from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    redis_hostname: str
    redis_port: str
    refresh_hour: int = Field(ge=0, le=23)

    class Config:
        env_file = ".env"
        
settings = Settings()