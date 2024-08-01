from fastapi import FastAPI, WebSocket
import uvicorn
from service.service import Service
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI()

service = Service()

@app.websocket("/ws")
async def spring(websocket: WebSocket):
    await websocket.accept()
    await service.route(websocket)


@app.websocket("/get")
async def client(websocket: WebSocket):
    await websocket.accept()
    await service.get(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
