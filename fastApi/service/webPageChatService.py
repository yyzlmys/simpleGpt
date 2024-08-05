import json
import asyncio
from fastapi import WebSocketDisconnect
from assistant.WebPageAssistant import WebPageAssistant

class WebPageChatService:
    def __init__(self):
        self.chat = None

    async def work(self, preData, websocket, sockets):
        self.chat = WebPageAssistant()
        while True:
            try:
                text_data = await websocket.receive_text()
                msg= json.loads(text_data)
                question = msg["content"]

                parts = question.split('\n')
                url = parts[0]
                question = parts[1]

                await self.chat.init_docs(url)

                # 处理问题并返回回答
                skt = None
                conversationId = str(msg["conversationId"])
                while skt == None:
                    skt = await sockets.get(conversationId)
                    await asyncio.sleep(0.1)

                if (self.chat.is_have_docs()):
                    reply = self.chat.get_answer(question)
                    await skt.send_text(reply)
                    await skt.close()
                    await websocket.send_text(reply)
                    await sockets.delete(conversationId)
                else:
                    await skt.send_text("您发的网址有问题，请重新发一下吧~")
                    await skt.close()
                    await websocket.send_text("您发的网址有问题，请重新发一下吧~")
                    await sockets.delete(conversationId)

            except WebSocketDisconnect:
                break