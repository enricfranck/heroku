import os
from pathlib import Path

from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
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
    DATABASE_URL_PROD = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # if you test in local
    DATABASE_URL_LOCAL = f"postgresql://postgres:postgres@localhost:5432/db_jobs"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins
    TEST_USER_EMAIL = "test@example.com"
    USE_LOCALHOST = True

    EMAIL_TEMPLATES_DIR = "/app/template"
    PROJECT_NAME = "Jobs Finder"

    config = Config('.env')
    oauth = OAuth(config)

    EMAILS_ENABLED = False

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    id = ""

    SMTP_TLS = os.getenv("SMTP_TLS")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME = os.getenv("EMAIL_NAME")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    PASSWORD_FROM_EMAIL = os.getenv("PASSWORD_FROM_EMAIL")

    TEST_SEND_MAIL = os.getenv("TEST_SEND_MAIL")

    conf = ConnectionConfig(
        MAIL_USERNAME="Franck Enric",
        MAIL_PASSWORD="",
        MAIL_FROM="enricfranck@gmail.com",
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_FROM_NAME="Enric Franck",
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    HTML = """
    <p> Bonjour, cordialement</>
    """


settings = Settings()
