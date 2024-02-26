class BaseSocketIOHandler:
    def __init__(self, event: str):
        self._event = event

    async def handle(self):
        pass

    @property
    def event(self):
        return self._event
