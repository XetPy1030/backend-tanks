from fastapi import FastAPI

from tanks.server.routers import router


def create_server(debug: bool = True) -> FastAPI:
    app = FastAPI(debug=debug)

    app.include_router(router)

    return app
