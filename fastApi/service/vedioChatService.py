import json
import asyncio
from fastapi import WebSocketDisconnect
from assistant.VideoAssistant import VideoAssistant

class VedioChatService:
    def __init__(self):
        self.chat = None

    async def work(self, preData, websocket, sockets):
        history = []
        isFirst = True
        for message in preData["lastMessages"]:
            history.append(message["content"])

        self.chat =VideoAssistant(history)

        while True:
            try:
                text_data = await websocket.receive_text()
                msg = json.loads(text_data)
                question = msg["content"]

                skt = None
                conversationId = str(msg["conversationId"])
                while skt == None:
                    skt = await sockets.get(conversationId)
                    await asyncio.sleep(0.1)

                if len(history) == 0 and isFirst == True:
                    isFirst = False
                    await self.chat.init_bilibili_video(question)

                    if self.chat.is_have_data():
                        await skt.send_text("我收到您发的视频啦，请尽管问我吧~")
                        await skt.close()
                        await websocket.send_text("我收到您发的视频啦，请尽管问我吧~")
                        await sockets.delete(conversationId)
                    else:
                        await skt.send_text("您发的网址有问题，请重新发一下吧~")
                        await skt.close()
                        await websocket.send_text("您发的网址有问题，请重新发一下吧~")
                        await sockets.delete(conversationId)
                        isFirst = True
                else:
                    if not self.chat.is_have_data():
                        await self.chat.init_bilibili_video(history[0])
                    reply = ''
                    async for chunk in self.chat.get_answer(question):
                        await skt.send_text(chunk)
                        await asyncio.sleep(0.0001)
                        reply += chunk
                    await skt.close()
                    await websocket.send_text(reply)
                    await sockets.delete(conversationId)


            except WebSocketDisconnect:
                break