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
