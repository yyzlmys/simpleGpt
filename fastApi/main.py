from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json
from Chat import Chat
import requests

app = FastAPI()

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

sockets = AsyncDict()

@app.websocket("/ws")
async def spring(websocket: WebSocket):
    await websocket.accept()

    libId = None
    name = None
    description = None
    history = []
    chat = Chat()
    m3eDir = "/root/m3e"
    #m3eDir = "./m3e"

    while True:
        try:
            text_data = await websocket.receive_text()
            data = json.loads(text_data)
            question = data["message"]["content"]
            isFirst = False

            if data["isFirst"] == 1:                # 第一次对话
                libId = data["libId"]
                name = data["name"]
                description = data["description"]
                for msg in data["lastMessages"]:
                    history.append(msg["content"])
                isFirst = True

            # 处理问题并返回回答
            skt = None
            conversationId = str(data["message"]["conversationId"])
            while skt == None:
                skt = await sockets.get(conversationId)
                await asyncio.sleep(0.01)

            libDir = None
            if libId != None:
                libDir =  "/root/shixun/lib" + str(libId)
                #libDir = "D:/shixun/lib" + str(libId)

            if isFirst == False:
                reply = await chat.notFirst(skt, question)
            else:
                reply, conversationName =await chat.isFirst(skt, question, libDir, history, m3eDir)

                if conversationName != None:
                    url = "http://localhost:619/conversation/name"
                    d = {
                        "name": conversationName,
                        "id": int(conversationId)
                    }
                    headers = {'Content-Type': 'application/json'}
                    requests.post(url, data=json.dumps(d), headers=headers)

            await websocket.send_text(reply)
            await sockets.delete(conversationId)

        except WebSocketDisconnect:
            break


@app.websocket("/get")
async def client(websocket: WebSocket):
    await websocket.accept()
    conversationId = await websocket.receive_text()
    await sockets.set(conversationId, websocket)
    # 保持连接打开状态
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
