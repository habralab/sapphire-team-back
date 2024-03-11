import socketio
from loguru import logger


class BaseNamespace(socketio.AsyncNamespace):
    namespace_name = "*"

    def on_connect(self, sid, environ):
        logger.info(f"User {sid} connected")

    def on_disconnect(self, sid):
        logger.info(f"User {sid} disconnected")
