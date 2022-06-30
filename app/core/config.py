import os
from pathlib import Path

from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from starlette.config import Config

env_path = Path('') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    print("eto amzay database url ",DATABASE_URL)

    SECRET_KEY: str = os.getenv("SECRET_KEY")  # new
    ALGORITHM = "HS256"  # new
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins  #new
    TEST_USER_EMAIL = "test@example.com"  # new

    config = Config('.env')
    oauth = OAuth(config)

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


settings = Settings()
