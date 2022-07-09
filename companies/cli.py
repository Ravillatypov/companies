import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from helpers.orjson import OrjsonResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from settings import setting
from tortoise.contrib.fastapi import register_tortoise
from uvicorn import run
from web.protected_routes import router as protected_router
from web.router import router

logger = logging.getLogger(__name__)


def make_app() -> FastAPI:
    """Make application."""
    app_ = FastAPI(  # noqa: WPS120
        debug=setting.debug,
        title='Companies mcs',
        description='Companies microservice',
        version=setting.version,
        openapi_url='/companies/openapi.json',
        docs_url='/companies/docs',
        redoc_url='/companies/redoc',
        default_response_class=OrjsonResponse,
    )
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',  # noqa: WPS323
        datefmt='%Y-%m-%d %H:%M:%S',  # noqa: WPS323
        handlers=[logging.StreamHandler()],
    )
    app_.include_router(router)
    app_.include_router(protected_router)
    app_.add_middleware(
        CORSMiddleware,
        allow_methods=['*'],
        allow_credentials=True,
        allow_origins=setting.allow_origins,
        allow_headers=['*'],
    )
    register_tortoise(
        app_,
        db_url=setting.db_url,
        modules={'models': ['repositories.pg_models']},
        generate_schemas=True,
    )
    if setting.sentry_dsn:
        sentry_sdk.init(
            setting.sentry_dsn,
            release=setting.version,
            environment=setting.env,
            integrations=[
                LoggingIntegration(level=logging.WARNING),
            ],
        )
        return SentryAsgiMiddleware(app_)
    return app_


app = make_app()


if __name__ == '__main__':
    app.debug = True
    run(app)
