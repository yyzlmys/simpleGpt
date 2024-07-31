import json
import asyncio
import requests
from fastapi import WebSocketDisconnect
from Utils.nameUtil import NameUtil
from assistant.LocalSearch import LocalSearchChat

class LocalSearchService:
    def __init__(self):
        self.chat = None

    async def work(self, preData, websocket, sockets):
        history = []
        isFirst = True
        for message in preData["lastMessages"]:
            history.append(message["content"])
        libId = preData["libId"]
        libDir = "/root/shixun/lib" + str(libId)

        self.chat = LocalSearchChat(history, "/root/m3e", libDir)

        while True:
            try:
                text_data = await websocket.receive_text()
                msg= json.loads(text_data)
                question = msg["content"]

                # 处理问题并返回回答
                skt = None
                conversationId = str(msg["conversationId"])
                while skt == None:
                    skt = await sockets.get(conversationId)
                    await asyncio.sleep(0.1)

                reply = ''
                async for chunk in self.chat.get_answer(question):
                    await skt.send_text(chunk)
                    await asyncio.sleep(0.0001)
                    reply += chunk

                if len(history) == 0 and isFirst == True:
                    isFirst = False
                    conversationName = NameUtil.summary(question, reply)
                    url = "http://localhost:619/conversation/name"
                    d = {
                        "name": conversationName,
                        "id": int(conversationId)
                    }
                    headers = {'Content-Type': 'application/json'}
                    requests.post(url, data=json.dumps(d), headers=headers)

                await skt.close()
                await websocket.send_text(reply)
                await sockets.delete(conversationId)

            except WebSocketDisconnect:
                break

