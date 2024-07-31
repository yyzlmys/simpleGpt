import asyncio


class AsyncDict:
    def __init__(self):
        self.data = {}
        self.lock = asyncio.Lock()

    async def set(self, key, value):
        async with self.lock:
            self.data[key] = value

    async def get(self, key):
        async with self.lock:
            return self.data.get(key)

    async def delete(self, key):
        async with self.lock:
            self.data.pop(key, None)