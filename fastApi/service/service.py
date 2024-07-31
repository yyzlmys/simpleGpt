import asyncio
import json
from Utils.hashmap import AsyncDict
from webSearchService import WebSearchService
from localSearchService import LocalSearchService
from defaultChatService import DefaultChatService

sockets = AsyncDict()

class Service:
    def __init__(self):
        self.chat = None

    async def get(self, websocket):
        conversationId = await websocket.receive_text()
        await sockets.set(conversationId, websocket)
        # 保持连接打开状态
        while True:
            await asyncio.sleep(1)

    async def route(self, websocket):
        text_data = await websocket.receive_text()
        preData = json.loads(text_data)
        robotId = preData["robotId"]

        if robotId == 1:
            libId = preData["libId"]
            if libId != None:
                self.chat = LocalSearchService()
                await self.chat.work(preData, websocket, sockets)
            else:
                self.chat = DefaultChatService()
                await self.chat.work(preData, websocket, sockets)
        elif robotId == 2:
            self.chat = WebSearchService()
            await self.chat.work(preData, websocket, sockets)


