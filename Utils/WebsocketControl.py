import websockets
from Utils.Logs import Log
from config import Config


class WebsocketControl:
    # websockets实例
    websocket: websockets.WebSocketClientProtocol

    @staticmethod
    async def connect(config: Config) -> None:
        """
        连接websockets
        """
        Log.info("websockets连接中...")
        WebsocketControl.websocket = await websockets.connect(config.websocket)
        Log.info("websockets连接成功")

    @staticmethod
    async def disconnect() -> None:
        """
        断开websockets连接
        """
        Log.info("websockets断开连接中...")
        await WebsocketControl.websocket.close()
        Log.info("websockets断开连接成功")
