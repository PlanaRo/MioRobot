import websockets
import asyncio
from config import Config
from Utils.Logs import Log
from Models.Event.EventControl import EventAdapter
from GroupControl import GroupControl
import traceback
from PluginLoader import PluginLoaderControl
import sys
import time
import uvicorn
from config import Config
from Utils.WebsocketControl import WebsocketControl


class OneBotReceive:
    """
    ws连接

    appHttp连接
    """

    # 插件加载器实例
    plugin = None
    # 配置信息
    config = None
    # websocket实例
    websocket = None

    def __init__(self, config: Config):
        self.config = config

    async def start(self):
        """
        启动ws连接
        """
        try:
            # 连接websocket
            WebsocketControl.connect()

            self.websocket = WebsocketControl.websocket
            # 初始化群管理类
            GroupControl.init()
            # 导入单例插件类
            self.plugin = PluginLoaderControl
            # 调用插件的初始化方法
            self.plugin.loading()
            # 调用接受方法
            await self.receive()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            # 查看详细错误信息
            # Log.error(
            #     f"ws连接错误\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
            # )
            Log.error("websockets连接失败，请检查配置")
            Log.info("将在10秒后尝试重新连接")
            time.sleep(10)
            await self.start()

    async def httpStart(self):
        try:
            Log.info("正在开启api服务......")
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: uvicorn.run(
                    "Net.appHttp:appHttp",
                    host="0.0.0.0",
                    port=int(self.config.UvicornPort),
                    reload=False,
                ),
            )

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            # 查看详细错误信息
            # Log.error(
            #     f"ws连接错误\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
            # )
            Log.error("http管理开启失败，请检查配置")
            Log.info("将在10秒后尝试重新连接")
            time.sleep(10)
            await self.httpStart()

    async def receive(self):
        """
        接收消息
        """
        while True:
            # 接收消息
            context = await self.Websocket.recv()
            # 判断是否为空
            if context.isspace():
                continue

            # 处理消息
            MessageData = EventAdapter.EventControl(context)

            try:
                if MessageData:

                    # 调用插件的接收方法
                    await self.plugin.call_back(
                        self.Websocket, MessageData.Post_Type, MessageData
                    )

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.error(
                    f"插件处理流程出错\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
                )


config = Config()
recv = OneBotReceive(config)
