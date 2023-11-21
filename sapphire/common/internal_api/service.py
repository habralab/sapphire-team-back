from facet import ServiceMixin
from fast_grpc import FastGRPC


class BaseInternalAPIService(ServiceMixin, FastGRPC):
    async def start(self):
        self.add_task(self.run_async())
