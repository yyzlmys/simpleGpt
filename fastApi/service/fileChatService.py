import json
import asyncio
import os

from fastapi import WebSocketDisconnect
from assistant.FileAssistant import FileAssistant

class FileChatService:
    def __init__(self):
        self.chat = None

    async def work(self, preData, websocket, sockets):
        self.chat = FileAssistant()

        while True:
            try:
                text_data = await websocket.receive_text()
                msg= json.loads(text_data)
                question = msg["content"]

                parts = question.split('\n')
                fileName = parts[0]
                question = parts[1]

                conversationId = str(msg["conversationId"])
                await self.chat.init_docs('/root/shixun/conversation'+conversationId+"/"+fileName)

                # 处理问题并返回回答
                skt = None
                while skt == None:
                    skt = await sockets.get(conversationId)
                    await asyncio.sleep(0.1)

                if(self.chat.is_have_docs()):
                    reply = self.chat.get_answer(question)
                    await skt.send_text(reply)
                    await skt.close()
                    await websocket.send_text(reply)
                    await sockets.delete(conversationId)
                else:
                    await skt.send_text("文档格式有误，请重新选取符合要求的文件~")
                    await skt.close()
                    await websocket.send_text("文档格式有误，请重新选取符合要求的文件~")
                    await sockets.delete(conversationId)

                try:
                    os.remove('/root/shixun/conversation'+conversationId+"/"+fileName)
                except OSError as e:
                    print(f"删除文件 {fileName} 时出现错误: {e}")

            except WebSocketDisconnect:
                break