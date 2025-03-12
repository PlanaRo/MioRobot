from Models.Event.BaseEvent import BaseEvent
from Models.Event.GroupMessageEvent import GroupMessageEvent
from Plugin import Plugin, PluginReturnMessage
from Models.Api.MessageApi import MessageApi


class MyPlugin(Plugin):
    def init(self):
        pass

    async def run(self, messageData: BaseEvent):
        # 构建返回消息
        pluginReturnMessage = PluginReturnMessage()
        # 确保messageData是GroupMessageEvent类型
        if not isinstance(messageData, GroupMessageEvent):
            return pluginReturnMessage

        if messageData.Message == "你好":
            await MessageApi.sendGroupMessage(messageData, "你好")
            pluginReturnMessage.updata()
        return pluginReturnMessage

    def dispose(self) -> None:
        pass
