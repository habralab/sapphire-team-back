import uvicorn


class UvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass
