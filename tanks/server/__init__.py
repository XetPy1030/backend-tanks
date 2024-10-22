from fastapi import FastAPI

from tanks.server.routers import router
from tanks.server.socket_manager import app as socketio_app


def create_server(debug: bool = True) -> FastAPI:
    app = FastAPI(debug=debug)

    app.include_router(router)
    app.mount("/", socketio_app)

    return app
