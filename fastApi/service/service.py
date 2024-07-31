import asyncio
import json
from Utils.hashmap import AsyncDict
from webSearchService import WebSearchService
from localSearchService import LocalSearchService
from defaultChatService import DefaultChatService
from codeChatService import CodeChatService
from TemplateChatService import TemplateChatService

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
            else:
                self.chat = DefaultChatService()
        elif robotId == 2:
            self.chat = WebSearchService()
        elif robotId == 3:
            self.chat = CodeChatService()
        else:
            self.chat = TemplateChatService()

        await self.chat.work(preData, websocket, sockets)


