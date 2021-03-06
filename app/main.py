from starlette.middleware.sessions import SessionMiddleware

from app.apis.base import api_router
from app.webapps.base import api_router as web_app_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine, SessionLocal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # new
from starlette.middleware.cors import CORSMiddleware

from app.db.init_data import init_db


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):  # new
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():  # new
    print("create_tables")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    init_db(db)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.add_middleware(SessionMiddleware, secret_key="!secret")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_router(app)
    create_tables()
    configure_static(app)  # new
    return app


app = start_application()
