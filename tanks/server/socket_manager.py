import socketio

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*",
    transports=["websocket"],
)
app = socketio.ASGIApp(
    socketio_server=sio, socketio_path="socket.io"
)


@sio.event
async def connect(sid, environ):
    print(f"connect {sid}")
