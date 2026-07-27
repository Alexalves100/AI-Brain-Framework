"""
Brain Project Template — Configuration
Version: 1.0.0
"""

import os
from pathlib import Path


class Config:
    """Project configuration."""

    PROJECT_NAME = "brain-project"
    VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    BASE_DIR = Path(__file__).parent
    AI_DIR = BASE_DIR / ".ai"
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"

    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(LOGS_DIR / "app.log"))

    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

    LOCALE = os.getenv("LOCALE", "en")

    @classmethod
    def init(cls) -> None:
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.AI_DIR.mkdir(parents=True, exist_ok=True)
