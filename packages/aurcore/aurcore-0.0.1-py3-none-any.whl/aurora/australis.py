import aursync


class Australis:

    def __init__(self):
        self.sync = aursync.Sync()

    async def init(self):
        await self.sync.init()
