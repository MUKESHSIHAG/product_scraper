from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    page_limit: int = 5
    proxy: Optional[str] = None
    static_token: str = "test_token"

settings = Settings()
