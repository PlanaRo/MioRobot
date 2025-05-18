import asyncio
from Models.Context.MessageContextBuild import MessageContextBuild
from Core.config import Config
from Utils.Logs import Log
from Models.Event.EventControl import EventAdapter
from Core.GroupControl import GroupControl
import traceback
from Core.PluginLoader import PluginLoader, PluginLoaderControl
import sys
import time
import uvicorn
from Core.config import Config
from Utils.WebsocketControl import WebsocketControl
from Net.AppHttp import appHttp


class CoreServer:
    """
    核心服务用于启动
    ws连接
    appHttp连接
    """

    # 插件加载器实例
    plugin: PluginLoader
    # 配置信息
    config: Config

    def __init__(self, config: Config):
        self.config = config

    async def start(self):
        """
        启动ws连接
        """
        try:
            # 连接websocket
            await WebsocketControl.connect(config)

            # 导入单例插件类
            self.plugin = PluginLoaderControl
            # 调用插件的初始化方法
            self.plugin.loading()
            # 初始化群管理类
            GroupControl.init(self.plugin.getPluginsName())
            # 调用接受方法
            await self.receive()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            # 查看详细错误信息
            Log.error(
                f"ws连接错误\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
            )
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
                    # "Net.AppHttp:appHttp",
                    appHttp,
                    host="0.0.0.0",
                    port=int(self.config.uvicornPort),
                    reload=False,
                ),
            )

        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            # 查看详细错误信息
            Log.error(
                f"ws连接错误\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
            )
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
            context: str = await WebsocketControl.websocket.recv()  # type: ignore
            # 判断是否为空
            if context.isspace():
                continue

            # 处理消息
            messageData = EventAdapter.EventControl(context)
            # 构建消息上下文
            messageContext = MessageContextBuild.build(messageData)

            if messageContext is None:
                continue

            try:

                await self.plugin.callBack(messageContext)

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.error(
                    f"插件处理流程出错\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
                )


config = Config()
coreServer = CoreServer(config)
