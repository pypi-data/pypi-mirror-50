import aursync


class Australis:

    def __init__(self):
        self.sync = aursync.Sync()

    async def init(self):
        await self.sync.init()

    async def register_heartbeat(self):
        async def respond(message):
            await self.sync.publish(f"{message}|{self.sync.name}", "_heartbeat")
        await self.sync.subscribe(respond, "_heartbeat")
