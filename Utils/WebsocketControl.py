import websockets
from Utils.Logs import Log
from config import Config


class WebsocketControl:
    websocket: websockets.WebSocketClientProtocol

    @staticmethod
    async def connect(config: Config) -> None:
        Log.info("websockets连接中...")
        WebsocketControl.websocket = await websockets.connect(config.websocket)
        Log.info("websockets连接成功")

    @staticmethod
    async def disconnect() -> None:
        Log.info("websockets断开连接中...")
        await WebsocketControl.websocket.close()
        Log.info("websockets断开连接成功")
